import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
import requests
import json
import numpy as np
import cv2
from ml_models.traffic_sign import tsc


# -------------- SETTINGS --------------
page_title = "AIML Test Service"
page_icon = "♻"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
tscmodel = tsc.tsc()

# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
nav_items = ["Submit Test Job", "View Test Result", "Traffic Sign Classification"]
torf = [True, False]

# --- Test service Url ---
cjurl = "http://127.0.0.1:8000/testservices/v1.0/create-job"
vjurl = "http://127.0.0.1:8000/testservices/v1.0/testjobs"


# --- HIDE STREAMLIT STYLE ---

# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=nav_items,
        # icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
        # orientation="horizontal",
    )

# --- Submit Test Job ---
if selected == "Submit Test Job":
    st.header("Config Your Test Job")
    with st.form("entry_form", clear_on_submit=True):
        st.text_input("Script Path:", value="robot/TestCases", key="path")
        st.text_input("Tags:", value="uiORapi", key="tag")
        st.text_input("Browser Type:", value="chromium", key="browser")
        col1, col2 = st.columns(2)
        col1.selectbox("Head Less:", torf, key="headless")
        col2.selectbox("Record Video:", torf, index=1, key="video")

        submitted = st.form_submit_button("Submit Job")
        if submitted:
            payload = {
                "recordVideo": st.session_state["video"],
                "headless": st.session_state["headless"],
                "tag": st.session_state["tag"],
                "script_path": st.session_state["path"],
                "browser": st.session_state["browser"],
            }
            res = requests.post(url=cjurl, data=json.dumps(payload))
            res_dict = json.loads(res.content)
            if res.status_code != 201:
                st.error(f"Status Code: {res.status_code} Message: {res_dict}")
            else:
                jobid = res_dict["jobid"]
                print(jobid)
                st.success(f"Test job: {jobid} created successfully")

# --- View Test Result ---
if selected == "View Test Result":
    st.header("View Test Job Status")
    with st.form("entry_form", clear_on_submit=True):
        st.text_input("Test Job id:", key="jobid")

        submitted = st.form_submit_button("Submit")
        if submitted:
            id = st.session_state["jobid"]
            res = requests.get(url=f"{vjurl}?id={id}")
            res_dict = json.loads(res.content)
            if res.status_code != 200:
                st.error(f"Status Code: {res.status_code} Message: {res_dict}")
            else:
                jobid = res_dict[0]["jobid"]
                jobstatus = res_dict[0]["jobstatus"]
                joblogs = res_dict[0]["job_logs"]
                print(jobid)

                st.success(f"Test job: {jobid} Status: {jobstatus}")
                st.text(joblogs)

# --- Traffic Sign Classification ---
if selected == "Traffic Sign Classification":
    st.header("Traffic Sign Classification")
    uploaded_file = st.file_uploader("Upload Image file", type=["jpg", "png", "ppm"])
    if uploaded_file is not None:
        st.image(uploaded_file, width=200)
        try:
            img_array = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, -1)
        except Exception as e:
            print(e)
        img = cv2.resize(img, (30, 30), interpolation=cv2.INTER_AREA)
        images = []
        images.append(img)
        result, confidence = tscmodel.classify(images)
        if confidence > 0.9:
            st.success(
                {"classification": result, "confidence": "{:.0%}".format(confidence)}
            )
        else:
            st.error({"Message": "confidence too low, can't classify the image"})

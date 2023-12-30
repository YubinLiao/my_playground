import random
import os
from fastapi import (
    FastAPI,
    Response,
    HTTPException,
    APIRouter,
    Depends,
    BackgroundTasks,
    status,
)
from typing import Union
from .. import apimodels
import subprocess

router = APIRouter(prefix="/testservices/v1.0", tags=["Test Microservices"])

# in this prototype project all job runtime info is saved in memory
# a database table can be implemented to keep those job execution data
job_procs = {}  # keep subprocess object for all test jobs
job_logs = {}  # keep all test job logs
job_status = {}  # keep all test job status


@router.post("/create-job", status_code=status.HTTP_201_CREATED)
async def create_test_job(
    background_task: BackgroundTasks, job_parameter: apimodels.JobIn
):
    """
    Create test job, return status.HTTP_201_CREATED if job created successfully\n
    :param job_parameter:\n
    :return: job id
    """
    # jobid should come from db table identity sequences
    # use random number since orm classes is not yet implemented
    jobid = random.randint(10000000, 99999999)
    tag = ""
    browser = ""
    headless = ""
    recordVideo = ""
    if job_parameter.tag is not None:
        tag = f"-i {job_parameter.tag} "
    if job_parameter.browser is not None:
        browser = f"--variable browser:{job_parameter.browser} "
    if job_parameter.headless is not None:
        headless = f"--variable headless:{job_parameter.headless} "
    if job_parameter.recordVideo is not None:
        recordVideo = f"--variable recordVideo:{job_parameter.recordVideo} "
    cmd = (
        f"robot {browser}{headless}{recordVideo}-T -d robot/Reports/{jobid} "
        f"{tag}{job_parameter.script_path}"
    )
    background_task.add_task(run_command, cmd, jobid)
    return {"jobid": f"{jobid}", "cmd": f"{cmd}"}


@router.get("/testjobs")
def get_testjobs(id: Union[int, None] = None):
    """
    Get all test job status in memory, filter by optional qurry parameter 'id'\n
    :param id: job id, if provided, only status of the job id is returned\n
    :return: list of test job status, id, log, status.\n
    """
    if id is not None:
        if id in job_status:
            return [
                {
                    "jobid": f"{id}",
                    "jobstatus": f"{job_status[id]}",
                    "job_logs": f"{job_logs[id]}",
                }
            ]
        else:
            raise HTTPException(status_code=404, detail="Job id not found")
    else:
        job_items = []
        for k, v in job_status.items():
            job_item = {
                "jobid": f"{k}",
                "jobstatus": f"{v}",
                "job_logs": f"{job_logs[k]}",
            }
            job_items.append(job_item)
        return job_items


def run_command(command: str, jobid: int):
    os.mkdir(f"./robot/Reports/{jobid}")
    proc = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    job_procs[jobid] = proc  # save the subprocess object for terminating if requested
    job_status[jobid] = "In_Progress"
    job_logs[jobid] = ""
    for line in iter(proc.stdout.readline, b""):
        job_log = line.decode("utf-8")[:-1]  # [:-1] to cut off newline char
        print(job_log)
        job_logs[jobid] += f"{job_log}\n"
    proc.stdout.close()
    proc.wait()
    job_status[jobid] = "Completed"

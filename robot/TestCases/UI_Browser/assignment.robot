*** Settings ***
Library     Browser
Library     Collections
Library     ../../Resources/util.py

Test Setup   UI Test Setup  ${browser}  ${headless}  ${recordVideo}
Test Teardown    UI Test Tearup

*** Variables ***
${browser}  chromium
${headless}  True
${recordVideo}  False

*** Test Cases ***
Cypress UI Components
    [Tags]  ui  plotly
    New Page    https://www.cypress.io/
    Hover   //h2[contains(text() ,"Loved by")]
    sleep  1s
    Hover  //a[@id="dropdownCompany"]
    Click  //span[text()="About Cypress "]
    sleep  1s
    Click  //button[contains(text(), "Install")]
    Click  //span[text()="npm install cypress"]
    sleep  1s
    ${text}=  get Clipboard Text

    # Should Be Equal As Strings    ${text}  npm install cypress --save-dev
    Click  //button[@aria-label = "Close"]
    Hover  //a[@id="dropdownProduct"]
    Click  //span[contains(text(), "Visual Reviews")]
    sleep  1s
    Hover  //a[@id="dropdownProduct"]
    Click  //span[contains(text(), "Smart Orchestration")]
    sleep  1s
    ${style1}=  Get Style  //a[contains(text(), "Test Analytics")]  border-block-start-color
    Hover  //a[contains(text(), "Test Analytics")]
    ${style2}=  Get Style  //a[contains(text(), "Test Analytics")]  border-block-start-color
    Should Not Be Equal As Strings    ${style1}    ${style2}
    sleep  1s

*** Keywords ***
UI Test Setup
    [Arguments]  ${browser}  ${headless}  ${recordVideo}
    IF    ${recordVideo} == ${True}
        ${videoDict}=    Create Dictionary    dir=./videos
    ELSE
        ${videoDict}=  Set Variable  ${None}
    END
    New Browser   ${browser}     headless=${headless}
    New Context   recordVideo=${videoDict}

UI Test Tearup
    Close Context
    Close Browser
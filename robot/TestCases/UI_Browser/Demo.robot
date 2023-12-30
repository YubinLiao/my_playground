*** Settings ***
Library     Browser
Library     Collections

Suite Setup   UI Test Setup  ${browser}  ${headless}  ${recordVideo}
Suite Teardown    UI Test Tearup

*** Variables ***
${browser}  chromium
${headless}  True
${recordVideo}  False

*** Test Cases ***
Test UI Components
    [Tags]  ui
    New Page    https://robotframework-browser.org/
    Set Browser Timeout    10 sec
    Get Title    ==    Browser Library

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
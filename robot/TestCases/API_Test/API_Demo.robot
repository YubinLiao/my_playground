*** Settings ***
Library               RequestsLibrary

*** Test Cases ***

Quick Get Request Test
    [Tags]  api
    ${response}=    GET  https://www.google.com
    Should Be Equal As Strings    ${response.status_code}  200

Quick Get Request With Parameters Test
    [Tags]  api
    ${response}=    GET  https://www.google.com/search  params=query=ciao  expected_status=200

Quick Get A JSON Body Test
    [Tags]  api
    ${response}=    GET  https://jsonplaceholder.typicode.com/posts/1
    Should Be Equal As Strings    1  ${response.json()}[id]

*** Settings ***
Library    SeleniumLibrary
Library    helper.py

Suite Teardown    Close Browser


*** Variables ***
${REPORT_FILE}      generated_report/report.html
${PARQUET_FOLDER}   parquet_data/facility_type_avg_time_spent_per_visit_date
${FILTER_DATE}      2026-10-10


*** Test Cases ***
Validate Report With Parquet

    Open Browser    file://${CURDIR}/${REPORT_FILE}    Edge

    ${html_df}=    Read Html Table
    ...    ${REPORT_FILE}

    ${parquet_df}=    Read Parquet Data
    ...    ${PARQUET_FOLDER}
    ...    ${FILTER_DATE}

    ${status}    ${result}=    Compare Dataframes
    ...    ${html_df}
    ...    ${parquet_df}

    Log To Console    ${result}

    Should Be True    ${status}
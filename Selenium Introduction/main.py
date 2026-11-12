import os
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.options import Options


def extract_chart_data(driver):

    chart_data = []

    texts = driver.find_elements(
        By.CSS_SELECTOR,
        "text.slicetext"
    )

    for text in texts:

        tspans = text.find_elements(
            By.TAG_NAME,
            "tspan"
        )

        if len(tspans) >= 2:

            category = tspans[0].text.strip()
            value = tspans[1].text.strip()

            chart_data.append(
                [category, value]
            )

    return chart_data


def save_chart_csv(chart_data, filename):

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Facility Type",
                "Min Average Time Spent"
            ]
        )

        writer.writerows(chart_data)

    print(f"{filename} created")


def create_table_csv(driver):

    headers = []

    header_blocks = driver.find_elements(
        By.ID,
        "header"
    )

    for header in header_blocks:

        text = header.text.strip()

        if text:
            headers.append(text)

    print("Headers:", headers)

    facility_type = []
    visit_date = []
    average_time = []

    all_cells = driver.find_elements(
        By.CLASS_NAME,
        "cell-text"
    )

    values = []

    for cell in all_cells:

        text = cell.text.strip()

        if text:
            values.append(text)

    for value in values:

        if value in [
            "Clinic",
            "Hospital",
            "Specialty Center"
        ]:

            facility_type.append(value)

        elif value.startswith("2026-"):

            visit_date.append(value)

        else:

            try:
                float(value)
                average_time.append(value)
            except:
                pass

    row_count = min(
        len(facility_type),
        len(visit_date),
        len(average_time)
    )

    with open(
        "table.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Facility Type",
                "Visit Date",
                "Average Time Spent"
            ]
        )

        for i in range(row_count):

            writer.writerow(
                [
                    facility_type[i],
                    visit_date[i],
                    average_time[i]
                ]
            )

    print("table.csv created")


# ======================
# MAIN
# ======================

edge_options = Options()

edge_options.add_experimental_option(
    "detach",
    True
)

driver = webdriver.Edge(
    options=edge_options
)

try:

    driver.maximize_window()

    html_path = os.path.abspath(
        "generated_report/report.html"
    )

    driver.get(
        f"file:///{html_path.replace(chr(92), '/')}"
    )

    time.sleep(3)

    print("Report opened")

    # Screenshot 0
    driver.save_screenshot(
        "screenshot0.png"
    )

    print("screenshot0.png created")

    # Table CSV
    create_table_csv(driver)

    # Initial chart CSV
    chart_data = extract_chart_data(driver)

    save_chart_csv(
        chart_data,
        "doughnut0.csv"
    )

    traces = driver.find_elements(
        By.CLASS_NAME,
        "traces"
    )

    print(
        f"Legend items found: {len(traces)}"
    )

    # Click every legend item
    for index in range(len(traces)):

        traces = driver.find_elements(
            By.CLASS_NAME,
            "traces"
        )

        trace = traces[index]

        toggle = trace.find_element(
            By.CLASS_NAME,
            "legendtoggle"
        )

        ActionChains(driver)\
            .move_to_element(toggle)\
            .click()\
            .perform()

        time.sleep(2)

        screenshot_name = (
            f"screenshot{index + 1}.png"
        )

        driver.save_screenshot(
            screenshot_name
        )

        print(
            f"{screenshot_name} created"
        )

        chart_data = extract_chart_data(
            driver
        )

        csv_name = (
            f"doughnut{index + 1}.csv"
        )

        save_chart_csv(
            chart_data,
            csv_name
        )

    print("\n================================")
    print("HOMEWORK COMPLETED SUCCESSFULLY")
    print("================================")
    print("table.csv")
    print("doughnut0.csv")
    print("doughnut1.csv")
    print("doughnut2.csv")
    print("doughnut3.csv")
    print("screenshot0.png")
    print("screenshot1.png")
    print("screenshot2.png")
    print("screenshot3.png")

    input("\nPress Enter to finish...")

except Exception as e:

    print("\nERROR:")
    print(e)

    input("\nPress Enter...")

finally:

    try:
        driver.quit()
    except:
        pass
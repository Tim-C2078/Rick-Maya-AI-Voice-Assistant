from AN2F_02 import helper_function_alert_window
from playwright.sync_api import expect
from datetime import datetime, timedelta
from pathlib import Path
from dateutil.parser import parse
from time import sleep
from word2number import w2n
import re
from credentials import sales_report_username, sales_report_password

delay = 7


# Convert text to numbers
def convert_ordinal_date(text):
    # Convert "first" -> "1"
    text = text.lower()

    ordinal_words = {
        "first": "1st",
        "second": "2nd",
        "third": "3rd",
        "fourth": "4th",
        "fifth": "5th",
        "sixth": "6th",
        "seventh": "7th",
        "eighth": "8th",
        "ninth": "9th",
        "tenth": "10th",
        "eleventh": "11th",
        "twelfth": "12th",
        "thirteenth": "13th",
        "fourteenth": "14th",
        "fifteenth": "15th",
        "sixteenth": "16th",
        "seventeenth": "17th",
        "eighteenth": "18th",
        "nineteenth": "19th",
        "twentieth": "20th",
        "twenty first": "21st",
        "twenty second": "22nd",
        "twenty third": "23rd",
        "twenty fourth": "24th",
        "twenty fifth": "25th",
        "twenty sixth": "26th",
        "twenty seventh": "27th",
        "twenty eighth": "28th",
        "twenty ninth": "29th",
        "thirtieth": "30th",
        "thirty first": "31st",
    }

    for word, number in ordinal_words.items():
        if word in text:
            text = text.replace(word, number)
            break

    return text


# date = "first march 2026"

# result = convert_ordinal_date(date)

# print(result)


def sales_report(start_range, end_range):
    # This is follow manual download with specific ranges:
    start_range = convert_ordinal_date(start_range)
    end_range = convert_ordinal_date(end_range)

    date1 = parse(start_range, fuzzy=True)
    date2 = parse(end_range, fuzzy=True)

    day1 = date1.day
    month1 = date1.month - 1  # jQuery UI uses 0-11
    year1 = date1.year

    day2 = date2.day
    month2 = date2.month - 1  # jQuery UI uses 0-11
    year2 = date2.year

    # #Testing Text to Date....
    # print(day1)
    # print(month1)
    # print(year1)

    return day1, day2, month1, month2, year1, year2


stores = [
    "ACCRA MALL",
    "ACHIMOTA",
    "ADENTA",
    "DANSOMAN",
    "EAST LEGON",
    "GHANA MASCO CIRCLE",
    "HAATSO",
    "KFC KIA",
    "KFC KWASHIEMAN",
    "KFC MASCO ABLEKUMA",
    "KFC AHODWO - KUMASI",
    "KFC ASHAIMAN",
    "KFC CAPE COAST",
    "KFC DODOWA",
    "KFC DOME",
    "KFC EAST LEGON BOUNDARY",
    "KFC EL HILLS",
    "KFC HO",
    "KFC JUNCTION MALL",
    "KFC KASOA",
    "KFC KNUST",
    "KFC KOFORIDUA",
    "KFC KWABENYA",
    "KFC MANET JUNCTION",
    "KFC MASCO ASOKWA",
    "KFC MASCO BEKWAI",
    "KFC MASCO TAMALE",
    "KFC MILE 7",
    "KFC OSU",
    "KFC TAKORADI",
    "KFC TARKWA",
    "MARINA MALL",
    "MELCOM",
    "SAKUMONO",
    "SUNYANI",
    "TEMA SHELL",
    "WEIJA",
]


def sales_report_automate(context, page, day1, day2, month1, month2, year1, year2):
    dest_folder = Path(__file__).parent / "downloads"
    dest_folder.mkdir(parents=True, exist_ok=True)

    context.clear_cookies()

    helper_function_alert_window(
        page, "In 5 seconds go to: https://web.gaap.co.za:1946/index.html"
    )
    page.goto("https://web.gaap.co.za:1946/index.html", wait_until="domcontentloaded")

    helper_function_alert_window(page, "Empty the username and password fields.")
    page.locator("//*[@id='edtUser']").fill("")
    page.locator("//*[@id='edtPass']").fill("")

    helper_function_alert_window(page, "Enter Username and Password in the webpage.")
    page.locator("//*[@id='edtUser']").fill(sales_report_username)
    page.locator("//*[@id='edtPass']").fill(sales_report_password)

    helper_function_alert_window(page, "Logging user in.")
    page.locator("//*[@id='btnLogin']/span").click()

    helper_function_alert_window(page, "Navigating to Management Overview Report.")
    page.locator("//*[@id='container2']/li[3]/ul/li/a").click()
    page.locator("//*[@id='ui-accordion-accordion-header-2']/a").click()
    page.locator("//*[@id='ui-accordion-accordion-panel-2']/div[1]").click()

    # Create a Specific Date Range Report
    helper_function_alert_window(page, "Select Start Date Range.")
    page.locator(
        "//*[@id='reportparams']/div[2]/img"
    ).click()  # Select Start Date Range

    page.locator('//*[@id="ui-datepicker-div"]/div/div/select[1]').select_option(
        str(month1)
    )  # Select Start Date Range

    page.locator('//*[@id="ui-datepicker-div"]/div/div/select[2]').select_option(
        str(year1)
    )  # Select Start Date Range

    page.locator(
        f'.ui-datepicker-calendar td[data-month="{month1}"][data-year="{year1}"]'
    ).get_by_text(
        str(day1), exact=True
    ).click()  # Select 1st September 2026

    helper_function_alert_window(page, "Select End Date Range.")
    page.locator("//*[@id='reportparams']/div[3]/img").click()  # Select End Date Range
    page.locator('//*[@id="ui-datepicker-div"]/div/div/select[1]').select_option(
        str(month2)
    )  # Select End Date Range

    page.locator('//*[@id="ui-datepicker-div"]/div/div/select[2]').select_option(
        str(year2)
    )  # Select End Date Range
    page.locator(
        f'.ui-datepicker-calendar td[data-month="{month2}"][data-year="{year2}"]'
    ).get_by_text(
        str(day2), exact=True
    ).click()  # Select 22nd September 2026

    for i, store in enumerate(stores):

        # =========================
        # OPEN BRANCH SELECTION
        # =========================

        helper_function_alert_window(page, f"Selecting {store}.")

        page.locator('//*[@id="mw_1"]').click()

        # Select current store
        page.locator("tbody[role='alert']").get_by_text(store, exact=True).click()

        # =========================
        # IF NOT FIRST STORE:
        # UNCHECK PREVIOUS STORE
        # =========================

        if i > 0:
            previous_store = stores[i - 1]

            page.locator("tbody[role='alert']").get_by_text(
                previous_store, exact=True
            ).click()

        # Confirm branch selection
        page.locator('//*[@id="mw_buttonok_1"]/div').click()

        # =========================
        # SELECT STOCK GROUP = ALL
        # =========================

        helper_function_alert_window(page, "Select Stock Group.")

        page.locator('//*[@id="mw_2"]').click()

        page.locator("#mw_quick").select_option("All")

        page.locator('//*[@id="mw_buttonok_2"]/div').click()

        # =========================
        # DOWNLOAD
        # =========================

        helper_function_alert_window(page, "Clicking Download button!")

        with page.expect_download() as download_info:
            page.locator('//*[@id="btnExcel2"]').click()

            # Wait 7 seconds for download
            sleep(delay)

        download = download_info.value

        # Keep the original file extension/format
        original_name = download.suggested_filename
        extension = Path(original_name).suffix

        # Rename using the store name
        download.save_as(dest_folder / f"{store}{extension}")

        helper_function_alert_window(page, "File Saved!")

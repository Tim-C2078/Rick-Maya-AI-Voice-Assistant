from AN2F_02 import helper_function_alert_window, playwright_web_interaction_base
from playwright.sync_api import expect
from datetime import datetime, timedelta
from pathlib import Path
from dateutil.parser import parse
from credentials import sales_report_username, sales_report_password

today = datetime.now()

yesterday = today - timedelta(days=1)
mtd_month = yesterday.month - 1  # jQuery UI uses 0-11
mtd_year = yesterday.year

# print(f"Yesterday: {yesterday.day}")
# print(f"Month: {mtd_month}")
# print(f"Year: {mtd_year}")

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

from time import sleep

delay = 7


def sales_report_automate1(context, page):
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

    # Month To Report Range
    helper_function_alert_window(page, "Select Start Date Range.")
    page.locator(
        "//*[@id='reportparams']/div[2]/img"
    ).click()  # Select Start Date Range
    page.locator(
        f'.ui-datepicker-calendar td[data-month="{mtd_month}"][data-year="{mtd_year}"]'
    ).get_by_text("1", exact=True).click()

    helper_function_alert_window(page, "Select End Date Range.")
    page.locator("//*[@id='reportparams']/div[3]/img").click()  # Select End Date Range
    page.locator(
        f'.ui-datepicker-calendar td[data-month="{mtd_month}"][data-year="{mtd_year}"]'
    ).get_by_text(str(yesterday.day), exact=True).click()

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

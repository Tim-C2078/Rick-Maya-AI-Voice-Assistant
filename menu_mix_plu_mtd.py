from calendar import day_name
from AN2F_04 import helper_function_alert_window, playwright_web_interaction_base1
from time import sleep
from dateutil.parser import parse
from datetime import datetime, timedelta
from credentials import Mx_username, Mx_password

stores = [
    "Osu",
    "Melcom Plus",
    "Sakumono - Spintex Road",
    "37 Liberation",
    "Dansoman",
    "KGH006 East Legon",
    "Shell Asokwa",
    "BOHYE",
    "Achimota Mall",
    "Tema Shell",
    "Shell Bekwai Roundabout",
    "Shell Haatso Atomic",
    "Shell Adenta",
    "TOTAL TAKORADI",
    "Shell Tamale",
    "Accra Mall",
    "Shell Weija",
    "Sunyani",
    "Circle",
    "Kwashieman Junction",
    "Ashiaman",
    "Kasoa",
    "Ahodwo (Sonar Center)",
    "Koforidua",
    "Ablekuma",
    "Techiman",
    "Cape Coast",
    "Boundary Road",
    "Kwabenya",
    "kfc Dome Ghana",
    "TARKWA",
    "KGH033 East Legon Hills Road",
    "KNUST",
    "Kia (Airport Shell)",
    "DODOWA",
    "Manet Junction",
    "Kumasi PATASI",
    "MILE 7",
    "TEMA C-25",
    "KOKOBEN KUMASI",
    "AFIENYA",
    "OYARIFA",
    "ASOKORE MAMPONG",
    "SOKOBAN",
]


# This is follow manual download with specific ranges:
command_text = "Get me all sales data for kfc Month to Date"

today = datetime.now()

first_day_of_month = today.replace(day=1)
day_name = first_day_of_month.strftime("%A")
yesterday = today - timedelta(days=1)

day2 = yesterday.day
day22 = yesterday.strftime("%A")  # "Tuesday"
day222 = yesterday.strftime("%d")  # "15"
month2 = yesterday.strftime("%B")  # "September"
year2 = yesterday.strftime("%Y")  # "2026"

print(day_name)
print(day2)
print(day22)
print(day222)
print(month2)
print(year2)


def send_text(context, page):
    context.clear_cookies()

    helper_function_alert_window(
        page, "In 5 seconds go to: https://kfcrossa.macromatix.net/MMS_Logon.aspx"
    )
    page.goto(
        "https://kfcrossa.macromatix.net/MMS_Logon.aspx", wait_until="domcontentloaded"
    )

    helper_function_alert_window(page, "Empty the username and password fields.")
    page.locator("#Login_UserName").fill("")
    page.locator("#Login_Password").fill("")

    helper_function_alert_window(page, "Enter Username and Password in the webpage.")
    page.locator("#Login_UserName").fill(Mx_username)
    page.locator("#Login_Password").fill(Mx_password)

    helper_function_alert_window(page, "Logging user in.")
    page.locator("#Login_Button1").click()

    helper_function_alert_window(page, "Navigate to menu mix report.")
    page.locator(".rpItem").get_by_text("Reporting", exact=True).click()
    page.locator(".rmItem").get_by_text("Report Selector", exact=True).click()
    page.locator('//*[@id="ctl00_ph_ListBoxReports"]').select_option(
        "Product Mix By Date with PLU"
    )

    sleep(1)

    helper_function_alert_window(page, "Select Start Range.")
    page.locator(
        '//*[@id="ctl00_ph_DateRangePicker_DatePickerStart_popupButton"]'
    ).click()
    page.locator(
        f"#ctl00_ph_DateRangePicker_DatePickerStart_calendar_Top "
        f'tbody td[title="{day_name}, {month2} 01, {year2}"] a'
    ).click()

    helper_function_alert_window(page, "Select End Range.")
    page.locator(
        '//*[@id="ctl00_ph_DateRangePicker_DatePickerEnd_popupButton"]'
    ).click()
    page.locator(
        f"#ctl00_ph_DateRangePicker_DatePickerEnd_calendar_Top "
        f'tbody td[title="{day22}, {month2} {day222}, {year2}"] a'
    ).click()

    helper_function_alert_window(page, "Change file format to Excel.")
    page.locator(
        '//*[@id="Skinnedctl00_ph_DropDownListReportFormat"]/span/span'
    ).click()
    page.locator("li[unselectable='on']").get_by_text("Excel", exact=True).click()

    for store in stores:
        helper_function_alert_window(page, f"Selecting {store}.")

        page.locator('//*[@id="ctl00_ph_DropDownListStore_Input"]').click()

        if store in ["KGH006 East Legon", "KGH033 East Legon Hills Road"]:
            page.locator('//*[@id="ctl00_ph_DropDownListStore_DropDown"]').get_by_text(
                store, exact=True
            ).click()

        else:
            page.locator('//*[@id="ctl00_ph_DropDownListStore_DropDown"]').get_by_text(
                store, exact=False
            ).click()

        helper_function_alert_window(page, f"Downloading Report for {store}.")
        page.locator('//*[@id="ctl00_ph_ButtonGenerate"]').click()

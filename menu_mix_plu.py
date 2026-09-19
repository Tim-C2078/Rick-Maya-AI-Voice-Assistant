from AN2F_04 import helper_function_alert_window, playwright_web_interaction_base1
from time import sleep
from dateutil.parser import parse
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


def menu_mix(start_range, end_range):
    # This is follow manual download with specific ranges:
    start_range = convert_ordinal_date(start_range)
    end_range = convert_ordinal_date(end_range)

    date1 = parse(start_range, fuzzy=True)
    date2 = parse(end_range, fuzzy=True)

    day1 = date1.day
    day11 = date1.strftime("%A")
    day111 = date1.strftime("%d")
    month1 = date1.strftime("%B")
    month_short2 = date1.strftime("%b")
    year1 = date1.year

    day2 = date2.day
    day22 = date2.strftime("%A")
    day222 = date2.strftime("%d")
    month2 = date2.strftime("%B")
    month_short3 = date2.strftime("%b")
    year2 = date2.year

    # # Testing Text to Date....
    # print(day1)
    # print(day11)
    # print(day111)
    # print(month1)
    # print(year1)

    return (
        day1,
        day11,
        day111,
        day2,
        day22,
        day222,
        month1,
        month2,
        year1,
        year2,
        month_short2,
        month_short3,
    )


def send_text4(
    context,
    page,
    day1,
    day11,
    day111,
    day2,
    day22,
    day222,
    month1,
    month2,
    year1,
    year2,
    month_short2,
    month_short3,
):
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

    helper_function_alert_window(page, "Navigate to staff meal report.")
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
        '//*[@id="ctl00_ph_DateRangePicker_DatePickerStart_calendar_Title"]'
    ).click()

    page.locator(f"#rcMView_{month_short2}").click()
    page.locator(f"#rcMView_{year1}").click()

    page.locator(f'//*[@id="rcMView_OK"]').click()

    page.locator(
        f"#ctl00_ph_DateRangePicker_DatePickerStart_calendar_Top "
        f'tbody td[title="{day11}, {month1} {day111}, {year1}"] a'
    ).click()

    helper_function_alert_window(page, "Select End Range.")
    page.locator(
        '//*[@id="ctl00_ph_DateRangePicker_DatePickerEnd_popupButton"]'
    ).click()

    page.locator(
        '//*[@id="ctl00_ph_DateRangePicker_DatePickerEnd_calendar_Title"]'
    ).click()

    page.locator(f"#rcMView_{month_short3}").click()
    page.locator(f"#rcMView_{year2}").click()

    page.locator(f'//*[@id="rcMView_OK"]').click()

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

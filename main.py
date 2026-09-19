from AN2F_02 import playwright_web_interaction_base
from AN2F_04 import playwright_web_interaction_base1


import pyttsx3
from nltk.tokenize import word_tokenize
import time
from datetime import datetime
import pywhatkit
import requests
import speech_recognition as sr
import smtplib
import psutil
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from newsapi import NewsApiClient
import os
import clipboard
import pyautogui
import webbrowser as wb
from time import sleep
import wikipedia
import time as tt
import pyjokes

# Import credentials from a private file (NOT named secrets.py)
from credentials import (
    sendermail,
    senderpassword,
    contacts,
    username,
    weather_api_key,
    news_api_key,
)

# Specific Date Range Reports
from sales_report import (
    sales_report,
    sales_report_automate,
)
from staff_meal_report import send_text3, staff_meal
from menu_mix_plu import send_text4, menu_mix

# Month To Date Imports
from sales_report_mtd import sales_report_automate1
from staff_meal_report_mtd import send_text1
from menu_mix_plu_mtd import send_text

# ------------------------------------------------------------------
# Global voice preference
# ------------------------------------------------------------------
CURRENT_VOICE_ID = None


# ------------------------------------------------------------------
# Speech
# ------------------------------------------------------------------
def speak(audio):
    print(f"[SPEAKING] {audio}")
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)

    if CURRENT_VOICE_ID is not None:
        engine.setProperty("voice", CURRENT_VOICE_ID)

    engine.say(audio)
    engine.runAndWait()
    engine.stop()
    del engine
    time.sleep(0.1)


def getvoices(voice):
    global CURRENT_VOICE_ID
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.stop()
    del engine

    if voice == "male":
        CURRENT_VOICE_ID = voices[0].id
        print(f"[VOICE] Male selected: {CURRENT_VOICE_ID}")
        speak("Hello, I am Sentry, your personal assistant.")
    elif voice == "female":
        CURRENT_VOICE_ID = voices[1].id
        print(f"[VOICE] Female selected: {CURRENT_VOICE_ID}")
        speak("Hello, I am Maya, your personal assistant.")


# ------------------------------------------------------------------
# Time / Date
# ------------------------------------------------------------------
def tell_time():
    now = datetime.now()
    current_minutes = now.minute
    current_hour = now.strftime("%I")
    period = now.strftime("%p")

    minutes_remaining = 60 - current_minutes
    next_hour = 1 + int(current_hour)

    t = f"The current time is {minutes_remaining} minutes past {next_hour} {period}."
    speak(t)


def tell_date():
    d = datetime.now().strftime("%A, %d %B %Y")
    speak(f"the current date is {d}")


def greeting():
    period = datetime.now().strftime("%p")
    hour = datetime.now().hour
    if period == "AM":
        speak("Good Morning Master!")
    elif 12 <= hour < 17:
        speak("Good Afternoon Master!")
    else:
        speak("Good Evening Master!")


def goodmessage():
    speak(
        "That's good to hear master. Always remeber to write your goals down... Clarity helps ... and again .... you will be fine."
    )


def badmessage():
    period = datetime.now().strftime("%p")
    hour = datetime.now().hour
    if period == "AM":
        speak(
            "Seems like you had a bad evening master. "
            "Please always remember the 7 philosophies for the same shit... "
            "Firstly - ... Shit happens but nothing really matters anyways ... "
            "Secondly - ... Shit happens but forcus on what you can control ... "
            "Thirdly - ... Shit happens but it's all part of the natural flow ... "
            "Forth - ... Shit happens because it was always going to happen ... "
            "Fifth - ... Shit happens and thats a confirmation that everything is going to be completely wrong ... "
            "Sixth - ... Shit happens but let's find a way to make it more pleasurable ... "
            "And lastly - ... when shit happens, fuck off and go to sleep. It helps."
        )
    elif 12 <= hour < 17:
        speak(
            "Seems like you had a bad morning master."
            "Please always remember the 7 philosophies for the same shit... "
            "Firstly - ... Shit happens but nothing really matters anyways ... "
            "Secondly - ... Shit happens but forcus on what you can control ... "
            "Thirdly - ... Shit happens but it's all part of the natural flow ... "
            "Forth - ... Shit happens because it was always going to happen ... "
            "Fifth - ... Shit happens and thats a confirmation that everything is going to be completely wrong ... "
            "Sixth - ... Shit happens but let's find a way to make it more pleasurable ... "
            "And lastly - ... when shit happens, fuck off and go to sleep. It helps."
        )
    else:
        speak(
            "Seems like you had a bad afternoon master."
            "Please always remember the 7 philosophies for the same shit... "
            "Firstly - ... Shit happens but nothing really matters anyways ... "
            "Secondly - ... Shit happens but forcus on what you can control ... "
            "Thirdly - ... Shit happens but it's all part of the natural flow ... "
            "Forth - ... Shit happens because it was always going to happen ... "
            "Fifth - ... Shit happens and thats a confirmation that everything is going to be completely wrong ... "
            "Sixth - ... Shit happens but let's find a way to make it more pleasurable ... "
            "And lastly - ... when shit happens, fuck off and go to sleep. It helps."
        )


def wishme():
    greeting()
    speak("Welcome back!")
    speak("I am at your service.")
    speak("How is your day going so far master?")


# ------------------------------------------------------------------
# Input
# ------------------------------------------------------------------
def takeCommand():
    return input("How may I assist you?\n")


def takeCommandMic(phrase_limit=15, pause=1.5):
    """
    Record from the mic.
      phrase_limit: max seconds of a single recording (default 15)
      pause:        seconds of silence that ends the recording (default 1.5)
    """
    r = sr.Recognizer()
    r.pause_threshold = pause

    with sr.Microphone() as source:
        print("Listening....")
        r.adjust_for_ambient_noise(source, duration=0.4)
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=phrase_limit)
        except sr.WaitTimeoutError:
            print("[MIC] No speech detected within 10 seconds.")
            return "none"

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language="en-GH")
        print("You said:", query)
    except sr.UnknownValueError:
        print("[MIC] Could not understand audio.")
        speak("Say that again master....")
        return "none"
    except sr.RequestError as e:
        print(f"[MIC] Google API error: {e}")
        speak("My speech service is unavailable.")
        return "none"
    return query


# ------------------------------------------------------------------
# Email
# ------------------------------------------------------------------
def sendEmail(to_addr, subject, body):
    print(f"[EMAIL] Sending to {to_addr} — subject: {subject}")
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sendermail
    msg["To"] = to_addr
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()

    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
    server.starttls()
    server.login(sendermail, senderpassword)
    server.sendmail(sendermail, [to_addr], msg.as_string())
    server.quit()
    print("[EMAIL] Done.")


def sendwhatsmsg(phone_no, message):
    Message = message.replace(" ", "%20")
    wb.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={Message}")
    sleep(15)
    pyautogui.press("enter")


def checkemotions():
    speak("I am sorry master, I am not programmed to have emotions")


def meaningoflife():
    speak(
        "Hmmm .... well master... I wish I had an easy answer for you,... since the is no one answer... But I think you need to decide,...and most importantly ... don't waste any time, just don't waste any time. God loves you sir... Remember that."
    )


def searchgoogle():
    speak("What would you like me to search for?")
    search = takeCommandMic(phrase_limit=10, pause=2.5).lower()
    wb.open(f"https://www.google.com/search?q={search}")


def news():

    speak("Which topic would you like to hear about?")
    topic = takeCommandMic(phrase_limit=10, pause=2.5).lower()  # Default topic

    newsapi = NewsApiClient(api_key=news_api_key)

    # Use get_everything for reliability on the free tier
    response = newsapi.get_everything(
        q=topic, language="en", sort_by="publishedAt", page_size=5
    )
    articles = response.get("articles", [])

    print(f"[DEBUG] Total articles returned: {len(articles)}")

    if not articles:
        speak("Sorry, I couldn't find any news right now.")
        return

    # Build the headline string
    headlines_text = "Here are the top news headlines. "
    for i, article in enumerate(articles[:3], start=1):
        title = article.get("title") or "No title available"
        title = title.split(" - ")[0]
        headlines_text += f"Headline {i}: {title}. "

    speak(headlines_text)
    speak("Which article would you like me to open? Say first, second, or third.")

    user_response = takeCommandMic(phrase_limit=5, pause=2.5)
    print(f"[DEBUG] User said: {user_response!r}")

    if not user_response:
        speak("I didn't catch that. Skipping the article.")
        speak("That's all for now. Stay informed and have a great day!")
        return

    user_response = user_response.lower().strip()

    index = None
    if any(word in user_response for word in ["first", "1", "one"]):
        index = 0
    elif any(word in user_response for word in ["second", "2", "two"]):
        index = 1
    elif any(word in user_response for word in ["third", "3", "three"]):
        index = 2

    if index is not None and index < len(articles):
        url = articles[index].get("url")
        if url:
            speak(f"Opening article {index + 1} now.")
            wb.open(url)
        else:
            speak("Sorry, I couldn't find a link for that article.")
    else:
        speak("Alright, I won't open the news website.")

    speak("That's all for now. Stay informed and have a great day!")


def text2speech():
    text = clipboard.paste()
    if text:
        speak(text)


def screenshot():
    name_img = tt.time()
    name_img = (
        f"C:\\Users\\Admin\\Desktop\\Projects\\jean.2.0\\screenshots\\{name_img}.png"
    )
    img = pyautogui.screenshot(name_img)
    img.show()


def cpu():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage}")
    battery = psutil.sensors_battery()
    speak(f"Battery is at ")
    speak(battery.percent)


# ------------------------------------------------------------------
# Main loop
# ------------------------------------------------------------------
if __name__ == "__main__":
    wishme()
    wakeword = "rick"
    while True:
        query = takeCommandMic(phrase_limit=5, pause=0.8).lower()
        query = word_tokenize(query)
        print(query)
        if wakeword in query:
            if "time" in query:
                tell_time()

            elif "date" in query:
                tell_date()

            elif "meaning of life" in query:
                meaningoflife()

            elif any(w in query for w in ["good", "fine", "can't complain"]):
                goodmessage()

            elif any(w in query for w in ["tired", "shit", "i don't know"]):
                badmessage()

            elif any(w in query for w in ["feeling", "emotions"]):
                checkemotions()

            elif "voice" in query:
                if "male" in query:
                    getvoices("male")
                elif "female" in query:
                    getvoices("female")

            elif "email" in query:
                try:
                    speak("Who is the recipient?")
                    name = takeCommandMic(phrase_limit=10, pause=1.5).lower().strip()

                    # Check if the contact exists in the contacts dictionary
                    recipient = contacts.get(name)

                    if not recipient:
                        speak("I don't know that contact.")
                        continue

                    speak("What is the subject?")
                    subject = takeCommandMic(phrase_limit=10, pause=1.5)

                    speak("What should I say?")
                    content = takeCommandMic(phrase_limit=20, pause=3.0)

                    sendEmail(recipient, subject, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry Master! I am unable to send this email.")

            elif "whatsapp" in query:
                try:
                    speak("Who is the recipient?")
                    name = takeCommandMic(phrase_limit=10, pause=1.5).lower().strip()

                    # Check if the username exists in the username dictionary
                    phone_no = username.get(name)

                    if not phone_no:
                        speak("I don't know that username.")
                        continue

                    speak("What should I say?")
                    message = takeCommandMic(phrase_limit=20, pause=3.0)

                    sendwhatsmsg(phone_no, message)
                    speak("Message has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry Master! I am unable to send this email.")

            elif "wikipedia" in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    speak(results)
                except Exception as e:
                    print(e)
                    speak(
                        "Sorry Master! I couldn't find any information on that topic."
                    )

            elif "search" in query:
                searchgoogle()

            elif "youtube" in query:
                speak("What would you like me to search for on YouTube?")
                topic = takeCommandMic(phrase_limit=10, pause=2.5).lower()
                pywhatkit.playonyt(topic)

            elif "weather" in query:
                speak("What city would you like me to check the weather for?")
                city = takeCommandMic(phrase_limit=10, pause=2.5).lower()
                url = "https://api.openweathermap.org/data/2.5/weather"
                params = {"q": city, "units": "imperial", "appid": weather_api_key}
                response = requests.get(url, params=params)
                data = response.json()
                weather = data["weather"][0]["main"]
                weather_description = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                temperature_celsius = (temperature - 32) * 5 / 9
                speak(
                    f"Well currently we have {weather} out in {city.capitalize()}, with {weather_description}. The temperature outside is {temperature_celsius:.1f}°C."
                )

            elif "news" in query:
                news()

            elif "text to speech" in query or "read text" in query:
                text2speech()

            elif "open code" in query:
                filepath = "C:\\Users\\Admin\\AppData\\Local\\Programs\\Microsoft VS Code\\code.exe"
                os.startfile(filepath)

            elif "open excel" in query:
                filepath = (
                    "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
                )
                os.startfile(filepath)

            elif "open word" in query:
                filepath = (
                    "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
                )
                os.startfile(filepath)

            elif "open powerpoint" in query:
                filepath = (
                    "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
                )
                os.startfile(filepath)

            elif "open power bi" in query:
                filepath = (
                    "C:\\Program Files\\Microsoft Power BI Desktop\\bin\\PBIDesktop.exe"
                )
                os.startfile(filepath)

            elif "sales report" in query:

                speak("Alright master")
                speak(
                    "Give me the starting date range. And please remember to mention the full date including the year."
                )
                start_range = takeCommandMic(phrase_limit=10, pause=1.5).lower().strip()
                speak(
                    "Give me the ending date range. And please remember to mention the full date including the year."
                )
                end_range = takeCommandMic(phrase_limit=10, pause=1.5).lower().strip()
                speak("Processing request master")

                # Convert the dates
                day1, day2, month1, month2, year1, year2 = sales_report(
                    start_range, end_range
                )
                print(start_range, end_range)

                # Start the Playwright automation
                playwright_web_interaction_base(
                    sales_report_automate,
                    "msedge",
                    day1,
                    day2,
                    month1,
                    month2,
                    year1,
                    year2,
                )

            elif "stuff mail" in query or "staff mail" in query:

                speak("Alright master")
                speak(
                    "Give me the starting date range. And please remember to mention the full date including the year."
                )
                start_range = takeCommandMic(phrase_limit=10, pause=1.5).lower().strip()
                speak(
                    "Give me the ending date range. And please remember to mention the full date including the year."
                )
                end_range = takeCommandMic(phrase_limit=10, pause=1.5).lower().strip()
                speak("Processing request master")

                (
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
                ) = staff_meal(start_range, end_range)

                print(start_range, end_range)

                # Start the Playwright automation
                playwright_web_interaction_base1(
                    send_text3,
                    "msedge",
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

            elif "menu mix" in query:

                speak("Alright master")
                speak(
                    "Give me the starting date range. And please remember to mention the full date including the year."
                )
                start_range = takeCommandMic(phrase_limit=10, pause=1.5).lower().strip()
                speak(
                    "Give me the ending date range. And please remember to mention the full date including the year."
                )
                end_range = takeCommandMic(phrase_limit=10, pause=1.5).lower().strip()
                speak("Processing request master")

                (
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
                ) = menu_mix(start_range, end_range)

                print(start_range, end_range)

                # Start the Playwright automation
                playwright_web_interaction_base1(
                    send_text4,
                    "msedge",
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

            elif "sales mtd" in query:
                speak("Processing request master")
                playwright_web_interaction_base(sales_report_automate1, "msedge")

            elif "stuff mail mtd" in query or "staff mail mtd" in query:
                speak("Processing request master")
                playwright_web_interaction_base1(send_text1, "msedge")

            elif "menu mix mtd" in query:
                speak("Processing request master")
                playwright_web_interaction_base1(send_text, "msedge")

            elif "screenshot" in query:
                screenshot()

            elif "cpu" in query:
                cpu()

            elif "joke" in query:
                speak(pyjokes.get_joke())

            elif "open" in query:
                os.system("explorer C://{}".format(query.replace("Open", "")))

            elif "remind me later" in query:
                speak("What should I remember you about?")
                data = takeCommandMic(phrase_limit=10, pause=1.5).lower().strip()
                speak(f"you said me to remeber you that {data}")
                remember = open("reminders\\data.txt", "w")
                remember.write(data)
                remember.close()

            elif "do you know something" in query:
                remember = open("reminders\\data.txt", "r")
                speak(f"you told me to remember that {remember.read()}")

            elif (
                "exit" in query
                or "quit" in query
                or "sleep" in query
                or "cancel" in query
            ):
                speak("Goodbye Master!")
                break

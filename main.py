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

# Name fragments used to match installed voices (case-insensitive).
# Based on your installed voice list.
VOICE_KEYWORDS = {
    # Male voices
    "brian": ["brian"],
    "geraint": ["geraint"],
    "joey": ["joey"],
    "russell": ["russell"],
    "david": ["david"],
    # Female voices
    "emma": ["emma"],
    "gwyneth": ["gwyneth"],
    "ivy": ["ivy"],
    "jennifer": ["jennifer"],
    "kendra": ["kendra"],
    "kimberly": ["kimberly"],
    "nicole": ["nicole"],
    "salli": ["salli"],
    "amy": ["amy"],
    "zira": ["zira"],
    # High-level aliases
    "male": ["brian", "geraint", "joey", "russell", "david", "male"],
    "female": [
        "emma",
        "gwyneth",
        "ivy",
        "jennifer",
        "kendra",
        "kimberly",
        "nicole",
        "salli",
        "amy",
        "zira",
        "female",
    ],
    # Persona names
    "sentry": ["brian"],  # Sentry = British male
    "maya": ["gwyneth"],  # Maya   = Welsh English female
}

# TTS tuning
TTS_RATE = 150  # 150 is a natural pace for Ivona; 170 is a bit fast
TTS_VOLUME = 1.0


# ------------------------------------------------------------------
# Speech
# ------------------------------------------------------------------
def speak(audio):
    print(f"[SPEAKING] {audio}")
    engine = pyttsx3.init()
    engine.setProperty("rate", TTS_RATE)
    engine.setProperty("volume", TTS_VOLUME)

    if CURRENT_VOICE_ID is not None:
        engine.setProperty("voice", CURRENT_VOICE_ID)

    # Small lead-in pause helps Ivona voices avoid clipping the first syllable
    time.sleep(0.15)
    engine.say(audio)
    engine.runAndWait()
    engine.stop()
    del engine
    time.sleep(0.1)


def getvoices(voice, announce=True):
    """Select a TTS voice by preference key.

    If announce=True and the voice actually changes, speak a greeting.
    If the voice is already active, stay silent.
    """
    global CURRENT_VOICE_ID

    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.stop()
    del engine

    keywords = VOICE_KEYWORDS.get(voice, [voice])
    matched = None

    for kw in keywords:
        for v in voices:
            if kw.lower() in v.name.lower():
                matched = v
                break
        if matched:
            break

    if not matched:
        matched = voices[0]
        print(f"[VOICE] No match for '{voice}', falling back to {matched.name}")

    # If it's the same voice we're already using, do nothing (no greeting)
    if matched.id == CURRENT_VOICE_ID:
        print(f"[VOICE] Already using: {matched.name} (no change)")
        return

    CURRENT_VOICE_ID = matched.id
    print(f"[VOICE] Selected: {matched.name}")
    print(f"[VOICE] ID: {CURRENT_VOICE_ID}")

    if announce:
        if voice in ("male", "sentry", "brian", "geraint", "joey", "russell", "david"):
            speak("Hello, I am Sentry, your personal assistant.")
        else:
            speak("Hello, I am Maya, your personal assistant.")


def listvoices():
    """Speak a short sample from every installed voice, one after another."""
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.stop()
    del engine

    speak(f"I found {len(voices)} voices installed on this system.")

    for i, v in enumerate(voices, start=1):
        print(f"[VOICE {i}] {v.name}")
        speak(f"Voice number {i}. {v.name}.")

        engine = pyttsx3.init()
        engine.setProperty("rate", TTS_RATE)
        engine.setProperty("volume", TTS_VOLUME)
        engine.setProperty("voice", v.id)
        time.sleep(0.15)
        engine.say(f"Hello master, this is voice number {i}.")
        engine.runAndWait()
        engine.stop()
        del engine
        time.sleep(0.2)

    speak("That is all the voices I have available.")


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


def takeCommandMic(phrase_limit=15, pause=2.5):
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

    # Two wake words — each maps to a persona voice
    WAKE_WORDS = {
        "rick": "male",  # "rick ..."  -> Sentry (male voice)
        "maya": "female",  # "maya ..."  -> Maya   (female voice)
    }

    # Default voice on startup
    getvoices("male")

    while True:
        query = takeCommandMic(phrase_limit=5, pause=0.8).lower()
        query = word_tokenize(query)
        print(query)

        # --- Detect wake word + auto-switch persona voice ---
        detected_wakeword = None
        for ww in WAKE_WORDS:
            if ww in query:
                detected_wakeword = ww
                break

        if detected_wakeword:
            # Switch voice to match the wake word's persona
            getvoices(WAKE_WORDS[detected_wakeword])

            # -------------------- Commands --------------------
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

            elif "list" in query and "voice" in query:
                listvoices()

            elif "voice" in query:
                if (
                    "geraint" in query
                    or "male" in query
                    or "sentry" in query
                    or "brian" in query
                ):
                    getvoices("male")
                elif (
                    "gwyneth" in query
                    or "female" in query
                    or "maya" in query
                    or "emma" in query
                ):
                    getvoices("female")
                elif "zira" in query:
                    getvoices("zira")
                elif "david" in query:
                    getvoices("david")
                else:
                    speak(
                        "Which voice would you like? Say male, female, Geraint, or Gwyneth."
                    )
                    choice = takeCommandMic(phrase_limit=5, pause=1.5).lower().strip()
                    if not choice:
                        speak("I did not catch that.")
                    elif any(
                        w in choice for w in ["geraint", "male", "sentry", "brian"]
                    ):
                        getvoices("male")
                    elif any(
                        w in choice for w in ["gwyneth", "female", "maya", "emma"]
                    ):
                        getvoices("female")
                    elif "zira" in choice:
                        getvoices("zira")
                    elif "david" in choice:
                        getvoices("david")
                    else:
                        speak("Sorry, I do not have that voice installed.")

            elif "email" in query:
                try:
                    speak("Who is the recipient?")
                    name = takeCommandMic(phrase_limit=10, pause=1.5).lower().strip()

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

                day1, day2, month1, month2, year1, year2 = sales_report(
                    start_range, end_range
                )
                print(start_range, end_range)

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

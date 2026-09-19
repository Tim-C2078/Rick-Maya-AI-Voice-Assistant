import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 170)

# Paste the exact ID from your list
engine.setProperty(
    "voice",
    "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\IVONA 2 Voice GeraintEN22",
)

engine.say("Hello master, I am now using the Ivona voice.")
engine.runAndWait()

# engine = pyttsx3.init()
# voices = engine.getProperty("voices")

# print(f"Found {len(voices)} voices:")
# for i, voice in enumerate(voices):
#     print(f"Index {i}:")
#     print(f"  Name: {voice.name}")
#     print(f"  ID: {voice.id}")
#     print("-" * 20)

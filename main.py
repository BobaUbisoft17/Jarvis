from vosk import Model, KaldiRecognizer
import pyaudio, json
import pyglet
import os
import asyncio
import multiprocessing
import webbrowser


model = Model("vosk-model-small-ru-0.22")
rec = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()


def manage_browser(search: str) -> None:
    if search == "meme":
        webbrowser.register(name="Chrome", klass=None, instance=webbrowser.BackgroundBrowser("C:/Program Files/Google/Chrome/Application/chrome.exe"))
        webbrowser.get(using="chrome").open_new_tab("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    elif search == "quit":
        os.system("taskkill /im chrome.exe /f")
    else:
        webbrowser.register(name="Chrome", klass=None, instance=webbrowser.BackgroundBrowser("C:/Program Files/Google/Chrome/Application/chrome.exe"))
        webbrowser.get(using="chrome").open_new_tab(f"https://www.google.com/search?q={search}")


def home_space():
    music = pyglet.resource.media("music/homespace/ACDC - Back In Black.mp3")
    music.play()

    pyglet.app.run()


def listen():
    thread = multiprocessing.Process(target=home_space)
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(rec.Result())["text"]
            if answer:
                if answer == "я дома":
                    thread.start()
                if answer == "выключи музыку":
                    thread.terminate()
                if answer == "ты доверяешь мне":
                    manage_browser("meme")
                if "найди в интернете" in answer:
                    manage_browser(answer[18:])
                if answer == "закрой браузер":
                    manage_browser("quit")
                if answer == "перезагрузка":
                    os.system("shutdown -r -t 0")
                if answer == "выключи комп":
                    os.system("shutdown -s -t 0")
                if answer == "пора на боковую":
                    quit()
                print(answer)


if __name__ == "__main__":
    listen()










"""for text in listen():
    if text == "привет":
        print("Вечер в хату")
    elif text == "до встречи":
        print("Бывай")
        quit()
    else:
        print(text)"""


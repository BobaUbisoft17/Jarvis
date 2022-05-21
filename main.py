import json
import os
import webbrowser
import pyaudio
import pygame
from vosk import Model, KaldiRecognizer
import glob

songs = ["/".join(song.split("/")[-2:]) for song in glob.glob("music/myplaylist/*")]

model = Model("vosk-model-small-ru-0.22")
rec = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=4096,
)
stream.start_stream()


class Player:
    def __init__(self) -> None:
        self.player = pygame.mixer
        self.player.init()
    
    def load(self, track: str) -> None:
        self.player.music.load(track)

    def play(self) -> None:
        self.player.music.play()

    def pause(self) -> None:
        self.player.music.pause()

    def unpause(self) -> None:
        self.player.music.unpause()

    def quit(self) -> None:
        self.player.quit()

    def volume_up(self, number: int) -> None:
        volume = self.player.music.get_volume()
        self.player.music.set_volume(volume + number / 100)
    
    def volume_down(self, number: int) -> None:
        volume = self.player.music.get_volume()
        if volume < number / 100:
            self.player.music.set_volume(0.0)
        else:
            self.player.music.set_volume(volume - number / 100)

    def turn_off_sound(self) -> None:
        self.player.music.set_volume(0.0)


class Browser:
    def meme() -> None:
        webbrowser.register(
                name="Chrome",
                klass=None,
                instance=webbrowser.BackgroundBrowser(
                    "C:/Program Files/Google/Chrome/Application/chrome.exe"
                ),
            )
        webbrowser.get(using="chrome").open_new_tab(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
    
    def quit() -> None:
        os.system("taskkill /im chrome.exe /f")

    def search(search: str) -> None:
        webbrowser.register(
                name="Chrome",
                klass=None,
                instance=webbrowser.BackgroundBrowser(
                    "C:/Program Files/Google/Chrome/Application/chrome.exe"
                ),
            )
        webbrowser.get(using="chrome").open_new_tab(
            f"https://www.google.com/search?q={search}"
        )


def listen() -> None:
    player = Player()
    count_songs = -1
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(rec.Result())["text"]
            if answer:
                if answer == "я дома":
                    player.load("music/homespace/ACDC-BackInBlack.wav")
                    player.play()
                if answer == "музыка стоп":
                    player.pause()
                if answer == "продолжи воспроизведение":
                    player.unpause()
                if answer == "выключи звук":
                    player.turn_off_sound()
                if  answer == "сделай тише":
                    player.volume_down(20)
                if answer == "сделай громче":
                    player.volume_up(20)
                if answer == "переключи трек":
                    if count_songs + 1 > len(songs) - 1:
                        count_songs = 0
                    else:
                        count_songs += 1
                    player.load(track=songs[count_songs])
                    player.play()
                if answer == "ты доверяешь мне":
                    Browser().meme()
                if "найди в интернете" in answer:
                    Browser().search(answer[18:])
                if answer == "закрой браузер":
                    Browser.quit()
                if answer == "перезагрузка":
                    os.system("shutdown -r -t 0")
                if answer == "выключи комп":
                    os.system("shutdown -s -t 0")
                if answer == "пора на боковую":
                    quit()
                print(answer)
print(songs)

if __name__ == "__main__":
    listen()

import json
import pyaudio
from browser import Browser
from music_player import Player, get_playlist
from manage_PC import mng_work_space
from vosk import Model, KaldiRecognizer


class Stream:
    def __init__(self) -> None:
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=4096,
        )
    def start_stream(self) -> None:
        self.stream.start_stream()


class Recognize:
    def __init__(self) -> None:
        self.model = Model("vosk-model-small-ru-0.22")
        self.rec = KaldiRecognizer(self.model, 16000)


def listen() -> None:
    player = Player()
    stream = Stream()
    stream.start_stream()
    recognize = Recognize()
    count_songs = -1
    myplaylist = get_playlist("userplaylist")
    mic_is_active = True
    while True:
        if mic_is_active:
            data = stream.stream.read(4000, exception_on_overflow=False)
            if recognize.rec.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(recognize.rec.Result())["text"]
                if answer:
                    if answer == "я дома":
                        player.load("music/homespace/ACDC-BackInBlack.wav")
                        player.play()
                    if answer in ("музыка стоп", "стой", "выключи музыку", "стоп"):
                        player.pause()
                    if answer in ("включи музыку", "музычку", "дай бит"):
                        if count_songs + 1 > len(myplaylist) - 1:
                            count_songs = 0
                        else:
                            count_songs += 1
                        player.load(track=myplaylist[count_songs])
                        player.play()
                    if answer == "продолжи воспроизведение":
                        player.unpause()
                    if answer == "выключи звук":
                        player.turn_off_sound()
                    if  answer in ("сделай тише", "потише"):
                        player.volume_down(20)
                    if answer in ("сделай громче", "громче"):
                        player.volume_up(20)
                    if answer in ("следующий трек", "дальше"):
                        if count_songs + 1 > len(myplaylist) - 1:
                            count_songs = 0
                        else:
                            count_songs += 1
                        player.load(track=myplaylist[count_songs])
                        player.play()
                    if answer in ("переключи обратно", "верни назад", "включи предыдущий трек"):
                        if count_songs - 1 < 0:
                            count_songs = len(myplaylist) - 1
                        else:
                            count_songs -= 1
                        player.load(track=myplaylist[count_songs])
                        player.play()
                    if answer == "выключи микрофон":
                        mic_is_active = False
                    if answer == "ты доверяешь мне":
                        Browser.meme()
                    if "найди в интернете" in answer:
                        Browser.search(answer[18:])
                    if "найди видео" in answer:
                        Browser.search_on_youtube(answer[12:])
                    if answer == "закрой браузер":
                        Browser.quit()
                    if answer == "я ушёл":
                        mng_work_space.block_display()
                    if answer == "перезагрузка":
                        mng_work_space.reboot()
                    if answer == "выключи комп":
                        mng_work_space.shutdown()
                    if answer == "пора на боковую":
                        quit()
                print(answer)
        else:
            while True:
                data = stream.stream.read(4000, exception_on_overflow=False)
                if recognize.rec.AcceptWaveform(data) and len(data) > 0:
                    if json.loads(recognize.rec.Result())["text"] in ("включи микрофон", "джарвис", "проснись"):
                        mic_is_active = True
                        break

if __name__ == "__main__":
    listen()

import json
import pyaudio
from browser import Browser
from music_player import Player, get_playlist
from manage_PC import mng_work_space
from vosk import Model, KaldiRecognizer


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


def listen() -> None:
    player = Player()
    count_songs = -1
    myplaylist = get_playlist("userplaylist")
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(rec.Result())["text"]
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
                if  answer == "сделай тише":
                    player.volume_down(20)
                if answer == "сделай громче":
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

if __name__ == "__main__":
    listen()

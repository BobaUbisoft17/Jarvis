import pyaudio
import wave
import time
import sys
import pygame
import glob


"""class MyStream:
    def __init__(self):
        self.origin = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)
    
    def run(self):
        self.origin.start_stream()

    def pause(self):
        self.origin.stop_stream()
    
    def quit(self):
        self.origin.close()
    
    def listen(self):
        self.pause()
        while True:
            word = input()
            if word == "start":
                self.run()
            elif word == "stop":
                self.pause()
            elif word == "quit":
                self.quit()
                break


wf = wave.open("ACDC-BackInBlack.wav", 'rb')
p = pyaudio.PyAudio()


# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)


stream = MyStream()
stream.listen()
wf.close()"""

class PygamePlayer:
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
        print(volume)
        self.player.music.set_volume(volume + number / 100)
    
    def volume_down(self, number: int) -> None:
        volume = self.player.music.get_volume()
        print(volume)
        self.player.music.set_volume(volume - number / 100)

    def turn_off_sound(self) -> None:
        self.player.music.set_volume(0.0)


stream = PygamePlayer()
stream.load("ACDC-BackInBlack.mp3")
songs = ["/".join(song.split("/")[-2:]) for song in glob.glob("music/myplaylist/*")]
print(songs)
while True:
    word = input()
    if word == "start":
        stream.play()
    elif word == "pause":
        stream.pause()
    elif word == "continue":
        stream.unpause()
    elif word == "volume up":
        stream.volume_up(20)
    elif word == "volume down":
        stream.volume_down(20)
    elif word == "shut up":
        stream.turn_off_sound()
    elif word == "next song":
        stream.load(songs[1])
    elif word == "quit":
        stream.quit()
        break

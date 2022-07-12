from typing import List
import pygame
import glob


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
    

def get_playlist(playlist: str) -> List[str]:
    pathname = ""
    if playlist == "homespace":
        pathname = "music/homespace/*"
    elif playlist == "userplaylist":
        pathname = "music/myplaylist/*"
    return ["/".join(song.split("/")[-2:]) for song in glob.glob(pathname)]
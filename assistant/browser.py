"""Модуль для раюоты с браузером."""

import webbrowser
import os


class Browser:
    """Класс для открытия браузера по запросам."""
    
    def meme() -> None:
        webbrowser.get().open(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
    
    def search(search: str) -> None:
        webbrowser.get().open_new_tab(
            f"https://www.google.com/search?q={search}"
        )
    
    def search_on_youtube(request: str) -> None:
        webbrowser.get().open(f"https://www.youtube.com/results?search_query={request}")

    def quit() -> None:
        os.system("taskkill /im chrome.exe /f")
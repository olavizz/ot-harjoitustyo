from tkinter import Tk, ttk, constants, StringVar
from ui.home_view import HomeView

class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
        self._show_home_view()

    def _show_home_view(self):
        self._current_view = HomeView(
            self._root
        )
        self._current_view.pack()


window = Tk()
window.title("Budget app")

ui = UI(window)
ui.start()

window.mainloop()
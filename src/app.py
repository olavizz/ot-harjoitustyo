from tkinter import Tk, constants
from ui.balance_view import BalanceView
from ui.expenses_view import ExpensesView

class UI:
    def __init__(self, root):
        self._root = root
        self._home_view = BalanceView(self._root)
        self._expenses_view = ExpensesView(self._root)

    def start(self):
        self._home_view._frame.grid(row=0, column=0, sticky=constants.W, padx=10, pady=10)
        self._expenses_view._frame.grid(row=1, column=0, sticky=constants.W, padx=10, pady=10)

window = Tk()
window.title("Budget app")

ui = UI(window)
ui.start()

window.mainloop()

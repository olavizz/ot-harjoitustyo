from tkinter import Tk, constants
from ui.balance_view import BalanceView
from ui.expenses_view import ExpensesView
from ui.login_view import LoginView

class UI:
    def __init__(self, root):
        self._root = root
        self._home_view = BalanceView(self._root)
        self._expenses_view = ExpensesView(self._root)
        self._login_view = LoginView(self._root, self.show_homepage_view)

        self._current_view = None

    def start(self):
        self._change_view(self._login_view)
    
    def _change_view(self, new_view):
        if self._current_view:
            self._current_view.hide()

        self._current_view = new_view
        self._current_view.show()

    def show_homepage_view(self):
        self._current_view.hide()
        self._home_view._frame.grid(row=0, column=0, sticky=constants.W, padx=10, pady=10)
        self._expenses_view._frame.grid(row=1, column=0, sticky=constants.W, padx=10, pady=10)
    
    def show(self):
        self._frame.grid(row=0, column=0, sticky=constants.W)

    def hide(self):
        self._frame.grid_remove()

window = Tk()
window.title("Budget app")

ui = UI(window)
ui.start()

window.mainloop()

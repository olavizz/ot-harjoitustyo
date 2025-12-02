from tkinter import Tk, constants

from ui.balance_view import BalanceView
from ui.expenses_view import ExpensesView
from ui.login_view import LoginView
from ui.register_view import RegisterView


class UI:
    def __init__(self, root):
        self._root = root
        self._register_view = RegisterView(self._root, self.start)
        self._home_view = BalanceView(self._root, self.start)
        self._expenses_view = ExpensesView(self._root)
        self._login_view = LoginView(self._root, self.show_homepage_view, self._show_register_view)
        self._current_view = None
        self._current_view_list = []

    def start(self):
        self._change_view(self._login_view)

    def _change_view(self, new_view):
        if self._current_view_list:
            for i in self._current_view_list:
                i.hide()

        self._current_view_list = [new_view]

        for i in self._current_view_list:
            i.show()

    def show_homepage_view(self):
        for i in self._current_view_list:
            i.hide()
        self._home_view._frame.grid(
            row=0, column=0, sticky=constants.W, padx=10, pady=10
        )
        self._expenses_view._frame.grid(
            row=1, column=0, sticky=constants.W, padx=10, pady=10
        )

        self._current_view_list = [self._home_view, self._expenses_view]
    
    def _show_register_view(self):
        self._change_view(self._register_view)


window = Tk()
window.title("Budget app")

ui = UI(window)
ui.start()

window.mainloop()

from tkinter import Tk, constants

import db_helper
from services.budget_service import budget_service
from ui.balance_view import BalanceView
from ui.expenses_view import ExpensesView
from ui.login_view import LoginView
from ui.register_view import RegisterView


class UI:
    def __init__(self, root):
        self._root = root
        self._logged_in_user_id = None

        self._current_view_list = []
        self._create_views()

    def _create_views(self):
        # luodaan kaikki näkymät *kerran*
        self._register_view = RegisterView(self._root, self.start)

        self._home_view = BalanceView(self._root, budget_service, self.start)

        self._expenses_view = ExpensesView(
            self._root,
            budget_service,
            self._home_view.update_balance,
        )

        self._login_view = None

    def start(self):
        self._logged_in_user_id = None

        self._home_view.set_user_id(None)
        self._expenses_view.set_user_id(None)

        self._login_view = LoginView(
            self._root,
            self.show_homepage_view,
            self._show_register_view,
            self._home_view.init_user,
        )

        self._change_view(self._login_view)

    def _change_view(self, new_view):
        if self._current_view_list:
            for v in self._current_view_list:
                v.hide()

        self._current_view_list = [new_view]
        new_view.show()

    def show_homepage_view(self, user_id):
        self._logged_in_user_id = user_id
        self._home_view.set_user_id(user_id)
        self._expenses_view.set_user_id(user_id)
        self._home_view.init_user(user_id)
        self._expenses_view._show_expenses()

        for v in self._current_view_list:
            v.hide()

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

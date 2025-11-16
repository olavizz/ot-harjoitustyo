from tkinter import Tk, ttk, constants, StringVar

class UI:
    def __init__(self, root):
        self._root = root
        self._balance_var = None
        self._expenses_var = None

    def start(self):
        self._balance_var = StringVar()
        self._balance_var.set("0")
        self._expenses_var = StringVar()
        self._expenses_var.set("0")

        balance = ttk.Label(master=self._root, text="balance", font=(20))
        expenses = ttk.Label(master=self._root, text="expenses", font=(20))

        balance_amount = ttk.Label(master=self._root, textvariable=self._balance_var)
        expenses_amount = ttk.Label(master=self._root, textvariable=self._expenses_var)

        balance.grid(row=0, column=0, columnspan=1, sticky=constants.W, padx=5)
        balance_amount.grid(row=0, column=3, columnspan=3, sticky=constants.W)
        expenses.grid(row=1, column=0, columnspan=1, sticky=constants.W, padx=5)
        expenses_amount.grid(row=1, column=3, columnspan=3, sticky=constants.W)

window = Tk()
window.title("Budget app")
window.geometry("300x300")

ui = UI(window)
ui.start()

window.mainloop()
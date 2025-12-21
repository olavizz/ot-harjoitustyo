from repositories.budget_repository import budget_repository as repo


class BudgetService:
    def __init__(self):
        self._cached_balance = {}
        self._cached_earnings = {}

    def increase_balance(self, amount, user_id):
        """Increase user's balance and total_earnings by amount."""
        try:
            add_val = float(amount)
        except Exception:
            add_val = 0.0

        current = repo.get_balance(user_id)
        new_balance = current + add_val
        total_earnings = repo.get_total_earnings(user_id) + add_val

        ok = repo.set_balance_and_earnings(user_id, new_balance, total_earnings)
        if ok:
            self._cached_balance[user_id] = new_balance
            self._cached_earnings[user_id] = total_earnings
        return new_balance, total_earnings

    def decrease_balance(self, amount, user_id):
        """Decrease user's balance by amount."""
        try:
            sub_val = float(amount)
        except Exception:
            sub_val = 0.0

        current = repo.get_balance(user_id)
        new_balance = current - sub_val

        ok = repo.update_balance(user_id, new_balance)
        if ok:
            self._cached_balance[user_id] = new_balance
        return new_balance

    def _get_balance(self, user_id):
        """Return cached balance if present, otherwise read from repository."""
        if user_id in self._cached_balance:
            return self._cached_balance[user_id]
        balance = repo.get_balance(user_id)
        self._cached_balance[user_id] = float(balance)
        return float(balance)

    def get_balance(self, user_id):
        return self._get_balance(user_id)

    def _get_total_earnings(self, user_id):
        earnings = repo.get_total_earnings(user_id)
        self._cached_earnings[user_id] = float(earnings)
        return float(earnings)

    def add_expense(self, description, amount, user_id):
        """Add an expense row and decrease the balance."""
        try:
            exp_id = repo.add_expense(user_id, description, float(amount))
        except Exception:
            exp_id = repo.add_expense(user_id, description, amount)

        self.decrease_balance(amount, user_id)
        return exp_id

    def get_expenses_amount(self, user_id):
        return repo.get_total_expenses_amount(user_id)

    def get_expenses(self, user_id):
        return repo.get_expenses_by_user(user_id)

    def delete_expense(self, expense_id, user_id):
        """Delete an expense and refund the amount to the user's balance."""
        expense = repo.get_expense_by_id(expense_id)
        if not expense:
            return False
        _, owner_id, _, amount = expense
        if owner_id != user_id:
            return False

        deleted = repo.delete_expense(expense_id)
        if not deleted:
            return False

        try:
            amt = float(amount)
        except Exception:
            try:
                amt = int(amount)
            except Exception:
                amt = 0.0

        current = repo.get_balance(user_id)
        new_balance = current + amt
        repo.update_balance(user_id, new_balance)

        self._cached_balance[user_id] = new_balance
        return True

    def edit_expense(self, expense_id, user_id, new_description, new_amount):
        """Update an expense and adjust the user's balance accordingly."""
        expense = repo.get_expense_by_id(expense_id)
        if not expense:
            return False
        eid, owner_id, old_description, old_amount = expense
        if owner_id != user_id:
            return False

        try:
            old_val = float(old_amount)
        except Exception:
            try:
                old_val = int(old_amount)
                old_val = float(old_val)
            except Exception:
                old_val = 0.0

        parsed_new = None
        try:
            parsed_new = float(new_amount)
        except Exception:
            try:
                parsed_new = int(new_amount)
                parsed_new = float(parsed_new)
            except Exception:
                parsed_new = None

        if parsed_new is None:
            # only update description
            updated = repo.update_expense(expense_id, new_description, old_val)
            return updated

        updated = repo.update_expense(expense_id, new_description, parsed_new)
        if not updated:
            return False

        delta = parsed_new - old_val

        current = repo.get_balance(user_id)
        new_balance = current - delta

        repo.update_balance(user_id, new_balance)
        self._cached_balance[user_id] = new_balance
        return True


budget_service = BudgetService()

```mermaid
 classDiagram
  UI -- loginView
  UI -- balanceView
  UI -- expensesView

  loginView -- loginService
  balanceView -- balanceService
  expensesView -- expensesService
  expensesService -- balanceService
```

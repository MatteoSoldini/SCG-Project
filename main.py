import pandas as pd

sales = pd.read_excel("files/Vendite.xlsx", decimal=',')
customers = pd.read_excel("files/Clienti.xlsx", decimal=',')
exchange_rates = pd.read_excel("files/Tassi di cambio.xlsx", decimal=',')

budget_exchange_rates = exchange_rates.loc[exchange_rates['Anno'] == "BUDGET"]
budget_sales = sales.loc[(sales['budget/cons'] == "BUDGET")]

budget_sales_with_exchange_rates = pd.merge(
    budget_sales, customers, how="left", left_on='Nr. origine', right_on='Nr.').merge(
    budget_exchange_rates, how="left", left_on='Valuta', right_on='Codice valuta')

euro_budget_sales = budget_sales_with_exchange_rates['Importo vendita in valuta locale (TOTALE VENDITA)'] / \
    budget_sales_with_exchange_rates['Tasso di cambio medio']

print(euro_budget_sales.sum())

final_exchange_rates = exchange_rates.loc[exchange_rates['Anno']
                                          == "CONSUNTIVO"]
final_sales = sales.loc[(sales['budget/cons'] == "Consuntivo")]

final_sales_with_exchange_rates = pd.merge(
    final_sales, customers, how="left", left_on='Nr. origine', right_on='Nr.').merge(
    final_exchange_rates, how="left", left_on='Valuta', right_on='Codice valuta')

euro_final_sales = final_sales_with_exchange_rates['Importo vendita in valuta locale (TOTALE VENDITA)'] / \
    final_sales_with_exchange_rates['Tasso di cambio medio']

print(euro_final_sales.sum())

# 'Importo vendita in valuta locale (TOTALE VENDITA)'].sum()

# print(budget_sales)

"""
df = pd.merge(sales, customers, how="left",
              left_on='Nr. origine', right_on='Nr.').head()

print(df)
"""

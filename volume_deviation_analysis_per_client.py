import pandas as pd

sales = pd.read_excel("files/Vendite.xlsx", decimal=',')
exchange_rates = pd.read_excel("files/Tassi di cambio.xlsx", decimal=',')
customers = pd.read_excel("files/Clienti.xlsx", decimal=',')

# Budget
budget_exchange_rates = exchange_rates.loc[exchange_rates['Anno'].str.lower(
) == "budget"]
budget_sales = sales.loc[(sales['budget/cons'].str.lower() == "budget")]

budget_sales_with_exchange_rates = pd.merge(
    budget_sales, customers, how="left", left_on='Nr. origine', right_on='Nr.').merge(
    budget_exchange_rates, how="left", left_on='Valuta', right_on='Codice valuta')

budget_sales_with_exchange_rates['Prezzo (€)'] = budget_sales_with_exchange_rates[
    'Importo vendita in valuta locale (TOTALE VENDITA)'] / budget_sales_with_exchange_rates['Tasso di cambio medio']

euro_budget_sales_groupped_by_client = budget_sales_with_exchange_rates[
    ['Nr. origine',
     'Quantità',
     'Prezzo (€)',
     ]].groupby(
    by=["Nr. origine"], as_index=False).sum(
        numeric_only=True).rename(
            columns={
                'Quantità': 'Quantità budget',
                'Prezzo (€)': 'Prezzo budget (€)',
            })

# Final
final_exchange_rates = exchange_rates.loc[exchange_rates['Anno'].str.lower(
) == "consuntivo"]
final_sales = sales.loc[(sales['budget/cons'].str.lower() == "consuntivo")]

final_sales_with_exchange_rates = pd.merge(
    final_sales, customers, how="left", left_on='Nr. origine', right_on='Nr.').merge(
    final_exchange_rates, how="left", left_on='Valuta', right_on='Codice valuta')

final_sales_with_exchange_rates['Prezzo (€)'] = final_sales_with_exchange_rates[
    'Importo vendita in valuta locale (TOTALE VENDITA)'] / final_sales_with_exchange_rates['Tasso di cambio medio']

euro_final_sales_groupped_by_client = final_sales_with_exchange_rates[
    ['Nr. origine',
     'Quantità',
     'Prezzo (€)']
].groupby(by=["Nr. origine"]).sum(numeric_only=True).rename(columns={
    'Quantità': 'Quantità consuntivo',
    'Prezzo (€)': 'Prezzo consuntivo (€)',
})

print(euro_budget_sales_groupped_by_client.merge(
    euro_final_sales_groupped_by_client,
    how="outer",
    on=['Nr. origine']
).to_excel('volume_deviation_analysis_per_client.xlsx'))

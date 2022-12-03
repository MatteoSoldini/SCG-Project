import pandas as pd
from IPython.display import display


sales = pd.read_excel("files/Vendite.xlsx", decimal=',')
customers = pd.read_excel("files/Clienti.xlsx", decimal=',')
exchange_rates = pd.read_excel("files/Tassi di cambio.xlsx", decimal=',')

# Budget sales
budget_exchange_rates = exchange_rates.loc[exchange_rates['Anno'] == "BUDGET"]
budget_sales = sales.loc[(sales['budget/cons'] == "BUDGET")]

budget_sales_with_exchange_rates = pd.merge(
    budget_sales, customers, how="left", left_on='Nr. origine', right_on='Nr.').merge(
    budget_exchange_rates, how="left", left_on='Valuta', right_on='Codice valuta')

euro_budget_sales = budget_sales_with_exchange_rates['Importo vendita in valuta locale (TOTALE VENDITA)'] / \
    budget_sales_with_exchange_rates['Tasso di cambio medio']

# Final sales
final_exchange_rates = exchange_rates.loc[exchange_rates['Anno']
                                          == "CONSUNTIVO"]
final_sales = sales.loc[(sales['budget/cons'] == "Consuntivo")]

final_sales_with_exchange_rates = pd.merge(
    final_sales, customers, how="left", left_on='Nr. origine', right_on='Nr.').merge(
    final_exchange_rates, how="left", left_on='Valuta', right_on='Codice valuta')

euro_final_sales = final_sales_with_exchange_rates['Importo vendita in valuta locale (TOTALE VENDITA)'] / \
    final_sales_with_exchange_rates['Tasso di cambio medio']

# Budget resource
# Production volume
resource_usage = pd.read_excel(
    "files/Impiego orario risorse.xlsx", decimal=',')

budget_resource_usage = resource_usage.loc[resource_usage['budget/consuntivo'] == 'BUDGET']
budget_production_volume = budget_resource_usage['Quantità di output'].sum()

# Total cost
budget_resources_cost = pd.read_excel(
    "files/Costo orario risorse - budget.xlsx", decimal=',')

budget_resource_usage_with_cost = budget_resource_usage.merge(budget_resources_cost, how="left", left_on=[
                                                              'Risorsa', 'Nr. Area di produzione'], right_on=['Risorsa', 'Area di produzione'])

budget_resource_usage_with_cost['Costo (€)'] = budget_resource_usage_with_cost['Tempo risorsa'] * \
    budget_resource_usage_with_cost['Costo orario (€/h)']

resource_cost_per_item = budget_resource_usage_with_cost.groupby(
    by=["nr articolo"]).sum()

print(resource_cost_per_item)

# Final resource
final_resource_usage = resource_usage.loc[resource_usage['budget/consuntivo'] == 'CONSUNTIVO']
final_production_volume = final_resource_usage['Quantità di output'].sum()

# creating a DataFrame
dict = {'Context': ['Budget', 'Final'],
        'Sales': [euro_budget_sales.sum(), euro_final_sales.sum()],
        'Production Volume': [budget_production_volume, final_production_volume]}
df = pd.DataFrame(dict)

# displaying the DataFrame
display(df)

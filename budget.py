import pandas as pd
from IPython.display import display


def BudgetItem() -> pd.DataFrame:
    sales = pd.read_excel("files/Vendite.xlsx", decimal=',')
    customers = pd.read_excel("files/Clienti.xlsx", decimal=',')
    exchange_rates = pd.read_excel("files/Tassi di cambio.xlsx", decimal=',')
    resource_usage = pd.read_excel(
        "files/Impiego orario risorse.xlsx", decimal=',')
    budget_resources_cost = pd.read_excel(
        "files/Costo orario risorse - budget.xlsx", decimal=',')
    raw_materials_usage = pd.read_excel("files/Consumi.xlsx", decimal=',')

    # Sales
    budget_exchange_rates = exchange_rates.loc[exchange_rates['Anno'] == "BUDGET"]
    budget_sales = sales.loc[(sales['budget/cons'] == "BUDGET")]

    budget_sales_with_exchange_rates = pd.merge(
        budget_sales, customers, how="left", left_on='Nr. origine', right_on='Nr.').merge(
        budget_exchange_rates, how="left", left_on='Valuta', right_on='Codice valuta')

    budget_sales_with_exchange_rates['Prezzo (€)'] = budget_sales_with_exchange_rates[
        'Importo vendita in valuta locale (TOTALE VENDITA)'] / budget_sales_with_exchange_rates['Tasso di cambio medio']

    budget_sales_groupped_by_item = budget_sales_with_exchange_rates.groupby(by=[
        "Nr articolo"], as_index=False).sum(numeric_only=True)

    budget_sales_groupped_by_item['Prezzo unitario (€/u)'] = budget_sales_groupped_by_item['Prezzo (€)'] / \
        budget_sales_groupped_by_item['Quantità']

    budget_sales_groupped_by_item['Mix (%)'] = budget_sales_groupped_by_item['Quantità'] / \
        budget_sales_groupped_by_item['Quantità'].sum(numeric_only=True)

    # print(budget_sales_groupped_by_item)

    # Costs

    # Resources cost
    budget_resource_usage = resource_usage.loc[resource_usage['budget/consuntivo'] == 'BUDGET']
    budget_production_volume = budget_resource_usage['Quantità di output'].sum(
    )

    budget_resource_usage_with_cost = budget_resource_usage.merge(budget_resources_cost, how="left", left_on=[
        'Risorsa', 'Nr. Area di produzione'], right_on=['Risorsa', 'Area di produzione'])
    budget_resource_usage_with_cost['Costo risorse (€)'] = budget_resource_usage_with_cost['Tempo risorsa'] * \
        budget_resource_usage_with_cost['Costo orario (€/h)']

    budget_resource_cost_per_item = budget_resource_usage_with_cost.groupby(
        by=["nr articolo"]).sum(numeric_only=True)

    # print(budget_resource_cost_per_item)

    # Raw materials cost
    budget_raw_materials_usage = raw_materials_usage.loc[(
        raw_materials_usage['Budget/cons'] == "BUDGET")]

    budget_raw_materials_cost = budget_raw_materials_usage.groupby(
        by=["Nr articolo"], as_index=False).sum(numeric_only=True).rename(columns={"Importo costo (TOTALE)": "Costo MP (€)"})[['Nr articolo', 'Costo MP (€)']]

    budget_item_cost = budget_resource_cost_per_item.merge(
        budget_raw_materials_cost, how="left", left_on=['nr articolo'], right_on=['Nr articolo'])

    budget_item_cost['Costo totale (€)'] = budget_item_cost['Costo MP (€)'] + \
        budget_item_cost['Costo risorse (€)']

    budget_item_cost = budget_item_cost.merge(budget_sales_groupped_by_item[[
        'Nr articolo', 'Quantità']], how="left", on=['Nr articolo'])

    budget_item_cost['Costo unitario (€/u)'] = budget_item_cost['Costo totale (€)'] / \
        budget_item_cost['Quantità']

    # All together
    budget_item = budget_sales_groupped_by_item.merge(
        budget_item_cost[['Nr articolo', 'Costo unitario (€/u)']], how="left", on=['Nr articolo'])

    return budget_item[['Nr articolo', 'Quantità',
                        'Prezzo unitario (€/u)', 'Costo unitario (€/u)', 'Mix (%)']]

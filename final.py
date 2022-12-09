import pandas as pd
from IPython.display import display


def FinalItem() -> pd.DataFrame:
    sales = pd.read_excel("files/Vendite.xlsx", decimal=',')
    customers = pd.read_excel("files/Clienti.xlsx", decimal=',')
    exchange_rates = pd.read_excel("files/Tassi di cambio.xlsx", decimal=',')
    resource_usage = pd.read_excel(
        "files/Impiego orario risorse.xlsx", decimal=',')
    final_resources_cost = pd.read_excel(
        "files/Costo orario risorse - consuntivo.xlsx", decimal=',')
    raw_materials_usage = pd.read_excel("files/Consumi.xlsx", decimal=',')

    # Sales
    final_exchange_rates = exchange_rates.loc[exchange_rates['Anno']
                                              == "CONSUNTIVO"]
    final_sales = sales.loc[(sales['budget/cons'] == "Consuntivo")]

    final_sales_with_exchange_rates = pd.merge(
        final_sales, customers, how="left", left_on='Nr. origine', right_on='Nr.').merge(
        final_exchange_rates, how="left", left_on='Valuta', right_on='Codice valuta')

    final_sales_with_exchange_rates['Prezzo (€)'] = final_sales_with_exchange_rates[
        'Importo vendita in valuta locale (TOTALE VENDITA)'] / final_sales_with_exchange_rates['Tasso di cambio medio']

    final_item_sales = final_sales_with_exchange_rates.groupby(by=[
        "Nr articolo"], as_index=False).sum(numeric_only=True)

    final_item_sales['Prezzo unitario (€/u)'] = final_item_sales['Prezzo (€)'] / \
        final_item_sales['Quantità']

    final_item_sales['Mix (%)'] = final_item_sales['Quantità'] / \
        final_item_sales['Quantità'].sum(numeric_only=True)

    # print(budget_sales_groupped_by_item)

    # Costs

    # Resources cost
    final_resource_usage = resource_usage.loc[resource_usage['budget/consuntivo'] == 'CONSUNTIVO']
    final_production_volume = final_resource_usage['Quantità di output'].sum(
        numeric_only=True)

    final_resource_usage_with_cost = final_resource_usage.merge(final_resources_cost, how="left", left_on=[
        'Risorsa', 'Nr. Area di produzione'], right_on=['Risorsa', 'Area di produzione'])
    final_resource_usage_with_cost['Costo risorse (€)'] = final_resource_usage_with_cost['Tempo risorsa'] * \
        final_resource_usage_with_cost['Costo orario (€/h)']

    final_resource_cost_per_item = final_resource_usage_with_cost.groupby(by=[
        "nr articolo"]).sum(numeric_only=True)

    # print(budget_resource_cost_per_item)

    # Raw materials cost
    final_raw_materials_usage = raw_materials_usage.loc[(
        raw_materials_usage['Budget/cons'] == "CONSUNTIVO")]

    final_raw_materials_cost = final_raw_materials_usage.groupby(
        by=["Nr articolo"], as_index=False).sum(numeric_only=True).rename(columns={"Importo costo (TOTALE)": "Costo MP (€)"})[['Nr articolo', 'Costo MP (€)']]

    final_item_cost = final_resource_cost_per_item.merge(
        final_raw_materials_cost, how="left", left_on=['nr articolo'], right_on=['Nr articolo'])

    final_item_cost['Costo totale (€)'] = final_item_cost['Costo MP (€)'] + \
        final_item_cost['Costo risorse (€)']

    final_item_cost = final_item_cost.merge(final_item_sales[[
        'Nr articolo', 'Quantità']], how="left", on=['Nr articolo'])

    final_item_cost['Costo unitario (€/u)'] = final_item_cost['Costo totale (€)'] / \
        final_item_cost['Quantità']

    final_item_cost.to_excel('export.xlsx')

    # All together
    final_item = final_item_sales.merge(
        final_item_cost[['Nr articolo', 'Costo unitario (€/u)']], how="left", on=['Nr articolo'])

    return final_item[['Nr articolo', 'Quantità',
                       'Prezzo unitario (€/u)', 'Costo unitario (€/u)', 'Mix (%)']]

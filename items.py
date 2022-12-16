import pandas as pd


def getItem(final: bool) -> pd.DataFrame:
    filter = 'consuntivo' if final else 'budget'

    sales = pd.read_excel("files/Vendite.xlsx", decimal=',')
    customers = pd.read_excel("files/Clienti.xlsx", decimal=',')
    exchange_rates = pd.read_excel("files/Tassi di cambio.xlsx", decimal=',')
    resource_usage = pd.read_excel(
        "files/Impiego orario risorse.xlsx", decimal=',')
    resources_cost = pd.read_excel(
        "files/Costo orario risorse - " + filter + ".xlsx", decimal=',')
    raw_materials_usage = pd.read_excel("files/Consumi.xlsx", decimal=',')

    # Sales
    exchange_rates = exchange_rates.loc[exchange_rates['Anno'].str.lower(
    ) == filter]
    sales = sales.loc[(sales['budget/cons'].str.lower() == filter)]

    sales_with_exchange_rates = pd.merge(
        sales, customers, how="left", left_on='Nr. origine', right_on='Nr.').merge(
        exchange_rates, how="left", left_on='Valuta', right_on='Codice valuta')

    sales_with_exchange_rates['Prezzo (€)'] = sales_with_exchange_rates[
        'Importo vendita in valuta locale (TOTALE VENDITA)'] / sales_with_exchange_rates['Tasso di cambio medio']

    sales_groupped_by_item = sales_with_exchange_rates.groupby(by=[
        "Nr articolo"], as_index=False).sum(numeric_only=True)

    sales_groupped_by_item['Prezzo unitario (€/u)'] = sales_groupped_by_item['Prezzo (€)'] / \
        sales_groupped_by_item['Quantità']

    sales_groupped_by_item['Mix (%)'] = sales_groupped_by_item['Quantità'] / \
        sales_groupped_by_item['Quantità'].sum(numeric_only=True)

    # Costs

    # Resources cost
    resource_usage = resource_usage.loc[resource_usage['budget/consuntivo'].str.lower(
    ) == filter]
    production_volume = resource_usage['Quantità di output'].sum(
    )

    resource_usage_with_cost = resource_usage.merge(resources_cost, how="left", left_on=[
        'Risorsa', 'Nr. Area di produzione'], right_on=['Risorsa', 'Area di produzione'])
    resource_usage_with_cost['Costo risorse (€)'] = resource_usage_with_cost['Tempo risorsa'] * \
        resource_usage_with_cost['Costo orario (€/h)']

    resource_cost_per_item = resource_usage_with_cost.groupby(
        by=["nr articolo"]).sum(numeric_only=True)

    # print(resource_cost_per_item)

    # Raw materials cost
    raw_materials_usage = raw_materials_usage.loc[(
        raw_materials_usage['Budget/cons'].str.lower() == filter)]

    raw_materials_cost = raw_materials_usage.groupby(
        by=["Nr articolo"], as_index=False).sum(numeric_only=True).rename(columns={"Importo costo (TOTALE)": "Costo MP (€)"})[['Nr articolo', 'Costo MP (€)']]

    item_cost = resource_cost_per_item.merge(
        raw_materials_cost, how="left", left_on=['nr articolo'], right_on=['Nr articolo'])

    item_cost['Costo totale (€)'] = item_cost['Costo MP (€)'] + \
        item_cost['Costo risorse (€)']

    item_cost = item_cost.merge(sales_groupped_by_item[[
        'Nr articolo', 'Quantità']], how="left", on=['Nr articolo'])

    item_cost['Costo unitario (€/u)'] = item_cost['Costo totale (€)'] / \
        item_cost['Quantità']
    item_cost['Costo unitario MP (€/u)'] = item_cost['Costo MP (€)'] / \
        item_cost['Quantità']
    item_cost['Costo unitario risorse (€/u)'] = item_cost['Costo risorse (€)'] / \
        item_cost['Quantità']

    # All together
    item = sales_groupped_by_item.merge(
        item_cost[['Nr articolo', 'Costo unitario (€/u)', 'Costo unitario MP (€/u)', 'Costo unitario risorse (€/u)']], how="left", on=['Nr articolo'])

    return item[['Nr articolo', 'Quantità',
                 'Prezzo unitario (€/u)', 'Costo unitario (€/u)', 'Costo unitario MP (€/u)', 'Costo unitario risorse (€/u)', 'Mix (%)']]

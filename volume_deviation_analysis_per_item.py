import pandas as pd
from items import getItem

budget_items = getItem(False)[
    ['Nr articolo',
     'Quantità',
     'Mix (%)',
     'Prezzo unitario (€/u)',
     'Costo unitario MP (€/u)',
     'Costo unitario risorse (€/u)']
].rename(columns={'Quantità': 'Quantità budget', 'Mix (%)': 'Mix budget (%)'})
final_items = getItem(True)[
    ['Nr articolo',
     'Quantità',
     'Mix (%)',
     'Prezzo unitario (€/u)',
     'Costo unitario MP (€/u)',
     'Costo unitario risorse (€/u)']
].rename(columns={'Quantità': 'Quantità consuntivo', 'Mix (%)': 'Mix consuntivo (%)'})

budget_items['Prezzo totale budget (€)'] = budget_items['Prezzo unitario (€/u)'] * \
    budget_items['Quantità budget']
budget_items['Costo totale MP budget (€)'] = budget_items['Costo unitario MP (€/u)'] * \
    budget_items['Quantità budget']
budget_items['Costo totale risorse budget (€)'] = budget_items['Costo unitario risorse (€/u)'] * \
    budget_items['Quantità budget']

final_items['Prezzo totale consuntivo (€)'] = final_items['Prezzo unitario (€/u)'] * \
    final_items['Quantità consuntivo']
final_items['Costo totale MP consuntivo (€)'] = final_items['Costo unitario MP (€/u)'] * \
    final_items['Quantità consuntivo']
final_items['Costo totale risorse consuntivo (€)'] = final_items['Costo unitario risorse (€/u)'] * \
    final_items['Quantità consuntivo']

print((budget_items[
    ['Nr articolo',
     'Quantità budget',
     'Mix budget (%)',
     'Prezzo totale budget (€)',
     'Costo totale MP budget (€)',
     'Costo totale risorse budget (€)']
].merge(final_items[
    ['Nr articolo',
     'Quantità consuntivo',
     'Mix consuntivo (%)',
     'Prezzo totale consuntivo (€)',
     'Costo totale MP consuntivo (€)',
     'Costo totale risorse consuntivo (€)']
], how="outer", on=['Nr articolo']).sort_values(
    by=['Quantità consuntivo'], ascending=False)))  # .to_excel('volume_deviation_analysis_per_item.xlsx'))

from budget import BudgetItem
from final import FinalItem
import pandas as pd

budget_items = BudgetItem()
final_items = FinalItem()

budget_price = 0
budget_cost = 0
for index, row in budget_items.iterrows():
    budget_price = row['Prezzo unitario (€/u)'] * \
        row['Quantità'] * row['Mix (%)']
    budget_cost = row['Costo unitario (€/u)'] * \
        row['Quantità'] * row['Mix (%)']

standard_mix_items = budget_items[['Nr articolo', 'Prezzo unitario (€/u)', 'Costo unitario (€/u)', 'Mix (%)']].merge(
    final_items[['Nr articolo', 'Quantità']], how="left", on=['Nr articolo'])
standard_mix_price = 0
standard_mix_cost = 0
for index, row in standard_mix_items.iterrows():
    standard_mix_price = row['Prezzo unitario (€/u)'] * \
        row['Quantità'] * row['Mix (%)']
    standard_mix_cost = row['Costo unitario (€/u)'] * \
        row['Quantità'] * row['Mix (%)']

actual_mix_items = budget_items[['Nr articolo', 'Prezzo unitario (€/u)', 'Costo unitario (€/u)']].merge(
    final_items[['Nr articolo', 'Quantità', 'Mix (%)']], how="left", on=['Nr articolo'])
actual_mix_price = 0
actual_mix_cost = 0
for index, row in actual_mix_items.iterrows():
    actual_mix_price = row['Prezzo unitario (€/u)'] * \
        row['Quantità'] * row['Mix (%)']
    actual_mix_cost = row['Costo unitario (€/u)'] * \
        row['Quantità'] * row['Mix (%)']

final_price = 0
final_cost = 0
for index, row in final_items.iterrows():
    final_price = row['Prezzo unitario (€/u)'] * \
        row['Quantità'] * row['Mix (%)']
    final_cost = row['Costo unitario (€/u)'] * \
        row['Quantità'] * row['Mix (%)']

print(pd.DataFrame({
    'Budget': [budget_price, budget_cost, budget_price - budget_cost],
    'Mix standard': [standard_mix_price, standard_mix_cost, standard_mix_price - standard_mix_cost],
    'Mix effettivo': [actual_mix_price, actual_mix_cost, actual_mix_price - actual_mix_cost],
    'Consuntivo': [final_price, final_cost, final_price - final_cost],
}, index=['Prezzi', 'Costi', 'MON']))

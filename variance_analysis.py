from budget import BudgetItem
from final import FinalItem
import pandas as pd

budget_items = BudgetItem()
final_items = FinalItem()

budget_volume = int(budget_items[['Quantità']].sum())
final_volume = int(final_items[['Quantità']].sum())

# Budget
budget_items['Prezzo totale (€)'] = budget_items['Prezzo unitario (€/u)'] * \
    budget_items['Quantità']
budget_items['Costo totale (€)'] = budget_items['Costo unitario (€/u)'] * \
    budget_items['Quantità']

budget_price = budget_items['Prezzo totale (€)'].sum()
budget_cost = budget_items['Costo totale (€)'].sum()

# Standard Mix
standard_mix_items = budget_items[['Nr articolo', 'Prezzo unitario (€/u)', 'Costo unitario (€/u)', 'Mix (%)']].merge(
    final_items[['Nr articolo', 'Quantità']], how="left", on=['Nr articolo'])

standard_mix_items['Prezzo totale (€)'] = standard_mix_items['Prezzo unitario (€/u)'] * \
    standard_mix_items['Mix (%)'] * final_volume
standard_mix_items['Costo totale (€)'] = standard_mix_items['Costo unitario (€/u)'] * \
    standard_mix_items['Mix (%)'] * final_volume

standard_mix_price = standard_mix_items['Prezzo totale (€)'].sum()
standard_mix_cost = standard_mix_items['Costo totale (€)'].sum()

# Actual Mix
actual_mix_items = budget_items[['Nr articolo', 'Prezzo unitario (€/u)', 'Costo unitario (€/u)']].merge(
    final_items[['Nr articolo', 'Quantità', 'Mix (%)']], how="left", on=['Nr articolo'])

actual_mix_items['Prezzo totale (€)'] = actual_mix_items['Prezzo unitario (€/u)'] * \
    actual_mix_items['Quantità']

actual_mix_items['Costo totale (€)'] = actual_mix_items['Costo unitario (€/u)'] * \
    actual_mix_items['Quantità']

actual_mix_price = actual_mix_items['Prezzo totale (€)'].sum()
actual_mix_cost = actual_mix_items['Costo totale (€)'].sum()

# Final
final_items['Prezzo totale (€)'] = final_items['Prezzo unitario (€/u)'] * \
    final_items['Quantità']
final_items['Costo totale (€)'] = final_items['Costo unitario (€/u)'] * \
    final_items['Quantità']

final_price = final_items['Prezzo totale (€)'].sum()
final_cost = final_items['Costo totale (€)'].sum()

print(pd.DataFrame({
    'Budget': [
        budget_price,
        budget_cost,
        budget_price - budget_cost
    ],
    'Δ B-MS': [
        standard_mix_price - budget_price,
        standard_mix_cost - budget_cost,
        (standard_mix_price - standard_mix_cost) - (budget_price - budget_cost)
    ],
    'Mix standard': [
        standard_mix_price,
        standard_mix_cost,
        standard_mix_price - standard_mix_cost
    ],
    'Δ MS-ME': [
        actual_mix_price - standard_mix_price,
        actual_mix_cost - standard_mix_cost,
        (actual_mix_price - actual_mix_cost) -
        (standard_mix_price - standard_mix_cost)
    ],
    'Mix effettivo': [
        actual_mix_price,
        actual_mix_cost,
        actual_mix_price - actual_mix_cost
    ],
    'Δ ME-C': [
        final_price - actual_mix_price,
        final_cost - actual_mix_cost,
        (final_price - final_cost) - (actual_mix_price - actual_mix_cost)
    ],
    'Consuntivo': [
        final_price,
        final_cost,
        final_price - final_cost
    ],
}, index=['Prezzi', 'Costi', 'MOL']).to_excel('export.xlsx'))

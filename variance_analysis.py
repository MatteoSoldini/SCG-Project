from items import getItem
import pandas as pd

budget_items = getItem(False)
final_items = getItem(True)

budget_volume = int(budget_items[['Quantità']].sum())
final_volume = int(final_items[['Quantità']].sum())

# Budget
budget_price = (budget_items['Prezzo unitario (€/u)']
                * budget_items['Quantità']).sum()
budget_cost = (budget_items['Costo unitario (€/u)']
               * budget_items['Quantità']).sum()
budget_raw_materials_cost = (
    budget_items['Costo unitario MP (€/u)'] * budget_items['Quantità']).sum()
budget_resources_cost = (budget_items['Costo unitario risorse (€/u)'] *
                         budget_items['Quantità']).sum()

# Standard Mix
standard_mix_items = budget_items[
    ['Nr articolo',
     'Prezzo unitario (€/u)',
     'Costo unitario (€/u)',
     'Costo unitario MP (€/u)',
     'Costo unitario risorse (€/u)',
     'Mix (%)']
].merge(final_items[
    ['Nr articolo',
     'Quantità']
], how="left", on=['Nr articolo'])


standard_mix_price = (standard_mix_items['Prezzo unitario (€/u)'] *
                      standard_mix_items['Mix (%)'] * final_volume).sum()
standard_mix_cost = (standard_mix_items['Costo unitario (€/u)']
                     * standard_mix_items['Mix (%)'] * final_volume).sum()
standard_raw_materials_cost = (
    standard_mix_items['Costo unitario MP (€/u)'] * standard_mix_items['Mix (%)'] * final_volume).sum()
standard_resources_cost = (
    standard_mix_items['Costo unitario risorse (€/u)'] * standard_mix_items['Mix (%)'] * final_volume).sum()

# Actual Mix

actual_mix_items = budget_items[
    ['Nr articolo',
     'Prezzo unitario (€/u)',
     'Costo unitario (€/u)',
     'Costo unitario MP (€/u)',
     'Costo unitario risorse (€/u)']
].merge(final_items[
    ['Nr articolo',
     'Quantità',
     'Mix (%)']
], how="left", on=['Nr articolo'])

actual_mix_price = (
    actual_mix_items['Prezzo unitario (€/u)'] * actual_mix_items['Quantità']).sum()
actual_mix_cost = (
    actual_mix_items['Costo unitario (€/u)'] * actual_mix_items['Quantità']).sum()
actual_raw_materials_cost = (
    actual_mix_items['Costo unitario MP (€/u)'] * actual_mix_items['Mix (%)'] * final_volume).sum()
actual_resources_cost = (
    actual_mix_items['Costo unitario risorse (€/u)'] * actual_mix_items['Mix (%)'] * final_volume).sum()

# Final
final_price = (final_items['Prezzo unitario (€/u)']
               * final_items['Quantità']).sum()
final_cost = (final_items['Costo unitario (€/u)']
              * final_items['Quantità']).sum()
final_raw_materials_cost = (
    final_items['Costo unitario MP (€/u)'] * final_items['Quantità']).sum()
final_resources_cost = (final_items['Costo unitario risorse (€/u)'] *
                        final_items['Quantità']).sum()

print(pd.DataFrame({
    'Budget': [
        budget_price,
        budget_cost,
        budget_raw_materials_cost,
        budget_resources_cost,
        budget_price - budget_cost
    ],
    'Δ B-MS': [
        standard_mix_price - budget_price,
        standard_mix_cost - budget_cost,
        standard_raw_materials_cost - budget_raw_materials_cost,
        standard_resources_cost - budget_resources_cost,
        (standard_mix_price - standard_mix_cost) - (budget_price - budget_cost)
    ],
    'Mix standard': [
        standard_mix_price,
        standard_mix_cost,
        standard_raw_materials_cost,
        standard_resources_cost,
        standard_mix_price - standard_mix_cost
    ],
    'Δ MS-ME': [
        actual_mix_price - standard_mix_price,
        actual_mix_cost - standard_mix_cost,
        actual_raw_materials_cost - standard_raw_materials_cost,
        actual_resources_cost - standard_resources_cost,
        (actual_mix_price - actual_mix_cost) -
        (standard_mix_price - standard_mix_cost)
    ],
    'Mix effettivo': [
        actual_mix_price,
        actual_mix_cost,
        actual_raw_materials_cost,
        actual_resources_cost,
        actual_mix_price - actual_mix_cost
    ],
    'Δ ME-C': [
        final_price - actual_mix_price,
        final_cost - actual_mix_cost,
        final_raw_materials_cost - actual_raw_materials_cost,
        final_resources_cost - actual_resources_cost,
        (final_price - final_cost) - (actual_mix_price - actual_mix_cost)
    ],
    'Consuntivo': [
        final_price,
        final_cost,
        final_raw_materials_cost,
        final_resources_cost,
        final_price - final_cost
    ],
}, index=['Prezzi', 'Costi totali', 'Costi MP', 'Costi risorse', 'MOL']))


print("Scostamento totale: " + str((final_price -
      final_cost) - (budget_price - budget_cost)))

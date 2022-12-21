import pandas as pd

budget_costs = pd.read_excel(
    "files/Costo orario risorse - budget.xlsx", decimal=',')
final_costs = pd.read_excel(
    "files/Costo orario risorse - consuntivo.xlsx", decimal=',')
resource_usage = pd.read_excel(
    "files/Impiego orario risorse.xlsx", decimal=',')

# Budget
budget_resource_usage = resource_usage.loc[(
    resource_usage['budget/consuntivo'].str.lower() == "budget")]

budget_resource_usage = budget_resource_usage.merge(
    budget_costs,
    how='left',
    left_on=[
        'Nr. Area di produzione',
        'Risorsa'
    ],
    right_on=[
        'Area di produzione',
        'Risorsa'
    ])

budget_resource_usage['Costo (€)'] = budget_resource_usage['Costo orario (€/h)'] * \
    budget_resource_usage['Tempo risorsa']

budget_production_areas = budget_resource_usage.groupby(
    by=['Area di produzione'], as_index=False).sum(numeric_only=True).sort_values(by=['Costo (€)'], ascending=False)

# Final
final_resource_usage = resource_usage.loc[(
    resource_usage['budget/consuntivo'].str.lower() == "consuntivo")]

final_resource_usage = final_resource_usage.merge(
    final_costs,
    how='left',
    left_on=[
        'Nr. Area di produzione',
        'Risorsa'
    ],
    right_on=[
        'Area di produzione',
        'Risorsa'
    ])

final_resource_usage['Costo (€)'] = final_resource_usage['Costo orario (€/h)'] * \
    final_resource_usage['Tempo risorsa']

final_production_areas = final_resource_usage.groupby(
    by=['Area di produzione'], as_index=False).sum(numeric_only=True).sort_values(by=['Costo (€)'], ascending=False)

# Variances
production_areas = budget_production_areas.merge(
    final_production_areas, how='left', on='Area di produzione', suffixes=[' budget', ' consuntivo'])

production_areas['Δ'] = production_areas['Costo orario (€/h) consuntivo'] - \
    production_areas['Costo orario (€/h) budget']

# Export
production_areas.to_excel('export/production_areas.xlsx')

# actual_hours_production

print(pd.DataFrame({
    'Costo budget':
        budget_production_areas['Costo (€)'].values,
    'Costo consuntivo':
        final_production_areas['Costo (€)'].values,
}, index=[budget_production_areas['Area di produzione']]))

# Analisi scostamento delle risorse

# risorse usate a budget, raggruppate per area di produzione e risorse
uso_risorse_budget = budget_resource_usage.groupby(
    by=['Risorsa', 'Area di produzione'], as_index=False).sum(numeric_only=True).sort_values(by=['Area di produzione'], ascending=False)

# risorse usate a consuntivo, raggruppate per area di produzione e risorse
uso_risorse_consuntivo = final_resource_usage.groupby(
    by=['Risorsa', 'Area di produzione'], as_index=False).sum(numeric_only=True).sort_values(by=['Area di produzione'], ascending=False)

risorse_budget_consuntivo = uso_risorse_budget.merge(
    uso_risorse_consuntivo, how='outer', on=['Area di produzione', 'Risorsa'], suffixes=[' budget', ' consuntivo']).sort_values(by=['Area di produzione'], ascending=False)

# questo perché facendo il group-by, venivano sommati i costi orari per risorse per aree di produzione
# anziché tenerli fissi come da tabella iniziale. Abbiamo quindi fatto un ulteriore merge per unire i costi a budget
# delle risorse divise per area di produzione e le risorse usate a budget e a consuntivo
risorse_budget_consuntivo_ore = risorse_budget_consuntivo.merge(
    budget_costs, how='inner', on=['Area di produzione', 'Risorsa'], suffixes=[' budget', ' consuntivo'])

# Tengo sia il costo orario che il tempo di utilizzo a budget
costo_tot_budget = risorse_budget_consuntivo_ore['Costo (€) budget'].values

# Tengo il costo orario a budget e il tempo a consuntivo
costo_ore_effettive = risorse_budget_consuntivo_ore['Tempo risorsa consuntivo'].values * risorse_budget_consuntivo_ore['Costo orario (€/h)'].values

# Tengo il costo orario e il tempo di utilizzo a consuntivo
costo_tot_consuntivo = risorse_budget_consuntivo_ore['Costo (€) consuntivo'].values

scostamento_risorse = pd.DataFrame({
    'Area di produzione':
        risorse_budget_consuntivo_ore['Area di produzione'].values,
    'Risorsa':
        risorse_budget_consuntivo_ore['Risorsa'].values,
    'Costo budget':
        costo_tot_budget,
    'Δ tempo':
        costo_ore_effettive - costo_tot_budget,
    'Costo ore effettive':
        costo_ore_effettive,
    'Δ costo orario':
        costo_tot_consuntivo - costo_ore_effettive,
    'Costo consuntivo':
        costo_tot_consuntivo,
})

scostamento_risorse.to_excel('export/scostamento_risorse.xlsx')
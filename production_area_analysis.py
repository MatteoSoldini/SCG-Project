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

# Analysis of variances

print(budget_resource_usage)
print(final_resource_usage)

# actual_hours_production

print(pd.DataFrame({
    'Costo budget':
        budget_production_areas['Costo (€)'].values,
    'Costo consuntivo':
        final_production_areas['Costo (€)'].values,
}, index=[budget_production_areas['Area di produzione']]))

budget_resource_cost = budget_resource_usage.groupby(
    by=['Risorsa'], as_index=False).sum(numeric_only=True).sort_values(by=['Costo (€)'], ascending=False)

print(budget_resource_cost)
budget_resource_cost.to_excel('export/budget_resource_cost.xlsx')

final_resource_cost = final_resource_usage.groupby(
    by=['Risorsa'], as_index=False).sum(numeric_only=True).sort_values(by=['Costo (€)'], ascending=False)

print(final_resource_cost)
final_resource_cost.to_excel('export/final_resource_cost.xlsx')

resource_usage_merge = (budget_resource_cost[
    [
        'Risorsa',
        'Tempo risorsa',
        'Costo orario (€/h)',
        'Costo (€)',
    ]
].merge(final_resource_cost[
    [
        'Risorsa',
        'Tempo risorsa',
        'Costo orario (€/h)',
        'Costo (€)',
    ]
], how="outer", on=['Risorsa']))


budget_cost_total = resource_usage_merge['Costo (€)_x']
print(budget_cost_total)

actual_hours_total = resource_usage_merge['Costo orario (€/h)_x'] * resource_usage_merge['Tempo risorsa_y']
print(actual_hours_total)

final_cost_total = resource_usage_merge['Costo (€)_y']
print(final_cost_total)

total = pd.DataFrame({
    'Risorsa': resource_usage_merge['Risorsa'],
    'Costo tot budget': budget_cost_total,
    'Δ Tempo risorsa': actual_hours_total - budget_cost_total,
    'Costo ore effettive': actual_hours_total,
    'Δ Costo orario (€/h)': final_cost_total - actual_hours_total,
    'Costo tot consuntivo': final_cost_total,
})

print(total)

#total.to_excel('export/variance_resource_usage.xlsx')

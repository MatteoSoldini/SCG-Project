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

import pandas as pd

sales = pd.read_excel("files/Vendite.xlsx", decimal=',')
exchange_rates = pd.read_excel("files/Tassi di cambio.xlsx", decimal=',')
customers = pd.read_excel("files/Clienti.xlsx", decimal=',')

# Budget
budget_exchange_rates = exchange_rates.loc[exchange_rates['Anno'].str.lower(
) == "budget"]
budget_sales = sales.loc[(sales['budget/cons'].str.lower() == "budget")]

budget_sales_with_exchange_rates = pd.merge(
    budget_sales, customers, how="left", left_on='Nr. origine', right_on='Nr.').merge(
    budget_exchange_rates, how="left", left_on='Valuta', right_on='Codice valuta').rename(
        columns={
            'Importo vendita in valuta locale (TOTALE VENDITA)': 'Prezzo totale fatture (VL)'}
)[
    ['Nr. origine',
     'Nr articolo',
     'Tasso di cambio medio',
     'Quantità',
     'Prezzo totale fatture (VL)',
     'Valuta']
].groupby(by=['Nr. origine', 'Valuta', 'Tasso di cambio medio', 'Nr articolo'], as_index=False).sum(numeric_only=True)

budget_sales_with_exchange_rates['Prezzo unitario fattura (VL/u)'] = budget_sales_with_exchange_rates['Prezzo totale fatture (VL)'] / \
    budget_sales_with_exchange_rates['Quantità']

# Final
final_exchange_rates = exchange_rates.loc[exchange_rates['Anno'].str.lower(
) == "consuntivo"]
final_sales = sales.loc[(sales['budget/cons'].str.lower() == "consuntivo")]

final_sales_with_exchange_rates = pd.merge(
    final_sales, customers, how="left", left_on='Nr. origine', right_on='Nr.').merge(
    final_exchange_rates, how="left", left_on='Valuta', right_on='Codice valuta').rename(
        columns={
            'Importo vendita in valuta locale (TOTALE VENDITA)': 'Prezzo totale fatture (VL)'}
)[
    ['Nr. origine',
     'Nr articolo',
     'Tasso di cambio medio',
     'Quantità',
     'Prezzo totale fatture (VL)',
     'Valuta']
].groupby(by=['Nr. origine', 'Valuta', 'Tasso di cambio medio', 'Nr articolo'], as_index=False).sum(numeric_only=True)

final_sales_with_exchange_rates['Prezzo unitario fattura (VL/u)'] = final_sales_with_exchange_rates['Prezzo totale fatture (VL)'] / \
    final_sales_with_exchange_rates['Quantità']

# Actual mix
actual_mix = budget_sales_with_exchange_rates[[
    'Valuta',
    'Nr. origine',
    'Nr articolo',
    'Prezzo unitario fattura (VL/u)',
    'Tasso di cambio medio']].merge(
        final_sales_with_exchange_rates[
            ['Nr. origine',
             'Nr articolo',
             'Quantità']],
    how='inner',
    on=['Nr. origine', 'Nr articolo'])
actual_mix['Prezzo totale fattura (€)'] = actual_mix['Prezzo unitario fattura (VL/u)'] / \
    actual_mix['Tasso di cambio medio'] * actual_mix['Quantità']

# Actual exchange mix
actual_exchange_mix = budget_sales_with_exchange_rates[[
    'Valuta',
    'Nr. origine',
    'Nr articolo',
    'Prezzo unitario fattura (VL/u)']].merge(
        final_sales_with_exchange_rates[
            ['Nr. origine',
             'Nr articolo',
             'Tasso di cambio medio',
             'Quantità']],
    how='inner',
    on=['Nr. origine', 'Nr articolo'])
actual_exchange_mix['Prezzo totale fattura (€)'] = actual_exchange_mix['Prezzo unitario fattura (VL/u)'] / \
    actual_exchange_mix['Tasso di cambio medio'] * \
    actual_exchange_mix['Quantità']

# Final mix
final_mix = final_sales_with_exchange_rates[
    ['Valuta',
     'Nr. origine',
     'Nr articolo',
     'Prezzo unitario fattura (VL/u)',
     'Tasso di cambio medio',
     'Quantità']]
final_mix['Prezzo totale fattura (€)'] = final_mix['Prezzo unitario fattura (VL/u)'] / \
    final_mix['Tasso di cambio medio'] * final_mix['Quantità']

print(pd.DataFrame({
    'Mix effettivo': [
        actual_mix['Prezzo totale fattura (€)'].sum(),
    ],
    'Δ E-TE': [
        actual_exchange_mix['Prezzo totale fattura (€)'].sum(
        ) - actual_mix['Prezzo totale fattura (€)'].sum(),
    ],
    'Mix tasso effettivo': [
        actual_exchange_mix['Prezzo totale fattura (€)'].sum()
    ],
    'Δ TE-C': [
        final_mix['Prezzo totale fattura (€)'].sum(
        ) - actual_exchange_mix['Prezzo totale fattura (€)'].sum(),
    ],
    'Consuntivo': [
        final_mix['Prezzo totale fattura (€)'].sum(),
    ],
}, index=['Prezzi']))

# Export
# actual_mix.to_excel('actual_mix.xlsx')
# actual_exchange_mix.to_excel('actual_exchange_mix.xlsx')
# final_mix.to_excel('final_mix.xlsx')

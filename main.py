import pandas as pd

sales = pd.read_excel("files/Vendite.xlsx")
customers = pd.read_excel("files/Clienti.xlsx")
df = pd.merge(sales, customers, how="left",
              left_on='Nr. origine', right_on='Nr.').head()

print(df)

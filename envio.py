import pandas as pd
import numpy as np
df_desconhecidos = pd.read_csv("88888888888888.csv",)
print(df_desconhecidos.shape)
x=df_desconhecidos.drop(columns=['Unnamed: 0'])
print(x.shape)
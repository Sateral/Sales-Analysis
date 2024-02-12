import warnings
warnings.filterwarnings("ignore", "\nPyarrow", DeprecationWarning)
import pandas as pd
import os

# Merge 12 months of sales data excel files into one file
path = "E:\Sales Analysis\Sales_Data"
salesFiles = [file for file in os.listdir(path)]

dataList = []
for file in salesFiles:
  data = pd.read_csv(os.path.join(path, file))
  dataList.append(data)

salesData = pd.concat(dataList)

salesData.to_csv("data.csv", index=False)
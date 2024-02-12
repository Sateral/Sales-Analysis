import warnings
warnings.filterwarnings("ignore", "\nPyarrow", DeprecationWarning)
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

#### Find best month for sales. Show the earnings of that month
data = pd.read_csv("data.csv")
LINE = "-" * 32
SPACER = f"\n{LINE}\n"

# Get rid of null rows
data.dropna(inplace=True)

# Create months column
data = data[data["Order Date"].str[:2] != "Or"]
dataDates = pd.DataFrame(pd.to_datetime(data["Order Date"], format="%m/%d/%y %H:%M"))
data["Month"] = dataDates["Order Date"].dt.month

# Create sales column
data["Sales"] = data["Quantity Ordered"].astype(int) * data["Price Each"].astype(float)

#Find total
totalSalesByMonth = pd.Series(data.groupby(["Month"])["Sales"].sum())
maxIndexMonth = totalSalesByMonth[totalSalesByMonth == totalSalesByMonth.max()].index[0]
print(f"The best month for sales was month {maxIndexMonth} with ${totalSalesByMonth.max()} of sales")

months = range(1, 13)
# plt.bar(months, totalSalesByMonth)
# plt.xticks(months)
# plt.ylabel("Months")
# plt.ylabel("Sales in USD (millions)")
# plt.show()

print(SPACER)

#### What city had the most sales
# Create city column
def get_city(address):
  return address.split(',')[1].strip()

def get_state(address):
  return address.split(',')[2].split(" ")[1].strip()

data["City"] = data["Purchase Address"].apply(lambda x: f"{get_city(x)} ({get_state(x)})") # In case same city, different state

#Find total
totalSalesByCity = pd.Series(data.groupby(["City"])["Sales"].sum())
maxIndexCity = totalSalesByCity[totalSalesByCity == totalSalesByCity.max()].index[0]

#Results
print(f"The best city for sales was {maxIndexCity[:-5]} with ${totalSalesByCity.max()} of sales")
cities = [city for city, df in data.groupby("City")]
# plt.bar(cities, totalSalesByCity)
# plt.xticks(cities, rotation="vertical", size=8)
# plt.ylabel("City")
# plt.ylabel("Sales in USD (millions)")
# plt.show()

print(SPACER)

#### What's the best time to display advertisements to maximize product sales
dataDates = pd.DataFrame(pd.to_datetime(data["Order Date"], format="%m/%d/%y %H:%M"))
data["Hour"] = dataDates["Order Date"].dt.hour
hours = [hour for hour, df in data.groupby("Hour")]
# plt.plot(hours, data.groupby(["Hour"]).count())
# plt.xticks(hours)
# plt.xlabel("Hour")
# plt.ylabel("Number of Sales")
# plt.grid()
# plt.show()
print("Based on the graph, the best time to display advertisements would be around 12pm and 7pm")

print(SPACER)

#### What products are most often sold together?
soldTogetherData = data[data["Order ID"].duplicated(keep=False)]

warnings.filterwarnings('ignore')
soldTogetherData["Grouped"] = soldTogetherData.groupby("Order ID")["Product"].transform(lambda x: ','.join(x))
warnings.filterwarnings('default')

soldTogetherData = soldTogetherData[["Order ID", "Grouped"]].drop_duplicates()

count = Counter()

for row in soldTogetherData["Grouped"]:
  row_list = row.split(",")
  count.update(Counter(combinations(row_list, 2)))

print("The most 5 common products bought together are:")
for key, value in count.most_common(5):
  product1, product2 = key
  print(f"-  {product1} and {product2} with {value} sales")
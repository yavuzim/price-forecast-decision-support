import json
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_PATH = "data/raw/iphone16e.json"

with open(DATA_PATH, "r", encoding="utf-8") as file:
    text = file.read().strip()

text = re.sub(r",\s*([\]}])", r"\1", text)

data = json.loads(text)

if isinstance(data, dict):
    products = [data]
elif isinstance(data, list):
    products = data
else:
    raise TypeError("JSON root must be a list or a dictionary.")

for i, product in enumerate(products):
    print(i, product.get("title", "Untitled product"))

product = products[0]
print("\nSelected product:", product.get("title"))

daily_records = product["analysis"]["3 Ay"]["daily"]

df = pd.DataFrame(daily_records)

df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")

def clean_price(raw_price):
    """Convert a Turkish-formatted price like '41.759,04 TL' to the float 41759.04."""
    raw_price = str(raw_price)
    raw_price = raw_price.replace(" TL", "")   
    raw_price = raw_price.replace(".", "")    
    raw_price = raw_price.replace(",", ".")    
    return float(raw_price)


df["price"] = df["price"].apply(clean_price)

df = (
    df.dropna(subset=["date", "price"])
      .sort_values("date")
      .reset_index(drop=True)
)

print("\nFirst records:")
print(df.head())

print("\nNumber of observations:", len(df))
print("Date range:", df["date"].min(), "-", df["date"].max())
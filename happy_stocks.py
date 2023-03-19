"""
happy_stocks.py

This is the Python version of "Happy-Stocks.ipynb" because FastAPI wants a py file specifically

This code takes pretrained models and information to predict how "generous" one should be towards
    a company with your money
"""

import os            # Interface with the OS
import csv           # Read in CSV files
import joblib        # Deserialize the models
import random        # Used to switch between API keys
import requests      # Get information from the APIs
import pandas as pd  # Used for dataframes

# Transform a stock into a country for ML models
def transform_stock(symbol):
    # All API keys I use because of the 5-request per API key
    api_keys = [
        "2RFQ9MPXDZ19H8ZB", "5HNZLHHXQ49419OW", "AD4QHR1QWWPX3PAZ",
        "DROMFL8PK13N9PVP", "0Z6NF5RSECY0KSUT", "43GLZYIC6DFBYGIT",
        "KUJBKMRA90WZSS7B"]

    # Get all the one-hot encoded columns
    f = open("columns.txt", "r")
    columns = f.read().split('-')[:-1]
    f.close()

    # Temp variables
    column_names = columns   # Column headers
    column_values = columns  # Temporary column values

    # Get General Data
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={random.choice(api_keys)}'
    r = requests.get(url)
    data = r.json()

    # Year
    column_values[0] = 0.5  # Default to median possible value

    # Try to find year in the stocks we have access to
    csv_file = csv.reader(open('pickable_stocks.csv', 'r'), delimiter=',')
    for row in csv_file:
        if symbol == row[7]:
            if row[7] is not None:
                column_values[0] = ((row[7] % 8) + 2023) / 8
            break

    # Country
    country = data["Country"]

    # Thankfully America's name is not standardized
    if country == "USA":
        country = 'United States'
    country = f"('{country}',)"

    # Do the one hot encoding
    for i in range(6, len(column_values)):
        if column_values[i] == country:
            column_values[i] = 1
        else:
            column_values[i] = 0

    # Economy
    column_values[2] = float(data["200DayMovingAverage"]) / 300  # Divide by 300 to put between 0 and 1

    # Health
    column_values[3] = float(data['ProfitMargin'])

    # Freedom
    column_values[4] = min(float(data['DividendYield']) * 100, 1)

    # Corruption
    column_values[5] = min(float(data['MarketCapitalization']) / (2 * (10 ** 12)), 1)

    # Get Sentiment Analysis Data
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers{symbol}&apikey={random.choice(api_keys)}'
    r = requests.get(url)
    data = r.json()

    # Happiness
    happiness = []
    for item in data["feed"]:
        for ticker in item["ticker_sentiment"]:
            if ticker["ticker"] == symbol:
                happiness.append(float(ticker["ticker_sentiment_score"]) * float(ticker["relevance_score"]))

    # If not happiness data, set to middle value
    if len(happiness) == 0:
        column_values[1] = 0.5
    else:
        score = ((sum(happiness) / len(happiness)) + 0.35) / 0.7
        column_values[2] = max(min(score, 1), 0)

    return pd.DataFrame([column_values], columns=column_names)

# Predict a stock based off a ticker
def predict_stock(stock):
    # Get the transformed stock (stock to country)
    stock_transform = transform_stock(stock)

    # Lists to hold items
    good_models = []  # All machine learning models that are voting
    predictions = []  # Hold all predictions so we can use the voting ideology

    # Get all machine learning models
    for file in os.listdir("."):
        if file.endswith(".pkl"):
            good_models.append(joblib.load(file))

    # Make a prediction for each model
    for model in good_models:
        predictions.append(model.predict(stock_transform.values))

    # Use the voting ideology to make the final prediction (average all of them)
    prediction = sum(predictions)[0] / len(predictions)

    return f"{stock},{prediction}"

# Predict a random stock from pickable_stocks.csv file
def predict_random_stock():
    # CSV File is small enough to read to memory fully
    csv_file = csv.reader(open('pickable_stocks.csv', 'r'), delimiter=',')

    # Choose a random stock
    chosen_row = random.choice(list(csv_file))

    # Return prediction for said random stock
    return predict_stock(chosen_row[0])

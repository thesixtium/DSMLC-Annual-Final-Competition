import os
import joblib
import csv
import random
import requests
import pandas as pd


def transform_stock(symbol):
    blue_chip_stock_200DayMovingAverage_max = 300
    api_keys = [
        "2RFQ9MPXDZ19H8ZB", "5HNZLHHXQ49419OW", "AD4QHR1QWWPX3PAZ",
        "DROMFL8PK13N9PVP", "0Z6NF5RSECY0KSUT", "43GLZYIC6DFBYGIT",
        "KUJBKMRA90WZSS7B"]

    f = open("columns.txt", "r")
    columns = f.read().split('-')[:-1]
    f.close()

    column_names = columns
    column_values = columns

    # Get General Data
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={random.choice(api_keys)}'
    r = requests.get(url)
    data = r.json()

    # Year
    column_values[0] = 1

    csv_file = csv.reader(open('pickable_stocks.csv', 'r'), delimiter=',')

    for row in csv_file:
        if symbol == row[7]:
            if row[7] is not None:
                column_values[0] = ((row[7] % 8) + 2023) / 8
            break

    # Country
    country = data["Country"]
    if country == "USA":
        country = 'United States'
    country = f"('{country}',)"

    for i in range(6, len(column_values)):
        if column_values[i] == country:
            column_values[i] = 1
        else:
            column_values[i] = 0

    # Economy
    column_values[2] = float(data["200DayMovingAverage"]) / blue_chip_stock_200DayMovingAverage_max

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

    if len(happiness) == 0:
        column_values[1] = 0.5
    else:
        score = ((sum(happiness) / len(happiness)) + 0.35) / 0.7
        column_values[2] = max(min(score, 1), 0)

    return pd.DataFrame([column_values], columns=column_names)


def predict_stock(stock):
    stock_transform = transform_stock(stock)
    predictions = []

    good_models = []

    for file in os.listdir("."):
        if file.endswith(".pkl"):
            good_models.append(joblib.load(file))

    for model in good_models:
        predictions.append(model.predict(stock_transform.values))

    prediction = sum(predictions)[0] / len(predictions)

    return f"{stock},{prediction}"


def predict_random_stock():
    csv_file = csv.reader(open('pickable_stocks.csv', 'r'), delimiter=',')
    chosen_row = random.choice(list(csv_file))

    return predict_stock(chosen_row[0])
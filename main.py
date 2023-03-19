# uvicorn main:app --reload
# streamlit run C:/Users/Sixtium/Documents/GitStuff/DSMLC-Annual-Final-Competition/app.py

from fastapi import FastAPI
from happy_stocks import predict_stock, predict_random_stock

app = FastAPI()


@app.get("/stock")
def run_predict_stock(prompt: str):
    return predict_stock(prompt)


@app.get("/rstock")
def run_predict_random_stock():
    return predict_random_stock()

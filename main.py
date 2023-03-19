"""
main file for the API

To run, do the following commands (assuming your path is the same as mine) in this order
 - uvicorn main:app --reload
 - streamlit run C:/Users/Sixtium/Documents/GitStuff/DSMLC-Annual-Final-Competition/app.py

Very small because ahhhhhhhh we love frameworks
"""

# Imports
from fastapi import FastAPI                                   # Framework for API
from happy_stocks import predict_stock, predict_random_stock  # Predictions functions

# Make a class of the framework
app = FastAPI()


# Handle request for "/stock"
@app.get("/stock")
def run_predict_stock(prompt: str):
    return predict_stock(prompt)


# Handle request for "/rstock" aka Random Stock
@app.get("/rstock")
def run_predict_random_stock():
    return predict_random_stock()

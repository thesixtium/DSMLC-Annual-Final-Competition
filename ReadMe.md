# Happy Stocks

Have you ever wanted to **invest** in stocks based on the World Happiness Report? Do **you** want to lose money because of bad financial advice? Are stocks **also** meaningless to you? 

Well then you're a perfect client for Happy Stocks (tm)! Using machine learning on the World Happiness Report, we created the most mediocre machine learning algorithm to judge stocks.

Simply type in a NASDAQ stock ticker, and we'll rate it on how happy it makes you! If you're feeling "lucky", leave the field blank and we'll pick a random stock for you.

*Please don't actually invest based on this application. Or do. I'm not your mom :)*

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar. Navigate to the folder "DSMLC-Annual-Final-Competition" and pip install everything at once:

```bash
cd C:\Users\path\to\DSMLC-Annual-Final-Competition
pip install -r requirements.txt
```
I'm like 50.1% sure this installs everything you need (correctly)

## How It Works

### The Training

The dataset given was an absolute mess due to non-standardization of the columns, linear vs logarithmic columns, and data just missing. After dealing with that, I then picked out models that fit my objective, and trained on them. Finally, I took stocks and converted company metrics into indicators in my data, and ran them to "recommend" stocks.

#### Pre-Processing

This is easily the step I spent the most time on. The dataset was a bit of a disaster and all over the place. To deal with it, I did a tonne of pre-processing. I first decided the columns I wanted to use, basically just by seeing which columns were shared by every year. The columns I went with are the following:
* Year
* Country
* Happiness
* Economy
* Health
* Freedom
* Corruption
* Generosity

Then, I imputered each column to replace all NaN's, inf's, and -inf's to the mean of the column. Less than 1% of any given column contained these values, so I feel like a relatively simple approach to dealing with them was best.

I then normalized each column. Even if a machine learning model accepts non-normalize data, it usually has better results when you normalize it. Therefore, it starts by weighing everything evenly and then deciding how to weigh them, instead of starting with them (probably wrongly) unevenly weighted.

#### Choosing my input and outputs

It seemed like the point of the dataset would be to predict the happiness of a country, but I wanted to predict generosity because I had never seen it predicted before. There's not really more to it than that.

#### Model Selection

This dataset was a classic linear regression problem. There are inputs in, and a continuous range of outputs (as opposed to a discrete range that would lend itself to classification).

I have no idea what the **best** linear regression algorithm would be, so I chose to use a voting setup. By training all the most mainstream (and hopefully best) algorithms, and then taking the ones that did the best to vote on every decision, I would hopefully be using the *Law of Large Numbers* to my advantage. While voting setups seem to mostly be in classification problems, I decided to use it here so I didn't have to guess and check models. 

Every model's vote is equal, and they are averaged for a prediction. In the future I could work on making the votes unequal, so the best trained models have slightly more say.

To find the models, I just googled "Best Regression Models to Train" and used those, and all models that were preforming better than the overall average in training were considered "good" models and allowed to vote when it came time to predict stuff.

#### Saving models

I picked stuff and it worked well. That is all. It was fast, easy, and simple. 

### Making Stocks Into Countries

All the models above were trained on countries and their data, so if I just gave them stocks they would be incredibly confused. Therefore, I needed to convert these stocks into countries.

You know how everyone universally agrees that economics and coding are art forms? Well, that ideology is **heavily** applied in the conversion of stocks to countries.

For every category, I made sure to normalize the data so it would look similar to the training data (providing a year of 2012 when the training data was from 0 to 1 would throw off the models).

#### Founding Year -> Year

This was the second easiest one, as I just took the company's IPO (when the stock was first available), and modulo'd it so the year fit within the training data range.

#### Country -> Country

This was the easiest one. Company country = Country. EZ

#### Sentiment Analysis -> Happiness

This was one I had the most fun with because I got to use a pretrained sentiment analysis model on the most recent news articles on the stock.

#### Stock Price -> Economy

Economy is how well a country is doing financially, and a stock price is a pretty good way of seeing how a company is doing. Stuff like splits or how many shares there are will throw this category off, but I love assuming things.

#### Profit Margin -> Health

This is where the "art" piece starting coming in. I feel like healthy companies have a decent profit margin generally, although this falls through for certain industries (food is a big one) while other industries naturally have a higher profit margin. While not the best metric, it was good enough.

#### Dividend Yield -> Freedom

I keep seeing on the news that passive income is the key to financial freedom. Because stock dividend's are technically a "set it and forget it" form of investments, I loosely drew the conclusion that dividends = freedom.

#### Market Capitalization -> Corruption

This is probably the most "art" and least "science" that I use on this entire project. I think generally bigger companies are seen as more corrupt. That is what my entire thought process was.

#### Generosity

This was my output variable, so I chose to interpret this as how generous should I be with my money to this company. Should I spend a lot? A little? Well, this variable will tell me!

### The Website

Webdev is my achilles heel. I despise front-end development, but luckily for me I recently when to a talk on deploying machine learning models (shout out YYC DataCon) and they showed how you could use python front to back for deployment. 

I made my backend the models I trained, which were python. I made my API using FastAPI, which uses python. I used Streamlit for my frontend, which is also python. 

I used these specific technologies because they are what were taught to me and I feel really good in Python. I don't really have better reasons than those two.

## Usage

You don't actually run any python files by clicking on them! Everything is launched from frameworks via the terminal. Here is what you should do:

1. Navigate to the folder "DSMLC-Annual-Final-Competition"
```bash
cd C:\Users\path\to\DSMLC-Annual-Final-Competition
```

2. Launch the backend
```bash
uvicorn main:app --reload
```

3. Launch the website
```bash
streamlit run C:/Users/path/to/DSMLC-Annual-Final-Competition/app.py
```

4. Go to the website in your [local browser with port 8501](http://localhost:8501/)

## Retraining

To retrain all the models, do the following:

1. Navigate to the folder "DSMLC-Annual-Final-Competition"
```bash
cd C:\Users\path\to\DSMLC-Annual-Final-Competition
```

2. Run Jupyter Notebook
```bash
jupyter notebook
```

3. Hit "Run All" within "Model-Trainer.ipynb"

4. Wait

5. Profit!

## Contributing

I have no idea why you'd want to contribute to this project. You are welcome to submit a pull request, but I have no idea what they are or what to do with it. 

I've been told to say "For major changes, please open an issue first to discuss what you would like to change", but if I can't deal with pull requests I have no hope for issues.

## License

I think I should use [MIT](https://choosealicense.com/licenses/mit/)? I am super unsure. 

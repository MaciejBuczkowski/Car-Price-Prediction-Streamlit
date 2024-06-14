# Car-Price-Prediction-Streamlit
 Webapp based off of my dissertation

## Purpose
This app was initially created for my disertation project with the main focus on the reasearch side of it. This app is a better developed front end than original using a similar model. This is also using the same dataset so this is by no means an accurate predictor as the data is 2 years out of date and I do not intend to keep it up to date.

## Requirements
- Python
- PostgreSQL
- Selenium - with chromedriver
- Streamlit
- Numpy
- Pandas
- Scikit Learn
- Plotly
- Joblib
- psycopg2
- sqlalchemy

These can all be installed via pip using the command:

```pip install selenium chromedriver streamlit numpy pandas scikit-learn plotly joblib psycopg2 sqlalchemy```

Postgres omitted incase you want to install through app instead of terminal.

## Setup
Once you have installed everything then you need to train a model using the notebook (its too large for me to upload here) and create a database in PostgreSQL.

Once you have a database create a table with the following format:
![Table](https://github.com/MaciejBuczkowski/Car-Price-Prediction-Streamlit/blob/main/Images/Screenshot%202024-06-11%20at%2018.57.19.png)

Then you need to populate this. The populate.sh script should allow you to do this but u can also do it manually. To do it with the script in the terminal type:

```shell
chmod u+x populate.sh
./populate.sh <Your PostgreSQL username> <PostgreSQL password> <Table name from earlier>
```

Then you will have to update the file .streamlit/secrets.toml to have your database credentials in instead of the placeholders.

Finally you will need to run the streamlit app. This can be done by navigating to the directory containing main.py and running:

```streamlit run main.py```

## In use
Once it is all set up then you can use the app.

![Home Screen Link](https://github.com/MaciejBuczkowski/Car-Price-Prediction-Streamlit/blob/main/README%20images/Screenshot%202024-06-14%20at%2016.18.50.png)

![Home Screen Manual](https://github.com/MaciejBuczkowski/Car-Price-Prediction-Streamlit/blob/main/README%20images/Screenshot%202024-06-14%20at%2016.19.09.png)

This is the main screen where you will have the option for manual entry or for link entry (links can only be taken from autotrader.co.uk for scraping)

The data is collected from this page and these sections of it. (The advert is first one from the top of the search page. Wouldnt catch me dead in an Audi)

![Main Advert](https://github.com/MaciejBuczkowski/Car-Price-Prediction-Streamlit/blob/main/README%20images/Screenshot%202024-06-14%20at%2016.17.45.png)

![Main Info](https://github.com/MaciejBuczkowski/Car-Price-Prediction-Streamlit/blob/main/README%20images/Screenshot%202024-06-14%20at%2016.17.56.png)

![Additional Info](https://github.com/MaciejBuczkowski/Car-Price-Prediction-Streamlit/blob/main/README%20images/Screenshot%202024-06-14%20at%2016.18.19.png)

These are the places that the scraper gets all of the data from for use in the app.

Once the app is ran on the either manually added data or the data scraped from the link it will output a small dashboard like this:

![Output](https://github.com/MaciejBuczkowski/Car-Price-Prediction-Streamlit/blob/main/README%20images/Screenshot%202024-06-14%20at%2016.19.42.png)

This is the output 'dashboard'. If you run it without a price in manual mode it wont show the scale or the red bar on the graph as those are to show the actual price and if its a good price.

(I am aware that the screenshot of the advert actually contains the scale but this project was originally done before this was widely used on the website)
# Sales forecast
In this project I made the forecast of sales amount for chain store for the year ahead.
## Models:
I tried several models to make forecast, such as: **ARIMA**, **LinearRegression**, [Prophet](https://facebook.github.io/prophet/), **XGBoost**, [CatBoost](https://catboost.ai/en/docs/). The prophet model showed the best quality, so that for final forecast I used prophet. The forecast saved in forecast.csv file.
## Data:
Data stored in train.zip file in csv format. Dataframe consist of 125 million rows with information about each sale such as: sale id, sale date, product number, amount saled products, store number, was it on promotion or not.

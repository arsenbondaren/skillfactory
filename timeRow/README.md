# Sales forecast
In this project, I made a forecast of sales for a chain store for the year ahead.
## Models:
I tried several models to make forecasts, such as: **ARIMA**, **LinearRegression**, [Prophet](https://facebook.github.io/prophet/), **XGBoost**, [CatBoost](https://catboost.ai/en/docs/). The prophet model showed the best quality, so that for final forecast I used prophet. The forecast saved in forecast.csv file.
## Data:
Data is stored in train.zip file in csv format. Dataframe consist of 125 million rows with information about each sale, such as sale id, sale date, product number, amount saled products, store number, and whether it was on promotion or not.

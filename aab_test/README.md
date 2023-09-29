# Information about data
Each dataset has information about user's action ("action_id" column): 0 - click, 1 - view, 2 - purchase (user look through a list of products, clicks on it and buy it finally).
## Metrics to compare groups
**Click through rate (CTR)** - how often users click on a product (clicks/views).
**Purchase rate** - how often users buy a product (purchases/views).
**Gross Merchandise Value (GMV)** - total value of products sold over a given period of time (product price * number of products sold)
## Tests in project:
**Shapiro-Wilk test** - to check if data in each sample has normal distribution.
**Z-test** - to compare the mean of the A/B samples

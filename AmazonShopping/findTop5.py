import sys
import csv
import numpy as np

class Product(object):
    def __init__(self, name, price, ratings, nReviews):
        self.name = name
        self.price = price
        self.ratings = ratings
        self.nReviews = nReviews
        self.score = None

    def normalize(self, priceMean, priceStd, ratingsMean, ratingsStd, nrMean, nrStd):
        self.n_price = (self.price-priceMean)/priceStd
        self.n_ratings = (self.ratings-ratingsMean)/ratingsStd * -1
        self.n_nReviews = (self.nReviews - nrMean)/nrStd * -1
        # lower the better

    def compute_score(self):
        self.score = self.n_price + self.n_ratings + self.n_nReviews

csv_name = sys.argv[1]

with open(csv_name, 'r') as csv_file:
    # creating a csv reader object
    csv_reader = csv.reader(csv_file)

    # extracting field names through first row
    fields = csv_reader.__next__()
    # Name Price Ratings, # of Reviews

    # extracting each data row one by one
    prices= []
    ratings = []
    nReviews = []
    products = []
    for row in csv_reader:
        if row[2].strip() == '' or row[3].strip() == '' or row[4].strip() == '':
            continue
        price = float(row[2].strip())
        rating = float(row[3].strip())
        nReview = float(row[4].strip().replace(',',''))

        products.append(Product(row[0], price, rating, nReview))
        prices.append(price)
        ratings.append(rating)
        nReviews.append(nReview)

    priceMean = np.mean(prices)
    ratingMean = np.mean(ratings)
    nReviewMean = np.mean(nReviews)
    priceStd = np.std(prices)
    ratingStd = np.std(ratings)
    nReviewStd = np.std(nReviews)

    for product in products:
        product.normalize(priceMean, priceStd, ratingMean, ratingStd, nReviewMean, nReviewStd)
        product.compute_score()

    products.sort(key= lambda x: x.score)
    print("TOP 5")
    for i in range(5):
        print("Name: " + products[i].name + " Score: " + str(products[i].score) + " Price:  " + str(products[i].price))
        print("----------------------------------------------------")

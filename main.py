import crochet
from flask import Flask , render_template, jsonify, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time
from eidolonSpider.eidolonSpider.spiders.eidolon_spider import EidolonRealSpider
from pymongo import MongoClient


crochet.setup()
app = Flask(__name__)

output_data = []
crawl_runner = CrawlerRunner()


# By Deafult Flask will come into this when we run the file
@app.route('/')
def index():
    return render_template("ind.html")  # Returns index.html file in templates folder.


# After clicking the Submit Button FLASK will come into this
@app.route('/send', methods=['POST'])
def submit():
    if request.method == 'POST':
        global baseURL
        baseURL = "https://stackoverflow.com/questions"
        info = scrape()
        rs = list()
        count = 0
        for point in info:
            if count > 6:
                break
                count += 1
            arr = list()
            arr.append(point['name'])
            arr.append(point['url'])
            arr.append(point['story'])
            rs.append(arr)

        c = len(rs) - 1
        return render_template('ind.html', title0=rs[c][0], link0=rs[c][1], story0=rs[c][2],
                               title1=rs[c - 1][0], link1=rs[c - 1][1], story1=rs[c - 1][2],
                               title2=rs[c - 2][0], link2=rs[c - 2][1], story2=rs[c - 2][2],
                               title3=rs[c - 3][0], link3=rs[c - 3][1], story3=rs[c - 3][2],
                               title4=rs[c - 4][0], link4=rs[c - 4][1], story4=rs[c - 4][2],
                               title5=rs[c - 5][0], link5=rs[c - 5][1], story5=rs[c - 5][2],
                               )


def scrape():
    scrape_with_crochet(baseURL=baseURL)  # Passing that URL to our Scraping Function

    time.sleep(10)  # Pause the function while the scrapy spider is running

    # final = jsonify(output_data)


    passwd = input("Enter mongoDB password: ")
    db = MongoClient("mongodb+srv://ayglory:{}@cluster0-jv8w4.gcp.mongodb.net/test?retry"
                     "Writes=true&w=majority".format(passwd))
    collection = db["eidolonDB"]["questions"]

    for data in output_data:
        good_item = True
        for value in data:
            if not value:
                good_item = False
                break
        if good_item:
            collection.insert_one(dict(data))

    print("\n\n Saved Successfully! \n\n")
    print("\n\n Closing collections! \n\n")
    db.close()

    return collection.find()


@crochet.run_in_reactor
def scrape_with_crochet(baseURL):
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)

    # This will connect to the EidolonRealSpider function in our scrapy file
    # and after each yield will pass to the crawler_result function.
    return crawl_runner.crawl(EidolonRealSpider, category=baseURL)


# This will append the data to the output data list.
def _crawler_result(item, response, spider):
    output_data.append(dict(item))


if __name__ == "__main__":
    app.run(debug=True)

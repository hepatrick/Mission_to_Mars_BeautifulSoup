from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars
import os

# create instance of Flask app
app = Flask(__name__)

# create mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars
collection = db.mars_info

@app.route("/")
def home():
#    return "hello"
    mars_info = collection.find_one()
    return  render_template('index.html', mars_info=mars_info)

@app.route("/scrape")
def scrape():
    mars_info = collection
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_image()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_hemispheres()
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
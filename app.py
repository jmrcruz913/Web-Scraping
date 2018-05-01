
# coding: utf-8

# In[14]:


import pymongo
from flask import Flask, jsonify, render_template
import scrape_mars


# In[15]:


client = pymongo.MongoClient()
db = client.marsdb
collection = db.marsdb.marscollection


# In[16]:



app = Flask(__name__)

@app.route("/")
def home():
    data = list(collection.find({}).sort("date", pymongo.DESCENDING).limit(1))
    latest_data = data[0]
    return render_template('index.html',mars=latest_data)


@app.route("/scrape")
def scrape():
    
    scraped_data = scrape_mars.scrape()
    collection.insert_one(scraped_data)
    data = collection.find_one({})
    print(data)
    return render_template('index.html',mars=scraped_data)

if __name__ == "__main__":
    app.run(debug=True)


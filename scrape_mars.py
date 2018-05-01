
# coding: utf-8

# In[59]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time

from splinter import browser
from selenium import webdriver


# In[60]:


url = "https://mars.nasa.gov/news/" 
response = requests.get(url)

soup = bs(response.text, 'html.parser')

print(soup.prettify())


# In[61]:


title = soup.find("div", class_="content_title").text
paragraph_text = soup.find("div", class_="rollover_description_inner").text


print(title)


# In[62]:


print(paragraph_text)


# In[63]:


def init_browser():
    chrome_location = "C:\Windows\Temp\Temp2_chromedriver_win32.zip\chromedriver.exe"
    chrome_location = chrome_location.replace("\\","/")
    executable_path = {"executable_path":chrome_location}
    
    return Browser("chrome", **executable_path, headless=False)


# In[64]:


def get_soup_objectget_sou (url):
    browser = init_browser()
    browser.visit(url)
    soup = BeautifulSoup(browser.html,"html.parser")
    return soup


# In[65]:


def get_latest_NASA_news():
    NASA_MARS_url = "https://mars.nasa.gov/news/"
    news_soup = get_soup_object(NASA_MARS_url)
    latest_news = news_soup.find_all("div",{"class":"list_text"})[0]
    return {
        "news-title":latest_news.find("div",{"class":"content_title"}).text,
        "news-content":latest_news.find("div",{"class":"article_teaser_body"}).text
    }


# In[66]:


def get_MARS_img():
    JPL_home_url = "https://www.jpl.nasa.gov"
    JPL_img_url = JPL_home_url+"/spaceimages/?search=&category=Mars"
    jpl_soup = get_soup_object(JPL_img_url)
    items = jpl_soup.find("div",{"class":"carousel_items"})
    img_title = items.find("h1",{"class":"media_feature_title"})
    featured_img = items.find("article")
    img_url = JPL_home_url+featured_img['style'].split(':')[1].split('\'')[1]
    return {
            "title":img_title,
            "img_url":img_url
           }


# In[67]:


def get_MARS_temperature():
    twitter_report_url = "https://twitter.com/marswxreport?lang=en"
    temp_soup = get_soup_object(twitter_report_url)
    return temp_soup.find("ol",{"id":"stream-items-id"}).find("li").find("p").text


# In[68]:


def get_MARS_facts():
    df = pd.read_html("https://space-facts.com/mars/")[0]
    df = df.rename(columns={0:"Description",1:"Value"})
    return df.to_dict()


# In[69]:


def get_MARS_hemisphere_data():
    browser = init_browser()
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    hms_soup = BeautifulSoup(browser.html,"html.parser")
    items = hms_soup.find("div",{"id":"product-section"}).find_all("div",{"class":"item"})

    hemisphere_data = []

    for item in items:
        img_main_url = "https://astrogeology.usgs.gov"+item.find("a")["href"]
        img_title = item.find("div",{"class":"description"}).find("a").find("h3").text
        browser.visit(img_main_url)
        time.sleep(1)
        img_soup = BeautifulSoup(browser.html,"html.parser")
        download_item = img_soup.find("div",{"class":"downloads"})
        hemisphere_item = {
            "title":img_title,
            "img_url": download_item.find("li").find("a")["href"]
        }
        hemisphere_data.append(hemisphere_item)
        
    return hemisphere_data


# In[70]:


def scrape():
    mars_news = get_latest_NASA_news()
    mars_img = get_MARS_img()
    mars_facts = get_MARS_facts()
    mars_temp = get_MARS_temperature()
    mars_hm_data = get_MARS_hemisphere_data()
    return {
        "news":mars_news,
        "featured_img":mars_img,
        "facts":mars_facts,
        "temperature":mars_temp,
        "hemisphere_data":mars_hm_data
    }


# In[71]:


scrape()


# In[72]:


df = pd.read_html("https://space-facts.com/mars/")[0]
df = df.rename(columns={0:"Description",1:"Value"})
df = df.set_index("Description")
df.to_dict()['Value']


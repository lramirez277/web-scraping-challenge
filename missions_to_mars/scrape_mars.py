#dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time 
from flask import Flask, render_template
import pymongo
import time 

#define browse
def init_browser():
    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)  

def scrape():
    browser = init_browser()
    mars_info = {}

    #news
    
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_info["title"] = soup.find('div', class_="content_title").get_text()
    mars_info["body"] = soup.find('div', class_="rollover_description_inner").get_text()

    #feature image 
    
    feature_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(feature_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    for x in range(50):
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('a',class_="button fancybox")

    for article in articles:
        img= article['data-fancybox-href']
        featured_image_url= 'https://www.jpl.nasa.gov'+img

    mars_info["featured_image"] = featured_image_url

    #weather
    
    weather_url='https://twitter.com/marswxreport?lang=en'
    
    browser.visit(weather_url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    articles= soup.find_all('div', class_="js-tweet-text-container")
    for article in articles:
        mars_weather=article.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    

    #facts
    
    url_facts="https://space-facts.com/mars/"
    table = pd.read_html(url_facts)
    df = table[0]
    df.columns = ["Facts", "Value"]
    f_html = df.to_html()
    f_html = f_html.replace("\n"," ")
    mars_info["Facts"]=f_html

    

    #Mars Hemispheres
    hemisphere_image_urls = []
    
    url1 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url1)
    soup = BeautifulSoup (html, 'html.parser')
     
    for x in range(4): 
        time.sleep(5)
        hem_img = browser.find_by_tag('h3')
        hem_img[x].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        ars = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ ars
        dictionary={"title":img_title,"img_url":img_url}
        hemisphere_image_urls.append(dictionary)
        browser.back()
        mars_info["Hemispheres"]=hemisphere_image_urls

    return mars_info













    

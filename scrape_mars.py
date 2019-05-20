# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

#executable_path = {'executable_path': 'chromedriver.exe'}
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

mars_info = {}

# NASA NEWS
def scrape_mars_news():

        url_mars = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
        response_mars = requests.get(url_mars)

        soup_mars = BeautifulSoup(response_mars.text, 'html.parser')

        # Retrieve the latest element that contains news title and news_paragraph
        new_title = soup_mars.find('div', class_='content_title').find('a').text
        #new_p = soup_mars.find('div', class_="article_teaser_body").text

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = new_title
        #mars_info['news_paragraph'] = new_p

        return mars_info

# FEATURED IMAGE
def scrape_mars_image():

        # URL of Jet Propulsion Lab
        url_jet = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url_jet)

        html_jet = browser.html
        soup_jet = BeautifulSoup(html_jet, 'html.parser')

        # find the url of image
        featured_image_url = soup_jet.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Adding website url in front
        main_url = 'https://www.jpl.nasa.gov'
        featured_image_url = main_url + featured_image_url

        # Dictionary entry from FEATURED IMAGE
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info

# Mars Weather 
def scrape_mars_weather():

        # Visit Mars Weather Twitter through splinter module
        url_tw = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url_tw)

        html_tw = browser.html
        soup_tw = BeautifulSoup(html_tw, 'html.parser')

        mars_weather = soup_tw.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
        mars_weather = mars_weather.replace('pic.twitter.com/0Eqt9nN21o','')

        mars_info['mars_weather'] = mars_weather
        
        return mars_info

# Mars Facts
def scrape_mars_facts():

        url_fact = 'https://space-facts.com/mars/'
        browser.visit(url_fact)

        html_fact = browser.html
        soup_fact = BeautifulSoup(browser.html, 'html.parser')

        fact_table = soup_fact.find('table', class_='tablepress tablepress-id-mars')

        column1 = fact_table.find_all('td', class_='column-1')
        column2 = fact_table.find_all('td', class_='column-2')

        # Pick columns info into two list and make a table
        column1_list = []
        column2_list = []

        for row in column1:
            temp_col1 = row.text.strip()
            column1_list.append(temp_col1)

        for row in column2:
            temp_col2 = row.text.strip()
            column2_list.append(temp_col2)

        mars_fact_df = pd.DataFrame({
            "Fact": column1_list,
            "Answer": column2_list
        })

        mars_fact_html = mars_fact_df.to_html(header = True, index = False)

        mars_info['mars_facts'] = mars_fact_html

        return mars_info

# Mars Hemispheres
def scrape_mars_hemispheres():

        url_hp = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url_hp)

        html_hp = browser.html
        soup_hp = BeautifulSoup(html_hp, 'html.parser')

        # find all the info with mars hp 
        items = soup_hp.find_all('div', class_='item')
        main_url2 = 'https://astrogeology.usgs.gov'
        pic_url_list = []
        title_list = []

        # Loop through the items previously stored
        for item in items:
            title = item.find('h3').text  # title in h3
    
            link = item.find('a', class_='itemLink product-item')['href']
            temp_link = main_url2 + link
    
            #visit the link
            browser.visit(temp_link)
            temp_html_hp = browser.html
            #read the info through the temp link
            temp_soup_hp = BeautifulSoup(temp_html_hp, 'html.parser')
    
            #in each hp find the pic
            pic_url = temp_soup_hp.find('img', class_='wide-image')['src']    
            pic_url = main_url2 + pic_url
            #print(pic_url)
            pic_url_list.append({"title":title, "img_url":pic_url})

            mars_info['Hemispheres'] = pic_url_list

        return mars_info



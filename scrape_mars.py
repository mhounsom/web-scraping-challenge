from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import pymongo
import requests
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    mars_dic = {}


    #----------NASA Mars News----------
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    # Scrape page into Soup
    html = browser.html
    news_soup = bs(html, "html.parser")

    news_t = news_soup.find('div', class_='list_text')

    news_title = news_t.find('div', class_='content_title').text

    #get the latest paragraph text
    news_p = news_t.find('div', class_='article_teaser_body').text

    time.sleep(3)

    #----------JPL Mars Space Images - Featured Image----------
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    # Scrape page into Soup
    html = browser.html
    image_soup = bs(html, "html.parser")

    #find where the url is located
    carousel = image_soup.find('article', class_='carousel_item')

    img_url = carousel["style"]

    #take out crap
    img_url_nocrap = img_url.split("'")

    img_url_nocrap_real = img_url_nocrap[1]

    featured_image_url = f'https://www.jpl.nasa.gov{img_url_nocrap_real}'

    time.sleep(3)

    #----------Mars Weather----------
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    # Scrape page into Soup
    html = browser.html
    weather_soup = bs(html, "html.parser")

    mars_weather = weather_soup.find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")

    tweet_list = []

    for tweet in mars_weather:
        tweet_text = str(tweet.text)
        if tweet_text.startswith('InSight sol'):
            tweet_list.append(tweet_text)

    updated_mars_weather = tweet_list[0]

    time.sleep(3)

    #----------Mars Facts----------
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    # Scrape page into Soup
    html = browser.html

    table = pd.read_html(facts_url)

    mars_table = table[0]

    mars_table.columns = ["Description", "Value"]

    mars_table.set_index("Description", inplace=True)

    html_mars = mars_table.to_html()

    html_mars_cleaned = html_mars.replace('\n', '')

    time.sleep(3)

#----------Mars Hemispheres----------
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)

    # Scrape page into Soup
    html = browser.html
    hemi_soup = bs(html, "html.parser")

    all_hemis = hemi_soup.find('div', class_='collapsible results')

    ind_hemis = all_hemis.find_all('div', class_='item')

    hemis_urls = []

    for hemi in ind_hemis:
        title = hemi.find('h3').text
        title = title.replace("Enhanced", "")
        
        url_path = hemi.find('a')['href']
        hemi_img_url = f'https://astrogeology.usgs.gov/{url_path}'
        browser.visit(hemi_img_url)
        
        html = browser.html
        new_hemi_soup = bs(html, "html.parser")
        
        download = new_hemi_soup.find('div', class_='downloads')
        image_url = download.find('a')['href']
        
        hemis_urls.append({"title": title, "img_url": image_url})

    time.sleep(3)

#----------Mars Dictionary----------
    mars_dic = {'news_title': news_title,
            'news_p': news_p,
            'featured_image_url': featured_image_url,
            'updated_mars_weather': updated_mars_weather,
            'html_mars_cleaned': html_mars_cleaned,
            'hemis_urls': hemis_urls}

    browser.quit()

    return mars_dic


    



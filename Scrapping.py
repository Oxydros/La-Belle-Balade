#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 17:52:15 2019

@author: geoffreycideron
"""

from bs4 import BeautifulSoup
import urllib.request

#URL = "https://www.tripadvisor.com.au/Restaurants-g255068-c8-Brisbane_Brisbane_Region_Queensland.html"

def get_info(link):
    response = urllib.request.urlopen(link)
    soup = BeautifulSoup(response.read(),"lxml")
    for items in soup.find_all(class_="shortSellDetails"):
        name = items.find(class_="property_title").get_text(strip=True)
        bubble = items.find(class_="ui_bubble_rating").get("alt")
        review = items.find(class_="reviewCount").get_text(strip=True)
        print(name,bubble,review)

#URL = "https://www.tripadvisor.fr/Attraction_Review-g187147-d188757-Reviews-Louvre_Museum-Paris_Ile_de_France.html"
#URL = "https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html"
URL = "https://www.tripadvisor.fr/Attractions-g187147-Activities-c49-t28-Paris_Ile_de_France.html"
#URL = "https://www.tripadvisor.fr/Attractions-g187147-Activities-Paris_Ile_de_France.html"
if __name__ == '__main__':
    response = urllib.request.urlopen(URL)
    soup = BeautifulSoup(response.read(),"lxml")
    for items in soup.find_all(class_="rs"):
        bubble = items.find(name='span').get("alt")[:3]
        
        href = items.find(href=True)['href']
        #notation = float(item.find(class_="ui_bubble_rating").get("alt")[:1]) / 5
        print(bubble, href)
        

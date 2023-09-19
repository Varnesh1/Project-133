from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import csv

# NASA Exoplanet URL
START_URL = "https://r.search.yahoo.com/_ylt=AwrkMZRy7Allp8YAmjcM34lQ;_ylu=Y29sbwNpcjIEcG9zAzEEdnRpZAMEc2VjA3Nj/RV=2/RE=1695177971/RO=10/RU=https%3a%2f%2fen.wikipedia.org%2fwiki%2fDwarf_planet%23%3a~%3atext%3dA%2520dwarf%2520planet%2520is%2520a%2520small%2520planetary-mass%2520object%2cclassical%2520planets.%2520The%2520prototypical%2520dwarf%2520planet%2520is%2520Pluto./RK=2/RS=L8hlJV0Ow8MtTM1Lh6vwyx475H8-"

# Webdriver
browser = webdriver.Chrome()

time.sleep(10)

planets_data = []

headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", 
            "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]

def scrape():
    for i in range(1,5):
        while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "html.parser")

            # Check page number    
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))

            if current_page_num < i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break

        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            # Get Hyperlink Tag
            hyperlink_li_tag = li_tags[0]

            temp_list.append("https://exoplanets.nasa.gov"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            
            planets_data.append(temp_list)

        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

        print(f"Page {i} scraping completed")


# Calling Method
scrape()

new_planets_data = []

def scraper2(hyperlink):
    try: 
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, 'html.parser')
        templist = []
        for tr in soup.find_all('tr', attrs={'class':'fact_row'}):
            td = tr.find_all('td')
            for tdtag in td:
                try:
                     templist.append(tdtag.find_all('div', attrs= {'class':'value'})[0].contents[0])
                except: 
                    templist.append('')
        new_planets_data.append(templist)
    except: 
            time.sleep(1)
            scraper2(hyperlink)







#Calling method

for index, data in enumerate(planets_data):
    scraper2(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")

print(new_planets_data[0:10])

final_planet_data = []

for index, data in enumerate(planets_data):
    new_planet_data_element = new_planets_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data + new_planet_data_element)

with open("finalnumbertwo.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_planet_data)

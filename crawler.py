from bs4 import BeautifulSoup
import requests
import json
import pandas as pd


def scrape_post(post_url) -> tuple:
    print(post_url)
    page = BeautifulSoup(requests.get(post_url).text, "html.parser")
    page_content = json.loads(page.find('script', type='application/ld+json').text)
    return page_content["articleSection"], page_content["headline"], page_content["articleBody"]

base_domain = "https://www.smogon.com"
top_level = "https://www.smogon.com/forums/forums/ruins-of-alph.31/"
top_level_page = BeautifulSoup(requests.get(top_level).text, "html.parser")


data = []

for element in top_level_page.find_all(class_='node-title'):
    link = (element.find('a', href=True))['href']
    #recurse into forums
    new_page = BeautifulSoup(requests.get(base_domain + link).text, "html.parser")

    next = True

    while(next):
        for element in new_page.find_all(class_='structItem-title'):
            post_link = (element.find_all('a', href=True))

            try:
                article_section, headline, article_body = scrape_post(base_domain + post_link[1]['href'])
                data.append(
                    {
                        "article_section" : article_section,
                        "headline" : headline,
                        "article_body" : article_body
                    }
                )
            except:
                continue
        #Try to get next page
        next = new_page.find(class_='pageNav-jump pageNav-jump--next')
        if(next):
            new_page = BeautifulSoup(requests.get(base_domain + next['href']).text, "html.parser")

with open("data.csv", "w") as f:
    json.dump(data, f)

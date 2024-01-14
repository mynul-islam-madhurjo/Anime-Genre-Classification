from selenium.webdriver.common.by import By
from selenium import webdriver
from tqdm import tqdm
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
def is_valid_url(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

def scrape_anime_details(anime_url):
    try:

        if not is_valid_url(anime_url):
            print(f"Ignoring invalid URL: {anime_url}")
            return None

        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(anime_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        time.sleep(3)

        # Extracting titles
        title_name_element = soup.find('h1', class_='title-name')
        title_english_element = soup.find('p', class_='title-english')

        title_name = title_name_element.text.strip() if title_name_element else None
        title_english = title_english_element.text.strip() if title_english_element else None


        # Extracting score label
        score_label_element = soup.find('div', class_='score-label')
        score_label = score_label_element.text.strip() if score_label_element else None


        # Extracting description
        description_element = soup.find('p', itemprop='description')
        description = description_element.text.strip() if description_element else None

        # Extracting episodes, aired date, premiered
        details_elements = soup.find_all('div', class_='spaceit_pad')
        episodes, aired, premiered = None, None, None
        for detail_element in details_elements:
            detail_text = detail_element.text.strip()
            if "Episodes:" in detail_text:
                episodes = detail_text.split(":")[1].strip()
            elif "Aired:" in detail_text:
                aired = detail_text.split(":")[1].strip()
            elif "Premiered:" in detail_text:
                premiered = detail_element.find('a').text.strip()

        # Extracting genres
        genres_elements = soup.find_all('span', itemprop='genre')
        genres = [genre.text.strip() for genre in genres_elements]

        driver.quit()

        return {
            "title_name": title_name,
            "title_english": title_english,
            "url": anime_url,
            "score_label": score_label,
            "description": description,
            "episodes": episodes,
            "aired": aired,
            "premiered": premiered,
            "genres": genres
        }

    except Exception as e:
        print(f"Error scraping details for {anime_url}: {e}")
        return None

if __name__ == "__main__":
    df = pd.read_csv("Data/anime_multipage_details2.csv")
    anime_urls = df.URL.to_list()
    anime_data = []
    for anime_url in tqdm(anime_urls):
        time.sleep(3)
        details = scrape_anime_details(anime_url)
        if details:
            anime_data.append(details)
            time.sleep(3)

    time.sleep(3)
    df_details = pd.DataFrame(data=anime_data, columns=anime_data[0].keys())
    df_details.to_csv("Data/anime_genre_details.csv", index=False)

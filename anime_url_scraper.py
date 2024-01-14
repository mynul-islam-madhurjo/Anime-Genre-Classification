from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import json


def scrape_page(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    anime_listings = soup.find_all('tr', class_='ranking-list')

    # Initialize lists for data extraction
    ranks = []
    titles = []
    urls = []

    for anime_listing in anime_listings:
        # Extract data from each anime listing
        rank_element = anime_listing.find('td', class_='rank').find('span', class_='lightLink')
        rank = rank_element.text.strip() if rank_element else None
        ranks.append(rank)

        title_element = anime_listing.find('h3', class_='anime_ranking_h3').find('a')
        title = title_element.text.strip() if title_element else None
        titles.append(title)

        url = title_element['href'] if title_element else None
        urls.append(url)

    driver.quit()

    return ranks, titles, urls



def main():
    try:
        base_url = 'https://myanimelist.net/topanime.php?limit='
        page_number = 0
        data_list = []

        while True:
            url = f'{base_url}{page_number}'

            ranks, titles, urls = scrape_page(url)

            if not ranks:
                print(f"No more listings found on page {page_number}. Exiting loop.")
                break

            # Append data from this page to the list
            data = {
                'Rank': ranks,
                'Title': titles,
                'URL': urls,
            }

            data_list.append(data)

            page_number += 50

        # Concatenate all the data collected from different pages into a single DataFrame
        if data_list:
            final_data = {key: sum([d.get(key, []) for d in data_list], []) for key in data_list[0].keys()}
            df = pd.DataFrame(final_data)
            df.to_csv('Data/anime_multipage_details.csv', index=False)
        else:
            print("No data collected. Something went wrong.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

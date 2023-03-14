from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir=chrome_data/")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


def return_search_results(query_text):
    driver.get("https://twitter.com/explore")

    form = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "input"))
    )
    form.send_keys(query_text)
    form.submit()
    return driver


def find_tweets(driver, num_loops=10):
    all_tweets = []
    for _ in range(num_loops):
        bs = BeautifulSoup(driver.page_source)
        articles = bs.find_all("article")
        for article in articles:
            l = article.find_all("span")[4].parent.find_all("span")
            l = [i.text for i in l]
            tweet = "".join(l)
            if tweet not in all_tweets:
                all_tweets.append(tweet)
        driver.execute_script(f"window.scrollBy(0,5*window.innerHeight)")
    return all_tweets


def get_all_search_tweets(query_text):
    driver = return_search_results(query_text)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "article"))
    )
    return find_tweets(driver)


print(get_all_search_tweets("Silicon Valley Bank"))

import time
from urllib.parse import quote

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


def find_tweets(driver, num_loops=10):
    all_tweets = []
    for _ in range(num_loops):
        bs = BeautifulSoup(driver.page_source)
        articles = bs.find_all("article")
        for article in articles:
            l = article.find("div", {"data-testid": "tweetText"}).find_all("span")
            l = [i.text for i in l]
            tweet = "".join(l)
            if tweet not in all_tweets:
                all_tweets.append(tweet)
        driver.execute_script(f"window.scrollBy(0,5*window.innerHeight)")
    return all_tweets


def get_all_search_tweets(query_text):
    return_search_results(query_text)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "article"))
    )
    return find_tweets(driver)


def get_all_topics_from_trending(tab_name: str = "trending"):
    driver.get(f"https://twitter.com/explore/tabs/{tab_name}")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[aria-label='Timeline: Explore']")
        )
    )

    bs = BeautifulSoup(driver.page_source)
    all_relevant_queries = bs.find_all(
        "div", {"class": "css-1dbjc4n r-1adg3ll r-1ny4l3l"}
    )
    all_keywords = []
    for query in all_relevant_queries:
        l = query.find_all("span")
        if len(l) > 3:
            all_keywords.append(l[3].text.replace("\n", ""))
    return all_keywords


def get_all_tweets_for_trending_topic(topic):
    topic_url_save = quote(topic)
    url = (
        f"https://twitter.com/search?q={topic_url_save}&src=trend_click&vertical=trends"
    )
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "article"))
    )
    return find_tweets(driver)


def get_all_tweets_for_user(user_name):
    driver.get(f"https://twitter.com/{user_name}")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "article"))
    )
    return find_tweets(driver)


def generate_tweet_summary(tweets):
    tweet_list_concat = " ".join(tweets)
    prompt = f"Generate a 5 line summary of the following tweets: {tweet_list_concat}"
    # query  gpt3/chatgpt


def generate_tweet_summary_for_user(tweets, username):
    tweet_list_concat = " ".join(tweets)
    prompt = f"Generate a 5 line summary of the following tweets posted by {username}: {tweet_list_concat}"
    # query  gpt3/chatgpt


def generate_bio(tweets, username):
    tweet_list_concat = " ".join(tweets)
    prompt = f"Generate a twitter bio for {username} who has tweeted the following: {tweet_list_concat}"
    # query  gpt3/chatgpt


# all_topics = get_all_topics_from_trending()
# print(get_all_tweets_for_trending_topic(all_topics[1]))
# print(get_all_tweets_for_user("elonmusk"))

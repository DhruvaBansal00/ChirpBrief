from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def return_search_results(query_text):
    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir=chrome_data/")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://twitter.com/explore")

    form = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "input"))
    )
    form.send_keys(query_text)
    form.submit()
    return driver


# driver = return_search_results("Dhruva Bansal?")
# print(driver.page_source)

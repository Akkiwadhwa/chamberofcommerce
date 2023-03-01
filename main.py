import time
import requests
from selenium.webdriver.common import keys
from selenium.webdriver.support import expected_conditions as EC
import cloudscraper
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException

options = uc.ChromeOptions()
# options.add_argument('--headless')
driver = uc.Chrome(options=options)
driver.get("https://www.chamberofcommerce.com")
# data = scraper.get().text
# print(data)
data = driver.page_source
soup = BeautifulSoup(data, 'lxml')
a = soup.select(".col.my-1.fw-bold.text-primary")[0]
# for i in a:
href = a.find("a")["href"]
link = "https://www.chamberofcommerce.com" + href + "cities?mc=false"
driver.get(link)
data1 = driver.page_source
soup = BeautifulSoup(data1, 'lxml')
driver.quit()
cities = soup.select(".col-6.col-lg-3.mt-2")
for q in cities:
    city = q.find("a")["href"]
    link1 = "https://www.chamberofcommerce.com" + city + "?mc=false"
    print(link1)
    driver = uc.Chrome()
    driver.get(link1)
    data = driver.page_source
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/section[2]/div/div/div[2]/button")))
    driver.find_element(By.XPATH, "/html/body/main/section[2]/div/div/div[2]/button").send_keys(keys.Keys.ENTER)
    p = driver.find_element(By.CLASS_NAME,
                            "row.g-lg-5.py-3.px-3.px-lg-5.mt-4.dynamic-list.text-center.fwr-bold").find_elements(
        By.TAG_NAME, "h6")
    for cat in p:
        link2 = cat.find_element(By.TAG_NAME, "a").get_attribute("href")
        driver.get(link2)
        data2 = driver.page_source
        soup = BeautifulSoup(data2, 'lxml')
        s_cat = soup.select("col-6.fs-6.col-lg-4.mt-2")
        for u in s_cat:
            cat_href = q.find("a")["href"]
            link3 = "https://www.chamberofcommerce.com" + cat_href + "?mc=false"
            driver.get(link3)
            data3 = driver.page_source
            soup = BeautifulSoup(data3, 'lxml')
            s_cat = soup.select("col-6.fs-6.col-lg-4.mt-2")
            for y in s_cat:
                cat_href1 = y.find("a")["href"]
                link4 = "https://www.chamberofcommerce.com" + cat_href1 + "?mc=false"
                scraper = cloudscraper.create_scraper()
                data4 = scraper.get(link4).text
                soup = BeautifulSoup(data4, 'lxml')
                scrape = soup.find("PlaceListings").find_all("a")
                for s_link in scrape:
                    print(s_link["href"])

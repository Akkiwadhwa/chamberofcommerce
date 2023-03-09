import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import cfscrape
from tqdm import tqdm
from lxml import etree
import concurrent.futures
from fake_useragent import UserAgent

# from curl_cffi import requests


s = requests


def cfDecodeEmail(encodedString):
    r = int(encodedString[:2], 16)
    email = ''.join([chr(int(encodedString[i:i + 2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email


response1 = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=a670edd0-aa51-4ad8-a0e1-19e55c11b5a4')


# headers = {
#     "upgrade-insecure-requests": "1",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-site": "none",
#     "sec-fetch-mod": "",
#     "sec-fetch-user": "?1",
#     "accept-encoding": "gzip, deflate, br",
#     "accept-language": "bg-BG,bg;q=0.9,en-US;q=0.8,en;q=0.7"
# }
def header(link):
    # v = random.randint(0, 9)
    # headers = response1.json()['result'][v]
    ua = UserAgent()
    headers = {
        "upgrade-insecure-requests": "1",
        "user-agent": ua.random,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-site": "none",
        "sec-fetch-mod": "",
        "sec-fetch-user": "?1",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "bg-BG,bg;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    return headers


def scrape(x):
    city = x.find("a")["href"]
    link1 = "https://www.chamberofcommerce.com" + city + "?mc=false"
    headers = header(link1)
    data1 = s.get(link1, headers=headers).text
    soup = BeautifulSoup(data1, 'lxml')
    p = soup.select(".col-6.fs-6.col-lg-4.mt-2")
    li1 = [i.find("a")["href"] for i in p]
    for cat in li1:
        link2 = "https://www.chamberofcommerce.com" + cat + "?mc=false"
        headers = header(link2)
        data2 = s.get(link2, headers=headers).text
        soup = BeautifulSoup(data2, 'lxml')
        p = soup.select(".col-6.fs-6.col-lg-4.mt-2")
        li2 = [i.find("a")["href"] for i in p]
        for u in li2:
            link3 = "https://www.chamberofcommerce.com" + u + "?mc=false"
            headers = header(link3)
            data3 = s.get(link3, headers=headers).text
            soup = BeautifulSoup(data3, 'lxml')
            p = soup.select(".col-6.fs-6.col-lg-4.mt-2")
            li3 = [i.find("a")["href"] for i in p]
            for y in li3:
                for i in range(1, 100):
                    link4 = "https://www.chamberofcommerce.com" + y + f"?page={i}"
                    headers = header(link4)
                    data4 = s.get(link4, headers=headers).text
                    soup = BeautifulSoup(data4, 'lxml')
                    try:
                        s1 = soup.select_one(".fs-3.text-uppercase.mb-5.mt-0").text.strip()
                    except:
                        s1 = None

                    if s1 == "404 Error - This Search Page Does Not Exist":
                        d = random.randrange(0, 2)
                        h = random.randrange(1, 9)
                        print(f"{d}.{h}")
                        time.sleep(float(f"{d}.{h}"))
                        break
                    else:
                        scrape = soup.select(".card.white-card.card-hover-shadow.mb-2.p-3.p-lg-4.FeaturedPlacePreview")
                        li4 = [s_link["href"] for s_link in scrape]
                        for r in li4:
                            d = random.randrange(0, 4)
                            h = random.randrange(1, 9)
                            print(f"{d}.{h}")
                            time.sleep(float(f"{d}.{h}"))
                            t = ""
                            email = ""
                            link5 = "https://www.chamberofcommerce.com" + r
                            headers = header(link5)
                            # scraper = cfscrape.create_scraper()
                            # data5 = scraper.get(link5, headers=headers).content
                            data5 = s.get(link5, headers=headers).text
                            soup = BeautifulSoup(data5, 'html.parser')
                            name = soup.select_one(".fw-bold.fs-3.pe-lg-5").text.strip()
                            address = soup.select(".mb-2.mb-lg-3")[0].text.strip()
                            phone = soup.select(".mb-2.mb-lg-3")[1].text.strip()
                            desc = soup.select_one("#BusinessAbout").text.strip()
                            try:
                                d = soup.select_one(".ul-lh-lg.list-unstyled.fw-bold.text-dark").find_all("li")
                                for ipp in d:
                                    if ipp.text.strip() == "[email protected]" or "email" in ipp.text.strip():
                                        email1 = ipp.find("span")
                                        sdf = email1.find("a").find("span")["data-cfemail"]
                                        email = cfDecodeEmail(sdf)

                            except:
                                email = None
                            try:
                                tags = soup.select(".ul-lh-lg.list-unstyled.text-dark")[1].find_all("li")
                                for o in tags:
                                    t += o.text.strip() + ","
                            except:
                                t = None
                            dict1 = {
                                "Name": name,
                                "Address": address,
                                "Phone": phone,
                                "Description": desc,
                                "Email": email,
                                "Tags": t,
                                "Link": link5
                            }
                            print(dict1)
                            new_li.append(dict1)


headers = header("https://www.chamberofcommerce.com")
r = s.get("https://www.chamberofcommerce.com", headers=headers).text
soup = BeautifulSoup(r, 'lxml')
a = soup.select(".col.my-1.fw-bold.text-primary")[0]
# for i in a:
href = a.find("a")["href"]
link = "https://www.chamberofcommerce.com" + href + "cities?mc=false"
print(link)
headers = header(link)
data = s.get(link, headers=headers).text
soup = BeautifulSoup(data, 'lxml')
cities = soup.select(".col-6.col-lg-3.mt-2")
for u in cities:
    new_li = []
    scrape(u)
    df = pd.DataFrame(new_li)
    df.to_csv(f"{href.split('/')[-2].strip()}-{u.text}.csv")
    # df.to_csv(f"{href.split('/')[-2].strip()}.csv")

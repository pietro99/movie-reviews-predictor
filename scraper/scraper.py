import requests
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import math
class scraper():

    def __init__(self):
        self.scores = []
        self.reviews = []
        self.top_rated_url =  "https://www.imdb.com/chart/top?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=4da9d9a5-d299-43f2-9c53-f0efa18182cd&pf_rd_r=WYEXRCRZRBGNA8Y2034C&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=bottom&ref_=chtbtm_ql_3"


    def __loadMore__(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--log-level=3")
        driver = webdriver.Chrome(options=options, executable_path="./chromedriver.exe")
        driver.get(url)
        html = driver.page_source.encode('utf-8')
        page_num = 0

        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        reviewString = soup.find('div', {'class':'header'}).findChildren()[0].text
        reloads_num = math.floor(int(reviewString.strip("Reviews").replace(",", ""))/25)
        counter = 0

        while counter<reloads_num:
            driver.find_element_by_css_selector('#load-more-trigger').click()
            page_num += 1
            print("page number "+str(page_num)+" out of "+str(reloads_num))
            time.sleep(1)
            counter+=1
        return driver.page_source.encode('utf-8')   

    def __getReviews(self, links):
        for link in links:
            reviews_url = "https://www.imdb.com"+link+"reviews?ref_=tt_urv"
            content = self.__loadMore__(reviews_url)
            #content = requests.get(reviews_url)
            soup = BeautifulSoup(content, 'html.parser')
            ratings = soup.find_all("span", {"class": 'rating-other-user-rating'})
            reviews = soup.find_all("div", {"class": "text show-more__control"})
            for rating in ratings:
                self.scores.append(rating.find_all('span')[0].text)
            for review in reviews:
                self.reviews.append(review.text)
                
            for i in range(len(reviews)):
                print(self.scores[i])
                print()
                print(self.reviews[i])
                print()
                



    def scrapeTopRated(self):    
        content = requests.get(self.top_rated_url)
        soup = BeautifulSoup(content.text, 'html.parser')
        title_divs = soup.find_all(class_='titleColumn')
        movie_links = []
        for div in title_divs:
            movie_links.append(div.findChildren()[0].attrs['href'])
        self.__getReviews(movie_links)
        return #print(title_divs)
   
scraper = scraper()
scraper.scrapeTopRated()
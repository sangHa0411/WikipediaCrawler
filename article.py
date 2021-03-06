import re
import time
import random
import requests
from bs4 import BeautifulSoup

class UrlCrawler :
    def __init__(self, ) :
        self.prefix = 'https://ko.wikipedia.org'
    
    def get_links(self, url) :
        try :
            response = requests.get(url, timeout=10)
            sleep_time = random.uniform(0.001, 0.003)
            time.sleep(sleep_time)

            bs = BeautifulSoup(response.text, 'html.parser')

            links = bs.find_all('a', {'href' : re.compile('^(/wiki/)')})
            next_urls = [self.prefix + link['href'] for link in links]
            return list(set(next_urls))
        except TypeError :
            return None  

class ArticleCrawler :
    def __init__(self,) :
        pass 

    def get_text(self, url) :
        try :
            response = requests.get(url)
            sleep_time = random.uniform(0.001, 0.003)
            time.sleep(sleep_time)

            bs = BeautifulSoup(response.text, 'html.parser')
            passages = bs.find_all('p')

            if len(passages) <= 3 :
                return None

            title = bs.title.text
            texts = []
            passages = passages[1:]
            for p in passages :
                passage = re.sub('[\n\t]', '', p.text)
                texts.append(passage.strip())
            
            return {'title' : title, 'text' : '\n'.join(texts)}
            
        except TypeError :
            return None
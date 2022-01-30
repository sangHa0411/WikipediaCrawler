import os
import sys
import json
import parmap
import argparse
import pandas as pd
import multiprocessing

from queue import Queue
from article import UrlCrawler

def progressBar(que_size, set_size, depth):
    sys.stdout.write("\rQueue Size : {0} , Set Size : {1} , Depth :{2}".format(que_size, set_size, depth))
    sys.stdout.flush()

def get(args) :
    with open('./info/category.json', 'r') as f :
        category_data = json.load(f)

    data = category_data[args.category]
    
    que = Queue()
    for category in data : 
        name = 'https://ko.wikipedia.org/wiki/' + category
        que.put((name,0))

    depth = 0
    urls = set()
    crawler = UrlCrawler()
    while que.qsize() > 0 :
        progressBar(que.qsize(), len(urls), depth)
        try :
            url, depth = que.get()
        
            links = crawler.get_links(url)
            links = [link for link in links if link not in urls]

            if depth >= args.depth :
                break

            for link in links :
                que.put((link, depth+1))
               
            urls.update(links)
        except ConnectionError :
            continue

    print('\nSize of data : %d ' %len(urls))

    url_remains = []
    while que.qsize() > 0 :
        url, _ = que.get()
        url_remains.append(url)
    print('\nSize of remained data : %d' %len(url_remains))

    num_cores = multiprocessing.cpu_count()
    url_list = parmap.map(crawler.get_links, url_remains,  pm_pbar=True, pm_processes=num_cores) 
    url_list = sum(url_list, [])
    urls.update(url_list)
    print('\nSize of extracted data : %d' %len(url_list))

    urls = list(urls)
    print('\nTotal size of data : %d ' %len(urls))
    article_df = pd.DataFrame({'ID' : range(1, len(urls)+1), 'URL' : urls})

    info_path = os.path.join('./info', args.category) + '.csv'
    article_df.to_csv(info_path)

if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument('--depth', type=int, default=2, help='height of BFS algorithm (default: 2)')
    parser.add_argument('--category', type=str, default='academic', help='category of wikipedia articles')

    args = parser.parse_args()
    get(args)

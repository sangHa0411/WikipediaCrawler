import os
import re
import parmap
import argparse
import pandas as pd
import multiprocessing
from article import ArticleCrawler

def save_data(url, article_crawler, size) :
    data = article_crawler.get_text(url)

    if data is not None :
        title = data['title']
        text = data['text']

        if len(text) > size : 
            try : 
                path = os.path.join('./data', title) + '.txt'
                with open(path, 'w') as f :
                    f.write(text)
            except (OSError, FileNotFoundError):
                pass

def get(args) :
    article_df = pd.read_csv(args.file_path)
    article_data = list(article_df['URL'])
    print('Size of articles : %d' %len(article_data))

    article_crawler = ArticleCrawler()
    num_cores = multiprocessing.cpu_count()
    print('The number of Cores : %d \n' %num_cores)

    parmap.map(save_data, article_data, article_crawler, args.size, pm_pbar=True, pm_processes=num_cores) 
    
if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, default=200, help='minimum of text size (default: 200)')
    parser.add_argument('--file_path', type=str, default='./info/wikipedia.csv', help='wikipedia articles urls')

    args = parser.parse_args()
    get(args)
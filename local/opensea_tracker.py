"""
run example:

python3 opensea_tracker.py \
--check_collection True \
--collection_name boredapeyachtclub
"""

from argparse import ArgumentParser, Namespace
from pathlib import Path
import requests
import json
import cloudscraper
from local.duneanalytics import DuneAnalytics
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime
import pandas as pd
from scrapingant_client import ScrapingAntClient



def dump_json(df, filename: str):
    with open(filename, "w", encoding='utf-8') as json_file:
        json.dump(df, json_file, indent=4)
    return None


def collection_info(collection_name: str) -> dict:
    url = "https://api.opensea.io/api/v1/collection/{}".format(collection_name)
    response = requests.get(url, headers={"Accept": "application/json"})
    df = json.loads(response.text)
    return df


def save_collection(collection: str):
    dump_json(collection, ".collection_list.json")
    return None


def web_script(): 
    url = "https://opensea.io/rankings"
    scp = cloudscraper.create_scraper(
        browser={
            'browser': 'firefox',
            'platform': 'windows',
            'mobile': False
        }
    )
    html = scp.get(url).text

    # print(html)
    for i in range(1,50):
        # nft_name = html.split('"name":"')[i].split('"')[0]
        # print(nft_name)
        nft_slug = html.split('"slug":"')[i].split('"')[0]
        print(nft_slug)

    return None

def check_ranking(chek_num: int) -> list: 
    url = "https://opensea.io/rankings"
    scp = cloudscraper.create_scraper(
        browser={
            'browser': 'firefox',
            'platform': 'windows',
            'mobile': False
        }
    )
    html = scp.get(url).text

    str_list = []
    for i in range(1,chek_num):
        nft_name = html.split('"name":"')[i].split('"')[0]
        str_list.append(nft_name)

    return str_list


def get_top() -> list: 
    url = "https://opensea.io/rankings"
    scp = cloudscraper.create_scraper(
        browser={
            'browser': 'firefox',
            'platform': 'windows',
            'mobile': False
        }
    )
    html = scp.get(url).text

    collection_name = []
    for i in range(1,300):
        nft_slug = html.split('"slug":"')[i].split('"')[0]
        collection_name.append(nft_slug)

    return collection_name


def captureDune(url: str) -> pd:
    client = ScrapingAntClient(token='e0114a40337e49d2bf9f985e519c4a1a')
    result = client.general_request(
        url=url,
    ).content
    data = pd.read_html(result)
    return data


def today_summarize() -> dict:

    url = "https://dune.com/embeds/383744/731808/f8b9b2f8-e151-4228-b1fa-7beb90147201"
    data = captureDune(url)[0]

    idx = 0
    # "{:,}".format(data['nfts_sold'][idx])
    users = "{:,}".format(data['users'][idx])
    nfts_sold = "{:,}".format(data['nfts_sold'][idx])
    volume = data['volume'][idx]

    return {'users': users, 'nfts_sold': nfts_sold, 'volume': volume}


def main(args):
    if args.check_collection:
        df = collection_info(args.collection_name)
        # print(df['collection']['name'])
        dump_json(df, 'collection_info.json')
        dump_json(df['collection']['stats'], f'{args.collection_name}_info.json')
    
    if args.save_collection:
        collection_list = get_top()
        save_collection(collection_list)
    
    if args.capture_data:
        # web_script()
        # trading_volume()
        active_user()
        # today_summarize()

    return None


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--check_collection", type=bool, default=False)
    parser.add_argument("--save_collection", type=bool, default=False)
    parser.add_argument("--capture_data", type=bool, default=False)
    parser.add_argument("--collection_name", type=str, default=None)
    
    args = parser.parse_args()
    return args
    

if __name__ == "__main__":
    args = parse_args()
    main(args)
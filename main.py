import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import argparse

def shorten_link(long_link, access_token):
    headers = {
            "Authorization": "Bearer {}".format(access_token)
    }
    payload = {
        "url": long_link,
        "v": "5.199"
    }
    url = "https://api.vk.ru/method/utils.getShortLink"
    response = requests.post(url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()['response']['short_url']



def link_count(user_input, access_token):
    headers = {
            "Authorization": "Bearer {}".format(access_token)
    }
    
    payload = {
        "key": user_input,
        "v": "5.199",
        "interval": "forever",
        "extended": 0
    }
    url = "https://api.vk.com/method/utils.getLinkStats"
    response = requests.post(url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()["response"]["stats"]


def main():
    load_dotenv()
    access_token = os.environ["VK_TOKEN"]
    parser = argparse.ArgumentParser(description='Данный скрип позволяет сокращать длинные ссылки, а так же получать количество кликов по уже сокращенным ссылкам')
    parser.add_argument('url', type=str, help='Введите ссылку')
    args = parser.parse_args()
    parsed_url = urlparse(args.url)
    
    try:
        if parsed_url.netloc == "vk.cc" :
            print("Количество кликов:", link_count(parsed_url.path[1:], access_token)[0]['views'])
        else:
            short_link = shorten_link(args.url, access_token)
            print("Сокращенная ссылка:", short_link)

    except requests.exceptions.HTTPError:
        print("Проверьте Вашу ссылку и попробуйте снова")


if __name__ == "__main__":
    main()


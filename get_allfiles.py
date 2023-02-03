# main.py
import json
import time

import requests
from playwright.sync_api import sync_playwright
from pygtrans import Translate


def get_all_urls(url):
    download_urls = []
    fns = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        # parse_item(page.content())
        down = page.locator("//a[contains(text(),'Download Part')]")
        print(
            page.locator("h2").first.inner_text(),
        )
        # 英语翻译中文
        the_v = page.locator("h2").first.inner_text()
        client = Translate()
        t_text = client.translate(the_v)
        print(t_text.translatedText)  # 谷歌翻译
        for text in down.all_inner_texts():
            download_urls.append(
                page.locator("//a[contains(text(),'{}')]".format(text)).get_attribute(
                    "href"
                )
            )
            fns.append("" + text)
    return download_urls

def main(url):
    print(get_all_urls(url))


def download_url(args):
    t0 = time.time()
    url, fn = args[0], args[1]
    try:
        r = requests.get(url)
        with open(fn, "wb") as f:
            f.write(r.content)
        return (url, time.time() - t0)
    except Exception as e:
        print("Exception in download_url():", e)


if __name__ == "__main__":
    url = "https://downloadly.net/2023/02/91199/02/nft-investing-masterclass-pro-tips-about-nft-investing/14/?#/91199-udemy-182304021602.html"
    main(url)
    # inputs = zip(urls, fns)
    # t0 = time.time()
    # for i in inputs:
    #     result = download_url(i)
    #     print('url:', result[0], 'time:', result[1])
    # print('Total time:', time.time() - t0)

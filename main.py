# -*- coding: utf-8 -*-
import time
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import pandas as pd
import os





def get_all_pages():
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36 "
    }

    r = requests.get(url="https://www.foxtrot.com.ua/ru/shop/led_televizory.html", headers=headers)

    if not os.path.exists("data"):
        os.mkdir("data")

    with open("data/page_1.html", "w", encoding="UTF-8") as file:
        file.write(r.text)

    with open("data/page_1.html", encoding="UTF-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    pages_count = int(soup.find("nav", class_="listing__pagination").find_all("a")[-2].text)

    for i in range(1, pages_count +  1):
        url = f"https://www.foxtrot.com.ua/ru/shop/led_televizory.html?page={i}"

        r = requests.get(url=url, headers=headers)

        with open(f"data/page_{i}.html", "w", encoding="UTF-8") as file:
            file.write(r.text)

        time.sleep(2)

    return pages_count + 1


def collect_data(pages_count):
    cur_date = datetime.now().strftime("%d_%m_%Y")

    # with open(f"data_{cur_date}.csv", "w") as file:
    #     writer = csv.writer(file)
    #     writer.writerow(
    #         (
    #             "Model"
    #             "Price"
    #             "Url"
    #         )
    #     )



    data = []
    for page in range(1, pages_count):
                with open(f"data/page_{page}.html", encoding="UTF-8") as file:
                    src = file.read()

                soup = BeautifulSoup(src, "lxml")
                items_card = soup.find_all("div", class_="card__body")


                for item in items_card:
                    Model = item.find("a", class_="card__title").text.strip().split(" ")
                    Price = item.find("div", class_="card-price").text.replace("₴", "").replace(" ", "").replace("\n", "")
                    Lnk = item.find("div", class_="card-comment__title").get("href")
                    Url = f'https://www.foxtrot.com.ua{Lnk}'
                    Row = Model[1:], Price, Url
                    data.append(Row)
                    print(Row)



                    # data.append(
                    # {
                    #     "Model": Model,
                    #     "Price": Price,
                    #     "URL": Url
                    # }
                    #  )
                    # with open(f"data_{cur_date}.csv", "a") as file:
                    #     writer = csv.writer(file)
                    #     writer.writerow(
                    #         (
                    #             Model,
                    #             Price,
                    #             Url
                    #         )
                    #     )

    print(f"[INFO] Обработана страница {page} /11 ")

    with open(f"data_{cur_date}.json", "a", encoding="UTF-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    df = pd.DataFrame(data, columns=['Model', 'Price', 'URL'])
    df.to_csv(f'data_{cur_date}.csv', index=False, sep=';', encoding='utf-8')

def main():
    pages_count_2 = get_all_pages()
    collect_data(pages_count=pages_count_2)


if __name__ == '__main__':
    main()


import requests
from bs4 import BeautifulSoup
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import time
import schedule


def job():
    REQUEST_URL = 'https://travel.rakuten.co.jp/yado/okinawa/nahashi.html'
    res = requests.get(REQUEST_URL)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, "html.parser")
    hotel_section_from_html = soup.select('section')

    hotel_section = []
    for hs in hotel_section_from_html:
        a = hs.select_one('p.area')
        if (a != None):
            hotel_section.append(hs)

    hotelName = []
    hotelMinCharge = []
    reviewAverage = []
    hotel_locate = []
    for hs in hotel_section:
        hs1 = hs.select_one('h1 a').text
        if (hs.select_one('p.htlPrice span') != None):
            hs2 = hs.select_one('p.htlPrice span').text.replace(
                "円〜", "").replace(",", "")
        else:
            hs2 = -1
        hs3 = hs.select_one('p.cstmrEvl strong').text
        hs4 = hs.select_one('p.htlAccess').text.replace("\n", "").replace(
            " ", "").replace("[地図を見る]", "").replace("　", "")
        hotelName.append(hs1)
        hotelMinCharge.append(hs2)
        reviewAverage.append(hs3)
        hotel_locate.append(hs4)

    data_list = {
        "hotelName": hotelName,
        "hotelMinCharge": hotelMinCharge,
        "reviewAverage": reviewAverage,
        "hotel_locate": hotel_locate,
    }

    df = pd.DataFrame(data_list)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    # ここまでスクレイピング

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = Credentials.from_service_account_file(
        'service_account.json',
        scopes=scopes
    )
    gc = gspread.authorize(credentials)

    SP_SHEET_KEY = '1a-lk8e9ZdDt23qkvvd4UCMNJh6nuLV3IH1bvhnS5x24'
    sh = gc.open_by_key(SP_SHEET_KEY)
    SP_SHEET = 'sample'
    worksheet = sh.worksheet(SP_SHEET)
    data = worksheet.get_all_values()
    df_old = pd.DataFrame(data[1:], columns=data[0])
    df_new = df
    df_upload = pd.concat([df_old, df_new])
    df_upload.reset_index(drop=True, inplace=True)
    set_with_dataframe(sh.worksheet("sample"), df_upload, include_index=False)


schedule.clear()
schedule.every().day.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

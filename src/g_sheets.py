# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import zvz


def AddNewZVZ(sheet_name, items_data, players_data):

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'cred.json', scope)
    gc = gspread.authorize(credentials)

    sp = gc.open('ZVZ')
    worksheet = sp.add_worksheet(title=sheet_name, rows="100", cols="20")

    worksheet.update_acell('A1', "Item resmi")
    worksheet.update_acell('B1', "Item ismi")
    worksheet.update_acell('C1', "Item adeti")
    worksheet.update_acell('D1', "Market degeri (Caerleon)")

    i = 2
    for item in items_data:

        print(f"[Sheets] Adding {item[0]}...")

        img_url = f'=IMAGE("https://gameinfo.albiononline.com/api/gameinfo/items/{item[0]}.png")'
        item_price = zvz.GetItemPrice(item[0], item[1])
        worksheet.update_cell(i, 1, img_url)
        worksheet.update_cell(i, 2, item[0])
        worksheet.update_cell(i, 3, item[1])
        worksheet.update_cell(i, 4, item_price)

        i += 1

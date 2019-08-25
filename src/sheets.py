# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import datetime
from datetime import timezone

import xlsxwriter
import zvz


def CreateZVZSheet(sheet_name, items_data, players_data, killboard_links):

    wb = xlsxwriter.Workbook(f'sheets/{sheet_name}.xlsx')
    ws = wb.add_worksheet(sheet_name)

    local_time = datetime.datetime.now()
    tr_time = local_time + datetime.timedelta(hours=1)
    tr_time_str = tr_time.strftime("%d/%m/%Y, %H:%M:%S")

    ws.write(0, 0, "Tarih")
    ws.write(1, 0, tr_time_str)
    ws.write(0, 1, "ItemFoto")
    ws.write(0, 2, "ItemIsmi")
    ws.write(0, 3, "ItemAdeti")
    ws.write(0, 4, "MarketDegeri(Caerleon)")
    ws.write(0, 7, "KillboardLinkleri")

    killboard_links.reverse()
    i = 2
    for link in killboard_links:
        ws.write(i, 7, players_data[i-2]['Player'])
        ws.write(i, 8, link)
        i+=1

    i = 2
    total_price = 0
    for item in items_data:

        print(f"[ZVZ Sheet] Adding {item[0]}")

        img_url = f'=IMAGE("https://gameinfo.albiononline.com/api/gameinfo/items/{item[0]}.png")'
        item_price = zvz.GetItemPrice(item[0], item[1])
        total_price += item_price

        ws.write(i, 1, img_url)
        ws.write(i, 2, item[0])
        ws.write(i, 3, item[1])
        ws.write(i, 4, item_price)

        i += 1
        
    ws.write(1, 4, f"Toplam : {total_price}")
    wb.close()

    return True, {"date": tr_time_str, "total_price": total_price}

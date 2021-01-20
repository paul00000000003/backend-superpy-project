import csv
from datetime import date, datetime, timedelta
import sys
import os


def process_sell_instruction(args, dates):
    items_to_be_sold = []
    # verzamel inventaris (kan hier nog bedorven zijn)
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_item = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_item:
                if row[0].isdigit():
                    price = float(row[3].replace(",", "."))
                    if len(row[2]) == 7:
                        row[2] = "0"+row[2]
                    if len(row[4]) == 7:
                        row[4] = "0"+row[4]
                    items_to_be_sold.append({"id": int(row[0]),
                                             "product_name": row[1],
                                             "buy_date": datetime.strptime(row[2], '%d%m%Y'),
                                             "buy_price": price,
                                             "expiration_date": datetime.strptime(row[4], '%d%m%Y'),
                                             "sold": row[5]})
        csvfile.close()
    except:
        None
    item_found = "N"
    bought_id = 0
    index = -1
    index_found = -1
    # zoek match tussen verkoopopdracht en aanwezige inventaris die nog niet is bedorven. Het oudste product wordt het eerst verkocht
    for item in items_to_be_sold:
        index = index+1
        if (item["product_name"] == args.product_name and item["expiration_date"] >= dates.today and item["sold"] == "N" and item_found == "N"):
            index_found = index
            item_found = "Y"
            bought_id = item["id"]
            bought_price = item["buy_price"]
            product_name = item["product_name"]
    # zet betrokken product in aankoopfile op verkocht. Dit vergemakkelijkt het als je deze functie opnieuw draait
    if index_found != -1:
        # vullen met verkoopdatum om referentie te houden voor andere soorten rapportage
        items_to_be_sold[index_found]["sold"] = dates.today_str
    with open('./bought.csv', 'w', newline='') as csvfile:
        bought_items = csv.writer(csvfile, delimiter=';',
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in items_to_be_sold:
            bought_items.writerow(
                [str(item["id"])]+[item["product_name"]]+[item["buy_date"].strftime("%d%m%Y")]+[str(item["buy_price"]).replace(".", ",")] +
                [item["expiration_date"].strftime("%d%m%Y")]+[item["sold"]])
    csvfile.close()

    if bought_id == 0:
        return False
    else:
        max_id = 0
        # bepaal hoogst aanwezige id in de verkopen. Normaliter doe je dat overigens aan de hand van een record in de database
        try:
            with open('./sold.csv', newline='') as csvfile:
                sold_item = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in sold_item:
                    if row[0].isdigit():
                        if int(row[0]) > max_id:
                            max_id = int(row[0])
            csvfile.close()
        except:
            None
        max_id = max_id+1
        # voeg record toe aan de verkoopfile
        with open('./sold.csv', 'a', newline='') as csvfile:
            sold_items = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            sold_items.writerow(
                [str(max_id)]+[str(bought_id)]+[product_name]+[dates.today_str]+[]+[str(args.price).replace(".", ",")]+[str(bought_price).replace(".", ",")])
        csvfile.close()
        return True

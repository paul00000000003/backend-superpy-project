# Imports
from process_stats_function import process_stats
from make_report_function import make_report_profit, make_report_inventory, make_report_revenue
from sold_function import process_sell_instruction
import argparse
import csv
from datetime import date, datetime, timedelta
import sys
import os
from types import SimpleNamespace as Namespace

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

# Your code below this line.


class setDates:
    def __init__(self, day):
        self.today = day
        self.yesterday = self.today+timedelta(days=-1)
        self.fortnight_day = self.today+timedelta(days=2)
        self.tomorrow = self.today+timedelta(days=1)
        self.today_str = self.today.strftime("%d%m%Y")
        self.yesterday_str = self.yesterday.strftime("%d%m%Y")
        self.tomorrow_str = self.tomorrow.strftime("%d%m%Y")
        self.fortnight_day_str = self.fortnight_day.strftime('%d%m%Y')


def parser_():
    parser = argparse.ArgumentParser(add_help=False)
    subparser = parser.add_subparsers(dest='command')
    buy = subparser.add_parser('buy')
    buy.add_argument("--product-name", type=str)
    buy.add_argument("--price", type=float)
    buy.add_argument("--expiration-date", type=str)
    sell = subparser.add_parser('sell')
    sell.add_argument("--product-name", type=str)
    sell.add_argument("--price", type=float)
    report = subparser.add_parser("report")
    subparser_subdivided = report.add_subparsers(dest="command")
    inventory = subparser_subdivided.add_parser("inventory")
    inventory.add_argument("--now", action="store_true")
    inventory.add_argument("--yesterday", action="store_true")
    inventory.add_argument("--date", type=str)
    revenue = subparser_subdivided.add_parser("revenue")
    revenue.add_argument("--yesterday", action="store_true")
    revenue.add_argument("--today", action="store_true")
    revenue.add_argument("--date", type=str)
    profit = subparser_subdivided.add_parser("profit")
    profit.add_argument("--yesterday", action="store_true")
    profit.add_argument("--today", action="store_true")
    profit.add_argument("--date", type=str)
    parser.add_argument("--advance-time", type=int)
    parser.add_argument("-h", action="store_true")
    parser.add_argument("--help", action="store_true")
    stats = subparser.add_parser("stats")
    stats.add_argument("--product-name", type=str)
    stats.add_argument("--start-date", type=str)
    stats.add_argument("--end-date", type=str)
    stats.add_argument("--number", action="store_true")
    stats.add_argument("--buy-price", action="store_true")
    stats.add_argument("--sell-price", action="store_true")
    stats.add_argument("--profit", action="store_true")
    stats.add_argument("--revenue", action="store_true")
    return parser.parse_args()


def get_referred_date(shift_number_of_days=0):
    # Met deze functie kan de datum een dag worden verzet. Hiervoor wordt een file gebruikt omdat
    # we nog geen link met sql hebben. Het wegschrijfformaat is hetzelfde als hetgeen wordt ingelezen.
    f_get_date = None
    date_validated = "N"
    try:
        f = open('./referred-date.txt', 'r')
        date_line = f.readline().lstrip()[0:10]
        f_get_date = datetime.strptime(date_line, '%d%m%Y')
        f.close()
    except:
        this_moment = datetime.now()
        this_moment_str = this_moment.strftime("%d%m%Y")
        f_get_date = datetime.strptime(this_moment_str, "%d%m%Y")
    if shift_number_of_days != 0:
        f_get_date = f_get_date+timedelta(shift_number_of_days)
    f = open('./referred-date.txt', 'w')
    f.write(f_get_date.strftime("%d%m%Y"))
    f.close()
    date_validated = "Y"
    return f_get_date, date_validated


def process_buy_instruction(args, dates):
    # Bij aanvang hoeft nog niets gekocht te zijn. Omdat we het id uniek willen houden moeten we bij een buy instructie kijken welke id's al zijn gevuld
    # Beetje dure operatie maar volgens mij noodzakelijk. Een van de zaken waar hier geen rekening mee wordt gehouden is als het programma 2 keer
    # tegelijk wordt gedraaid. Aangezien er niet van een database gebruik wordt gemaakt, kan dat probleem volgens mij niet worden voorkomen tenzij we bv dezelfde
    # file gebruiken die we voor de datum gebruiken
    max_id = 0
    success = False
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_item = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_item:
                if row[0].isdigit():
                    if int(row[0]) > max_id:
                        max_id = int(row[0])
        csvfile.close()
    except:
        None

    # bij de onderstaande opening van de file voegen we een regel toe en daarom gebruiken we de a voor append
    max_id = max_id+1
    with open('./bought.csv', 'a', newline='') as csvfile:
        bought_item = csv.writer(csvfile, delimiter=';',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        expiration_date = datetime.strptime(args.expiration_date, "%Y-%m-%d")
        if max_id != 0:
            bought_item.writerow([str(max_id)]+[args.product_name]+[dates.today_str] +
                                 [str(args.price).replace('.', ',')] + [expiration_date.strftime("%d%m%Y")]+["N"])
            success = True
    csvfile.close()
    return success


def get_sell_data(start_date, end_date):
    sold_items = []
    total_amount_sold = 0
    try:
        with open('./sold.csv', newline='') as csvfile:
            sold_items_source = csv.reader(
                csvfile, delimiter=';', quotechar='|')
            for row in sold_items_source:
                if row[0].isdigit():
                    if len(row[3]) == 7:
                        row[3] = "0"+row[3]
                    sell_date = datetime.strptime(row[3], "%d%m%Y")
                    if (sell_date >= start_date and sell_date <= end_date):
                        total_amount_sold = total_amount_sold + \
                            float(row[4].replace(",", "."))
                        sold_items.append({"id": row[0],
                                           "buy_id": row[1],
                                           "product_name": row[2],
                                           "sell_price": float(row[4].replace(',', '.')),
                                           "sell_date": sell_date,
                                           "buy_price": float(row[5].replace(',', '.'))})
        csvfile.close()
    except:
        None
    return sold_items, total_amount_sold


def report_inventory_data_and_report(ref_date):
    # de voorraad wordt altijd op een datum weergegeven. De voorraad is gelijk aan hetgeen er is
    # gekocht maar nog niet is verkocht en nog niet is bedorven. Hetgeen is bedorven behoort dus niet tot de voorraad
    # De voorraad wordt bepaald op de aangegeven dag vlak voor dat de winkel open gaat

    # het formaat van inventoryData wordt b.v. { brood : {"10032021":10,"11032021:3"},melk :{"20012021":3,"27012021:4}} enz
    inventoryData = {}
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_item = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_item:
                if row[0].isdigit():
                    # als je het spreadsheet opent en de dag is kleiner dan 10, wordt er maar 1 karakter voor de dag gebruikt
                    if len(row[2]) == 7:
                        # terwijl je er 2 voor nodig hebt, anders gaat de conversie niet goed
                        row[2] = "0" + row[2]
                    if len(row[4]) == 7:
                        row[4] = "0"+row[4]
                    if (datetime.strptime(row[2], "%d%m%Y") < ref_date and
                            datetime.strptime(row[4], "%d%m%Y") > ref_date):
                        checkSell = 'N'  # om het produkt op een bepaalde datum op voorraad te hebben moet het of niet verkocht zijn dan
                        # wel pas op een later tijdstip dan het controlemoment voor de voorraad ('s ochtends voor openingstijd)
                        if row[5] == "N":
                            checkSell = "Y"
                        else:
                            if len(row[5]) == 7:
                                row[5] = '0'+row[5]
                            if datetime.strptime(row[5], "%d%m%Y") >= ref_date:
                                checkSell = "Y"
                        if checkSell == "Y":
                            if row[1] in inventoryData:
                                if row[4] in inventoryData[row[1]]:
                                    if row[3].replace(',', '.') in inventoryData[row[1]][row[4]]:
                                        inventoryData[row[1]][row[4]][row[3].replace(",", ".")
                                                                      ] = inventoryData[row[1]][row[4]][row[3].replace(",", ".")]+1
                                    else:
                                        inventoryData[row[1]
                                                      ][row[4]][row[3].replace(",", ".")] = 1
                                else:
                                    inventoryData[row[1]][row[4]] = {}
                                    inventoryData[row[1]][row[4]
                                                          ][row[3].replace(",", ".")] = 1
                            else:
                                inventoryData[row[1]] = {}
                                inventoryData[row[1]][row[4]] = {}
                                inventoryData[row[1]][row[4]
                                                      ][row[3].replace(",", ".")] = 1
        csvfile.close()
    except:
        print("the file bought.csv couldn't be opened")
    make_report_inventory(inventoryData, ref_date)


def report_revenue_data_and_report(start_date, end_date):
    sellData = []
    sellData, total_amount_sold = get_sell_data(start_date, end_date)
    make_report_revenue(sellData, total_amount_sold, start_date, end_date)


def report_profit_data_and_report(start_date, end_date):
    # revenue = omzet van een dag : totale verkoop - totaal gekocht op die dag - hetgeen er die dag is bedorven en nog niet verkocht
    # en niet op diezelfde dag is gekocht
    purchased_items = []
    expired_items = []
    sold_items = []
    total_amount_sold = 0
    total_amount_bought = 0
    total_amount_perished = 0
    sold_items, total_amount_sold = get_sell_data(start_date, end_date)
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_item = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_item:
                if row[0].isdigit():
                    # als je het spreadsheet opent en de dag is kleiner dan 10, wordt er maar 1 karakter voor de dag gebruikt
                    # terwijl je er 2 voor nodig hebt, anders gaat de conversie niet goed
                    if len(row[2]) == 7:
                        row[2] = "0"+row[2]
                    if len(row[4]) == 7:
                        row[4] = "0"+row[4]
                    buy_date = datetime.strptime(row[2], "%d%m%Y")
                    if (buy_date >= start_date and buy_date <= end_date):
                        purchased_items.append({"id": row[0],
                                                "product_name": row[1],
                                                "price": float(row[3].replace(",", ".")),
                                                "buy_date": buy_date,
                                                "expiration_date": datetime.strptime(row[4], '%d%m%Y'),
                                                "sold ": row[5]})
                        total_amount_bought = total_amount_bought + \
                            float(row[3].replace(",", "."))
                    else:
                        checkSell = 'N'  # het produkt gaat alleen verloren als de houdbaarheidsdatum verstreken is en het dan nog niet is verkocht
                        if row[5] == "N":
                            checkSell = "Y"
                        else:
                            if len(row[5]) == 7:
                                row[5] = '0'+row[5]
                            sell_date = datetime.strptime(row[5], "%d%m%Y")
                            if sell_date <= end_date and sell_date >= start_date:
                                checkSell = "Y"
                        if checkSell == "Y":
                            expiration_date = datetime.strptime(
                                row[4], '%d%m%Y')
                            if (expiration_date >= start_date and expiration_date <= end_date):
                                total_amount_perished = total_amount_perished + \
                                    float(row[3].replace(",", "."))
                                expired_items.append({"id": row[0],
                                                      "product_name": row[1],
                                                      "price": float(row[3].replace(",", ".")),
                                                      "buy_date": datetime.strptime(row[2], '%d%m%Y'),
                                                      "expiration_date": expiration_date,
                                                      "sold ": row[5]})

        csvfile.close()
    except:
        None
    make_report_profit(sold_items, purchased_items, expired_items,
                       total_amount_sold, total_amount_bought, total_amount_perished, start_date, end_date)
    # os.system("help.md")


def call_on_report(args, called_report, dates, ref_today, subparse_version):
    if ref_today == True:
        if subparse_version == "inventory":
            called_report(dates.today)
        else:
            called_report(dates.today, dates.today)
    elif args.yesterday == True:
        if subparse_version == "inventory":
            called_report(dates.yesterday)
        else:
            called_report(dates.yesterday, dates.yesterday)
    else:
        if subparse_version == "inventory":
            date_approved = "Y"
            try:
                date_approved = "N"
                ref_date = datetime.strptime(args.date, "%Y-%m-%d")
                date_approved = "Y"
            except:
                print("Date should have the format yyyy-mm-dd")
            if date_approved == "Y":
                called_report(ref_date)
        else:
            date_range_approved = "N"
            try:
                month = datetime.strptime(args.date, '%Y-%m')
                start_date_str = month.strftime("%Y%m")+'01'
                start_date = datetime.strptime(start_date_str, '%Y%m%d')
                end_date = start_date
                end_date = end_date.replace(day=28)
                end_date = end_date+timedelta(days=4)
                end_date = end_date-timedelta(days=end_date.day)
                date_range_approved = "Y"
            except:
                print("date is not a month in yyyy-mm format")
            if date_range_approved == "Y":
                called_report(start_date, end_date)


def main():
    args = parser_()
    if isinstance(args.command, str):
        subparse_version = args.command
    else:
        subparse_version = ""
    if args.advance_time:
        referred_date, date_validated = get_referred_date(args.advance_time)
        if date_validated == "Y":
            print("OK")
        else:
            print("NOK")
    else:
        referred_date, date_validated = get_referred_date()
    if args.h == True or args.help == True:
        print(
            "The number of arguments which can be accepted by this program is fairly large.")
        print("Hence I strongly recommend the user of this program to read the word document 'functional specification for superpy.py.docx' ")
        print("in order to gain a fundamental understanding of the functionality and the outcomes which are perceived")
    dates = setDates(referred_date)
    if subparse_version == "buy":
        buy = process_buy_instruction(args, dates)
        if buy == True:
            print("OK")
        else:
            print("NOK")
    elif subparse_version == "sell":
        sell = process_sell_instruction(args, dates)
        if sell == True:
            print("Ok")
        else:
            print("ERROR. Product not in stock")
    if subparse_version == "profit":
        call_on_report(args, report_profit_data_and_report,
                       dates, args.today, subparse_version)

    if subparse_version == "revenue":
        call_on_report(args, report_revenue_data_and_report,
                       dates, args.today, subparse_version)

    if subparse_version == "inventory":
        call_on_report(args, report_inventory_data_and_report,
                       dates, args.now, subparse_version)
    if subparse_version == "stats":
        process_stats(args, dates)


if __name__ == '__main__':
    main()

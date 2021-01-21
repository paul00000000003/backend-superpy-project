from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import csv


def make_stats_graph(type_of_plot, data_dict, x_label, y_label, title, start_date, end_date):
    # plt.plot(data_dict.keys(), data_dict.values())
    if len(data_dict.keys()) <= 1 and type_of_plot == "line":
        print("ERROR. Can not draw a line with 1 or 0 data")
    else:
        plt.figure(figsize=(15, 6))  # breedte, hoogte van de grafiek
        if type_of_plot == "bar":
            plt.bar(data_dict.keys(), data_dict.values(), width=1,
                    color='green')  # width : breedte staaf in diagram
        else:
            # om ipv barchart linechart te maken. Doe ik voor profit (ziet er wat beter uit)
            plt.plot(data_dict.keys(), data_dict.values())
        plt.xlim(start_date, end_date)  # Set the visible limits of the x axis.
        min_value = min(data_dict.values())
        max_value = max(data_dict.values())
        if min_value < 0:
            min_value_yaxis = 1.2*min_value
        else:
            min_value_yaxis = 0.8*min_value
        if max_value < 0:
            max_value_yaxis = 0.8*max_value
        else:
            max_value_yaxis = 1.2*max_value
        plt.ylim(min_value_yaxis, max_value_yaxis)
        plt.xlabel(x_label)
        # plt.yaxis.set_major_formatter(str(y).replace(".",","))
        plt.ylabel(y_label)
        plt.title(title)
        plt.show()


def is_float(string):
    # algemene toepassing om te kijken of string een float bevat
    # misschien een beetje flauw omdat je een standaard functie zou willen gebruiken maar ok
    # wellicht zou die niet veel meer doen dan dit
    try:
        return float(string) and '.' in string
    except ValueError:
        return False


def is_integer(string):
    # in dit geval kan het ook met str.isdigit(), maar het float alternatief ken ik niet.
    try:
        return int(string)
    except ValueError:
        return False


def get_revenue_dict(start_date, end_date, product_name):
    revenue_dict = {}
    try:
        with open('./sold.csv', newline='') as csvfile:
            sold_items = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in sold_items:
                if row[0].isdigit():
                    # als je het spreadsheet opent en de dag is kleiner dan 10, wordt er maar 1 karakter voor de dag gebruikt
                    if len(row[3]) == 7:
                        # terwijl je er 2 voor nodig hebt, anders gaat de conversie niet goed
                        row[3] = "0" + row[3]
                    sell_date = datetime.strptime(row[3], "%d%m%Y")
                    if sell_date >= start_date and sell_date <= end_date and product_name == row[2]:
                        if is_float(row[4].replace(",", ".")):
                            if sell_date in revenue_dict:
                                revenue_dict[sell_date] = revenue_dict[sell_date] + \
                                    float(row[4].replace(",", "."))
                            else:
                                revenue_dict[sell_date] = float(
                                    row[4].replace(",", "."))
                        else:
                            print("{row[4]} is geen getal met een punt")
    except:
        print("file sold.csv kon niet worden geopend. ")
    return revenue_dict


def compute_avg_prices(mult_prices):
    avg_prices_dict = {}
    for k, v in mult_prices.items():
        date = k
        tot_number = 0
        tot_value = 0
        if isinstance(v, dict):
            value = v
            tot_number = 0
            tot_value = 0
            for k, v in value.items():
                if is_float(k):
                    tot_number = tot_number+v
                    price_number = float(k)
                    tot_value = tot_value+price_number*v
                elif is_integer(k):
                    tot_number = tot_number+v
                    price_number = int(k)
                    tot_value = tot_value+price_number*v
        if tot_number != 0:
            avg_prices_dict[date] = tot_value/tot_number
        else:
            print(f"on date {k} the number of prices equals zero")
    return avg_prices_dict


def stats_process_numbers(product_name, start_date, end_date):
    try:
        with open('./sold.csv', newline='') as csvfile:
            sold_items = csv.reader(csvfile, delimiter=';', quotechar='|')
            numbers_dict = {}
            for row in sold_items:
                if row[0].isdigit():
                    # als je het spreadsheet opent en de dag is kleiner dan 10, wordt er maar 1 karakter voor de dag gebruikt
                    if len(row[3]) == 7:
                        # terwijl je er 2 voor nodig hebt, anders gaat de conversie niet goed
                        row[3] = "0" + row[3]
                    sell_date = datetime.strptime(row[3], "%d%m%Y")
                    if sell_date >= start_date and sell_date <= end_date and row[2] == product_name:
                        if sell_date in numbers_dict:
                            numbers_dict[sell_date] = numbers_dict[sell_date]+1
                        else:
                            numbers_dict[sell_date] = 1
    except:
        print("file sold.csv kon niet worden geopend. ")
    make_stats_graph("bar", numbers_dict, "date", "number",
                     f"Numbers of {product_name}s sold in period {start_date.strftime('%d-%m-%Y')} until {end_date.strftime('%d-%m-%Y')}", start_date, end_date)


def stats_process_buy_price(product_name, start_date, end_date):
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_items = csv.reader(csvfile, delimiter=';', quotechar='|')
            mult_bought_prices_dict = {}
            for row in bought_items:
                if row[0].isdigit():
                    # als je het spreadsheet opent en de dag is kleiner dan 10, wordt er maar 1 karakter voor de dag gebruikt
                    if len(row[2]) == 7:
                        # terwijl je er 2 voor nodig hebt, anders gaat de conversie niet goed
                        row[2] = "0" + row[2]
                    bought_date = datetime.strptime(row[2], "%d%m%Y")
                    if bought_date >= start_date and bought_date <= end_date and row[1] == product_name:
                        if bought_date in mult_bought_prices_dict:
                            if row[3].replace(",", ".") in mult_bought_prices_dict[bought_date]:
                                mult_bought_prices_dict[bought_date][row[3]
                                                                     ] = mult_bought_prices_dict[bought_date][row[3].replace(",", ".")]+1
                            else:
                                mult_bought_prices_dict[bought_date][row[3].replace(
                                    ",", ".")] = 1
                        else:
                            mult_bought_prices_dict[bought_date] = {}
                            mult_bought_prices_dict[bought_date][row[3].replace(
                                ",", ".")] = 1
    except:
        print("file bought.csv kon niet worden geopend. ")
    avg_bought_prices_dict = compute_avg_prices(mult_bought_prices_dict)
    make_stats_graph("bar", avg_bought_prices_dict, "date", "average buying price in eur",
                     f"Average price of {product_name}s bought in period {start_date.strftime('%d-%m-%Y')} until {end_date.strftime('%d-%m-%Y')}",
                     start_date, end_date)


def stats_process_sell_price(product_name, start_date, end_date):
    try:
        with open('./sold.csv', newline='') as csvfile:
            sold_items = csv.reader(csvfile, delimiter=';', quotechar='|')
            mult_sell_prices_dict = {}
            for row in sold_items:
                if row[0].isdigit():
                    # als je het spreadsheet opent en de dag is kleiner dan 10, wordt er maar 1 karakter voor de dag gebruikt
                    if len(row[3]) == 7:
                        # terwijl je er 2 voor nodig hebt, anders gaat de conversie niet goed
                        row[3] = "0" + row[3]
                    sell_date = datetime.strptime(row[3], "%d%m%Y")
                    if sell_date >= start_date and sell_date <= end_date and product_name == row[2]:
                        if sell_date in mult_sell_prices_dict:
                            if row[4].replace(",", ".") in mult_sell_prices_dict[sell_date]:
                                mult_sell_prices_dict[sell_date][row[4].replace(",", ".")
                                                                 ] = mult_sell_prices_dict[sell_date][row[4].replace(",", ".")]+1
                            else:
                                mult_sell_prices_dict[sell_date][row[4].replace(
                                    ",", ".")] = 1
                        else:
                            mult_sell_prices_dict[sell_date] = {}
                            mult_sell_prices_dict[sell_date][row[4].replace(
                                ",", ".")] = 1
    except:
        print("file sold.csv kon niet worden geopend. ")
    avg_sell_prices_dict = compute_avg_prices(mult_sell_prices_dict)
    make_stats_graph("bar", avg_sell_prices_dict, "date", "average selling price in eur",
                     f"Average price of {product_name}s sold in period {start_date.strftime('%d-%m-%Y')} until {end_date.strftime('%d-%m-%Y')}",
                     start_date, end_date)


def stats_process_profit(product_name, start_date, end_date):
    revenue_dict = get_revenue_dict(start_date, end_date, product_name)
    purchased_dict = {}
    expired_dict = {}
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_items = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_items:
                if row[0].isdigit():
                    # als je het spreadsheet opent en de dag is kleiner dan 10, wordt er maar 1 karakter voor de dag gebruikt
                    if len(row[2]) == 7:
                        # terwijl je er 2 voor nodig hebt, anders gaat de conversie niet goed
                        row[2] = "0" + row[2]
                    bought_date = datetime.strptime(row[2], "%d%m%Y")
                    exp_date = datetime.strptime(row[4], "%d%m%Y")
                    if bought_date >= start_date and bought_date <= end_date and product_name == row[1]:
                        if is_float(row[3].replace(",", ".")):
                            if bought_date in purchased_dict:
                                purchased_dict[bought_date] = purchased_dict[bought_date] + \
                                    float(row[3].replace(",", "."))
                            else:
                                purchased_dict[bought_date] = float(
                                    row[3].replace(",", "."))
                        else:
                            print("{row[3]} is not a number with a , or .")
                    elif exp_date >= start_date and exp_date <= end_date and product_name == row[1] and row[5] != "Y":
                        if is_float(row[3].replace(",", ".")):
                            if bought_date in purchased_dict:
                                expired_dict[bought_date] = expired_dict[bought_date] + \
                                    float(row[3].replace(",", "."))
                            else:
                                expired_dict[bought_date] = float(
                                    row[3].replace(",", "."))
                        else:
                            print("{row[3]} is geen getal met een punt")
    except:
        print("file bought.csv kon niet worden geopend. ")
    fill_date = start_date
    profit_dict = {}
    while fill_date <= end_date:
        sold_amount = 0
        bought_amount = 0
        expired_amount = 0
        value_found = "N"
        if fill_date in revenue_dict:
            sold_amount = revenue_dict[fill_date]
            value_found = "Y"
        if fill_date in purchased_dict:
            bought_amount = purchased_dict[fill_date]
            value_found = "Y"
        if fill_date in expired_dict:
            expired_amount = expired_dict[fill_date]
            value_found = "Y"
        if value_found == "Y":
            profit_value = sold_amount-bought_amount-expired_amount
            profit_dict[fill_date] = profit_value
        fill_date = fill_date+timedelta(days=1)
    make_stats_graph("line", profit_dict, "date", "profit in eur",
                     f"Daily profit of {product_name}s for period {start_date.strftime('%d-%m-%Y')} until {end_date.strftime('%d-%m-%Y')}",
                     start_date, end_date)


def stats_process_revenue(product_name, start_date, end_date):
    revenue_dict = get_revenue_dict(start_date, end_date, product_name)
    make_stats_graph("bar", revenue_dict, "date", "revenue in eur on date",
                     f"Revenue of {product_name}s sold in period {start_date.strftime('%d-%m-%Y')} until {end_date.strftime('%d-%m-%Y')}",
                     start_date, end_date)


def process_stats(args, dates):
    product_name = args.product_name
    dates_approved = "N"
    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
        if start_date > end_date:
            raise ValueError("Start date shouldn't be before end date")
        dates_approved = "Y"
    except ValueError as error:
        print(error)
    if dates_approved == "Y":
        if args.number == True:
            stats_process_numbers(product_name, start_date, end_date)
        if args.buy_price == True:
            stats_process_buy_price(product_name, start_date, end_date)
        if args.sell_price == True:
            stats_process_sell_price(product_name, start_date, end_date)
        if args.profit == True:
            stats_process_profit(product_name, start_date, end_date)
        if args.revenue == True:
            stats_process_revenue(product_name, start_date, end_date)

import calendar
import emoji
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.style import Style


def table_heading(purpose, rep, start_date, end_date):
    if purpose == "Revenue" or purpose == "Profit":
        if start_date == end_date:
            rep.print(f"{purpose} report for date " +
                      start_date.strftime('%d-%m-%Y'), style="red on white")
        else:
            rep.print(f"{purpose} report for the month " +
                      calendar.month_name[start_date.month], style="red on white")
    else:
        rep.print(f"{purpose} part", style="red on white")


def report_sell_part(purpose, sold_items, start_date, end_date, total_amount_sold):
    console = Console()
    table = Table(show_header=True, header_style="bold", show_lines=False)
    if purpose == "Revenue":
        table_heading("Revenue", console, start_date, end_date)
    else:
        table_heading("Sell", console, start_date, end_date)
    table.add_column("sold id", style="dim", width=10)
    table.add_column("buy id ", style="dim", width=10)
    table.add_column("product name", style="dim", width=30)
    if start_date != end_date:
        table.add_column("sell date", style="dim", width=30)
    table.add_column("buy price in eur", style="dim", width=20)
    table.add_column("sold price in eur", style="dim", width=20)
    sales_reportable = "N"

    for item in sold_items:
        sales_reportable = "Y"
        if start_date == end_date:
            table.add_row(item['id'],
                          item['buy_id'],
                          item['product_name'],
                          str(item['buy_price']).replace('.', ','),
                          str(item['sell_price']).replace('.', ','))
        else:
            table.add_row(item['id'],
                          item['buy_id'],
                          item['product_name'],
                          str(item['sell_date'].strftime("%d-%m-%Y")),
                          str(item['buy_price']).replace('.', ','),
                          str(item['sell_price']).replace('.', ','))
    if sales_reportable == "Y":
        console.print(table)
    else:  # voor de leesbaarheid is hier niet voor een elif statement gekozen
        if start_date == end_date:
            console.print(
                f"No sales reportabele for date {start_date.strftime('%d-%m-%Y')}", style="red on white")
        else:
            console.print(
                f"No sales reportable for the month {calendar.month_name[start_date.month]}")
    if sales_reportable == "Y":
        sold_tot_amount = str('%.2f' % round(
            total_amount_sold, 2)).replace('.', ',')
        if start_date == end_date:
            print(''.ljust(69), end="")
            console.print(
                f"Total sold eur {sold_tot_amount}", style="red on white")
        else:
            print(''.ljust(85), end="")
            console.print(
                f"Total sold eur {sold_tot_amount}", style="red on white")


def make_report_profit(sold_items, purchased_items, expired_items,
                       total_amount_sold, total_amount_bought, total_amount_perished, start_date,
                       end_date):

    # Dit rapport bestaat uit drie stukken : een voor de verkoop, een voor de aankoop en een voor bedorven produkten
    console = Console()
    table = Table(show_header=True, header_style="bold", show_lines=False)
    table_heading("Profit", console, start_date, end_date)

    # verkoopgedeelte
    report_sell_part("Sell", sold_items, start_date,
                     end_date, total_amount_sold)

    # koopgedeelte
    table = Table(show_header=True, header_style="bold", show_lines=False)
    table_heading("Bought", console, start_date, end_date)
    table.add_column("buy id", style="dim", width=22)
    table.add_column("product name", style="dim", width=35)
    if start_date != end_date:
        table.add_column("buy date", style="dim", width=34)
    table.add_column("expiration date", style="dim", width=25)
    table.add_column("buy price in eur", style="dim", width=25)
    purchases_reportable = "N"
    for item in purchased_items:
        purchases_reportable = "Y"
        if start_date == end_date:
            table.add_row(item['id'],
                          item['product_name'],
                          item['expiration_date'].strftime('%d-%m-%Y'),
                          str(item['price']).replace('.', ','))
        else:
            table.add_row(item['id'],
                          item['product_name'],
                          item['buy_date'].strftime('%d-%m-%Y'),
                          item['expiration_date'].strftime('%d-%m-%Y'),
                          str(item['price']).replace('.', ','))
    if purchases_reportable == "Y":
        console.print(table)
        bought_tot_amount = str('%.2f' % round(
            total_amount_bought, 2)).replace('.', ',')
        if start_date == end_date:
            print(''.ljust(65), end="")
            console.print(
                f"Total purchased eur {bought_tot_amount}", style="red on white")
        else:
            print(''.ljust(77), end="")
            console.print(
                f"Total purchased eur {bought_tot_amount}", style="red on white")
    else:
        if start_date == end_date:
            console.print(
                f"No purchases reportable for date {start_date.strftime('%d-%m-%Y')}", style="red on white")
        else:
            console.print(
                "No purches reportable for the month {calendar.month_name[start_date.month]}", style="red on white")
    # bedorven produkten. Voor het grootste gedeelte hetzelfde als het aankoopstuk. Kan eventueel samen tot een stuk worden genomen.
    # Dat scheelt wel wat, maar is niet overdreven veel.
    if len(expired_items) == 0:
        None
    else:
        table = Table(show_header=True, header_style="bold", show_lines=False)
        table_heading("Perished", console, start_date, end_date)
        table.add_column("buy id", style="dim", width=22)
        table.add_column("product name", style="dim", width=35)
        if start_date != end_date:
            table.add_column("buy date", style="dim", width=34)
        table.add_column("expiration date", style="dim", width=25)
        table.add_column("buy price in eur", style="dim", width=25)

        for item in expired_items:
            if start_date == end_date:
                table.add_row(item['id'],
                              item['product_name'],
                              item['expiration_date'].strftime('%d-%m-%Y'),
                              str(item['price']).replace('.', ','))
            else:
                table.add_row(item['id'],
                              item['product_name'],
                              item['buy_date'].strftime('%d-%m-%Y'),
                              item['expiration_date'].strftime('%d-%m-%Y'),
                              str(item['price']).replace('.', ','))
        console.print(table)
        expired_tot_amount = str('%.2f' % round(
            total_amount_perished, 2)).replace('.', ',')
        if start_date == end_date:
            print(''.ljust(32), end="")
            console.print(
                "Total amount for which goods perished eur {expired_tot_amount}", style="red on white")
        else:
            print(''.ljust(57), end="")
            console.print(
                f"Total amount for which goods perished eur {expired_tot_amount}", style="red on white")

    # en de waarde van de winst
    profit = str('%.2f' % round(total_amount_sold-total_amount_bought -
                                total_amount_perished, 2)).replace(".", ",")
    if start_date == end_date:
        console.print(
            f"The total profit on date {start_date.strftime('%d-%m-%Y')} equals eur {profit}", style="red on white")
    else:
        console.print(
            f"The total profit for the month {calendar.month_name[start_date.month]} equals eur {profit}", style="red on white")


def make_report_revenue(sellData, total_amount_sold, start_date, end_date):
    # totaal verkoop
    report_sell_part("Revenue", sellData, start_date,
                     end_date, total_amount_sold)


def make_report_inventory(inventory_data, ref_date):
    # voorraad
    console = Console()
    console.print(
        f"Inventory on {ref_date.strftime('%d-%m-%Y')}", style="red on white")
    if len(inventory_data) == 0:
        print("There's no inventory on this date")
    else:
        table = Table(show_header=True, header_style="bold", show_lines=False)
        table.add_column("Product name", style="dim", width=30)
        table.add_column("Count")
        table.add_column("Buy price in eur", justify="right")
        table.add_column("Expiration date", justify="right")
        if isinstance(inventory_data, dict):
            for k, v in inventory_data.items():
                product_name = k
                if isinstance(v, dict):
                    value = v
                    for k, v in value.items():
                        expiry_date_str = k
                        if len(expiry_date_str) == 7:
                            expiry_date_str = "0"+expiry_date_str
                        expiry_date = datetime.strptime(
                            expiry_date_str, "%d%m%Y")
                        value = v
                        if isinstance(v, dict):
                            for k, v in value.items():
                                buy_price = k
                                number = v
                                table.add_row(product_name,
                                              str(number),
                                              buy_price.replace('.', ','),
                                              expiry_date.strftime("%d-%m-%Y"),)
        console.print(table)

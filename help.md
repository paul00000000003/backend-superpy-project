**Introduction**

Superpy.py is a program by means of which the administration of a supermarket can be kept. The program can accept several kinds op cli (command line interface) commands. A cli command is simply a string of several arguments by means of which the program superpy.pi will carry out a specific instruction.

**Elaboration of CLI-commands**

As mentioned in the introduction the program allows for a number of CLI commands. These will be discussed underneath mentioning examples of these. Note that any item or value never uses "" or =. It always starts of by   py(thon) superpy.py e.g. py superpy.py --h to access the help file or 
py superpy.py buy --product-name orange --price 0.68 --expiration-date 2021-01-1 for a buying instruction. Please be concise in formatting your instruction because the instructions are sensitive for hyphens, colons, equal signs(=) and basicly any other reading sign/character. Also stick to the order in which the arguments make up for the instruction. Numbers which have . in common life should be written as such (e.g. 1.00 for prices) The instructions are :
1. --advance-time x. Running the program with these arguments shifts the reference day forward by x days. Note 
   that x should be a positive number because we only go forward in time.
2. buy --product-name xxxxxx --price xxx.yy --expiration-date yyyy-mm-dd. As you can see there are 6 individual 
   parts in this instruction among which :
   buy : this is the main part of the instruction which identifies its purpose buy
   --product-name   : tag identifying the product name. Should be copied exactly this way.  
   xxxxxxxx         : any product/item sold by the supermarket such as apple, orange, milk, bread etc. Please use the single form of the article.Avoid using e.g. apples, oranges etc. 
   --price          : the price in eur for which the article has been bought by the supermarket.  
   xxx.yy           : the number for the price of the article
   --expiration-date: tag indentifying the expiration date. Should be copied exactly this way.
   yyyy-mm-dd       : value for the expiration date (y: year, m: month, d: month)
   
   Note that the buying date is actuall set by the system for this instruction and equals the reference date 
   registered in the referred_date.txt file 
3. sell --product-name xxxxxx --price xxx.yy
   sell : main part of the instruction specifying the instruction type 
   --product-name : tag identifying the product name. Should be kept identical
   xxxxxx : specification of the product name i.e. orange, apple, banana, coffee, bread etc. Like with the buy 
instruction please don't use plural format like apples oranges, bananas etc. 
   --price : identification of the selling price. Keep this description identical as specified here.
   xxx.yy  : specification of selling price in eur. Use a similar format meaning x as a certain number of digits 
before the decimal point and yy as two digits after the decimal point e.g. 1.98
4. report. For reporting three different categories of data are used. All reporting is displayed by means 
   of tables in the systems console window (either MS Dos or the Linux system's interface). The categories are 
   inventory (how much is in stock), revenue (total amount sold), profit (total amount sold - total amount bought-
   total amount perished). In this case for each subsection a separate subtable is created). The formats of the
   instructions are :
   report inventory --now 
   report inventory --yesterday
   report inventory --date yyyy-mm-dd
   report profit --today 
   report profit --yesterday
   report profit date yyyy-mm
   report revenue --today
   report revenue --yesterday
   report revenue --date yyyy-mm 

   Both the --now and --today values refer to what's taken place so far today. The program can after all be run 
   on a variety of time values whereas there may be more purchases or sells made throughout the day. Notice the
   inventory can be monitored on any other specific day whereas the revenue and profit can be computed for any 
   other month. Notice the profit and revenue are computed for all products but not separately 
5. stats. Stats are computed for all products separately, hence a product name makes up a part of the                instruction. Another contrast compared to reporting is stats requires a start and end date. The output for the 
   stats instruction is a bar chart except for profit in which case it's a line chart. In each case the display
   has the date on the x axis. The significance of the y axis depends on the kind of report which is made.The 
   instruction for stats is specified as follows :

   stats --product-name xxxxx --start-date yyyy-mm-dd --end-date yyyy-mm-dd zzzzzzzzz
   
   stats : principle indication of the report category. Stats stands for statistics. Statistics means the output
will be a graphical display on the basis of which conclusions can be drawn
   
   --product-name : identification of the product name. Please keep this unchanged.
   xxxx  : specification of the product name ie apple, orange, banana, milk, bread etc. Please report these 
products in single format. Avoid writing apples, oranges etc. 
   --start-date : identification of the start of the period for which the graph will be made. 
   yyyy-mm-dd : value for the start date which should be marked as y (year), m(month), d(day)
   --end-date : identification of the end of the period. Please copy unchanged. 
   yyyy-mm-dd : value for the end date of which the format should be y (year) m(month) d(day)
   
   zzzzz  : this field can have one of the following 5 values. Each refers to the specific product. 
            --number : fluctuation of inventory on different dates
            --buy-price : fluctuation of the average daily price for which the goods are bought
            --sell-price : fluctuation of the average price for which the goods are sold
            --revenue : fluctuation of the daily revenue 
            --profit : fluctuation of the daily profit   


** Examples **

In line with the preceeding paragraph, this paragraph contains a list of examples :
python superpy.py --advance-time 1 In order to start testing I recommend setting the date somewhere in the past 
                                   e.g. the first of january. Since we're not using sql yet the date is 
                                   registered in the file referred_date.txt 

Logically the next step would be filling the inventory for a few days using buy e.g. as follows :                               
py superpy.py buy --product-name orange --price 0.68 --expiration-date 2021-01-15
py superpy.py buy --product-name pear --price 0.70 --expiration-date 2021-01-14
py superpy.py buy --product-name coconut --price 2.50 --expiration-date 2021-03-01
py superpy.py buy --product-name melon --price 0.55 --expiration-date 2021-01-20
py superpy.py buy --product-name milk --price 0.95 --expiration-date 2021-01-15
py superpy.py buy --product-name yoghurt --price 0.88 --expiration-date 2022-01-20

When you've done this, check the spreadsheet bought.csv. Explication of this file is as follows :
column 1 : Unique purchase id
column 2 : Product name
column 3 : Purchase date (equals reference date registered in referred_date.txt)
column 4 : Price for which the item was bought
column 5 : Expiration date 
column 6 : either N when the item hasn't been sold or the date on which the item was sold 

After having done this sell a couple of items using the following instructions :
py superpy.py sell --product-name orange --price 0.75
py superpy.py sell --product-name pear --price 0.80
py superpy.py sell --product-name coconut --price 2.80

Check the selling date really gets filled in the bought.csv file according to the instructions you gave. 
After each selling instruction the file sold.csv gets appended. The explication of the columns in this file is as follows :
Column 1. Unique selling id
Column 2. Related buying id 
Column 3. Product name
Column 4. Selling date in dd-mm-yyyy
Column 5. Price for which the product got sold 
Column 6. Price for which the product got bought

Now after the first buying instruction has been carried out, the inventory should be raised. In order to check the inventory use one of the following CLI's :
py superpy.py report inventory –-now
py superpy.py report inventory --yesterday 
py superpy.py report inventory --date 2021-01-01 (or an alternate date)

Also immediately the revenue can be checked. In order to do this use one of the following instructions :
py superpy.py report revenue --today
py superpy.py report revenue --yesterday
py superpy.py report revenue --date 2021-01  (notice in this case the month is used where as for the inventory 
                                              the date is used with a day)
It's also possible to check the profit. 
py superpy.py report profit --today
py superpy.py report profit --yesterday
py superpy.py report profit --date 2021-01 (notice whichever option is used, the calculation of the profit always 
                                            entails the calculation of the revenue as well as the computation of 
                                            purchases and loss due to decay/expired products)





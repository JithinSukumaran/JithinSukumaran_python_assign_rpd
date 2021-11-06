import scrapy
import pandas as pd
import numpy as np
import re
import time

class ZacksSpider(scrapy.Spider):
    name = 'zacks'
    ticker = pd.read_csv('data.csv')  # The data.csv file contains the ticker names
    list_ticker = ticker['Ticker '].tolist()
    urls = [f'https://www.zacks.com/funds/etf/{x}/holding' for x in list_ticker]
    start_urls = urls  # list of start urls, 4 in total with tickers xle,xlu,spy and veu

    def parse(self, response):
        ticker = response.url.split('/')[-2]  # Storing the ticker name to be used later in the csv file name
        contents = response.xpath('//script')[19].extract()  # Extracting the data which was stored in the script tag of the source code
        
        def convert(x):
            '''
            To convert the "NA" elements of Weight(%) & 52 Wk Change(%)
            to null and remaining elements to float
            '''
            try:
                x= float(x)
                return x
            except ValueError:
                return np.nan

        # Regex for separating each row of data to individual list elements
        pattern = re.compile(r'\[([+()\\/<>=\w\d,."&\'\s_-]+)\]')

        # Regex for cleaning the Security name column
        namePat = re.compile(r'(?<=title=\\")[()\'+/\s\d\w&.-]+(?=\\)')

        # Regex for cleaning the symbol column
        symPat = re.compile(r'(?<=>)([.\w\d]+)(?=<)')

        matches = re.finditer(pattern,contents)

        data = []
        for m in matches:
            text = re.sub(r',(?=\d)','',m.group(1))  # Regex to remove the , in Shares column
            text = text.split(',')  # Spliting to make columns of the row separate elements of the list
            
            '''
            here text[0] = Security name
                text[1] = Symbol
                text[2] = Shares
                text[3] = Weight(%)
                text[4] = 52 Wk Change(%)
                text[5] = Report
            '''
            
            if 'span' in text[0]:  # To Extract the Security name from the html tags
                text[0] = re.findall(namePat,text[0])[0]
                
            if 'button' in text[1]:  # To Extract the Symbol from the html tags
                text[1] = re.findall(symPat,text[1])[0]
                
            for num in range(5):  # To delete all the unwanted " 
                text[num] = re.sub('"','',text[num]).strip()
            
            data.append(text)  # Appending the every row to data list

        # Making a DataFrame out of the data list
        df = pd.DataFrame(data,columns=['Security Name','Symbol',
                                    'Shares','Weight(%)',
                                    '52 Wk Change(%)','Report'])

        # Cleaning the data of Shares, Weight(%) & 52 Wk Change(%) columns
        df['Shares'] = df['Shares'].apply(lambda x: int(x) if x.isdigit() else np.nan)
        df['Weight(%)'] = df['Weight(%)'].apply(convert)
        df['52 Wk Change(%)'] = df['52 Wk Change(%)'].apply(convert)

        df['Date'] = time.strftime("%d/%m/%Y") # adding the date column 

        df.drop('Report',axis=1,inplace=True) # Deleting the Report column as its not needed

        # Arranging the columns of the DataFrame in proper order
        df = df[['Date','Security Name', 'Symbol', 'Shares', 'Weight(%)', '52 Wk Change(%)']]

        df.set_index('Date',drop=True,inplace=True)  # Setting the date column as the index

        df.to_csv(f'{ticker}.csv')  # To save the result in a csv file
    
        # You will find 4 csv files in the folder containing the spider

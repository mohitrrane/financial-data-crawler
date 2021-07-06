# -*- coding: utf-8 -*-
"""
Created on Wed May 20 11:21:00 2020

@authors: Mohit Rane, Ojasv Kamal
"""

class MoneyControlCrawler():
    def __init__(self, executable_path = r'C:\Users\Mohit Rane\Desktop\chromedriver.exe'):
        # Importing libraries
        import platform
        from selenium import webdriver
        
        # Get the Driver for the crawling
        if platform.system() == "Linux":
            # Only for Linux
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.add_argument("--disable-infobars")
            options.add_experimental_option("prefs",{
                "profile.default_content_setting_values.notifications":1
            })
            driver = webdriver.Chrome(options = options)

        elif platform.system() == 'Windows':
            # Only for Windows
            driver = webdriver.Chrome(executable_path = executable_path)
        
        # Staring driver to load website
        driver.get("https://www.moneycontrol.com/")
        driver.maximize_window()
        import time
        time.sleep(10)
        self.driver = driver
        
        print(">>> Crawler Ready")
        
    def crawl_by_company(self, company_name):
        import time
        import pandas
        from bs4 import BeautifulSoup

        print('>>> Started Crawling')
        driver = self.driver
        
        # Querying in the search-box
        stock_name = driver.find_element_by_id("search_str")
        stock_name.click()
        stock_name.send_keys(company_name)
        
        # Submitting the query
        submit_button = driver.find_element_by_class_name("FR")
        submit_button.click()
        
        
        # Loading balance sheet
        # time.sleep(10)       # for waiting till full page loads
        balance_sheet_button = driver.find_element_by_link_text("Balance Sheet")
        balance_sheet_button.click()
        time.sleep(2)

        # Parse the page as string to bs4
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, features="lxml")
        
        # Locating the table rows in the Page
        
        bs_table = soup.find(id='BalanceSheet').find(class_ ='mctable1')
        if bs_table is None:
            bs_table = soup.find(id='SBalanceSheet').find(class_ ='mctable1')
        bs_rows = bs_table.find('tbody').find_all('tr')
        bs_rows_head = bs_table.find('thead').find_all('th')


        print('>>> Started Scraping Balance Sheet')

        tab_bs = [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]]

        for i in range(0,6):
            tab_bs[i][0] = bs_rows_head[i].text

        

        for i in range(1,5):
            for j in range(0,6):
                tab_bs[j][i] =bs_rows[i-1].find_all('td')[j].text 
        import numpy
        
        tab_bs = numpy.transpose(tab_bs)        

        import csv
        with open(company_name + '_balance_sheet0'+'.csv',"w+") as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(tab_bs)

        tab_bs = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
        bs_table = soup.find(id='BalanceSheet').find_all(class_ ='mctable1')[1]
        bs_rows = bs_table.find('tbody').find_all('tr')
        for i in range(0,4):
            for j in range(0,6):
                tab_bs[j][i] =bs_rows[i].find_all('td')[j].text
        tab_bs = numpy.transpose(tab_bs)
        with open(company_name + '_balance_sheet1'+'.csv',"w+") as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(tab_bs)

        with open(company_name + '_balance_sheet1'+'.csv', 'r') as f1, open(company_name + '_balance_sheet0'+'.csv', 'a+') as f2:
        	f2.write(f1.read())
        
        import os
        os.remove(company_name + '_balance_sheet1'+'.csv')

        tab_bs = [[1],[1],[1],[1],[1],[1]]
        bs_table = soup.find(id='BalanceSheet').find_all(class_ ='mctable1')[2]
        bs_rows = bs_table.find('tbody').find_all('tr')
        for i in range(0,1):
            for j in range(0,6):
                tab_bs[j][i] =bs_rows[i].find_all('td')[j].text
        tab_bs = numpy.transpose(tab_bs)
        with open(company_name + '_balance_sheet2'+'.csv',"w+") as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(tab_bs)

        with open(company_name + '_balance_sheet2'+'.csv', 'r') as f1, open(company_name + '_balance_sheet0'+'.csv', 'a+') as f2:
            f2.write(f1.read())
        
        
        os.remove(company_name + '_balance_sheet2'+'.csv')

        # print('>>> Balance Sheet Scraped Successfully')

        # print('>>> Started Scraping Profit and Loss Statement')

        # Loading the Profit and loss Chart
        pnl_button = driver.find_element_by_link_text("Profit & Loss")
        link_to_pnl_chart = pnl_button.get_attribute("href")
        driver.get(link_to_pnl_chart)

        # Parse the page as string to bs4
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, features="lxml")
        
        # Locating the table rows in the Page
        pnl_table = soup.find(class_ ='mctable1')
        pnl_rows = pnl_table.find('tbody').find_all('tr')
        
        # Converting the table row by row to dictionary
        pnl_column_titles = []
        pnl_table = {}
        for i, row in enumerate(pnl_rows[0:40]):
            if i == 0:
                # Column Headings
                for column_in_row in row.find_all('td'):
                    column_in_row = column_in_row.find(text = True)
                    pnl_table[column_in_row] = []
                    pnl_column_titles.append(column_in_row)
            else:
                # Rows of table content
                for j, column_in_row in enumerate(row.find_all('td')):
                    column_in_row = column_in_row.text
                    pnl_table[pnl_column_titles[j]].append(column_in_row)
        
        # Converting Dictionary to DataFrame and Saving it
        df = pandas.DataFrame.from_dict(pnl_table)
        df.to_csv(company_name + '_pnl_statement_'+'.csv', index = False)
        print('>>> Profit and Loss table saved')

        ratios_button = driver.find_element_by_xpath("/html/body/section/div[2]/section[1]/div[2]/div/div[1]/div[3]/div/div/nav/div/ul/li[8]/ul/li[8]/a")
        ratios_button.click()
        time.sleep(5)

        # from selenium.webdriver.common.keys import Keys

        # print(driver.current_url)
        window_before = driver.window_handles[0]
        window_after = driver.window_handles[1]
        driver.switch_to_window(window_after)

        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        # time.sleep(5)

        # print(driver.current_url)

        html_source = driver.page_source
        soup = BeautifulSoup(html_source, features="lxml")

        ratios_table = soup.find(class_ ='mctable1')
        ratios_rows = ratios_table.find('tbody').find_all('tr')
        
        # Converting the table row by row to dictionary
        ratios_column_titles = []
        ratios_table = {}
        for i, row in enumerate(ratios_rows[0:53]):
            if i == 0:
                # Column Headings
                for column_in_row in row.find_all('td'):
                    column_in_row = column_in_row.find(text = True)
                    ratios_table[column_in_row] = []
                    ratios_column_titles.append(column_in_row)
            else:
                # Rows of table content
                for j, column_in_row in enumerate(row.find_all('td')):
                    column_in_row = column_in_row.text
                    ratios_table[ratios_column_titles[j]].append(column_in_row)
        
        # Converting Dictionary to DataFrame and Saving it
        df = pandas.DataFrame.from_dict(ratios_table)
        df.to_csv(company_name + '_ratios'+'.csv', index = False)
        print('>>> Ratios table saved')

        # Closing the Driver
        driver.close()
        print('>>> Crawler Destroyed')
        
    def close(self):
        self.driver.close() 
        print('>>> Crawler Destroyed')

# Executing The Crawler
MCC = MoneyControlCrawler()
MCC.crawl_by_company("Hindustan Unilever")
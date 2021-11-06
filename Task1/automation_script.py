# This script will use helium and firefox browser to download the required csv file
# If helium is not present type pip install helium in the CLI

from helium import *
from selenium.webdriver import FirefoxOptions,FirefoxProfile
import time

url = 'https://www.zacks.com/screening/stock-screener?icid=screening-screening-nav_tracking-zcom-main_menu_wrapper-stock_screener'
username = 'laboc57506@ampswipe.com'
password = 'msJ$eb8EJu72@Bj'

options = FirefoxOptions()
options.add_argument('--maximize')
options.add_argument('--headless') # Setting for a headless browser
# Tweaking the preferences so that csv files get saved to the downloads folder by default
options.set_preference("browser.helperApps.neverAsk.saveToDisk","application/csv")

helium.start_firefox(url=url,options=options)

click('my screen')  # To click on my screen tab

# Inserting the username and password to sign in
write(username,into=S('#username'))
write(password,into=S('#password'))
click(S('.button'))

click(S('//a[@id="btn_run_162817"]')) # To click on the run button

click(S('#select_all_tickers')) # To select all companies
click('csv')  # To click on csv to download the csv file

time.sleep(3)
helium.kill_browser()  # To shut down the browser

print('Script ran successfully, the csv file is downloaded to the downloads folder')

# The csv file will be in the downloads folder

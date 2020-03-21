from os import path
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

def enable_download_in_headless_chrome(driver, download_dir):
        """
        there is currently a "feature" in chrome where
        headless does not allow file download: https://bugs.chromium.org/p/chromium/issues/detail?id=696481
        This method is a hacky work-around until the official chromedriver support for this.
        Requires chrome version 62.0.3196.0 or above.
        """

        # add missing support for chrome "send_command"  to selenium webdriver
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = driver.execute("send_command", params)

def downloadPDF(OGRN):

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('.\\Chrome Driver\\chromedriver.exe', options = options)
    download_path = path.dirname(path.realpath(__file__))
    enable_download_in_headless_chrome(driver, download_path)
    driver.get("https://egrul.nalog.ru/index.html")
    elem = driver.find_element_by_id("query")
    elem.send_keys(OGRN)
    elem = driver.find_element_by_id("btnSearch")
    elem.click()
    elem = None
    try:
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "op-excerpt"))
        )
    except TimeoutException:
      return False
    if not (elem is None):
        elem.click()
    time.sleep(5)# ИСПРАВИТЬ!
    driver.close()
    return True

downloadPDF(1177746582298)




from selenium import webdriver
import os
import sys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

USER_NAME = "09199107274"
PASSWORD = "3579852Ah"
EXPECTED_NAME = "احمد هاشمی زاده"


def close_all_windows(current_web_driver):
    for window in current_web_driver.window_handles:
        current_web_driver.switch_to.window(window)
        time.sleep(10)
        current_web_driver.close()


def report_exception(current_web_driver, current_exception):
    sys.stderr.write("Error: {0}\n".format(current_exception))
    ss = "screenshots/{0}.png".format(int(time.time()))
    current_web_driver.save_screenshot(ss)
    sys.stderr.write("Screenshot saved in {0}".format(os.path.abspath(ss)))


def wait_for_page_ready(current_web_driver):
    ready_state = ""
    for i in range(10000):
        ready_state = current_web_driver.execute_script(
            'return document.readyState')
        if ready_state == "complete":
            break

        time.sleep(0.5)

    if ready_state != "complete":
        raise Exception("never ready")


if __name__ == "__main__":
    wd = webdriver.Chrome(executable_path="./chromedriver")
    wd.maximize_window()
    wd.get("https://www.digikala.com/")

    try:
        # step 1: click on login in main page
        wait_for_page_ready(current_web_driver=wd)
        wd.find_element(by=By.PARTIAL_LINK_TEXT,
                        value="ورود | ثبت‌نام").click()

        # step 2: enter username and submit
        wait_for_page_ready(current_web_driver=wd)
        wd.find_element(by=By.NAME, value="username").send_keys(USER_NAME)
        wd.find_element(by=By.PARTIAL_LINK_TEXT, value="ورود").submit()
      # step 3: enter password and submit
        wait_for_page_ready(current_web_driver=wd)
        wd.find_element(by=By.NAME, value="password").send_keys(PASSWORD)
        wd.find_element(by=By.XPATH, value='//button[@type="submit"]').submit()

        # step 4: check user info
        wait_for_page_ready(current_web_driver=wd)
        wd.find_element(by=By.ID, value="dropdown").click()
        WebDriverWait(wd, 5).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, '/profile'))
        )
        name_element = wd.find_element(
            by=By.ID,
            value="/html/body/div[1]/div[1]/div[1]/header/div/div/div/div[2]/div[1]/div[2]/a/div/div[2]/span"
        )
        assert name_element.text == EXPECTED_NAME

    except Exception as e:
        report_exception(current_web_driver=wd, current_exception=e)

    finally:
        close_all_windows(current_web_driver=wd)

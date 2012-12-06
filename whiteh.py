import random
import string
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, WebDriverException
import redis_cli

def pick_zipcode():
    #pyzipcode
    return 12345


def sleeprand(secs):
    randomtime = min(secs, 5) * random.random()
    sleep(secs + randomtime)

class WhiteHoo:
    def __init__(self, webdriver):
        uname = ''.join(random.choice(string.ascii_lowercase) for x in range(13))
        self.first_name = uname
        uname2 = ''.join(random.choice(string.ascii_lowercase) for x in range(13))
        self.last_name = uname2
        self.zipcode = pick_zipcode()
        self.email = self.last_name + "@mailinator.com"
        try:
            webdriver.delete_all_cookies()
        except WebDriverException:
            webdriver.get("http://change.org")
            webdriver.delete_all_cookies()
        self.wb = webdriver

    def make_account(self):
        wb = self.wb
        wb.get("https://petitions.whitehouse.gov/register")
        sleeprand(3)
        wb.find_element_by_id('edit-mail').send_keys(self.email)
        wb.find_element_by_id('edit-profile-main-field-first-name-und-0-value').send_keys(self.first_name)
        wb.find_element_by_id('edit-profile-main-field-last-name-und-0-value').send_keys(self.last_name)
        wb.find_element_by_id('edit-profile-main-field-zip-und-0-value').send_keys(self.zipcode)
        element = wb.find_element_by_id('recaptcha_image')
        import process
        img_src = process.make_html_img(element, wb)
        solution = redis_cli.find_solution(img_src)
        wb.find_element_by_id('recaptcha_response_field').send_keys(solution)
        sleeprand(2)
        wb.find_element_by_id('edit-submit').click()
        sleeprand(3)


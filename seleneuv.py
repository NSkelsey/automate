from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import requests
from bs4 import BeautifulSoup
import random
import string
from IPython import embed

vuln_url = "http://drudgeretort.uservoice.com/forums/184052-general/suggestions/3358099-seed-this-forum-with-your-ideas"

def get_mailinator_url(uname):
    top_url = "http://www.mailinator.com/maildir.jsp?email=%s" % uname
    base_page = requests.get(top_url)
    soup = BeautifulSoup(base_page.text)
    li = soup.findAll("a")
    for a in li:
        ref = a.attrs["href"]
        if ref is not None and ref.startswith("/display"):
            url = "http://mailinator.com%s" % ref
            break
    #url = "http://www.mailinator.com/displayemail1.jsp?email=fakeemailo&msgid=76825"
    mail_page = requests.get(url)
    soup = BeautifulSoup(mail_page.text)
    url = soup.strong.a.attrs['href']
    print url
    return url

def upvote_uv(vuln_url, uname, wb):
  wb.delete_all_cookies()
  wb.get(vuln_url)
  sleep(1)
  btn = wb.find_element_by_css_selector('button.uvIdeaVoteFormTriggerState-no_votes.uvStyle-button')
  btn.click()
  a = wb.find_element_by_class_name("uvIdeaVoteCount")
  num = a.text.split("\n")[0]
  print "current count at: %s, and uname is %s" % (num, uname)
  b = wb.find_element_by_id("email_1")
  b.send_keys("%s@mailinator.com" % uname)
  sleep(3)
  c = wb.find_element_by_id("display_name_1")
  c.send_keys(uname)
  btn = wb.find_element_by_class_name("uvIdeaVoteButton-3-votes")
  btn.click()
  sleep(3)
  a = wb.find_element_by_class_name("uvIdeaVoteCount")
  num = a.text.split("\n")[0]
  print "after voting num is now %s" % num
  sleep(10)
  uv_reg_url = get_mailinator_url(uname)
  wb.get(uv_reg_url)
  sleep(3)


if __name__ == '__main__':
  wb = Remote("http://0.0.0.0:4444/wd/hub", DesiredCapabilities.FIREFOX)
  for i in range(5):
    uname = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(13))
    vuln_url = "http://drudgeretort.uservoice.com/forums/184052-general/suggestions/3358935-i-think-therefore-i-am"
    upvote_uv(vuln_url, uname, wb)
    sleep(random.random()*20)
  wb.close()



import sys
from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import requests
from bs4 import BeautifulSoup
import random
import string
from IPython import embed
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, WebDriverException
#import whiteh


vuln_url = "http://drudgeretort.uservoice.com/forums/184052-general/suggestions/3358099-seed-this-forum-with-your-ideas"

def sleeprand(secs):
    randomtime = min(secs, 5) * random.random()
    sleep(secs + randomtime)    

def uservoice_email(soup):
    return soup.strong.a.attrs['href']

def change_email(soup):
    return soup.findAll('a')[-1].attrs['href']

def get_mailinator_url(uname, url_func): # pass in the url func depending on the website
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
    url = url_func(soup)
    #print "auth url: " + url
    return url

def upvote_uv(vuln_url, uname, wb):
    wb.delete_all_cookies()
    wb.get(vuln_url)
    sleeprand(1)
    btn = wb.find_element_by_css_selector('button.uvIdeaVoteFormTriggerState-no_votes.uvStyle-button')
    btn.click()
    a = wb.find_element_by_class_name("uvIdeaVoteCount")
    num = a.text.split("\n")[0]
    print "current count at: %s, and uname is %s" % (num, uname)
    b = wb.find_element_by_id("email_1")
    b.send_keys("%s@mailinator.com" % uname)
    sleeprand(3)
    c = wb.find_element_by_id("display_name_1")
    c.send_keys(uname)
    btn = wb.find_element_by_class_name("uvIdeaVoteButton-3-votes")
    btn.click()
    sleeprand(3)
    a = wb.find_element_by_class_name("uvIdeaVoteCount")
    num = a.text.split("\n")[0]
    print "after voting num is now %s" % num
    sleeprand(10)
    uv_reg_url = get_mailinator_url(uname, uservoice_email)
    wb.get(uv_reg_url)
    sleeprand(3)

class Change:
    def __init__(self, webdriver):
        uname = ''.join(random.choice(string.ascii_lowercase) for x in range(13))
        self.first_name = uname
        self.last_name = uname
        self.reason = "reasons"
        self.password = 123456
        self.zipcode = 22904
        self.address = str(random.randint(1,500)) + " " + uname + " Street"
        self.city = 'charlottesville'
        self.state = 'VA'
        self.email = self.last_name + "@mailinator.com"
        try:
            webdriver.delete_all_cookies()
        except WebDriverException:
            webdriver.get("http://change.org")
            webdriver.delete_all_cookies()
        self.wb = webdriver
        self.broke = False
        self.signed = "No"

    def validate_email(self):
        try:
            auth_url = get_mailinator_url(self.last_name, change_email)
            wb.get(auth_url)
            wb.find_element_by_xpath("(//input[@name='user[password]'])[2]").send_keys(self.password) #renters password
            wb.find_element_by_css_selector('button.submit').click()
            sleeprand(2)
            return True
        except (UnboundLocalError, NoSuchElementException) as e:
            self.broke = True
            return False

    def make_account(self):
        wb = self.wb
        sleeprand(1)
        try:
            wb.get("http://change.org")
        except WebDriverException:
            return False
        sleeprand(1)
        try:
            wb.find_element_by_css_selector("button.small").click() #opens signin pane
            sleeprand(2)
            wb.find_element_by_name('new_user[profile][first_name]').send_keys(self.first_name)
            wb.find_element_by_name('new_user[profile][last_name]').send_keys(self.last_name)
            wb.find_element_by_name('new_user[email]').send_keys(self.email)
            wb.find_element_by_name('new_user[password]').send_keys(self.password)
            wb.find_element_by_id('new_user_submit').click()
            sleeprand(10)
            return self.validate_email()
        except (NoSuchElementException, WebDriverException) as e:
            return False

    def sign(self, url, sft):
        signatures, failures = sft
        try:
            wb = self.wb
            wb.get(url)
            sleeprand(1)
            wb.find_element_by_name('signature[address]').send_keys(self.address)
            wb.find_element_by_name('signature[city]').send_keys(self.city)
            wb.find_element_by_name('signature[zip_code]').send_keys(self.zipcode)
            #wb.find_element_by_name('signature[message]').send_keys(self.reason)
            wb.find_elements_by_name('signature[public]')[-1].click()
            sleeprand(2)
            wb.find_element_by_class_name('submit').click()
            signatures += 1
            self.signed = "Yes"
        except (ElementNotVisibleException, NoSuchElementException, WebDriverException) as e:
            failures += 1
        return (signatures, failures)
        
class UserVoice:
    def __init__(self, webdriver):
        #uva-style ID
        self.randomstring = (''.join(random.choice(string.ascii_lowercase) for x in range(3)) 
                               + str(random.randint(0,9)) 
                               + ''.join(random.choice(string.ascii_lowercase) for x in range(2))
                            )
        self.name = self.randomstring
        self.email = self.randomstring + "@virginia.edu"
        print "New UserVoice with random=" + self.randomstring
        try:
            webdriver.delete_all_cookies()
        except WebDriverException:
            webdriver.get(url)
            webdriver.delete_all_cookies()
        #print "Cookies deleted"
        self.wb = webdriver
        self.broke = False
        self.signed = "No"
            
    def sign(self, url, sft):
        signatures, failures = sft
        try:
            wb = self.wb
            wb.get(url)
            sleeprand(1)
            #click vote
            btn = wb.find_element_by_css_selector("button.uvIdeaVoteFormTriggerState-no_votes.uvStyle-button")
            btn.click()
            #print "Vote button clicked"
            #enter e-mail
            emailbox = wb.find_element_by_id('email_1')
            emailbox.send_keys(self.email)
            #print "Email field filled with " + self.email
            #enter name
            sleeprand(1)
            namebox = wb.find_element_by_id('display_name_1')
            namebox.send_keys(self.name)           
            #print "Name field filled with " + self.name 
            #click 3 votes
            votes3 = wb.find_element_by_xpath("(//button[@name='to'])[3]")
            votes3.click()
            print "Voted 3 with email = " + self.email
            signatures += 1
            self.signed = "Yes"
        except (ElementNotVisibleException, NoSuchElementException, WebDriverException) as e:
            failures += 1
        return (signatures, failures)


def uservoice_run(url, numIterations, sftUV):
    print "..--==****STUFFING USERVOICE PAGE****==--.."
    print "URL = " + url
    print "-------------------------------------------"
    sleep(5)
    for i in range(5):
        print "=====Starting iteration with sftUV=" + str(sftUV) + "======"
        newwb = webdriver.Firefox()
        uv = UserVoice(newwb)
        sftUV = uv.sign(url, sftUV)
        newwb.close()

def change_run(url, numIterations, sft):
    wb = webdriver.Firefox()
    for i in range(numIterations):
        change  = Change(wb)
        if not change.make_account():
            sft = (sft[0], sft[1] + 1)
            li.append(change)
            continue
        sft = change.sign(url, sft)
        print "<itr: %s, Accnt: %s, Created: %s, Signed: %s>" % (str(i), change.last_name, str(not change.broke), change.signed)
    print "retrying accts: %s" % len(li)
    saves = 0
    for change in li:
        sleeprand(2)
        change.validate_email()
        if change.sign(url, (0,0)):
            saves += 1
            print "<Accnt: %s, Created: %s, Signed: %s>" % ( change.last_name, str(not change.broke), change.signed)

    log = "="*50 + "\nRUN COMPLETED\n"
    log += "Successes: %s\nFailures: %s\nSaves: %s\nTotal: %s\n" % (sft[0], sft[1], saves, saves+sft[0])
    log += "="*50
    print log
    f = open('log.txt', 'w')
    f.write(log)
    f.close()

def redis_run(url, numIterations):
    for i in range(numIterations):
        import process
        import redis
        wb = webdriver.Firefox()
        wb.get(url)
        c = 'CMDS'
        _id = random.randint(0, pow(2,17))
        element = wb.find_element_by_id("recaptcha_image")
        img = process.make_html_img(element, wb)
        rconn = redis.StrictRedis(host='50.17.215.201', port=6379, db=0, password="reallylongandhardtoguesspassword")
        ps = rconn.pubsub()
        print _id
        rconn.publish(c, str(_id) + img) # I am listening here for the solution
        ps.subscribe(str(_id))
        solution = ""
        for m in ps.listen():
            if m['type'] == 'message':
                solution = m.get('data')
                break
        print solution
        field = wb.find_element_by_id('recaptcha_response_field')
        field.send_keys(solution)
        field.send_keys('\n')
        wb.close()
"""
def white_run(url, numIterations): #DANGER
    for i in range(numIterations):
        wb = webdriver.Firefox()
        whoo = whiteh.WhiteHoo(wb)
        whoo.make_account()
        wb.close()
"""

if __name__ == '__main__':
    sft = (0, 0)
    sftUV = (0, 0)
    li = []
    if (len(sys.argv) < 3):
        url = vuln_url
        numIterations = 5
    else:
        url = sys.argv[1]
        numIterations = int(sys.argv[2])
    exploit_site = sys.argv[3]
    if exploit_site == 'uv' or exploit_site == "studco":
        uservoice_run(url, numIterations, sftUV)
    elif exploit_site == "change":
        change_run(url, numIterations, sft)
    elif exploit_site == "test":
        redis_run(url, numIterations)
#    elif exploit_site == "government": #DANGER
#        white_run(url, numIterations)
    else:
        print "You must specify which site to use"





"""
  for i in range(5):
uname = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(13))
vuln_url = "http://drudgeretort.uservoice.com/forums/184052-general/suggestions/3358935-i-think-therefore-i-am"
upvote_uv(vuln_url, uname, wb)
sleep(random.random()*20)
wb.close()
"""

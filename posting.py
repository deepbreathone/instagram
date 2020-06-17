from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
from os import listdir
from os.path import isfile, join
import json
import random


class HomePage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get("https://m.instagram.com/")
        with open("credentials.json", "r") as f:
            credentials = json.loads(f.read())

        self.insta_username = credentials["username"]
        self.insta_password = credentials["password"]

    def login(self):
        login_button = self.browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div/div/div/div[2]/button"
        ).click()
        username_input = self.browser.find_element_by_css_selector(
            "input[name='username']"
        )
        password_input = self.browser.find_element_by_css_selector(
            "input[name='password']"
        )
        username_input.send_keys(self.insta_username)
        password_input.send_keys(self.insta_password)
        password_input.send_keys(Keys.ENTER)
        sleep(2)
        save_login = None
        try:
            save_login = browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/div/section/div/div[2]"
            )
        except NoSuchElementException:
            print("Unable to locate element")  # TODO log
        if save_login:
            save_login_text = "Deine Login-Informationen speichern?"
            if save_login.text == save_login_text:
                # Not now
                self.browser.find_element_by_css_selector("button").click()
            else:
                raise Exception(
                    'Expecting "%s", got "%s".' % (save_login_text, save_login.text)
                )
        sleep(2)


class InstaPage:
    def __init__(self, browser):
        super().__init__()
        self.browser = browser

        with open("hashtags.txt") as f:
            self.hashtags = [h.strip() for h in f.read().split(",")]

        with open("descriptions.txt") as f:
            self.descriptions = [h.strip() for h in f.read().split(",")]

        # Get random picutre
        pictures = [p for p in listdir("pictures") if isfile(join("pictures", p))]
        self.picture_path = os.path.abspath(join("pictures", random.choice(pictures)))
        print(self.picture_path)

    def upload(self):
        # Disable the file picker and call sendKeys on an <input type="file">
        # which is by design the only type of element allowed to receive/hold a file
        # disable the OS file picker
        browser.execute_script(
            """document.addEventListener('click', function(evt) {
                if (evt.target.type === 'file')
                    evt.preventDefault();
                }, true)
            """
        )
        # make an <input type="file"> available
        element = browser.find_element_by_xpath(
            "/html/body/div[1]/section/nav[2]/div/div/div[2]/div/div/div[3]"
        ).click()
        # assign the file to the <input type="file">

        browser.find_element_by_css_selector("input[type=file]").send_keys(
            self.picture_path
        )
        sleep(2)
        browser.find_element_by_xpath(
            "/html/body/div[1]/section/div[1]/header/div/div[2]/button"
        ).click()
        sleep(1.5)
        textarea = browser.find_element_by_xpath(
            "/html/body/div[1]/section/div[2]/section[1]/div[1]/textarea"
        )
        text = random.choice(self.descriptions) + " ".join(
            random.sample(self.hashtags, 5)
        )
        print(text)
        textarea.send_keys(text)
        # share
        browser.find_element_by_xpath(
            "/html/body/div[1]/section/div[1]/header/div/div[2]/button"
        ).click()


user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", user_agent)
browser = webdriver.Firefox(profile)
browser.set_window_size(360, 640)
browser.implicitly_wait(2)

home_page = HomePage(browser)
home_page.login()
insta_page = InstaPage(browser)
insta_page.upload()

browser.close()

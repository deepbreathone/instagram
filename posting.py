from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import shutil
import os
from os import listdir
from os.path import isfile, join
import json
import random
import pandas as pd

from generate_image_quote import generate_and_get_image_path


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
            save_login = self.browser.find_element_by_xpath(
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

    def upload(self, picture_path, text):
        # Disable the file picker and call sendKeys on an <input type="file">
        # which is by design the only type of element allowed to receive/hold a file
        # disable the OS file picker
        self.browser.execute_script(
            """document.addEventListener('click', function(evt) {
                if (evt.target.type === 'file')
                    evt.preventDefault();
                }, true)
            """
        )
        # make an <input type="file"> available
        element = self.browser.find_element_by_xpath(
            "/html/body/div[1]/section/nav[2]/div/div/div[2]/div/div/div[3]"
        ).click()
        # assign the file to the <input type="file">

        self.browser.find_element_by_css_selector("input[type=file]").send_keys(
            picture_path
        )
        sleep(2)
        self.browser.find_element_by_xpath(
            "/html/body/div[1]/section/div[1]/header/div/div[2]/button"
        ).click()
        sleep(1.5)
        textarea = self.browser.find_element_by_xpath(
            "/html/body/div[1]/section/div[2]/section[1]/div[1]/textarea"
        )

        print(text)
        textarea.send_keys(text)
        # share
        self.browser.find_element_by_xpath(
            "/html/body/div[1]/section/div[1]/header/div/div[2]/button"
        ).click()


def get_quote_of_the_day():
    df = pd.read_csv("quotes/quotes_to_post.csv")
    quote_of_the_day = df.sample()
    df.drop(df.index[quote_of_the_day.index]).to_csv(
        "quotes/quotes_to_post.csv", index=False
    )

    df_posted = pd.read_csv("quotes/quotes_posted.csv")
    df_posted.append(quote_of_the_day).to_csv("quotes/quotes_posted.csv", index=False)
    return quote_of_the_day


def get_description(quote, hashtags):
    description = quote["Description - can be same as pic"]
    if quote["direct quote"] == "Yes" and (
        quote["Reference"] != "Maria" or quote["Reference"] != "Ben's notes"
    ):
        description = f"{description} by {quote['Reference']} #{quote['Reference'].replace(' ', '')} "
    return description + " ".join(random.sample(hashtags, 10))


def main():
    user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", user_agent)
    browser = webdriver.Firefox(profile)
    browser.set_window_size(360, 640)
    browser.implicitly_wait(2)

    home_page = HomePage(browser)
    home_page.login()
    insta_page = InstaPage(browser)

    quote = get_quote_of_the_day()
    picture_path = generate_and_get_image_path(quote)
    print(picture_path)
    with open("hashtags.txt") as f:
        hashtags = [h.strip() for h in f.read().split(",")]

    # Quote has to be a series
    description = get_description(quote.iloc[0], hashtags)

    # Path has to be the full absolute path
    insta_page.upload(
        f"/Users/doreensacker/Desktop/DB/instagram/{picture_path}", description
    )

    browser.close()


if __name__ == "__main__":
    main()


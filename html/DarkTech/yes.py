from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
from selenium.common.exceptions import StaleElementReferenceException
import tweepy
# from fp.fp import FreeProxy
from selenium.webdriver.common.proxy import Proxy, ProxyType
import tkinter as tk
from tkinter import Menu, Label, Button, Checkbutton, Text, messagebox, Menu, Entry
from PIL import Image, ImageTk
import json
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.common.action_chains import ActionChains

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAC61oAEAAAAATv3V%2Bw%2BDdSmQVzAvpezr44IMGNI%3DD1Vpa8eaAG2r0C2Z0lrzXYUKD7MeLiwWbfPVQAwK9bh7PhqCP5"

class Helper:
    def GetApiKey(self):
        with open("api.json", "r") as f:
            data = json.load(f)
            bearer = data["bearer"]
            access_token = data["access_token"]
            access_token_secret = data["access_token_secret"]
            api_key = data["consumer_key"]
            api_key_secret = data["consumer_key_secret"]
            client_id = "bzRHdWNDUXZGNjIyalN0NVJDZnM6MTpjaQ"
            client_id_secret = "KmCoAZapOhXI9b-pq37Eq8jwFefAWDS1ynfXm6rTR9kQu-Qokl"
            return bearer, access_token, access_token_secret, api_key, api_key_secret, client_id, client_id_secret
    def GetComments(self):
        with open("comments.txt", "r") as f:
            data = f.read()
            return data
    def SaveComments(self, data):
        with open("comments.txt", "w") as f:
            f.write(data)
    def GetTopics(self):
        with open("topic.txt", "r") as f:
            data = f.read()
            return data


class ScrapeTweets:
    def __init__(self):
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
            'referer':'https://www.google.com/',
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }
        
        # Get the current user's home directory
        self.home_dir = os.path.expanduser("~")

        # Append the rest of the path
        self.chrome_data_dir = os.path.join(self.home_dir, "AppData", "Local", "Google", "Chrome", "User Data", "Person 1")

        self.op = webdriver.ChromeOptions()
        try:
            self.op.add_argument(f"user-data-dir={self.chrome_data_dir}")
        except:
            print("No chrome data dir found")
            self.op.add_argument(f"user-data-dir=/Users/vigowalker/Library/Application Support/Google/Chrome/Default")
        self.query = "Entrepreneur"
        self.url = requests.get("https://twitter.com/explore", headers=self.header)
        self.Creds = Helper().GetApiKey()
        self.CLIENT_ID_SECRET = self.Creds[6]
        self.CLIENT_ID = self.Creds[5]
        self.API_KEY = self.Creds[3]
        self.API_KEY_SECRET = self.Creds[4]
        self.ACCESS_TOKEN = self.Creds[1]
        self.ACCESS_TOKEN_SECRET = self.Creds[2]
        self.BEARER_TOKEN = self.Creds[0]
        self.base_url = "https://api.twitter.com/2/"
        self.headers = {"Authorization": f"Bearer {self.BEARER_TOKEN}"}
        self.client = self.authenticate()
        # Set up the proxy
        try:
            self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=self.op)
            self.driver.get(self.url.url)
        except:
            self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=self.op)
            self.driver.get(self.url.url)

    def authenticate(self):
        oauth2_user_handler = tweepy.OAuth2UserHandler(
            client_id=self.CLIENT_ID,
            redirect_uri="Callback / Redirect URI / https://theshadowtech.com",
            scope=["Scope here", "Scope here"],
            client_secret=self.CLIENT_ID_SECRET
        )

        client = tweepy.Client(
            consumer_key=self.API_KEY,
            consumer_secret=self.API_KEY_SECRET,
            access_token=self.ACCESS_TOKEN,
            access_token_secret=self.ACCESS_TOKEN_SECRET
        )
        return client
    def Last24Hours(self):
        now = time.time()
        return now - 86400
    def Scrape(self):
        while True:
            try:
                # self.Login()
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "r-30o5oe")))
                inp1 = self.driver.find_element(By.CLASS_NAME, "r-30o5oe")
                inp1.click()
                inp1.send_keys(self.query)
                inp1.send_keys(Keys.RETURN)
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-1dbjc4n")))
                tweets = self.driver.find_elements(By.CLASS_NAME, "css-1dbjc4n")
                time.sleep(10)
                print("Sleeping for 10 seconds")
                users = self.driver.find_elements(By.CSS_SELECTOR, ".css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
                if len(users) == 0:
                    time.sleep(10)
                    print("Sleeping for 10 seconds")
                elif users == None:
                    time.sleep(10)
                    print("Sleeping for 10 seconds")
                print(f"Found {len(users)} users")
                for user in users:
                    try: 
                        user_formated = str(user.text).split()
                        for i in user_formated:
                            at = "@"
                            data = ''
                            if i.startswith(at):
                                data = i.replace("@", "")
                                time.sleep(3)
                                self.driver.execute_script("window.open('');")
                                self.driver.switch_to.window(self.driver.window_handles[1])
                                self.driver.get(f"https://twitter.com/{data}")
                                print(f"user: {data}")
                                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]")))
                                followers = self.driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]')
                                for follower in followers:
                                    print(follower.text)
                                    if "Followers" in follower.text:
                                        follower_count = None
                                        if 'K' in follower.text:
                                            follower2 = follower.text.replace("Followers", "")
                                            follower_count = follower2.replace("K", "000")
                                        if 'M' in follower.text:
                                            follower2 = follower.text.replace("Followers", "")
                                            follower_count = follower2.replace("M", "000000")
                                        if follower_count != None:
                                            follower_count_formated = follower_count.replace(".", "")
                                            follower_count2 = int(follower_count_formated)
                                            print(f"Found {follower_count2}")
                                            if follower_count2 > 100000:
                                                with open("followers.txt", "a") as f:
                                                    f.write(f"{data}\n")
                                                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-4rbku5.css-18t94o4.css-901oao.r-1bwzh9t.r-1loqt21.r-xoduu5.r-1q142lx.r-1w6e6rj.r-37j5jr.r-a023e6.r-16dba41.r-9aw3ui.r-rjixqe.r-bcqeeo.r-3s2u2q.r-qvutc0")))
                                                last_tweet = self.driver.find_elements(By.CSS_SELECTOR, ".css-4rbku5.css-18t94o4.css-901oao.r-1bwzh9t.r-1loqt21.r-xoduu5.r-1q142lx.r-1w6e6rj.r-37j5jr.r-a023e6.r-16dba41.r-9aw3ui.r-rjixqe.r-bcqeeo.r-3s2u2q.r-qvutc0")
                                                pinned_tweet = self.driver.find_elements(By.CSS_SELECTOR, ".css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
                                                if pinned_tweet != None:
                                                    print("pinned tweet found, searching for last tweet")
                                                    for tweet, pin in zip(last_tweet, pinned_tweet):
                                                        if pin.text != None:
                                                            print(f"pinned tweet found, skipping")
                                                            pass
                                                        elif pin.text == None:
                                                            print(f"last tweet found, scraping")
                                                            print(tweet.text)
                                                else:
                                                    print("no pinned tweet found, searching for last tweet")
                                                    tweet_data = last_tweet[0].text
                                                    print(tweet_data)

                                                get_users = self.client.get_user(username=data, user_auth=True, user_fields="public_metrics")
                                                responselist= str(get_users).split()
                                                for word in responselist:
                                                    if word.startswith("id="):
                                                        id=''
                                                        for s in word:
                                                            if s.isdigit():
                                                                id+=s
                                                        get_tweets = self.client.get_users_tweets(id=id, tweet_fields="public_metrics", max_results=10, user_auth=True)
                                                        get_tweets_formatted = str(get_tweets).split()
                                                        try:
                                                            for word in get_tweets_formatted:
                                                                if word.startswith("id="):
                                                                    id2=''
                                                                    for s in word:
                                                                        if s.isdigit():
                                                                            id2+=s
                                                                    print(id2)
                                                                    self.client.create_tweet(text="Nice tweet!! Love your content.", user_auth=True, in_reply_to_tweet_id=id2)
                                                                    time.sleep(3)
                                                        except:
                                                            print("Erro trying to reply to tweet")
                                                self.driver.close()
                                                self.driver.switch_to.window(self.driver.window_handles[0])
                    except StaleElementReferenceException:
                        time.sleep(3)
                        print(f"going for exception")
                        

                        #self.driver.get(f"https://twitter.com/search?q={self.query}&src=typed_query")
                print("quiting...")
                self.driver.quit()
                break
            except:
                print("Too many requests, waiting 5 minutes...")
                time.sleep(300)
                print("restarting...")

    def ScrapeWithMatches(self, content: list):
        while True:
            print(content)
            try:
                for datasat in content:
                    # self.Login()
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "r-30o5oe")))
                    inp1 = self.driver.find_element(By.CLASS_NAME, "r-30o5oe")
                    inp1.click()
                    inp1.send_keys(self.query)
                    inp1.send_keys(Keys.RETURN)
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-1dbjc4n")))
                    tweets = self.driver.find_elements(By.CLASS_NAME, "css-1dbjc4n")
                    time.sleep(10)
                    print("Sleeping for 10 seconds")
                    users = self.driver.find_elements(By.CSS_SELECTOR, ".css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
                    if len(users) == 0:
                        time.sleep(10)
                        print("Sleeping for 10 seconds")
                    elif users == None:
                        time.sleep(10)
                        print("Sleeping for 10 seconds")
                    print(f"Found {len(users)} users")
                    for user in users:
                        try: 
                            user_formated = str(user.text).split()
                            for i in user_formated:
                                at = "@"
                                data = ''
                                if i.startswith(at):
                                    data = i.replace("@", "")
                                    time.sleep(3)
                                    self.driver.execute_script("window.open('');")
                                    self.driver.switch_to.window(self.driver.window_handles[1])
                                    self.driver.get(f"https://twitter.com/{data}")
                                    print(f"user: {data}")
                                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-4rbku5.css-18t94o4.css-901oao.r-1nao33i.r-1loqt21.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-qvutc0")))
                                    followers = self.driver.find_elements(By.CSS_SELECTOR, '.css-4rbku5.css-18t94o4.css-901oao.r-1nao33i.r-1loqt21.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-qvutc0')
                                    for follower in followers:
                                        print(follower.text)
                                        if "Followers" in follower.text:
                                            follower_count = None
                                            if 'K' in follower.text:
                                                follower2 = follower.text.replace("Followers", "")
                                                follower_count = follower2.replace("K", "000")
                                            if 'M' in follower.text:
                                                follower2 = follower.text.replace("Followers", "")
                                                follower_count = follower2.replace("M", "000000")
                                            if follower_count != None:
                                                follower_count_formated = follower_count.replace(".", "")
                                                follower_count2 = int(follower_count_formated)
                                                print(f"Found {follower_count2}")
                                                if follower_count2 < 100000:
                                                    print("Not enough followers")
                                                    pass
                                                if follower_count2 > 100000:
                                                    with open("followers.txt", "a") as f:
                                                        f.write(f"{data}\n")
                                                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-4rbku5.css-18t94o4.css-901oao.r-1bwzh9t.r-1loqt21.r-xoduu5.r-1q142lx.r-1w6e6rj.r-37j5jr.r-a023e6.r-16dba41.r-9aw3ui.r-rjixqe.r-bcqeeo.r-3s2u2q.r-qvutc0")))
                                                    last_tweet = self.driver.find_elements(By.CSS_SELECTOR, ".css-4rbku5.css-18t94o4.css-901oao.r-1bwzh9t.r-1loqt21.r-xoduu5.r-1q142lx.r-1w6e6rj.r-37j5jr.r-a023e6.r-16dba41.r-9aw3ui.r-rjixqe.r-bcqeeo.r-3s2u2q.r-qvutc0")
                                                    pinned_tweet = self.driver.find_elements(By.CSS_SELECTOR, ".css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
                                                    if pinned_tweet != None:
                                                        print("pinned tweet found, searching for last tweet")
                                                        for tweet, pin in zip(last_tweet, pinned_tweet):
                                                            if pin.text != None:
                                                                print(f"pinned tweet found, skipping")
                                                                pass
                                                            elif pin.text == None:
                                                                print(f"last tweet found, scraping")
                                                                print(tweet.text)
                                                    else:
                                                        print("no pinned tweet found, searching for last tweet")
                                                        tweet_data = last_tweet[0].text
                                                        print(tweet_data)
                                                    time.sleep(3)
                                                    get_users = self.client.get_user(username=data, user_fields="public_metrics", user_auth=True)
                                                    responselist= str(get_users).split()
                                                    for word in responselist:
                                                        if word.startswith("id="):
                                                            id=''
                                                            for s in word:
                                                                if s.isdigit():
                                                                    id+=s
                                                            time.sleep(3)
                                                            get_tweets = self.client.get_users_tweets(id=id, tweet_fields="public_metrics", max_results=5, user_auth=True)
                                                            get_tweets_formatted = str(get_tweets).split()
                                                            try:
                                                                for word in get_tweets_formatted:
                                                                    if word.startswith("id="):
                                                                        id2=''
                                                                        for s in word:
                                                                            if s.isdigit():
                                                                                id2+=s
                                                                        self.client.create_tweet(text=datasat, in_reply_to_tweet_id=id2)
                                                                        print(f"Replied to tweet {id2}")
                                                                        time.sleep(3)
                                                            except:
                                                                print("Erro trying to reply to tweet")
                                                    self.driver.close()
                                                    self.driver.switch_to.window(self.driver.window_handles[0])
                        except StaleElementReferenceException:
                            time.sleep(3)
                            print(f"going for exception")
                            pass

                    print("waiting 3 seconds to refresh")
                    time.sleep(3)
                    pass
                    print("Failed, waiting 2 minutes to quit")
                    time.sleep(120)
                    print("quiting...")
                    self.driver.quit()
                    break
            except:
                print("Failed, waiting 2 minutes to quit")
                time.sleep(120)
                continue


    def Login(self, username, password):
        try:
            self.driver.get("https://twitter.com/login")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "r-30o5oe")))
            email = self.driver.find_element(By.CLASS_NAME, "r-30o5oe")
            email.click()
            email.send_keys(username)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-901oao")))
            btn_sbn_1 = self.driver.find_element(By.CLASS_NAME, "css-901oao")
            btn_sbn_1.click()
            print("clicked, waiting for password")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[1]/a/div")))
            btn_sbn_2 = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[1]/a/div")
            btn_sbn_2.click()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "r-30o5oe")))
            email1 = self.driver.find_element(By.CLASS_NAME, "r-30o5oe")
            email1.click()
            email1.send_keys(username)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div")))
            btn_sbn_3 = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div")
            btn_sbn_3.click()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")))
            inp1 = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")
            inp1.click()
            inp1.send_keys(password)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div")))
            btn1 = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div")
            btn1.click()
            pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
            print("logged in")
        except:
            print("You are already loged in")
    def test(self, content, topic):
        while True:
            print(content)
            print("Starting to test")
            try:
                for datasat in content:
                    # self.Login()
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "r-30o5oe")))
                    inp1 = self.driver.find_element(By.CLASS_NAME, "r-30o5oe")
                    inp1.click()
                    inp1.send_keys(topic)
                    inp1.send_keys(Keys.RETURN)
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-1dbjc4n")))
                    tweets = self.driver.find_elements(By.CLASS_NAME, "css-1dbjc4n")
                    time.sleep(10)
                    print("Sleeping for 10 seconds")
                    users = self.driver.find_elements(By.CSS_SELECTOR, ".css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
                    if len(users) == 0:
                        time.sleep(10)
                        print("Sleeping for 10 seconds")
                    elif users == None:
                        time.sleep(10)
                        print("Sleeping for 10 seconds")
                    print(f"Found {len(users)} users")
                    for user in users:
                        try: 
                            user_formated = str(user.text).split()
                            for i in user_formated:
                                at = "@"
                                data = ''
                                if i.startswith(at):
                                    data = i.replace("@", "")
                                    time.sleep(3)
                                    self.driver.execute_script("window.open('');")
                                    self.driver.switch_to.window(self.driver.window_handles[1])
                                    self.driver.get(f"https://twitter.com/{data}")
                                    print(f"user: {data}")
                                    with open("users.txt", "r") as f:
                                        if data in f.read():
                                            print("User already in file")
                                            self.driver.close()
                                            self.driver.switch_to.window(self.driver.window_handles[0])
                                        elif data not in f.read():
                                            with open("users.txt", "a") as f:
                                                f.write(f"{data}\n")
                                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]")))
                                    followers = self.driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]')
                                    for follower in followers:
                                        print(follower.text)
                                        try:
                                            if "Followers" in follower.text:
                                                follower_count = None
                                                if 'K' in follower.text:
                                                    follower2 = follower.text.replace("Followers", "")
                                                    follower_count = follower2.replace("K", "00")
                                                if 'M' in follower.text:
                                                    follower2 = follower.text.replace("Followers", "")
                                                    follower_count = follower2.replace("M", "000000")
                                                if follower_count == None:
                                                    print("Does not meet requirements")
                                                    self.driver.close()
                                                    self.driver.switch_to.window(self.driver.window_handles[0])
                                                    pass
                                                if follower_count != None:
                                                    follower_count_formated = follower_count.replace(".", "")
                                                    follower_count2 = int(follower_count_formated)
                                                    print(f"Found {follower_count2}")
                                                    if follower_count2 < 100000:
                                                        print("Not enough followers")
                                                        self.driver.close()
                                                        self.driver.switch_to.window(self.driver.window_handles[0])
                                                        pass
                                                    if follower_count2 > 100000:
                                                        with open("followers.txt", "a") as f:
                                                            f.write(f"{data}\n")
                                                        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-4rbku5.css-18t94o4.css-901oao.r-1bwzh9t.r-1loqt21.r-xoduu5.r-1q142lx.r-1w6e6rj.r-37j5jr.r-a023e6.r-16dba41.r-9aw3ui.r-rjixqe.r-bcqeeo.r-3s2u2q.r-qvutc0")))
                                                        last_tweet = self.driver.find_elements(By.CSS_SELECTOR, ".css-4rbku5.css-18t94o4.css-901oao.r-1bwzh9t.r-1loqt21.r-xoduu5.r-1q142lx.r-1w6e6rj.r-37j5jr.r-a023e6.r-16dba41.r-9aw3ui.r-rjixqe.r-bcqeeo.r-3s2u2q.r-qvutc0")
                                                        pinned_tweet = self.driver.find_elements(By.CSS_SELECTOR, ".css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
                                                        if pinned_tweet != None:
                                                            print("pinned tweet found, searching for last tweet")
                                                            for tweet, pin in zip(last_tweet, pinned_tweet):
                                                                if pin.text != None:
                                                                    print(f"pinned tweet found, skipping")
                                                                    pass
                                                                elif pin.text == None:
                                                                    print(f"last tweet found, scraping")
                                                                    print(tweet.text)
                                                        else:
                                                            print("no pinned tweet found, searching for last tweet")
                                                            tweet_data = last_tweet[0].text
                                                            print(tweet_data)
                                                        time.sleep(3)
                                                        print("god")
                                                        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div[1]")))
                                                        comment = self.driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div[1]")
                                                        print("Wup Wup")
                                                        for i in comment:
                                                            i.click()
                                                            print("Done")
                                                            print("Nice")
                                                            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div")))
                                                            comment_txt = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div")
                                                            actions = ActionChains(self.driver)
                                                            comment_txt.click()
                                                            comment_txt.send_keys(datasat)
                                                            btn_one = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]")
                                                            btn_one.click()
                                                            time.sleep(10)
                                                        self.driver.close()
                                                        self.driver.switch_to.window(self.driver.window_handles[0])
                                        except Exception as e:
                                            print(f"Error: {e}")
                                            pass
                        except StaleElementReferenceException:
                            time.sleep(3)
                            print(f"going for exception")
                            pass

                    print("waiting 3 seconds to refresh")
                    time.sleep(3)
                    pass
                    print("Failed, waiting 2 minutes to quit")
                    time.sleep(120)
                    print("quiting...")
                    self.driver.quit()
                    break
            except Exception as e:
                print("Failed, waiting 2 minutes to restart")
                print(f"Error: {e}")
                break




class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Form1")
        self.geometry("800x450")

        self.GetMathData = tk.IntVar()

        # Dropdown menu
        self.menu_var = tk.StringVar(self)
        self.menu_var.set("Menu")  # default value

        self.dropdown_menu = tk.OptionMenu(self, self.menu_var, "Home", "Log In", "License", "Console", "Help", command=self.on_select)
        self.dropdown_menu.pack()

        # Labels
        self.label1 = Label(self, text="")
        self.label1.place(x=80, y=46)

        self.label2 = Label(self, text="")
        self.label2.place(x=678, y=46)

        self.label3 = Label(self, text="", font=("MV Boli", 13))
        self.label3.place(x=12, y=97)

        # Button
        self.button1 = Button(self, text="activate", font=("MV Boli", 14), bg="white", command=self.button1_click)
        self.button1.place(x=710, y=27)

        # Textbox
        self.richtextbox2 = Text(self, font=("MV Boli", 13))
        self.richtextbox2.place(x=12, y=123, width=776, height=315)
        self.richtextbox2.insert("1.0", Helper().GetComments())

        # topic shooser
        self.topic = tk.Entry(self, font=("MV Boli", 13))
        self.topic.place(x=100, y=80, width=500, height=25)
        self.topic.insert(index=1, string=Helper().GetTopics())

        # topic label
        self.topic_label = Label(self, text="Topic:", font=("MV Boli", 13))
        self.topic_label.place(x=20, y=80)

        # Checkbox
        self.checkbox1 = Checkbutton(self, text="Match Content", font=("MV Boli", 13), variable=self.GetMathData, onvalue=1, offvalue=0)
        self.checkbox1.place(x=539, y=30)

        self.image = Image.open('logo.png')
        self.photo = ImageTk.PhotoImage(self.image)
        self.picture_label = Label(self, image=self.photo)
        self.picture_label.place(x=0, y=27)

    def button1_click(self):
        # Add your button click event here
        if self.richtextbox2.get("1.0", tk.END) == "":
            messagebox.showerror("Error", "Please enter a message")
        if self.richtextbox2.get("1.0", tk.END) != "":
            messagebox.showinfo("Your bot started!", "Get ready to get some sales!")
            if self.GetMathData.get() == 1:
                print("Match Content")
                data = str(self.richtextbox2.get("1.0", tk.END)).split()
                with open("topic.txt", "w") as f:
                    f.write(self.topic.get())
                with open("comments.txt", "r") as f:
                    if f.read()  == self.richtextbox2.get("1.0", tk.END):
                        print("Same Content")
                    elif f.read() != self.richtextbox2.get("1.0", tk.END):

                        Helper().SaveComments(self.richtextbox2.get("1.0", tk.END))
                ScrapeTweets().test(content=self.richtextbox2.get("1.0", tk.END), topic=self.topic.get())
            if self.GetMathData.get() == 0:
                print("Not Match Content")
                ScrapeTweets().test(content=self.richtextbox2.get("1.0", tk.END), topic=self.topic.get())
                with open("topic.txt", "w") as f:
                    f.write(self.topic.get())
    def on_select(self, selection):
        if selection == "Log In":
            self.Login()
        if selection == "License":
            self.License()
        if selection == "Console":
            self.Console()
        # Add other actions for other menu items here
    def Login(self):
        self.form2 = Form2()
    def License(self):
        self.form3 = Form3()
    def Console(self):
        self.form4 = Form4()
class Form2(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title('Form2')
        self.geometry("800x450")

        # Labels
        self.label1 = tk.Label(self, text='Log In', font=("MV Boli", 13))
        self.label1.place(x=107, y=80)

        self.label2 = tk.Label(self, text='Username', font=("MV Boli", 13))
        self.label2.place(x=23, y=146)

        self.label3 = tk.Label(self, text='Password', font=("MV Boli", 13))
        self.label3.place(x=23, y=261)

        self.label4 = tk.Label(self, text='API keys', font=("MV Boli", 13))
        self.label4.place(x=588, y=82)

        self.label5 = tk.Label(self, text='Bearer', font=("MV Boli", 13))
        self.label5.place(x=441, y=143)

        self.label6 = tk.Label(self, text='Access Token', font=("MV Boli", 13))
        self.label6.place(x=390, y=199)

        self.label7 = tk.Label(self, text='Access Token Secret', font=("MV Boli", 13))
        self.label7.place(x=326, y=258)

        self.label8 = tk.Label(self, text='Consumer Key', font=("MV Boli", 13))
        self.label8.place(x=380, y=332)

        self.label9 = tk.Label(self, text='Consumer Key Secret', font=("MV Boli", 13))
        self.label9.place(x=316, y=395)

        # Text Boxes
        self.username_entry = tk.Entry(self)
        self.username_entry.place(x=23, y=186, width=251)

        self.password_entry = tk.Entry(self)
        self.password_entry.place(x=23, y=287, width=251)

        self.bearer_entry = tk.Entry(self)
        self.bearer_entry.place(x=516, y=146, width=251)

        self.access_token_entry = tk.Entry(self)
        self.access_token_entry.place(x=516, y=199, width=251)

        self.access_token_secret_entry = tk.Entry(self)
        self.access_token_secret_entry.place(x=516, y=261, width=251)

        self.consumer_key_entry = tk.Entry(self)
        self.consumer_key_entry.place(x=516, y=332, width=251)

        self.consumer_key_secret_entry = tk.Entry(self)
        self.consumer_key_secret_entry.place(x=516, y=395, width=251)

        # Button
        self.submit_button = tk.Button(self, text='Submit', font=("MV Boli", 12), command=self.btn_click)
        self.submit_button.place(x=96, y=332, width=75, height=26)
    def btn_click(self):
        if self.username_entry.get() == "" or self.password_entry.get() == "" or self.bearer_entry.get() == "" or self.access_token_entry.get() == "" or self.access_token_secret_entry.get() == "" or self.consumer_key_entry.get() == "" or self.consumer_key_secret_entry.get() == "":
            messagebox.showerror("Error", "Please fill in all fields")
        # Add your button click event here
        if self.username_entry.get() != "" and self.password_entry.get() != "" and self.bearer_entry.get() != "" and self.access_token_entry.get() != "" and self.access_token_secret_entry.get() != "" and self.consumer_key_entry.get() != "" and self.consumer_key_secret_entry.get() != "":
            messagebox.showinfo("Done!", "Thanks for submitting!")
            with open("api.json", "w") as f:
                data = {
                    "bearer": self.bearer_entry.get(),
                    "access_token": self.access_token_entry.get(),
                    "access_token_secret": self.access_token_secret_entry.get(),
                    "consumer_key": self.consumer_key_entry.get(),
                    "consumer_key_secret": self.consumer_key_secret_entry.get()
                }
                json.dump(data, f)
            Helper().GetApiKey()
            ScrapeTweets().Login(self.username_entry.get(), self.password_entry.get())
            self.destroy()
class Form3(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title('Form3')
        self.geometry("452x218")

        # Menu
        self.menu = Menu(self)
        self.config(menu=self.menu)

        self.home_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Home", menu=self.home_menu)

        self.login_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Log In", menu=self.login_menu)

        self.license_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="License", menu=self.license_menu)

        self.console_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Console", menu=self.console_menu)

        self.help_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

        # Label
        self.label = Label(self, text='License Key', font=("MV Boli", 12))
        self.label.place(x=180, y=27)

        # Text Box
        self.text_box = Entry(self)
        self.text_box.place(x=11, y=90, width=433)

        # Button
        self.button = Button(self, text='Submit', font=("MV Boli", 12))
        self.button.place(x=203, y=140, width=75, height=30)

        # Picture
        # Note: Replace 'your_image.png' with the path to your image file
        self.image = Image.open('logo.png')
        self.photo = ImageTk.PhotoImage(self.image)
        self.picture_label = Label(self, image=self.photo)
        self.picture_label.place(x=0, y=27)

class Form4(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title('Form4')
        self.geometry("800x450")

        # Menu
        self.menu = Menu(self)
        self.config(menu=self.menu)

        self.home_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Home", menu=self.home_menu)

        self.login_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Log In", menu=self.login_menu)

        self.license_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="License", menu=self.license_menu)

        self.console_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Console", menu=self.console_menu)

        self.help_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

        # Label
        self.label = Label(self, text='Console', font=("MV Boli", 14))
        self.label.place(x=366, y=75)

        # Text Box
        self.text_box = Text(self)
        self.text_box.place(x=12, y=123, width=776, height=315)

        # Picture
        # Note: Replace 'your_image.png' with the path to your image file
        self.image = Image.open('logo.png')
        self.photo = ImageTk.PhotoImage(self.image)
        self.picture_label = Label(self, image=self.photo)
        self.picture_label.place(x=12, y=27)


if __name__ == "__main__":
    app = Application()
    app.mainloop()

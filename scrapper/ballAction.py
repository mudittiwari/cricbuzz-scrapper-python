import sys
import json
from classes.MatchCard import getLastBallAction 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

if len(sys.argv) > 1:
    options = Options()
    options.headless = True
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--tz=Asia/Kolkata")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    matchLink = sys.argv[1]
    print(json.dumps(getLastBallAction(matchLink,driver=driver), default=lambda o: o.__dict__, indent=4))
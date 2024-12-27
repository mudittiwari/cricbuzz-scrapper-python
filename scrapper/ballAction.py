import sys
import json
from classes.MatchCard import getLastBallAction 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def getBallAction(matchLink, lastOverBall):
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
    driver = webdriver.Chrome(options=options)
    data = getLastBallAction(matchLink,lastOverBall,driver=driver)
    file_path = "match_data.txt"
    content = f"Match Link: {matchLink}, Last Over Ball: {lastOverBall}, data :{data}\n"
    with open(file_path, "a") as file:
        file.write(content)
    return json.dumps(data, default=lambda o: o.__dict__, indent=4)

while True:
    message = socket.recv_json()
    if  message.get("task") == "getLastBallAction":
        jsonData = getBallAction(message.get("matchLink"), message.get("lastOverBall"))
        socket.send_json(jsonData)
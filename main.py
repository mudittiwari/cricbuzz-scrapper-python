import requests
from bs4 import BeautifulSoup
from classes.MatchCard import MatchCard,getMatchesInfo
url="https://www.cricbuzz.com/"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
r = requests.get(url,headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')



matchCardsUl = soup.find('ul', class_='cb-col cb-col-100 videos-carousal-wrapper cb-mtch-crd-rt-itm')
matchCardsList = matchCardsUl.find_all('li') if matchCardsUl else []

getMatchesInfo(matchCardsList);



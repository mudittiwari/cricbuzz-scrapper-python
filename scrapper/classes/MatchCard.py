from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import sys
import io

def suppress_print(func):
    def wrapper(*args, **kwargs):
        temp_stdout = sys.stdout
        sys.stdout = io.StringIO()
        result = func(*args, **kwargs)
        sys.stdout = temp_stdout
        return result
    return wrapper



class UpcomingMatchCard:
    def __init__(self, matchLink, team1, team2, matchType, matchTiming):
        self.matchLink = matchLink
        self.team1 = team1
        self.team2 = team2
        self.matchType = matchType
        self.matchTiming = matchTiming

    def __repr__(self):
        return (f"UpcomingMatchCard(match_link='{self.matchLink}', "
                f"team1='{self.team1}', team2='{self.team2}', "
                f"match_type='{self.matchType}', "
                f"match_timing='{self.matchTiming}')")
class RunningMatchCard:
    def __init__(self, matchLink, team1, team2, matchType, team1Players, team2Players):
        self.matchLink = matchLink
        self.team1 = team1
        self.team2 = team2
        self.matchType = matchType
        self.team1Players = team1Players
        self.team2Players = team2Players

    def __repr__(self):
        return (f"RunningMatchCard(matchLink='{self.matchLink}', "
                f"team1='{self.team1}', team2='{self.team2}', "
                f"matchType='{self.matchType}', "
                f"team2Players='{self.team2Players}', "
                f"team1Players='{self.team1Players}')")    

class CompletedMatchCard:
    def __init__(self, matchLink):
        self.matchLink = matchLink

    def __repr__(self):
        return (f"CompletedMatchCard(match_link='{self.matchLink}')")

@suppress_print
def getUpcomingMatchesInfo(matchCardsList,driver):
    matchesList=[]
    for item in matchCardsList:
        # print(item.get_attribute("innerHTML"))
        # print("\n\n\n")
        try:
            matchLinkElement = item.find_element(By.TAG_NAME, 'a')
            matchLink = matchLinkElement.get_attribute('href')
        except NoSuchElementException:
            print("Match link element not found, skipping this match. \n\n")
            continue
        
        try:
            matchTypeElement = item.find_element(By.CLASS_NAME, 'cb-card-match-format')
            matchType=driver.execute_script("return arguments[0].textContent;", matchTypeElement).strip()
        except NoSuchElementException:
            print("Match type element not found, skipping this match. \n\n")
            continue
        try:
            previewElement = item.find_element(By.CSS_SELECTOR, '.cb-ovr-flo.cb-mtch-crd-time.cb-font-12.cb-text-preview')
            # print(previewElement)
            previewText = driver.execute_script("return arguments[0].textContent;", previewElement).strip()
        except NoSuchElementException:
            print("Preview element not found, skipping this match. \n\n")
            continue
        if previewText.startswith("Today"):
            teamElements = item.find_elements(By.CLASS_NAME, 'cb-hmscg-bat-txt')
            if len(teamElements) >= 2:
                try:
                    spanElement1 = teamElements[0].find_element(By.TAG_NAME, 'span')
                    spanElement2 = teamElements[1].find_element(By.TAG_NAME, 'span')
                    team1 = driver.execute_script("return arguments[0].textContent;", spanElement1).strip()
                    team2 = driver.execute_script("return arguments[0].textContent;", spanElement2).strip()
                    matchCard = UpcomingMatchCard(
                        matchLink=matchLink,
                        team1=team1,
                        team2=team2,
                        matchType=matchType,
                        matchTiming=previewText
                    )
                    matchesList.append(matchCard)
                except Exception as e:
                    print("An error occurred while fetching team names:", str(e))
            else:
                print("Could not find both teams using the 'cb-hmscg-bat-txt' class.")
    return matchesList


def getNextOver(currentOver: str) -> str:
    over, ball = map(int, currentOver.split('.'))
    ball += 1
    if ball > 6:
        ball = 1
        over += 1
    return f"{over}.{ball}"


# @suppress_print
def getLastBallAction(matchUrl, currentOver, driver):
    nextOverFound=False
    time.sleep(3)
    try:
        driver.get(matchUrl)
        lastBallAction = {
            "scoreDone": "N/A",
            "bowler": "Unknown",
            "batsman": "Unknown",
            "over": "Unknown"
        }
        try:
            xpathExpression = f"//div[contains(@class, 'cb-mat-mnu-wrp') and text()='{currentOver}']"
            xPathNextOverExpression = f"//div[contains(@class, 'cb-mat-mnu-wrp') and text()='{getNextOver(currentOver)}']"
            recentOverContent = driver.find_element(By.XPATH, xpathExpression)
            recentOverParent = recentOverContent.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
            try:
                precedingSiblingRecentOverContent = driver.find_element(By.XPATH, xPathNextOverExpression)
                commentarySource = precedingSiblingRecentOverContent.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
                nextOverFound=True
            except Exception as e:
                commentarySource = recentOverParent
            precedingSiblings = commentarySource.find_elements(By.XPATH, "./preceding-sibling::*")
            filteredSiblings = []
            for sibling in precedingSiblings:
                try:
                    recentOverContentFromSource = sibling.find_element(By.CSS_SELECTOR, '.cb-mat-mnu-wrp.cb-ovr-num')
                    filteredSiblings.append(sibling)
                except:
                    continue
            numberOfPrecedingSiblings = len(filteredSiblings)
            if not nextOverFound:
                siblingToSearch=filteredSiblings[-1]
                recentOverContentFromSource = siblingToSearch.find_element(By.CSS_SELECTOR, '.cb-mat-mnu-wrp.cb-ovr-num')
                recentOverContentText = driver.execute_script("return arguments[0].textContent;", recentOverContentFromSource).strip()
                if recentOverContent == "0.1":
                    commentarySource=siblingToSearch
            try:
                recentOverContentFromSource = commentarySource.find_element(By.CSS_SELECTOR, '.cb-mat-mnu-wrp.cb-ovr-num')
                recentOverContentText = driver.execute_script("return arguments[0].textContent;", recentOverContentFromSource).strip()
            except Exception as e:
                recentOverContentText = ""
            try:
                recentCommentaryContent = commentarySource.find_element(By.CSS_SELECTOR, 'p.cb-com-ln')
                recentCommentaryContentText = driver.execute_script("return arguments[0].textContent;", recentCommentaryContent).strip()
            except Exception as e:
                recentCommentaryContentText = ""
        
        except Exception as e:
            recentOverContentFromSource = driver.find_element(By.CSS_SELECTOR, '.cb-mat-mnu-wrp.cb-ovr-num')
            recentOverContentText = driver.execute_script("return arguments[0].textContent;", recentOverContentFromSource).strip()
            recentCommentaryContent = driver.find_element(By.CSS_SELECTOR, 'p.cb-com-ln')
            recentCommentaryContentText = driver.execute_script("return arguments[0].textContent;", recentCommentaryContent).strip()
        try:
            recentCommentarySplitList = recentCommentaryContentText.split(',')
            playersInvolvedStringList = recentCommentarySplitList[0].split('to')
            bowler = playersInvolvedStringList[0].strip() if len(playersInvolvedStringList) > 0 else "Unknown"
            batsman = playersInvolvedStringList[1].strip() if len(playersInvolvedStringList) > 1 else "Unknown"
        except Exception as e:
            bowler = "Unknown"
            batsman = "Unknown"
        try:
            recentScoreContainer = driver.find_element(By.CSS_SELECTOR, 'div.cb-min-rcnt')
            recentScoreSpan = recentScoreContainer.find_elements(By.TAG_NAME, "span")[1]
            recentScoreSpanText = driver.execute_script("return arguments[0].textContent;", recentScoreSpan).strip()
            file_path = "match_data.txt"
            with open(file_path, "a") as file:
                file.write(recentScoreSpanText)
            cleanedList = [element.strip('|') for item in recentScoreSpanText.split() for element in item.split() if element.strip('|')]
        except Exception as e:
            recentScoreSpanText = ""
        if 'numberOfPrecedingSiblings' in locals():
            lastBallAction = {
                "scoreDone": cleanedList[-(numberOfPrecedingSiblings+1)].strip() if recentScoreSpanText else "N/A",
                "bowler": bowler,
                "batsman": batsman,
                "over": recentOverContentText
            }
        else:
            lastBallAction = {
                "scoreDone": cleanedList[-1].strip() if recentScoreSpanText else "N/A",
                "bowler": bowler,
                "batsman": batsman,
                "over": recentOverContentText
            }
    except Exception as e:
        lastBallAction = {
            "scoreDone": "N/A",
            "bowler": "Unknown",
            "batsman": "Unknown",
            "over": "Unknown"
        }

    return lastBallAction






@suppress_print
def getSquadsUrl(liveScoresUrl):
    return liveScoresUrl.replace("live-cricket-scores", "cricket-match-squads")
    
@suppress_print
def fetchSquads(liveScoresUrl, driver):
    try:
        squadsUrl = getSquadsUrl(liveScoresUrl)
        driver.get(squadsUrl)
        time.sleep(3)
        squadsContainer = driver.find_element(By.CSS_SELECTOR, 'div.cb-col.cb-col-67.cb-sqds-lft-col')
        teamHeaders = squadsContainer.find_element(By.CLASS_NAME, 'cb-teams-hdr')
        leftSquad = squadsContainer.find_element(By.CSS_SELECTOR, 'div.cb-col.cb-play11-lft-col').find_elements(By.CSS_SELECTOR, '.cb-player-card-left')
        rightSquad = squadsContainer.find_element(By.CSS_SELECTOR, 'div.cb-col.cb-play11-rt-col').find_elements(By.CSS_SELECTOR, '.cb-player-card-right')

        teamsInfo = {}
        team1List = []
        team2List = []
        for item in leftSquad:
            try:
                playerName = item.find_element(By.CSS_SELECTOR, '.cb-player-name-left').text.split('\n')[0]
                team1List.append(playerName)
            except Exception as e:
                print(f"Error extracting player from left squad: {e}")
        for item in rightSquad:
            try:
                playerName = item.find_element(By.CSS_SELECTOR, '.cb-player-name-right').text.split('\n')[0]
                team2List.append(playerName)
            except Exception as e:
                print(f"Error extracting player from right squad: {e}")
        try:
            teamsInfo[teamHeaders.text.split('\n')[0]] = team1List
            teamsInfo[teamHeaders.text.split('\n')[1]] = team2List
            return teamsInfo
        except Exception as e:
            print(f"Error extracting team names: {e}")

    except Exception as e:
        print(f"An error occurred while fetching squads: {e}")

@suppress_print
def getRunningMatchesInfo(matchCardsList, driver):
    matchesList = []
    for item in matchCardsList:
        try:
            matchStateElement = item.find_element(By.CLASS_NAME, 'cb-mtch-crd-state')
            matchStateClass = matchStateElement.get_attribute('class')
            if 'cb-text-apple-red' not in matchStateClass:
                continue
            matchLinkElement = item.find_element(By.TAG_NAME, 'a')
            matchLink = matchLinkElement.get_attribute('href')
        except NoSuchElementException:
            print("Match link or state element not found, skipping this match. \n\n")
            continue

        try:
            matchTypeElement = item.find_element(By.CLASS_NAME, 'cb-card-match-format')
            matchType = driver.execute_script("return arguments[0].textContent;", matchTypeElement).strip()
        except NoSuchElementException:
            print("Match type element not found, skipping this match. \n\n")
            continue

        try:
            team1Element = item.find_element(By.CLASS_NAME, 'cb-hmscg-bat-txt').find_element(By.TAG_NAME, 'span')
            team2Element = item.find_element(By.CLASS_NAME, 'cb-hmscg-bwl-txt').find_element(By.TAG_NAME, 'span')
            team1 = driver.execute_script("return arguments[0].textContent;", team1Element).strip()
            team2 = driver.execute_script("return arguments[0].textContent;", team2Element).strip()
            matchCard = RunningMatchCard(matchLink, team1, team2, matchType, [], [])
            matchesList.append(matchCard)
        except NoSuchElementException:
            print("Error finding teams of the match. \n\n")
            continue

    return matchesList

@suppress_print
def getCompletedMatchesInfo(matchCardsList,driver):
    matchesList=[]
    for item in matchCardsList:
        try:
            matchLinkElement = item.find_element(By.TAG_NAME, 'a')
            matchLink = matchLinkElement.get_attribute('href')
        except NoSuchElementException:
            print("Match link element not found, skipping this match. \n\n")
            continue
        try:
            previewElement = item.find_element(By.CSS_SELECTOR, '.cb-ovr-flo.cb-mtch-crd-state.cb-font-12.cb-text-preview')
            # print(previewElement)
            previewText = driver.execute_script("return arguments[0].textContent;", previewElement).strip()
        except NoSuchElementException:
            print("Preview element not found, skipping this match. \n\n")
            continue
        if previewText.count("Won")>0:
            matchCard=CompletedMatchCard(matchLink)
            matchesList.append(matchCard)
    return matchesList

@suppress_print
def getUpcomingMatchesTossUpdate(matchCardsList,driver):
    matchesList=[]
    for item in matchCardsList:
        # print(item.get_attribute("innerHTML"))
        # print("\n\n\n")
        try:
            matchLinkElement = item.find_element(By.TAG_NAME, 'a')
            matchLink = matchLinkElement.get_attribute('href')
        except NoSuchElementException:
            print("Match link element not found, skipping this match. \n\n")
            continue
        
        try:
            matchTypeElement = item.find_element(By.CLASS_NAME, 'cb-card-match-format')
            matchType=driver.execute_script("return arguments[0].textContent;", matchTypeElement).strip()
        except NoSuchElementException:
            print("Match type element not found, skipping this match. \n\n")
            continue
        try:
            previewElement = item.find_element(By.CSS_SELECTOR, '.cb-ovr-flo.cb-mtch-crd-state.cb-font-12.cb-text-preview')
            # print(previewElement)
            previewText = driver.execute_script("return arguments[0].textContent;", previewElement).strip()
        except NoSuchElementException:
            print("Preview element not found, skipping this match. \n\n")
            continue
        if previewText.count("opt"):
            teamElements = item.find_elements(By.CLASS_NAME, 'cb-hmscg-bat-txt')
            if len(teamElements) >= 2:
                try:
                    spanElement1 = teamElements[0].find_element(By.TAG_NAME, 'span')
                    spanElement2 = teamElements[1].find_element(By.TAG_NAME, 'span')
                    team1 = driver.execute_script("return arguments[0].textContent;", spanElement1).strip()
                    team2 = driver.execute_script("return arguments[0].textContent;", spanElement2).strip()
                    matchCard = UpcomingMatchCard(
                        matchLink=matchLink,
                        team1=team1,
                        team2=team2,
                        matchType=matchType,
                        matchTiming=previewText
                    )
                    matchesList.append(matchCard)
                except Exception as e:
                    print("An error occurred while fetching team names:", str(e))
            else:
                print("Could not find both teams using the 'cb-hmscg-bat-txt' class.")
    return matchesList
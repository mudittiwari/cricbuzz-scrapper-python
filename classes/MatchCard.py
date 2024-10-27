class MatchCard:
    def __init__(self, matchLink, team1, team2, matchType, matchTiming):
        self.matchLink = matchLink
        self.team1 = team1
        self.team2 = team2
        self.matchType = matchType
        self.matchTiming = matchTiming

    def __repr__(self):
        return (f"MatchCard(match_link='{self.matchLink}', "
                f"team1='{self.team1}', team2='{self.team2}', "
                f"match_type='{self.matchType}', "
                f"match_timing='{self.matchTiming}')")


def getMatchesInfo(matchCardsList):
    for item in matchCardsList:
        matchLink = item.find('a')['href']
        fullMatchLink = f"https://www.cricbuzz.com{matchLink}"
        team1 = item.find('div', class_='cb-hmscg-bat-txt').find('span').text
        print(team1)
        team2 = item.find('div', class_='cb-hmscg-bwl-txt').find('span').text
        matchType = item.find('div', class_='cb-card-match-format').text.strip()
        matchTiming = item.find('div', class_='cb-col-90').text.strip()
        resultElement = item.find('div', class_='cb-mtch-crd-state')
        resultText = resultElement.text.strip() if resultElement else ""
        if resultText.startswith("Today"):
            matchCard = MatchCard(
                match_link=fullMatchLink,
                team1=team1,
                team2=team2,
                match_type=matchType,
                match_timing=matchTiming
            )
            print(matchCard)
        else:
            print("Match result does not start with 'Today', rejecting the match.")
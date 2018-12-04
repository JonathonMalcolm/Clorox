from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np

def find_team(teams, cur_index, team):
    # cur_date = teams[cur_index][2]
    for i in range(cur_index, cur_index+20):
        if i >= teams.shape[0]:
            break
        if teams[i][0] == team:
            return i
    for j in [cur_index-1, cur_index-2, cur_index-3, cur_index-4, cur_index-5, cur_index-6, cur_index-7, cur_index-8, cur_index-9, cur_index-10, cur_index-11, cur_index-12, cur_index-13, cur_index-14, cur_index-15, cur_index-16, cur_index-17, cur_index-18, cur_index-19, cur_index-20]:
        if j < 0:
            break
        if teams[j][0] == team:
            return j
    print("ERROR HERE: Index: %d    Team: %s" % (cur_index, team))
    return 69696969

def convert_row_data(row):
    if row.contents[0].contents[0].text == "\xa0":
        return None
    wins = row.contents[0].contents[4].text
    loses = row.contents[0].contents[5].text
    ties = row.contents[0].contents[6].text
    ot_loses = row.contents[0].contents[7].text
    points = row.contents[0].contents[8].text
    goals_for = row.contents[0].contents[9].text
    goals_against = row.contents[0].contents[10].text
    shootout_wins = row.contents[0].contents[11].text
    shootout_loses = row.contents[0].contents[12].text
    shots_for = row.contents[0].contents[13].text
    shots_against = row.contents[0].contents[14].text
    ppg = row.contents[0].contents[15].text
    pp_opportunities = row.contents[0].contents[16].text
    pp_percentage = row.contents[0].contents[17].text
    times_shorthand = row.contents[0].contents[18].text
    pp_goals_against = row.contents[0].contents[19].text
    penalty_kill_percent = row.contents[0].contents[20].text
    fo_won = row.contents[0].contents[21].text
    fo_loss = row.contents[0].contents[22].text
    fo_win_percent = row.contents[0].contents[23].text

    return [float(wins),float(loses),float(ties),float(ot_loses),float(points),float(goals_for),float(goals_against),
            float(shootout_wins),float(shootout_loses),float(shots_for),float(shots_against),float(ppg),
            float(pp_opportunities),float(pp_percentage),float(times_shorthand),float(pp_goals_against),
            float(penalty_kill_percent),float(fo_won),float(fo_loss),float(fo_win_percent), 0, 0, 0]
# 0 here is for the date since


def convert_team_row_data(row):
    team_dict = {"Atlanta Flames": "AFM", "Anaheim Ducks": "ANA", "Arizona Coyotes": "ARI", "Atlanta Thrashers": "ATL",
                "Boston Bruins": "BOS", "Brooklyn Americans": "BRK", "Buffalo Sabres": "BUF",
                "Carolina Hurricanes": "CAR", "California Golden Seals": "CGS", "Calgary Flames": "CGY",
                "Chicago Blackhawks": "CHI", "Columbus Blue Jackets": "CBJ", "Cleveland Barons": "CLE",
                "Colorado Rockies": "CLR", "Colorado Avalanche": "COL", "Dallas Stars": "DAL",
                "Detroit Falcons": "DFL",  "Detroit Cougars": "DCG", "Detroit Red Wings": "DET",
                "Edmonton Oilers": "EDM", "Florida Panthers": "FLA", "Hamilton Tigers": "HAM",
                "Hartford Whalers": "HFD", "Kansas City Scouts": "KCS", "Los Angeles Kings": "LAK",
                "Minnesota Wild": "MIN", "Montreal Maroons": "MMR", "Minnesota North Stars": "MNS",
                "Montréal Canadiens": "MTL", "Montreal Wanderers": "MWN", "Nashville Predators": "NSH",
                "New Jersey Devils": "NJD", "New York Americans": "NYA", "New York Islanders": "NYI",
                "New York Rangers": "NYR", "Oakland Seals": "OAK", "Ottawa Senators": "OTT",
                "Philadelphia Flyers": "PHI", "Phoenix Coyotes": "PHX", "Pittsburgh Pirates": "PIR",
                "Pittsburgh Penguins": "PIT", "Philadelphia Quakers": "QUA", "Quebec Nordiques": "QUE",
                "Quebec Bulldogs": "QBD", "Ottawa Senators (original)": "SEN", "San Jose Sharks": "SJS",
                "St. Louis Eagles": "SLE", "St. Louis Blues": "STL", "Toronto Arenas": "TAN",
                "Tampa Bay Lightning": "TBL", "Toronto Maple Leafs": "TOR", "Toronto St. Patricks": "TSP",
                "Vancouver Canucks": "VAN", "Vegas Golden Knights": "VGK", "Winnipeg Jets (original)": "WIN",
                "Winnipeg Jets": "WPG", "Washington Capitals": "WSH"}
    # Teams
    if row.contents[0].contents[0].text == "\xa0":
        return None

    team1 = team_dict[row.contents[0].contents[1].text]
    team2 = row.contents[0].contents[2].text[-3:]
    win = row.contents[0].contents[4].text
    if row.contents[0].contents[2].text[-5] == "s":
        home = 1
    else:
        home = 0

    date = row.contents[0].contents[2].text[:10]
    return [team1, team2, date, home, win]

def parse_date(string):
    year = int(string[:4])
    month = int(string[5:7])
    day = int(string[8:10])
    return (year - 1990) * 365 + (month * 30) + day


def sum_stats(table, table_stat, team):
    count = 0
    sumRow = np.zeros(table_stat.shape[1])
    old_date = parse_date(table[0][2])
    win_streak = 0
    lose_streak = 0
    for i in range(table.shape[0]):
        team_row = table[i]
        stat_row = table_stat[i]

        if team_row[0] == team:
            count = count + 1
            sumRow = np.sum([sumRow, stat_row], axis=0)
            table_stat[i] = sumRow / count
            cur_date = parse_date(team_row[2])
            time_since = cur_date - old_date
            old_date = cur_date
            table_stat[i][20] = time_since
            table_stat[i][21] = win_streak
            table_stat[i][22] = lose_streak
            if int(team_row[4]) == 1:
                win_streak = win_streak + 1
                lose_streak = 0
            else:
                lose_streak = lose_streak + 1
                win_streak = 0

    return table_stat




#url = 'http://www.nhl.com/stats/team?reportType=game&dateFrom=2017-10-04&dateTo=2018-04-08'
#url = 'http://www.nhl.com/stats/team?reportType=game&dateFrom=2015-10-07&dateTo=2016-04-10'
url = 'http://www.nhl.com/stats/team?reportType=game&dateFrom=2016-10-04&dateTo=2017-04-10'
browser = webdriver.Firefox()
browser.implicitly_wait(500)
browser.get(url)

python_button = browser.find_element_by_xpath("//div[@title='Game']")
python_button.click()
python_button = browser.find_element_by_xpath("//div[@title='Game']")
python_button.click()

soup = BeautifulSoup(browser.page_source, 'html.parser')
table = soup.find("div", class_="rt-tbody")

teams = []
team_stats = []
currentDate = ""
count = 1
# print(table.contents)
for row in table.children:
    converted_team_row = convert_team_row_data(row)
    converted_row = convert_row_data(row)
    if converted_team_row is None:
        break
    teams.append(converted_team_row)
    team_stats.append(converted_row)


while count <= 51:

    python_button = browser.find_element_by_xpath("//div[@class='-next']/button")
    python_button.click()

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    table = soup.find("div", class_="rt-tbody")

    count = count + 1

    for row in table.children:
        converted_team_row = convert_team_row_data(row)
        converted_row = convert_row_data(row)
        if converted_team_row is None:
            break
        teams.append(converted_team_row)
        team_stats.append(converted_row)

browser.quit()


# sum_stats(teams, "TOR")

team_array = np.asarray(teams)
stat_array = np.asarray(team_stats)

stat_array = sum_stats(team_array, stat_array, "AFM")
stat_array = sum_stats(team_array, stat_array, "ANA")
stat_array = sum_stats(team_array, stat_array, "ARI")
stat_array = sum_stats(team_array, stat_array, "ATL")
stat_array = sum_stats(team_array, stat_array, "BOS")
stat_array = sum_stats(team_array, stat_array, "BRK")
stat_array = sum_stats(team_array, stat_array, "BUF")
stat_array = sum_stats(team_array, stat_array, "CAR")
stat_array = sum_stats(team_array, stat_array, "CGS")
stat_array = sum_stats(team_array, stat_array, "CGY")
stat_array = sum_stats(team_array, stat_array, "CHI")
stat_array = sum_stats(team_array, stat_array, "CBJ")
stat_array = sum_stats(team_array, stat_array, "CLE")
stat_array = sum_stats(team_array, stat_array, "CLR")
stat_array = sum_stats(team_array, stat_array, "COL")
stat_array = sum_stats(team_array, stat_array, "DAL")
stat_array = sum_stats(team_array, stat_array, "DFL")
stat_array = sum_stats(team_array, stat_array, "DCG")
stat_array = sum_stats(team_array, stat_array, "DET")
stat_array = sum_stats(team_array, stat_array, "EDM")
stat_array = sum_stats(team_array, stat_array, "FLA")
stat_array = sum_stats(team_array, stat_array, "HAM")
stat_array = sum_stats(team_array, stat_array, "HFD")
stat_array = sum_stats(team_array, stat_array, "KCS")
stat_array = sum_stats(team_array, stat_array, "LAK")
stat_array = sum_stats(team_array, stat_array, "MIN")
stat_array = sum_stats(team_array, stat_array, "MMR")
stat_array = sum_stats(team_array, stat_array, "MNS")
stat_array = sum_stats(team_array, stat_array, "MTL")
stat_array = sum_stats(team_array, stat_array, "MWN")
stat_array = sum_stats(team_array, stat_array, "NSH")
stat_array = sum_stats(team_array, stat_array, "NJD")
stat_array = sum_stats(team_array, stat_array, "NYA")
stat_array = sum_stats(team_array, stat_array, "NYI")
stat_array = sum_stats(team_array, stat_array, "NYR")
stat_array = sum_stats(team_array, stat_array, "OAK")
stat_array = sum_stats(team_array, stat_array, "OTT")
stat_array = sum_stats(team_array, stat_array, "PHI")
stat_array = sum_stats(team_array, stat_array, "PHX")
stat_array = sum_stats(team_array, stat_array, "PIR")
stat_array = sum_stats(team_array, stat_array, "PIT")
stat_array = sum_stats(team_array, stat_array, "QUA")
stat_array = sum_stats(team_array, stat_array, "QUE")
stat_array = sum_stats(team_array, stat_array, "QBD")
stat_array = sum_stats(team_array, stat_array, "SEN")
stat_array = sum_stats(team_array, stat_array, "SJS")
stat_array = sum_stats(team_array, stat_array, "SLE")
stat_array = sum_stats(team_array, stat_array, "STL")
stat_array = sum_stats(team_array, stat_array, "TAN")
stat_array = sum_stats(team_array, stat_array, "TBL")
stat_array = sum_stats(team_array, stat_array, "TOR")
stat_array = sum_stats(team_array, stat_array, "TSP")
stat_array = sum_stats(team_array, stat_array, "VAN")
stat_array = sum_stats(team_array, stat_array, "VGK")
stat_array = sum_stats(team_array, stat_array, "WIN")
stat_array = sum_stats(team_array, stat_array, "WPG")
stat_array = sum_stats(team_array, stat_array, "WSH")

# make new array with differences per game
# winner - loser and have a column for home =1 or away = 0

# print(np.concatenate((team_array, stat_array), axis=1))

#np.savetxt("rawCumulativeData.csv", np.concatenate((team_array, stat_array), axis=1), delimiter=",", fmt="%s")


train_stats = []

for i in range(stat_array.shape[0]):
    team_row = team_array[i]
    stat_row = stat_array[i]
    win = int(team_row[4])

    if win == 1:
        win_team_index = i
        lose_team_index = find_team(team_array, i, team_row[1])
    else:
        win_team_index = find_team(team_array, i, team_row[1])
        lose_team_index = i

    if win_team_index == 69696969 or lose_team_index == 69696969:
        break

    home = int(team_row[3])
    days_since = stat_row[20]
    win_streak = stat_row[21]
    lose_streak = stat_row[22]
    if win == 1:
        wins = stat_array[win_team_index][0] - stat_array[lose_team_index][0]
        loses = stat_array[win_team_index][1] - stat_array[lose_team_index][1]
        ties = stat_array[win_team_index][2] - stat_array[lose_team_index][2]
        ot_loses = stat_array[win_team_index][3] - stat_array[lose_team_index][3]
        points = stat_array[win_team_index][4] - stat_array[lose_team_index][4]
        goals_for = stat_array[win_team_index][5] - stat_array[lose_team_index][5]
        goals_against = stat_array[win_team_index][6] - stat_array[lose_team_index][6]
        shootout_wins = stat_array[win_team_index][7] - stat_array[lose_team_index][7]
        shootout_loses = stat_array[win_team_index][8] - stat_array[lose_team_index][8]
        shots_for = stat_array[win_team_index][9] - stat_array[lose_team_index][9]
        shots_against = stat_array[win_team_index][10] - stat_array[lose_team_index][10]
        ppg = stat_array[win_team_index][11] - stat_array[lose_team_index][11]
        pp_opportunities = stat_array[win_team_index][12] - stat_array[lose_team_index][12]
        pp_percentage = stat_array[win_team_index][13] - stat_array[lose_team_index][13]
        times_shorthand = stat_array[win_team_index][14] - stat_array[lose_team_index][14]
        pp_goals_against = stat_array[win_team_index][15] - stat_array[lose_team_index][15]
        penalty_kill_percent = stat_array[win_team_index][16] - stat_array[lose_team_index][16]
        fo_won = stat_array[win_team_index][17] - stat_array[lose_team_index][17]
        fo_loss = stat_array[win_team_index][18] - stat_array[lose_team_index][18]
        fo_win_percent = stat_array[win_team_index][19] - stat_array[lose_team_index][19]
        days_since = stat_array[win_team_index][20] - stat_array[lose_team_index][20]
        win_streak = stat_array[win_team_index][21] - stat_array[lose_team_index][21]
        lose_streak = stat_array[win_team_index][22] - stat_array[lose_team_index][22]
    else:
        wins = stat_array[lose_team_index][0] - stat_array[win_team_index][0]
        loses = stat_array[lose_team_index][1] - stat_array[win_team_index][1]
        ties = stat_array[lose_team_index][2] - stat_array[win_team_index][2]
        ot_loses = stat_array[lose_team_index][3] - stat_array[win_team_index][3]
        points = stat_array[lose_team_index][4] - stat_array[win_team_index][4]
        goals_for = stat_array[lose_team_index][5] - stat_array[win_team_index][5]
        goals_against = stat_array[lose_team_index][6] - stat_array[win_team_index][6]
        shootout_wins = stat_array[lose_team_index][7] - stat_array[win_team_index][7]
        shootout_loses = stat_array[lose_team_index][8] - stat_array[win_team_index][8]
        shots_for = stat_array[lose_team_index][9] - stat_array[win_team_index][9]
        shots_against = stat_array[lose_team_index][10] - stat_array[win_team_index][10]
        ppg = stat_array[lose_team_index][11] - stat_array[win_team_index][11]
        pp_opportunities = stat_array[lose_team_index][12] - stat_array[win_team_index][12]
        pp_percentage = stat_array[lose_team_index][13] - stat_array[win_team_index][13]
        times_shorthand = stat_array[lose_team_index][14] - stat_array[win_team_index][14]
        pp_goals_against = stat_array[lose_team_index][15] - stat_array[win_team_index][15]
        penalty_kill_percent = stat_array[lose_team_index][16] - stat_array[win_team_index][16]
        fo_won = stat_array[lose_team_index][17] - stat_array[win_team_index][17]
        fo_loss = stat_array[lose_team_index][18] - stat_array[win_team_index][18]
        fo_win_percent = stat_array[lose_team_index][19] - stat_array[win_team_index][19]
        days_since = stat_array[lose_team_index][20] - stat_array[win_team_index][20]
        win_streak = stat_array[lose_team_index][21] - stat_array[win_team_index][21]
        lose_streak = stat_array[lose_team_index][22] - stat_array[win_team_index][22]

    newROW = [win, home, wins, loses, ot_loses, points, goals_for, goals_against, shootout_wins,
               shots_for, shots_against, ppg, pp_opportunities, pp_percentage, times_shorthand, pp_goals_against,
               penalty_kill_percent, fo_won, days_since, win_streak, lose_streak]

    # newROW = [win, home, wins, loses, ties, ot_loses, points, goals_for, goals_against, shootout_wins, shootout_loses,
    #           shots_for, shots_against, ppg, pp_opportunities, pp_percentage, times_shorthand, pp_goals_against,
    #           penalty_kill_percent, fo_won, fo_loss, fo_win_percent, days_since, win_streak, lose_streak]

    train_stats.append(newROW)

training_stats = np.asarray(train_stats)
#print(training_stats)
np.savetxt("trainingData_1617.csv", training_stats, delimiter=",", fmt="%.5f")

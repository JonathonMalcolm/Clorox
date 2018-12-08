from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt

row_dict = {"VGK": 1,"VAN": 2,"CGY " :3,"EDM" : 4,"SJS" : 5,"LAK" : 6,"MIN" : 7,"DAL" : 8,
"STL" : 9,"CBJ" : 10,"MTL" : 11,"BUF" : 12,"NJD" : 13,"OTT" :14,"TBL" :15,"DET" :16,"FLA" :17,
"COL" :18,"NSH" :19,"CAR" :20,"TOR" : 21,"CAP" :22,"NYI" :23,"BOS" :24,"ARI" :25,"CHI" :26,
"ANA" :27,"WPG" :28,"NYR" :29,"PHI" :30,"CHI" :31}

# import test data
model = load_model('modelbackup.h5')
X = np.loadtxt("X_dev.csv", delimiter=",")
Y = np.loadtxt("Y_dev.csv", delimiter=",")
n = X.shape[0] #length of dataset

def getData(hometeam, awayteam, array):
    m = array.shape[0]
    n = array.shape[1]
    index1 = row_dict[hometeam]
    index2 = row_dict[awayteam]
    homestats = array[m-index1,0:n]
    awaystats = array[m-index2,0:n]
    statsDiff = homestats - awaystats
    Q = getData(hometeam, awayteam, X)
    p = model.predict(Q)
    return p

def getBetAmount(bank_roll,team1,team2,home_bet,away_bet):
    pred = getData(team1, team2, X)

    # Calculation to Decide Bet Amount
    def Kelly_Crit(b, p):
        f = (p * (b + 1) - 1) / b
        return f

    home = Kelly_Crit(home_bet, pred)
    away = Kelly_Crit(away_bet, (1 - pred))
    max_bet = max(home, away);
    if max_bet > 0:
        #if we bet on the home team
        if max_bet == home:
           odds = home_bet
        else:
            odds = away_bet
    return (odds*bank_roll)

####################################################
#returns the amount of money won as the result of betting per game in an array
def Bet_Playoffs(money,team1,team2,home_bet,away_bet,winner):
    pred = getData(team1, team2, X)
    print("Prediction")
    print(pred)

    # Calculation to Decide Bet Amount
    def Kelly_Crit(b ,p):
       f =  (p*(b+1)-1)/b
       return f

    home = Kelly_Crit(home_bet,pred)
    away= Kelly_Crit(away_bet,(1-pred))
    max_bet = max(home,away);
    print("Max Bet")
    print(max_bet)

    #if we bet something
    if max_bet > 0:
        #if we bet on the home team
        if max_bet == home:
            team = 1
            odds = home_bet
        else:
            team = 0
            odds = away_bet

        if team == winner:
            money.append(money[-1]+(max_bet*money[-1])*odds)
        else:
            money.append(money[-1]-(max_bet*money[-1]))
    else:
        money.append(money[-1])

##################################################################
team1 = np.loadtxt('NHL_PlayOff_Series.csv', dtype='str', delimiter=',', usecols=(0), unpack=True)
team2 = np.loadtxt('NHL_PlayOff_Series.csv', dtype='str', delimiter=',', usecols=(1), unpack=True)
home_bet= np.loadtxt('NHL_PlayOff_Series.csv', dtype='float', delimiter=',', usecols=(2), unpack=True)
away_bet= np.loadtxt('NHL_PlayOff_Series.csv', dtype='float', delimiter=',', usecols=(3), unpack=True)
winner= np.loadtxt('NHL_PlayOff_Series.csv', dtype='int', delimiter=',', usecols=(4), unpack=True)
money = [1000]
for i in range(len(winner)):
    Bet_Playoffs(money,team1[i],team2[i],home_bet[i],away_bet[i],winner[i])

# Plotting
games = [i for i in range(len(money))]
for k in range(len(games)):
    plt.text(games[k], money[k], '('  + str(round(money[k])) + ')')
plt.title("Bank Roll vs Playoff Games")
plt.xlabel("Game")
plt.ylabel("BankRoll ")
plt.plot(games, money, 'r-o')
plt.show()

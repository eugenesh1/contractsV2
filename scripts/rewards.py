#!/usr/bin/python3

'''
start_block_number: 11243754 (1605197144)
end_block_number: 11291000 (1605822429)
'''

import csv
import numpy as np


def getUSDTValue(symbol, principal):
    ETHPrice = 506.11
    WBTCPrice = 16679
    LENDPrice = 0.6511
    KNCPrice = 0.952
    MKRPrice = 513.36
    BZRXPrice = 0.2129
    LINKPrice = 12.2396
    YFIPrice = 21116
    UNIPrice = 3.2299
    AAVEPrice = 59.158

    if symbol == 'ETH':
        return principal * ETHPrice
    elif (symbol == 'WBTC'):
        return principal * WBTCPrice
    elif (symbol == 'LEND'):
        return principal * LENDPrice
    elif (symbol == 'KNC'):
        return principal * KNCPrice
    elif (symbol == 'MKR'):
        return principal * MKRPrice
    elif (symbol == 'BZRX'):
        return principal * BZRXPrice
    elif (symbol == 'LINK'):
        return principal * LINKPrice
    elif (symbol == 'YFI'):
        return principal * YFIPrice
    elif (symbol == 'UNI'):
        return principal * UNIPrice
    elif (symbol == 'AAVE'):
        return principal * AAVEPrice
    elif (symbol == 'USDT' or symbol == 'USDC' or symbol == 'DAI'):
        return principal
    else:
        raise ValueError("unhandled symbol", symbol)


filePath = './query31.csv'
num_lines = sum(1 for line in open(filePath))
with open(filePath, newline='') as csvfile:

    transactions = csv.reader(csvfile, delimiter=',')
    next(transactions)  # skip header

    # Tom if you are going to change below you have to rerun sql
    lastWeekRewardBlock = 1605839741 
    thisWeekRewardBlockEnd = 1606422331  # block 11336208 

    prevUserAddress = 0
    prevBlockTime = 0

    totalPrincipalSumUntillLastWeekInUSDT = 0

    totalPrincipalSumOverTimeFromLastWeekInUSDT = 0

    overallResults = []

    #Prices in USDT

	# useraddress,loantoken,tokensymbol,block_time,index,paymenttype,newprincipaldecimal

    for row in transactions:
        useraddress = row[0]
        tokensymbol = row[1]

        newprincipaldecimal = np.around(float(row[2]), decimals=5)

        index = row[3]
        loantoken = row[4]
        paymenttype = row[5]
        block_time = int(row[6])

        if (prevUserAddress != useraddress or num_lines == transactions.line_num):  # count last result as well

            # totalPrincipalSumUntillLastWeekInUSDT = np.around(
            #     totalPrincipalSumUntillLastWeekInUSDT, decimals=2)

            # if (totalPrincipalSumUntillLastWeekInUSDT > 0):
            if (totalPrincipalSumOverTimeFromLastWeekInUSDT == 0 and totalPrincipalSumUntillLastWeekInUSDT > 0):
                # this week user didn't have any action but he has principal from last week
                timeBetweenActions = thisWeekRewardBlockEnd - block_time
                totalPrincipalSumOverTimeFromLastWeekInUSDT = totalPrincipalSumOverTimeFromLastWeekInUSDT + \
                    totalPrincipalSumUntillLastWeekInUSDT * timeBetweenActions

                print(prevUserAddress, totalPrincipalSumUntillLastWeekInUSDT,
                    totalPrincipalSumOverTimeFromLastWeekInUSDT)
                overallResults.append(
                    [prevUserAddress, totalPrincipalSumUntillLastWeekInUSDT, totalPrincipalSumOverTimeFromLastWeekInUSDT])
            elif (totalPrincipalSumOverTimeFromLastWeekInUSDT > 0):
                # extend untill end of the week
                timeBetweenActions = thisWeekRewardBlockEnd - block_time
                totalPrincipalSumOverTimeFromLastWeekInUSDT = totalPrincipalSumOverTimeFromLastWeekInUSDT + \
                    totalPrincipalSumUntillLastWeekInUSDT * timeBetweenActions

                print(prevUserAddress, totalPrincipalSumUntillLastWeekInUSDT,
                    totalPrincipalSumOverTimeFromLastWeekInUSDT)
                overallResults.append(
                    [prevUserAddress, totalPrincipalSumUntillLastWeekInUSDT, totalPrincipalSumOverTimeFromLastWeekInUSDT])


            prevUserAddress = useraddress
            totalPrincipalSumUntillLastWeekInUSDT = 0
            totalPrincipalSumOverTimeFromLastWeekInUSDT = 0
            prevBlockTime = block_time


        if (block_time < lastWeekRewardBlock):
            # calculating outstanding principal in the begining of the week
            if (paymenttype == 'borrow' or paymenttype == 'trade'):
                totalPrincipalSumUntillLastWeekInUSDT = totalPrincipalSumUntillLastWeekInUSDT + \
                    getUSDTValue(tokensymbol, float(newprincipaldecimal))
            else:
                totalPrincipalSumUntillLastWeekInUSDT = totalPrincipalSumUntillLastWeekInUSDT - \
                    getUSDTValue(tokensymbol, float(newprincipaldecimal))
        else:
            # calculate form last week onwards counting time as well
            timeBetweenActions = block_time - prevBlockTime

            totalPrincipalSumOverTimeFromLastWeekInUSDT = totalPrincipalSumOverTimeFromLastWeekInUSDT + \
                totalPrincipalSumUntillLastWeekInUSDT * timeBetweenActions

            if (paymenttype == 'borrow' or paymenttype == 'trade'):
                totalPrincipalSumUntillLastWeekInUSDT = totalPrincipalSumUntillLastWeekInUSDT + \
                    getUSDTValue(tokensymbol, float(newprincipaldecimal))
            else:
                totalPrincipalSumUntillLastWeekInUSDT = totalPrincipalSumUntillLastWeekInUSDT - \
                    getUSDTValue(tokensymbol, float(newprincipaldecimal))

        # if (useraddress == '00000000000000000000000073eb7a4756ef34b903d8f0d320138fa4f2e4ec5b'):
        #     if (block_time < lastWeekRewardBlock):
        #         print("before week", useraddress)
        #     else:
        #         print("after", useraddress)
        #     print("debug",useraddress, totalPrincipalSumUntillLastWeekInUSDT, paymenttype, totalPrincipalSumOverTimeFromLastWeekInUSDT, block_time, lastWeekRewardBlock)


print("number of addresses eligible for rewards", len(overallResults))

print("calculating ALL principal over time")

totalOverTimeEverybody = 0

for row in overallResults:
    totalOverTimeEverybody = totalOverTimeEverybody + row[2]
print("totalOverTimeEverybody", totalOverTimeEverybody)


print("calculating ratios")
for row in overallResults:
    row.append(row[2]/totalOverTimeEverybody)
    # print("row", row)


print("results:")
for row in overallResults:
    # print(row[0], '{0:.4f}'.format(row[3] * 2060000), '{0:.0f}'.format(row[3] * 2060000 * 1000000000000000000))
    print('0x'+row[0][24:], '{0:.4f}'.format(row[3] * 2060000), '{0:.0f}'.format(row[3] * 2060000 * 1000000000000000000))

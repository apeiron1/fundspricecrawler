from bs4 import BeautifulSoup
import requests
import re
import csv
import sys
import fileinput

print('')

## take funds from list
with open('lista.txt') as lista:
    funds = lista.readlines()

## main function
def main(url):
    ## crawling ##
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    div = soup.findAll('div' ,attrs={'id':'overviewQuickstatsDiv'})
    td = div[0].findAll('td' ,attrs={'class':'line text'})
    price = td[0].renderContents()
    price = re.sub(r'[^0-9,]*', '', str(price))
    price = price[2:]

    span = div[0].findAll('span' ,attrs={'class':'heading'})
    date = str(span[0].renderContents())
    date = date[7:-1]

    div2 = soup.findAll('div' ,attrs={'class':'snapshotTitleBox'})
    h1 = div2[0].find('h1')
    title = str(h1)
    title = title[4:-5]

    isin = str(td[3].renderContents()).replace('b\'', '')
    isin = isin[:-1]

    ## print output ##
    print(title,' - ISIN: ',isin)
    print(price,' ',date)
    print('')

    ## create .csv ##
    name = isin+'.csv'
    try:
        file = open(name,'a')
        file.close()
    except:
        print("Error occured")
        sys.exit(0)

    ## write to .csv #
    with open(name, 'a', newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        data = [[date, price]]
        a.writerows(data)

    ## remove duplicates from .csv
    seen = set()
    for line in fileinput.FileInput(name, inplace=1):
        if line in seen: continue # skip duplicates

        seen.add(line)
        print(line)

## cycle
for i in range(len(funds)):
    # url = urllib.urlopen("http://www.morningstar.it/it/funds/snapshot/snapshot.aspx?id="+funds[i])
    url = 'http://www.morningstar.it/it/funds/snapshot/snapshot.aspx?id='+funds[i]
    main(url)

from requests import get
from bs4 import BeautifulSoup
import pandas
import json

url = 'https://hdlbits.01xz.net/wiki/Special:VlgStats/'

#open profiles.json

with open('profiles.json') as json_file:
    data = json.load(json_file)
    for user in data:
        response = get(url + user['id'])

        html_soup = BeautifulSoup(response.text, 'html.parser')

        #get the table id = summary and td string is 'current rank'
        table = html_soup.find('table', id='summary')
        #get <td> value before '<td>Current rank:</td>'
        rank = table.find('td', string='Current rank:').find_next('td').text.strip()
        #add rank in user data
        user['rank'] = int(rank) 

#order users by rank and print
users = sorted(data, key=lambda k: k['rank'])



#print users colocation, name and rank line by line
for i in range(len(users)):
    users[i]['position'] = i + 1
    print(str(i+1) + " " + users[i]['Name'] + " " + str(users[i]['rank']) + "\n")

#save users in csv file
df = pandas.DataFrame(users)
df.to_csv('output.csv', index=False)

import requests
from bs4 import BeautifulSoup
from models.classCountry import ClassCountry
from models.classDataSave import ClassDataSave
from models.dict2Class import Dict2Class

import io, json

def createCountryObject(name, code, id):
      countryObj = ClassCountry(name, code, id);
      return countryObj

##Brings all FIFA country codes
page = requests.get('https://en.wikipedia.org/wiki/List_of_FIFA_country_codes')
soup = BeautifulSoup(page.text, 'html.parser')
contries_list = soup.find_all(class_='wikitable')
contries_list = contries_list[ : -6]

countriesSaveList = [];

countryId = 1;
for countries in contries_list:    
    for country in countries.find_all('tr'):    
        countryA = country.find('a')           
        if countryA is not None:            
            countryTD = country.find_all('td')
            countryObj = createCountryObject(countryA.getText(), countryTD[1].getText(), countryId)
            countriesSaveList.append(countryObj)
            countryId = countryId + 1

obj = ClassDataSave(countriesSaveList)
json_str = json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)

with open('countries.json', 'w') as f:
    json.dump(json_str, f)

f = open('countries.json')  
data = json.load(f)

dictionary = json.loads(data)

result = Dict2Class(dictionary)

new_lst = []
for i in result.objList:
    person = createCountryObject(i["name"], i["code"], i["id"])
    new_lst.append(person)
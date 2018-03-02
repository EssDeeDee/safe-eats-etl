from bs4 import BeautifulSoup
import requests

# Retrieve inspection data between 8/1/2017 and 3/1/2018
r = requests.get("http://foodinspections.nashville.gov/FoodScores.aspx?BegDate=8/1/2017&EndDate=3/1/2018")
print(r.status_code)

soup = BeautifulSoup(r.text, 'html.parser')
print(soup.prettify())


print(soup.title)
print(soup.find_all('p'))

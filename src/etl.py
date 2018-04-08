import requests
from bs4 import BeautifulSoup
from flask import Flask, request

# ****************************** To Do List ******************************
# ToDo: Create a function to parse beginning/end dates and concat to base
#       for search
# ToDo: Extract parsing returned html (beautifulsoup4) into it's own
#       function. This function will take html, and return json containing
#       scores for restaurants (good and bad). Format to be determined.
# ****************************** To Do List ******************************


#  Define server
app = Flask(__name__)


# App routes
@app.route("/ping")
def ping_route():
    return "Ping! Service is available."


@app.route("/scores")
def return_report():
    b_date = request.args.get('b')
    e_date = request.args.get('e')
    dates_query = "?BegDate=" + str(b_date) + "&EndDate=" + str(e_date)

    return fetch_scores(dates_query)


def fetch_scores(dates):
    """Fetch scores given beginning and end dates as parameters
    Input(s):
      - dates: Built url query for beginning/end dates

    Output:
      - html of scores from dates input query
    """

    # Todo: Though unlikely, base_url should be configurable in the event that it changes
    # base_url = "http://foodinspections.nashville.gov/FoodScores.aspx?BegDate=3/1/2018&EndDate=4/1/2018"
    base_url = "http://foodinspections.nashville.gov/FoodScores.aspx"

    url_query = base_url + dates

    # Retrieve inspection data between 8/1/2017 and 3/1/2018
    r = requests.get(url_query)
    print(r.status_code)

    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup.prettify())

    # print(soup.title)
    sections = soup.find_all('p')
    print(sections)
    sections2 = soup.select('p .style1')
    print(sections2)

    for section in sections:
        for content in section.stripped_strings:
            print(content, type(content))
            # print(str(content))
        print("---------------------")

    return r.text
    # print(soup.find_all('p'))


# Main
# if __name__ == "__main__":
#     score_url = "http://foodinspections.nashville.gov/FoodScores.aspx?BegDate=8/1/2017&EndDate=3/1/2018"
#     fetch_scores(score_url)

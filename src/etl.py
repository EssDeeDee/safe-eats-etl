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

    return r.text


def parse_scores(input_html):
    """Parse input_html using BeautifulSoup
    Input(s):
      - input_html: HTML returned from the food inspection website

    Output(s):
      - score_data: parsed JSON score data"""

    low_score_flag = 0

    soup = BeautifulSoup(input_html, 'html.parser')
    # print(soup.prettify())

    # print(soup.title)
    main_sections = soup.find_all('p')
    # print(sections)
    sections2 = soup.select('p .style1')
    # print(sections2)

    for section in main_sections:
        # for content in section.stripped_strings:
        #     print(content, type(content))
        #     # print(str(content))
        content = section.stripped_strings
        name = str(next(content))
        if low_score_flag == 0 and name != "Low Scores:":
            address = str(next(content))
            inspection_date = str(next(content))
            score = str(next(content))

            print("Name: ", name)
            print("Score: ", score)
            print("---------------------")
        elif name == "Low Scores:":
            low_score_flag = 1
        else:
            if name == "There are no updates available for the date range you selected.":
                break
            print("Process low scores here, please!")

    return input_html
    # print(soup.find_all('p'))


#  Define server
app = Flask(__name__)


# App routes
@app.route("/ping")
def ping_route():
    return "Ping! Service is available."


@app.route("/scores")
def return_report():
    b_date = request.args.get('from')
    e_date = request.args.get('to')
    dates_query = "?BegDate=" + str(b_date) + "&EndDate=" + str(e_date)

    html_scores = fetch_scores(dates_query)

    return parse_scores(html_scores)


# Main
# if __name__ == "__main__":
#     score_url = "http://foodinspections.nashville.gov/FoodScores.aspx?BegDate=8/1/2017&EndDate=3/1/2018"
#     fetch_scores(score_url)

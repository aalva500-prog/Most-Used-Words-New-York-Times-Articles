from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
import requests
import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

from Project2_Flask import main_functions


class ArticlesForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    year = IntegerField('Year')
    month = SelectField('Month', choices=[('1', 'January'), ('2', 'February'),
                                          ('3', 'March'), ('4', 'April'),
                                          ('5', 'May'), ('6', 'June'),
                                          ('7', 'July'), ('8', 'August'),
                                          ('9', 'September'), ('10', 'October'),
                                          ('11', 'November'), ('12', 'December')])


def generate_data_from_api(year, month):
    api_url = "https://api.nytimes.com/svc/archive/v1/"
    # Extract API_key from api_key.jason
    api_key_dict = main_functions.read_from_file("Project2_Flask/JSON_Files/api_key.json")
    my_api_key = api_key_dict["my_api_key"]
    if int(year) >= 1851:
        # Extract information from API using the topic selected and the API_key
        final_url = api_url + year + "/" + month + ".json?api-key=" + my_api_key
        # Make the request
        response = requests.get(final_url).json()
        # Save information to archive.json file
        main_functions.save_to_file(response, "Project2_Flask/JSON_Files/archive.json")
        return True
    return False


def get_total_of_articles():
    # Get information from archive.json
    response_dict = main_functions.read_from_file("Project2_Flask/JSON_Files/archive.json")
    # Get the total of articles
    no_articles = response_dict["response"]["meta"]["hits"]
    return no_articles


def get_most_common_words():
    # Get information from archive.json
    response_dict = main_functions.read_from_file("Project2_Flask/JSON_Files/archive.json")
    # Save the extracted information
    str1 = ""

    for i in response_dict["response"]["docs"]:
        str1 = str1 + i["abstract"]

    # Get words from the text
    words = word_tokenize(str1)
    # Get rid of the punctuation marks
    words_no_punctuation = []

    for w in words:
        if w.isalpha():
            words_no_punctuation.append(w.lower())

    # Get rid of the stop words
    stop_words = stopwords.words("english")
    clean_words = []

    for w in words_no_punctuation:
        if w not in stop_words:
            clean_words.append(w)

    # Get the 10 most frequent words
    fdist = FreqDist(clean_words)
    most_common_words = fdist.most_common(10)

    return most_common_words

from Project2_Flask import app, forms
from flask import request, render_template


@app.route('/', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def home():
    my_form = forms.ArticlesForm(request.form)

    if request.method == "POST":
        # Get the values provided by the user
        year = request.form['year']
        month = request.form['month']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Call the API
        # Generate the requested data
        valid = forms.generate_data_from_api(year, month)
        most_common_words = forms.get_most_common_words()
        no_articles = forms.get_total_of_articles()

        return render_template('results.html', year=year, month=month, first_name=first_name,
                               last_name=last_name, no_articles=no_articles,
                               most_common_words=most_common_words, valid=valid, form=my_form)

    return render_template('search.html', form=my_form)

from flask import Flask, render_template, flash, request
import applog.list_jobs as jobs
import applog.count_keywords as keywords
import applog.generate_wordcloud as cloud

app = Flask(__name__)


@app.route('/')
def homepage():
    flash('flash test')
    return render_template('main.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/search-results/', methods=['GET'])
def results():
    render_template('loader.html')
    search_query = request.args.get('q')
    search_location = request.args.get('l')
    search_url = 'https://www.indeed.com/' + \
                 'jobs?q=' + search_query + \
                 '&l=' + search_location

    # Get primary dataframe
    df = jobs.get_all_parameters_for_all_listings(search_url)
    flash(str(len(df)) + ' result(s) were found.')

    # Get dictionary of words by frequency
    words_by_frequency = keywords.get_words_by_freq(
                                                    df['Link'].tolist(),
                                                    None,
                                                    5)

    flash(words_by_frequency)

    # Generate wordcloud
    # wordcloud = cloud.generate_wordcloud(words_by_frequency)

    # Clean up the table to be displayed
    del df['Link']
    TABLE = df.to_html(
                       classes='table table-hover',
                       index=False,
                       escape=False
                       )

    return render_template('results.html', TABLE=TABLE)


@app.route('/loading/')
def loader():
    return render_template('loader.html')


if __name__ == '__main__':
    app.run(debug=True)

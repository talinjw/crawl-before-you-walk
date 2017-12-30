from flask import Flask, render_template, flash, request, redirect
import applog.list_jobs as jobs


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
    search_string = 'jobs?q=' + search_query + '&l=' + search_location
    search_url = 'https://www.indeed.com/' + search_string

    # Clean up the displayed table
    df = jobs.get_all_parameters_for_all_listings(search_url)
    del df['Link']
    TABLE = df.to_html(
        classes='table table-hover',
        index=False,
        escape=False
        )

    flash(str(len(df)) + ' result(s) were found.')

    return render_template('results.html', TABLE=TABLE)


@app.route('/loading/')
def loader():
    return render_template('loader.html')


if __name__ == '__main__':
    app.run(debug=True)

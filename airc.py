from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    user = {'username': 'Test Testovich'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'I love vodka and 9!'
        },
        {
            'author': {'username': 'Vasya'},
            'body': 'I luv Guinness and cider!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


def show_calendar():
    pass

if __name__ == '__main__':
    app.run(debug=True)
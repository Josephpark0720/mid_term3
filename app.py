from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'random'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80), unique=True)
    content = db.Column(db.String(300), unique=True)

    def __repr__(self):
        return "User<{}, {}, {}>".format(self.title, self.name, self.content)

@app.route('/')
def home():
    data = db.session.query(User).all()
    return render_template('home.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        title = User(title="title")
        name = User(name="name")
        content = User(content="content")
        db.session.add_all([title, name, content])
        db.session.commit()
        return redirect(url_for('home'))
    else:
        data = db.session.query(User).all()
        return render_template('form.html')

@app.route('/post')
def post():
    return render_template('post.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
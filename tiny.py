#!/usr/local/bin/python
import uuid
import string
from random import choice, randint, choices
# could also use this way to generate tiny urls
from werkzeug.security import generate_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tiny.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

TINY_BASE = "tier.app/"


# models
class Url(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True)
    tiny_url = db.Column(db.String, unique=True)
    creation_Date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Tiny Url => url: {} => tiny_Url: {}>'.format(self.url, self.tiny_url)


class Visit(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    url_request_number = db.Column(db.Integer)
    tiny_visit_number = db.Column(db.Integer)

    def __repr__(self):
        return '<Visists NB => url: {} | tiny_Url: {}>'.format(self.url_request_number, self.tiny_visit_number)



# views
@app.route("/<url_long>")
def long_to_tiny(url_long):
    init_visit()
    if not url_long:
        return 'please feed me with an url'

    is_url_in_base = Url.query.filter_by(url=url_long).first()
    visit_url_counter = Visit.query.all()[0]
    visit_url_counter.url_request_number += 1
    db.session.commit()

    if is_url_in_base:
        return is_url_in_base.tiny_url, 'already in base'  # not sure about return tuple

    tiny_url = tiny_url_generator()
    is_tiny_in_base = Url.query.filter_by(tiny_url=tiny_url).first()
    # TODO: test that
    while is_tiny_in_base:
        tiny_url = tiny_url_generator()
        is_tiny_in_base = Url.query.filter_by(tiny_url=tiny_url).first()

    url = Url(url=url_long, tiny_url=tiny_url)
    db.session.add(url)
    db.session.commit()
    print(tiny_url)
    return TINY_BASE + tiny_url


@app.route("/tier.app/<url_tiny>")
def tiny_to_long(url_tiny):
    orignal_url = Url.query.filter_by(tiny_url=url_tiny).first()
    if orignal_url:
        visit_tiny_counter = Visit.query.all()[0]
        visit_tiny_counter.tiny_visit_number += 1
        db.session.commit()
        return orignal_url.url
    else:
        return "no connection with that tiny url, please give us another one"

# utils
def init_visit():
    """
    small init for visits
    """
    visits = Visit.query.all()
    if not visits:
        v = Visit(url_request_number=0, tiny_visit_number=0)
        db.session.add(v)
        db.session.commit()


def tiny_url_generator():
    """
    Generates tiny url,
    Returns:
        String -> ex:Go4DfeX2
    """
    tiny_string = ''
    for x in range(9):
        tiny_string += choices(population=(choice(string.printable[:10]), choice(string.printable[10:62])), weights=[0.4, 0.6], k=1)[0]
    return tiny_string

    # feels like uudi are nice
    # uuid_string = str(uuid.uuid4())
    # hash_base = uuid_string[:8]
    # improved_uuid = ''
    # for char in hash_base:
    #     if not char.isalpha():
    #         improved_uuid += char
    #     else:
    #         upper_or_lower = random.randint(0, 10)
    #         rand_letter = random.randint(0, 25)
    #         if upper_or_lower > 5:
    #             remapped_letter = string.ascii_lowercase[rand_letter]
    #         else:
    #             remapped_letter = string.ascii_uppercase[rand_letter]
    #         improved_uuid += remapped_letter
    # return improved_uuid


if __name__ == "__main__":
    app.run()

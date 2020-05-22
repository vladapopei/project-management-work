"""
Holds marshmallow schemas and database models for the application.
"""
from helpr import db

posting_categories = db.Table('posting_categories',
                              db.Column('posting_id', db.Integer, db.ForeignKey('posting.id'), primary_key=True),
                              db.Column('categori_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
                              )


class Posting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.column(db.String(200))
    pricing = db.column(db.Float)
    date_posted = db.column(db.DateTime)
    body = db.Column(db.String(2500))
    categories = db.relationship('Category', secondary=posting_categories, lazy='subquery',
                                 backref=db.backref('postings', lazy=True))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    contact_email = db.Column(db.String(250))
    contact_number = db.column(db.String(30))
    postings = db.relationship('Posting', backref='business', lazy=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(30))
    service_requests = db.relationship('RequestForService', backref='request', lazy=True)


class RequestForService(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', backref='service_request', lazy=True)
    posting = db.relationship('Posting', backref='posting', lazy=True)
    details = db.Column(db.String(1000))

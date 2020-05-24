"""
Holds marshmallow schemas and database models for the application.
"""
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import post_load

from helpr import db, ma, cfg
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer,
                          BadSignature,
                          SignatureExpired)

posting_categories = db.Table('posting_categories',
                              db.Column('posting_id', db.Integer, db.ForeignKey('posting.id'), primary_key=True),
                              db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
                              )
db: SQLAlchemy
ma: Marshmallow


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))


class Posting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    pricing = db.Column(db.Float)
    date_posted = db.Column(db.DateTime)
    body = db.Column(db.String(2500))
    business = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=True)
    tags = db.relationship('Category', secondary=posting_categories, lazy='subquery',
                           backref=db.backref('postings', lazy=True))


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owning_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200))
    contact_email = db.Column(db.String(250))
    contact_number = db.Column(db.String(30))
    postings = db.relationship('Posting', backref='poster', lazy=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    accepted = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(120))
    completed = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(30))
    service_requests = db.relationship('ServiceRequest', backref='requester', lazy=True)
    businesses = db.relationship('Business', backref='manager', lazy=True)

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(cfg['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(cfg['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class ServiceRequest(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    details = db.Column(db.String(1000))


class ServiceRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceRequest


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category


class PostingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Posting
        include_fk = True


class BusinessSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Business

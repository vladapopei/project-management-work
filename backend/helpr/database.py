"""
Holds marshmallow schemas and database models for the application.
"""
from helpr import db, ma

posting_categories = db.Table('posting_categories',
                              db.Column('posting_id', db.Integer, db.ForeignKey('posting.id'), primary_key=True),
                              db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
                              )


class Posting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    pricing = db.Column(db.Float)
    date_posted = db.Column(db.DateTime)
    body = db.Column(db.String(2500))
    business = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=True)
    tags = db.relationship('Category', secondary=posting_categories, lazy='subquery',
                           backref=db.backref('posting', lazy=True))


class PostingSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Posting


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    contact_email = db.Column(db.String(250))
    contact_number = db.Column(db.String(30))
    postings = db.relationship('Posting', backref='poster', lazy=True)


class BusinessScehma(ma.SQLAlchemySchema):
    class Meta:
        model = Business


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accepted = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(30))
    service_requests = db.relationship('ServiceRequests', backref='requester', lazy=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class ServiceRequests(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    details = db.Column(db.String(1000))


class ServiceRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceRequests

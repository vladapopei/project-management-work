"""
The main body of routes for the application. Handle the creation, updating, and access of postings.
"""
from flask import request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

from helpr import app, db, auth
from helpr.database import User, Business, UserSchema, BusinessSchema, PostingSchema, Posting

user_schema = UserSchema()
business_schema = BusinessSchema()
posting_schema = PostingSchema()


@app.route('/business/register', methods=['POST'])
@auth.login_required
def business():
    """
    Allows a user to create a business.

    This route should not be implicitly accessible from users.
    In order to get approved for a business, they must be manually vetted.
    However, as of now, it just applies auth the normal way.
    :return: json(Business)
    """
    json_data = request.get_json()
    if not json_data:
        return {'message': 'no input received'}
    try:
        data = business_schema.load(json_data)
    except ValidationError as e:
        return e.messages, 422

    business = Business(**data, owning_user=User.query.filter_by(username=request.authorization.username).first().id)
    db.session.add(business)
    db.session.commit()
    return business_schema.dump(business)


@app.route('/business/posting', methods=['PUT', 'POST'])
@auth.login_required
def posting():
    """
    This allows a business to post OR update a posting. Requires a json of posting in the body.

    If no ID is posting, this will create a brand new posting for the business.
    IF an ID is posting, it will update the posting to match what was received in the request.
    This route validates that the posting and associated business belong to the authenticated user.
    :return: json(Service)
    """
    json_data = request.get_json()
    if not json_data:
        return {'message': 'no input received'}
    try:
        data = posting_schema.load(json_data)
    except ValidationError as e:
        return e.messages, 422
    current_user = User.query.filter_by(username=request.authorization.username).first().id
    current_posting = Posting(**data, business=Business.query.filter_by(owning_user=current_user).first().id)
    db.session.add(current_posting)
    db.session.commit()
    return posting_schema.dump(current_posting)


@app.route('/request_service', methods=['POST'])
@auth.login_required
def request_service():
    """
    This allows a user to request a service from a business. Requires a json of Service in the body.
    :return: json(ServiceRequest)
    """


@app.route('/category', methods=['POST', 'PUT'])
@auth.login_required
def category():
    """
    This allows a user to create or update a category.
    It should only be accessible to authenticated staff members.
    :return: json(Category)
    """

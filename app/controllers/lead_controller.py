from datetime import datetime
from re import fullmatch
from sqlalchemy.exc import IntegrityError
from flask import jsonify, request
from http import HTTPStatus
from app.models.lead_model import LeadModel
from app.configs.database import db
from app.helpers.leads_decorators import keys_verifier, email_verifier
from werkzeug.exceptions import BadRequest, NotFound

@keys_verifier
def create():
    try:
        lead_data = request.get_json()
    
        if fullmatch(r"^\([0-9]{2}\)[0-9]{5}-[0-9]{4}$", lead_data['phone']) is None:
            raise BadRequest
        
        lead = LeadModel(**lead_data)
        
        db.session.add(lead)
        db.session.commit()
        
        return jsonify(lead), HTTPStatus.CREATED
    except BadRequest:
        return {
            "format expected": '(88)88888-8888',
            'format received': lead_data['phone'],
        }, HTTPStatus.BAD_REQUEST
        
    except IntegrityError as e:
        error_details = str(e.orig).split("DETAIL:  ")[1][:-2]
        
        return {"message": error_details}, HTTPStatus.CONFLICT
    
def retrieve_leads():
    try: 
        data = LeadModel.query.order_by(LeadModel.visits.desc()).all()
        
        if len(data) == 0:
            raise NotFound
        
        return jsonify(data), HTTPStatus.OK
    
    except NotFound:
        return {'msg': "data not found"}, HTTPStatus.NOT_FOUND
    
@email_verifier
def patch_lead():
    try:
        data = request.get_json()
        
        lead = LeadModel.query.filter_by(email=data['email']).first_or_404()
        
        lead.visits = lead.visits + 1
        lead.last_visit = datetime.now()
        db.session.add(lead)
        db.session.commit()
        
        return "", HTTPStatus.NO_CONTENT
    except NotFound:
        return {'msg': "email not found"}, HTTPStatus.NOT_FOUND
        
    
@email_verifier        
def delete_lead():
    try:
        data = request.get_json()
        lead = LeadModel.query.filter_by(email=data['email']).first_or_404()
        db.session.delete(lead)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT
    except NotFound:
        return {'msg': "email not found"}, HTTPStatus.NOT_FOUND

        
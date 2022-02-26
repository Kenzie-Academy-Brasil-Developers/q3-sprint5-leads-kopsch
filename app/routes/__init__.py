from flask import Flask
from app.routes.lead_blueprint import bp_lead

def init_app(app: Flask):
    app.register_blueprint(bp_lead)
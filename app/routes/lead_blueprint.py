from flask import Blueprint
from app.controllers import lead_controller

bp_lead = Blueprint('bp_lead', __name__, url_prefix='/leads')

bp_lead.get("")(lead_controller.retrieve_leads)
bp_lead.post("")(lead_controller.create)
bp_lead.patch("")(lead_controller.patch_lead)
bp_lead.delete("")(lead_controller.delete_lead)
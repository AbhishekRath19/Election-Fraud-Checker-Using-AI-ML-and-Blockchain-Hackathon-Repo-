from flask import Blueprint

voting_bp = Blueprint('voting', __name__)

from . import vote_processing
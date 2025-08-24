from flask import Blueprint

blockchain_bp = Blueprint('blockchain', __name__)

from . import web3_integration, sync, sync_routes
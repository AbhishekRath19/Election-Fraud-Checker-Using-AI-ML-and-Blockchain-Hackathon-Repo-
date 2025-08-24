from flask import Flask
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from . import authentication
from flask import Blueprint, render_template, request, jsonify, url_for
import requests
from bs4 import BeautifulSoup
from datetime import datetime

bp = Blueprint('itooza', __name__, url_prefix='/itooza')

@bp.route('/start/')
def start():
    return render_template('itooza.html')


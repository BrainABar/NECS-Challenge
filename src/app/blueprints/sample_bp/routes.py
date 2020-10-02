""" Personal Pages Blueprint routes """
from typing import Any
from flask import Blueprint, render_template, abort


bp = Blueprint('sample_bp', __name__,
               template_folder='templates',
               static_folder='static',
               static_url_path='/sample_bp/static')

'''
@bp.route('/', methods=['GET'])
def index() -> Any:
    """
    :return: Any
    """
    return render_template('index.html', title='Home')
'''


@bp.route('/ping', methods=['GET'])
def ping():
    """
    :return:
    """
    return 'pong'

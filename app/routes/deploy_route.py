from flask import Blueprint, render_template, redirect, url_for, request,session
from flask_login import login_user, logout_user,current_user

import app.models as mdl


deploy_bp = Blueprint('deploy', __name__)


@deploy_bp.route('/deploy_website', methods=['POST'])
def deploy_state():

    return redirect(url_for('main.success'))
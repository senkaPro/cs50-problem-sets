import random, string

from flask import redirect, render_template, request, session
from functools import wraps
from models import User

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = User.query.filter_by(username=session['username']).first()
        if user.is_authenticated == False:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



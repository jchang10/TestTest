from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from . import auth, httpauth
from .. import db
from .oauth import OAuthSignIn
from ..models import User, OauthUser
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/oauth/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@auth.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    oauth = OAuthSignIn.get_provider(provider)
    #social_id, username, email = oauth.callback()
    me = oauth.callback()
    if me['social_id'] is None:
        flash('Authentication failed.')
        return redirect(url_for('main.index'))
    ouser = OauthUser.query.filter(OauthUser.provider == provider, \
                                   OauthUser.social_id == me['social_id']).first()
    if not ouser:
        # create oauth user record. see if a user record exists with matching email.
        # otherwise, create the new user record.
        ouser = OauthUser(provider=provider,
                          social_id=me['social_id'],
                          username=me.get('username', None),
                          email=me.get('email', None),
                          name=me.get('name', None)
        )
    # ouser should now exist. find its user record.
    user = ouser.user
    if not user:
        # see if a matching user_id or email exists
        user = User.query.filter_by(id=ouser.user_id).first() or \
               User.query.filter_by(email=ouser.email).first()
        if not user:
            # if user record still does not exist, then create one.
            user = User(email=ouser.email,
                    username=ouser.username if ouser.username else ouser.email,
            )
        # user should now exist.
        user.socials.append(ouser)
    db.session.add(user)
    db.session.add(ouser)
    db.session.commit()
    login_user(user, True)
    return redirect(url_for('main.index'))


@httpauth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


from flask import jsonify, g

@auth.route('/token')
@httpauth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@auth.route('/test')
@httpauth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


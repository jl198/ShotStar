from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, EmptyForm, GameForm
from app.models import User, Game
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = GameForm()
    if form.validate_on_submit():
        game = Game(score=form.score.data, date_played=form.date_played.data, timestamp=datetime.now(), owner=current_user)
        db.session.add(game)
        db.session.commit()
        flash('just added game')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    games = current_user.games_played.paginate(page, current_app.config['GAMES_PER_PAGE'], False)
    next_url = url_for('main.index', page=games.next_num) if games.has_next else None
    prev_url = url_for('main.index', page=games.prev_num) if games.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           games=games.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    games = Game.query.order_by(Game.timestamp.desc()).paginate(page, current_app.config['GAMES_PER_PAGE'], False)
    next_url = url_for('main.explore', page=games.next_num) if games.has_next else None
    prev_url = url_for('main.explore', page=games.prev_num) if games.has_prev else None
    return render_template('index.html', title='Explore',
                           games=games.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    games = user.games_played.order_by(Game.timestamp.desc()).paginate(page, current_app.config['GAMES_PER_PAGE'],
                                                                         False)
    next_url = url_for('main.user', username=user.username, game=games.next_num) if games.has_next else None
    prev_url = url_for('main.user', username=user.username, game=games.prev_num) if games.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, games=games.items, next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

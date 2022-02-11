from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, EmptyForm, GameForm, ScoreGameForm
from app.models import User, Game, Scored_Game
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
        game = Game(score=form.score.data, date_played=form.date_played.data, timestamp=datetime.now(),
                    owner=current_user)
        db.session.add(game)
        db.session.commit()
        flash('just added game')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    games = current_user.games_played.paginate(page, current_app.config['GAMES_PER_PAGE'], False)
    scored_games = current_user.scored_games_played.paginate(page, current_app.config['GAMES_PER_PAGE'], False)
    next_url = url_for('main.index', page=games.next_num) if games.has_next else None
    prev_url = url_for('main.index', page=games.prev_num) if games.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           games=games.items, scored_games=scored_games.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    games = Game.query.order_by(Game.timestamp.desc()).paginate(page, current_app.config['GAMES_PER_PAGE'], False)
    next_url = url_for('main.explore', page=games.next_num) if games.has_next else None
    prev_url = url_for('main.explore', page=games.prev_num) if games.has_prev else None
    return render_template('index.html', title='Explore', games=games.items, next_url=next_url, prev_url=prev_url)


@bp.route('/score_game', methods=['GET', 'POST'])
@login_required
def score_game():
    form = ScoreGameForm()
    if form.validate_on_submit():
        date_played = form.date_played.data
        number_of_players = form.number_of_players.data
        starting_position = form.starting_position.data
        # other_positions = form.other_positions.data
        auto_or_manual = True if form.auto_or_manual.data == 'Auto' else False
        file_name = form.file_name.data
        scored_game = Scored_Game(date_played=date_played, number_of_players=number_of_players,
                                  starting_position=starting_position, auto_or_manual=auto_or_manual,
                                  file_name=file_name, timestamp=datetime.now(), owner=current_user)
        db.session.add(scored_game)
        db.session.commit()
        flash('Scored game submitted!')
        return redirect(url_for('main.score_game'))
    return render_template('score_game.html', title='Score Game', form=form)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    games = user.games_played.order_by(Game.timestamp.desc()).paginate(page, current_app.config['GAMES_PER_PAGE'],
                                                                       False)
    scored_games = user.scored_games_played.order_by(Scored_Game.timestamp.desc()).paginate(page, current_app.config[
        'GAMES_PER_PAGE'], False)
    games_next_url = url_for('main.user', username=user.username, page=games.next_num) if games.has_next else None
    games_prev_url = url_for('main.user', username=user.username, page=games.prev_num) if games.has_prev else None
    scored_games_next_url = url_for('main.user', username=user.username,
                                    page=scored_games.next_num) if scored_games.has_next else None
    scored_games_prev_url = url_for('main.user', username=user.username,
                                    page=scored_games.prev_num) if scored_games.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, games=games.items, scored_games=scored_games.items,
                           games_next_url=games_next_url, games_prev_url=games_prev_url,
                           scored_games_next_url=scored_games_next_url, scored_games_prev_url=scored_games_prev_url,
                           form=form)


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

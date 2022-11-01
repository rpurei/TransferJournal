from flask import Blueprint, render_template, flash, current_app

views_handler = Blueprint('views', __name__)


@views_handler.app_errorhandler(404)
def handle_404(err):
    current_app.logger.critical(str(err))
    flash(f'Ошибка: {str(err)}', 'danger')
    return render_template('404.html'), 404


@views_handler.app_errorhandler(500)
def handle_500(err):
    current_app.logger.critical(str(err))
    flash(f'Ошибка: {str(err)}', 'danger')
    return render_template('500.html'), 500

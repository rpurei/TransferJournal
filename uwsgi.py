from app_logger import logger_output
from config import APP_HOST, APP_PORT, DEBUG
from app import create_app

try:
    app = create_app()
    app.run(host=APP_HOST, port=APP_PORT, debug=True)
    app.app_context().push()
except Exception as err:
    logger_output(str(err), DEBUG, 'error')

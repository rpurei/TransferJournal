#!/bin/bash
cd /var/www/TransferJournal
source /var/www/TransferJournal/venv/bin/activate
pip install -r requirements.txt
/var/www/TransferJournal/venv/bin/gunicorn -w=4 -b :5000 "app:create_app()"

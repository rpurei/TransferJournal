#!/bin/bash
cd /var/www/TransferJournal
sudo git pull
sudo chown -R www-data:www-data /var/www/TransferJournal
sudo systemctl stop transferjournal
sudo systemctl start transferjournal
sudo systemctl restart nginx

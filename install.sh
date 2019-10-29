set -a
source backend.env
source env-postgres.env
set +a


sudo dpkg-reconfigure locales
sudo echo "LC_ALL=en_US.UTF-8" | sudo tee -a /etc/environment
sudo echo "LANG=en_US.UTF-8 UTF-8" | sudo tee -a /etc/environment


sudo apt install -y python3
sudo apt install -y python3-pip


sudo apt install -y nginx
sudo cp nginx_mi_apio.conf /etc/nginx/sites-available

# Hardcoded ports and names
sudo ln -s /etc/nginx/sites-available/nginx_mi_apio.conf /etc/nginx/sites-enabled/nginx_mi_apio

# Get ssl certificates https://certbot.eff.org/lets-encrypt/pip-nginx
sudo apt-get install -y certbot
sudo certbot certonly --authenticator standalone -d $SERVER_NAME --pre-hook "service nginx stop" --post-hook "service nginx start"
echo '0 0 1 * * sudo certbot renew --pre-hook "service nginx stop" --post-hook "service nginx start"' | sudo tee -a /etc/crontab > /dev/null


sudo apt install -y postgresql-$POSTGRES_VERSION libpq-dev postgresql-client postgresql-client-common
echo "host all all 192.168.1.0/24 md5" | sudo tee -a /etc/postgresql/$POSTGRES_VERSION/main/pg_hba.conf
sudo sed -i "/^#listen_addresses.*/a listen_addresses\ =\ '*'" /etc/postgresql/$POSTGRES_VERSION/main/postgresql.conf
sudo systemctl restart postgresql
sudo su postgres -c "psql  -c \"CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';\""
sudo su postgres -c "psql  -c \"CREATE DATABASE $POSTGRES_USER OWNER $POSTGRES_USER;\""


sudo apt install -y uvicorn


pip3 install -r requirements.txt
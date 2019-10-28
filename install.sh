sudo apt update
sudo apt upgrade

sudo apt install -y python3
sudo apt install -y python3-pip
sudo apt install -y git


sudo apt install -y nginx

# Get ssl certificates https://certbot.eff.org/lets-encrypt/pip-nginx
sudo apt-get install certbot
sudo certbot certonly --authenticator standalone -d $SERVER_NAME --pre-hook "service nginx stop" --post-hook "service nginx start"
echo '0 0 1 * * sudo certbot renew --pre-hook "service nginx stop" --post-hook "service nginx start"' | sudo tee -a /etc/crontab > /dev/null



sudo apt install postgresql-$POSTGRES_VERSION libpq-dev postgresql-client postgresql-client-common
sudo echo "host all all 192.168.1.0/24 trust" >> /etc/postgresql/$POSTGRES_VERSION/main/pg_hba.conf
sudo sed "/^#listen_addresses*/listen_addresses = '127.0.0.1,192.168.1.26'" /etc/postgresql/$POSTGRES_VERSION/main/postgresql.conf > /etc/postgresql/$POSTGRES_VERSION/main/postgresql.conf
sudo systemctl restart postgresql
sudo su postgres -c "psql  -c \"CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';\""
sudo su postgres -c "psql  -c \"CREATE DATABASE $POSTGRES_USER OWNER $POSTGRES_USER;\""
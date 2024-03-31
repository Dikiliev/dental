apt update
apt install snapd
snap install core; sudo snap refresh core
snap install --classic certbot
ln -s /snap/bin/certbot /usr/bin/certbot
certbot certonly --standalone --non-interactive --agree-tos --email rosul.um@gmail.com -d ldent.online

nginx -g 'daemon off;'
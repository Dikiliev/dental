nginx -g 'daemon off;'

apt-get update && apt-get install -y certbot
certbot certonly --standalone --non-interactive --agree-tos --email rosul.um@gmail.com -d ldent.online

cp /etc/letsencrypt/live/your_domain.com/fullchain.pem /etc/letsencrypt/ssl.crt
cp /etc/letsencrypt/live/your_domain.com/privkey.pem /etc/letsencrypt/ssl.key

nginx -s reload
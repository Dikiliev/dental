apt-get update && apt-get install python3 python3-venv python3-pip -y
python3 -m venv /root/venv
/root/venv/bin/pip install certbot certbot-nginx
/root/venv/bin/certbot certonly --standalone --non-interactive --agree-tos --email rosul.um@gmail.com -d ldent.online

nginx -s reload
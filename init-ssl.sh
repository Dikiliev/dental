certbot certonly --standalone --non-interactive --agree-tos --email rosul.um@gmail.com -d ldent.online

nginx -g 'daemon off;'
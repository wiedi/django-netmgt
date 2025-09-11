# certbot-netmgt

Certbot plugin to manage dns-01 challanges via netmgt API.

### Setup

Create config file, for example `/etc/letsencrypt/netmgt.ini`:

```
dns_netmgt_endpoint = https://netmgt.example.com
dns_netmgt_admin_token = "secret_token"

```

Request certificate:

```
certbot certonly -a dns-netmgt --dns-netmgt-credentials /etc/letsencrypt/netmgt.ini -d test.example.com
```
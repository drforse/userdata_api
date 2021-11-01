### bind mounts
db.sqlite3 and config.ini, should be found on host, config.ini template is in resources dir
### api configuration (config.ini)
it should probably look like this:
```
[DEFAULT]
db_path = sqlite:///db.sqlite3

[userdata_api]
creds_directory = /.userdata_api/shadow/
host = 0.0.0.0
port = 7772
public_url_base = https://{ip_addr or domain}

[photos_api]
creds_directory = /.photos_api/shadow/
host = 0.0.0.0
port = 7771
public_url_base = https://{ip_addr or domain}
```

### nginx configuration
```
server {
        listen 443 ssl;
        server_name valid_server_name (ip_addr or domain);

        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
        ssl_certificate /path/to/crt;
        ssl_certificate_key /path/to/key;

        # userdata api
        location /api/ {
               proxy_pass         http://127.0.0.1:7772/api/;
               proxy_redirect     off;
               proxy_set_header   Host $host;
               proxy_set_header   X-Real-IP $remote_addr;
               proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
               proxy_set_header   X-Forwarded-Host $server_name;
       }

        # photos
        location /photos/ {
                proxy_pass         http://127.0.0.1:7771/photos/;
                proxy_redirect     off;
                proxy_set_header   Host $host;
                proxy_set_header   X-Real-IP $remote_addr;
                proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header   X-Forwarded-Host $server_name;
        }
}
```
### additional required steps
don't forget to run `docker exec <container> python generate_userdata_api_key.py` for userdata_api container and `docker exec <container> python generate_photos_api_key.py` for photos_api container, this steps are required for generating unique api keys for apis
the first key is for /api/users/ requests, the seconds one is for /photos/ requests

## Methods docs
All methods take api_key in query args


POST /api/users
takes multipart/data as parameters

data["user_data"]: json str
```
{
    "first_name": str,
    (optional) "last_name": str,
    (optional) "email_address": str,
    (optional) "user_pass": {
        "number": str,
        "country": str,
        "issue_date": int,  # ordinal value
        "expiration_date": int  # ordinal value
    }
}
```
files["photo"]: file structure (optional)

returns {"user_id": int} or success


GET /api/users/{user_id: int}
takes no specific parameters
returns:
```
{
    "id": int,
    "first_name": str,
    (optional) "last_name": str,
    (optional) "email_address": str,
    (optional) "photo_path": str,  # relative path
    (optional) "user_pass": {
        "id": int,
        "user_id": int,
        "number": str,
        "country": str,
        "issue_date": int,  # ordinal value
        "expiration_date": int  # ordinal value
    },
    (optional) "photo": str  # url withou api_key, to access -> you need api_key
}
```

DELETE /api/users/{user_id: int}
deletes user from db, and his pass data, and his photo
returns 204


GET /photos/{filename}
static files

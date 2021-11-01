### bind mounts
db.sqlite3 and config.ini, should be found on host
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
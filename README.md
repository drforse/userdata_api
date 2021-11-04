### api configuration (config.ini)
not used anymore
### api configuration (.env)
apps can work without this file, as there are default values in .env.default (that is copied inside image) and docker-compose.yml (for build-time required vars), but I highly recommend to configure mysql :)
IF YOU WILL CONFIGURE .env.default OR/AND docker-compose.yml, BE AWARE OF DEFAULT ENV VARS, SOME ARE DUPLICATED IN THERE FILES, AND SHOULD BE THE SAME (USERDATA_API_LISTEN_PORT, USERDATA_API_CREDS_DIR, PHOTOS_API_LISTEN_PORT, PHOTOS_API_CREDS_DIR)
example (the default values are shown here):
```
DB_ADDRESS=mysql+pymysql://userdata_user:UsErdAtAPaSSW0RD@db:7770/userdata_db
MYSQL_ROOT_PASSWORD=N0pAssw0rd
MYSQL_DATABASE=userdata_db
MYSQL_USER=userdata_user
MYSQL_PASSWORD=UsErdAtAPaSSW0RD
MYSQL_PORT=7770  # same port for outside container and for inside container

USERDATA_API_LISTEN_HOST=0.0.0.0
USERDATA_API_LISTEN_PORT=7772  # same port for outside container and for inside container
USERDATA_API_CREDS_DIR=/.userdata_api/shadow/

PHOTOS_API_LISTEN_HOST=0.0.0.0
PHOTOS_API_LISTEN_PORT=7771 # same port for outside container and for inside container
PHOTOS_API_PUBLIC_URL_BASE=http://127.0.0.1
PHOTOS_API_CREDS_DIR=/.photos_api/shadow/
```

### additional required steps
don't forget to run `docker exec <container> python generate_userdata_api_key.py` for userdata_api container and `docker exec <container> python generate_photos_api_key.py` for photos_api container, this steps are required for generating unique api keys for apis
the first key is for /api/users/ requests, the seconds one is for /photos/ requests
well, it isn't actually required, but you won't be able of using apis without keys
#### moving from first version to second
in first version, SQLAlchemy models didn't support mysql, so in second version, if you want to stay on sqlite, you will need to create table in your sqlite db:
```
CREATE TABLE IF NOT EXISTS alembic_version (
	version_num VARCHAR(32) PRIMARY KEY
);
INSERT INTO alembic_version (version_num) VALUES ('6313e1cb41c9');
```

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

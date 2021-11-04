FROM python:3.9

WORKDIR /app

COPY userdata_api /app/userdata_api
COPY requirements.txt /app/
COPY generate_userdata_api_key.py /app/
COPY migrations /app/migrations
COPY alembic.ini /app/
COPY create_db_if_not_exists.py /app/
COPY .env.default /app/

RUN pip install -r requirements.txt

RUN echo "don't forget to run 'docker exec <container> python generate_userdata_api_key.py'"

CMD python create_db_if_not_exists.py && alembic upgrade head && python -m userdata_api

FROM python:3.9

WORKDIR /app

COPY photos_api /app/photos_api
COPY requirements.txt /app/
COPY generate_photos_api_key.py /app/
COPY .env.default /app/

RUN pip install -r requirements.txt

RUN echo "don't forget to run 'docker exec <container> python generate_photos_api_key.py'"

CMD ["python", "-m", "photos_api"]

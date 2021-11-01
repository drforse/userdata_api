FROM python:3.9

WORKDIR /app

EXPOSE 7772

COPY userdata_api /app/userdata_api
COPY requirements.txt /app/
COPY generate_userdata_api_key.py /app/

RUN pip install -r requirements.txt

RUN echo "don't forget to run 'docker exec <container> python generate_userdata_api_key.py'"

CMD ["python", "-m", "userdata_api"]

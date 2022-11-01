FROM python:3.10.6-slim-buster
WORKDIR /RoadApp
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /RoadApp
RUN flask db upgrade
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

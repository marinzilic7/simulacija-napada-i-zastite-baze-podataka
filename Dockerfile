FROM python:3.11

WORKDIR /home/app

COPY model /home/app

COPY requirements.txt /home/app/requirements.txt

RUN pip install -r requirements.txt

CMD [ "python3", "model/app.py" ]


FROM python:3.11

WORKDIR /home/app


COPY app /home/app
COPY app/templates /home/app/templates
COPY requirements.txt /home/app/requirements.txt
RUN pip install -r requirements.txt

CMD [ "python3", "app.py" ]

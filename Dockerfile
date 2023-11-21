FROM python:3.12.0-alpine3.18

COPY miapp miapp/

WORKDIR /miapp

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
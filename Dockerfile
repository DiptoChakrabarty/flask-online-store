FROM python:3.8

ENV FLASK_APP=app.py

ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /app

COPY . .

# Install packages
RUN pip3 install -r requirements.txt

RUN rm site.db

EXPOSE 5000

CMD ["python3", "app.py"]
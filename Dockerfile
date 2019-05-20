FROM python:3.6
WORKDIR /root
ENV FLASK_ENV="production"
EXPOSE "${PORT:-5000}"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD flask run --host 0.0.0.0 --port "${PORT:-5000}"

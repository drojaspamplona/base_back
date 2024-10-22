FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV TIMEOUT=300

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN python -m pip install -r requirements.txt
COPY . .

EXPOSE 80

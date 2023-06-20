FROM python:3.9

WORKDIR /app

COPY Pipfile* ./
COPY config.py .  

RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev \
    && pip install pipenv \
    && pipenv install --system --deploy \
    && apt-get remove -y default-libmysqlclient-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8087

CMD ["python", "app.py"]

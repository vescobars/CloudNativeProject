FROM python:3.9
LABEL authors="d.granadam@uniandes.edu.co"
WORKDIR /code

RUN pip install pipenv && \
  apt-get update && \
  apt-get install -y libpq-dev gcc && \
  apt-get install -y --no-install-recommends gcc python3-dev libssl-dev

RUN pip install pipenv psycopg2

COPY Pipfile ./

RUN pipenv install

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
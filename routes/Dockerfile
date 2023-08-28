FROM python:3.9
LABEL authors="v.escobar1@uniandes.edu.co"
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY /src /code/src
EXPOSE 8001
CMD ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8001"]

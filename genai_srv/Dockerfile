FROM python:3.12.6-bookworm

WORKDIR /code/genai_srv

COPY ./requirements.txt /code/genai_srv/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/genai_srv/requirements.txt

RUN playwright install
RUN playwright install-deps

COPY ./app /code/genai_srv/app

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload" ]

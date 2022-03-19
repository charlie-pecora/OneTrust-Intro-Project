FROM python:3.9
COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

RUN useradd -ms /bin/bash fastapi

USER fastapi
WORKDIR /home/fastapi
COPY ./api api/

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
FROM alpine
COPY . /home
COPY ./requirements.txt /home

WORKDIR /home

RUN apk add py3-pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
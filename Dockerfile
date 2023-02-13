FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /digeizTechTask
COPY requirements.txt /digeizTechTask/requirements.txt
RUN pip install -r requirements.txt

COPY ./src/api /digeizTechTask/api
COPY ./src/main.py /digeizTechTask/
COPY ./migrations /digeizTechTask/migrations

COPY entrypoint.sh /digeizTechTask/
RUN chmod +x entrypoint.sh

CMD ./entrypoint.sh
FROM python:3
WORKDIR /simple_api
COPY /requirements.txt /simple_api
RUN pip install -r requirements.txt
COPY . /simple_api
EXPOSE 5000
CMD ["python", "/.simple_api"]
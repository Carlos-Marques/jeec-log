FROM python:3.9.1-slim
WORKDIR /app
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD . .
CMD python app.py

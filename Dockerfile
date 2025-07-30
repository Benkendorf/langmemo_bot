FROM python:3.9-alpine⁠
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

CMD python langmemo_bot.py

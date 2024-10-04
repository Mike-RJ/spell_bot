FROM python:3.10-slim
WORKDIR /bot
COPY ./bot .
ENV AUDIT_CHANNEL_ID=""
ENV API_TOKEN=""
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]
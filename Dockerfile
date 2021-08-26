FROM python:3.9

ADD bot.py .

RUN pip install discord.py beautifulsoup4 requests lxml

CMD ["python", "./bot.py"]
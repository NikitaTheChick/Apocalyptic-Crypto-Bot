FROM python:3.11
WORKDIR Apocalyptic-Crypto-Bot/ACB/
ADD wsgi.py .
ENV STATIC_URL /static
ENV STATIC_PATH /Apocalyptic-Crypto-Bot/ACB/static
RUN pip install matplotlib robin_stocks flask
COPY . .
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
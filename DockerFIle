FROM python:3.10.12
RUN apt-get update && apt-get install -y git-lfs && git lfs install
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN git lfs pull
CMD ["gunicorn", "Tennis_website.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120"]

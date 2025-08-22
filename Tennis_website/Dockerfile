FROM python:3.10.12

RUN apt-get update && apt-get install -y git-lfs && git lfs install

WORKDIR /app

RUN git clone https://github.com/Kbujdoso/tennis_match_prediction_webapp.git . \
    && git lfs pull

RUN pip install --no-cache-dir -r Tennis_website/requirements.txt

CMD ["gunicorn", "Tennis_Website.Tennis_Website.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120"]

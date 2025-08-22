FROM python:3.10.12

RUN apt-get update && apt-get install -y git-lfs && git lfs install

WORKDIR /app

RUN git clone https://github.com/Kbujdoso/tennis_match_prediction_webapp.git Tennis_website
RUN git -C Tennis_website lfs pull

RUN pip install --no-cache-dir -r Tennis_website/requirements.txt

WORKDIR /app/Tennis_website

CMD ["gunicorn", "Tennis_website.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120"]

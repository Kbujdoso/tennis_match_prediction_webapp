FROM python:3.10.12

RUN apt-get update && apt-get install -y git-lfs && git lfs install

WORKDIR /app

RUN git clone https://github.com/Kbujdoso/tennis_match_prediction_webapp.git Tennis_website
RUN git -C Tennis_website lfs pull

WORKDIR /app/Tennis_website/Tennis_website
RUN pip install --no-cache-dir -r requirements.txt
ENV DJANGO_SETTINGS_MODULE=Tennis_website.settings
RUN python3 manage.py migrate
RUN mkdir -p /app/Tennis_website/Tennis_website/staticfiles
RUN python3 manage.py collectstatic --noinput

EXPOSE 8000


CMD ["gunicorn", "Tennis_website.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120"]

# base image
FROM python:3.11-slim

# variables environnement
ENV PYTHONUNBUFFERED 1

# créer et se placer dans le dossier app
WORKDIR /app

# copier requirements
COPY requirements.txt .

# installer dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# copier le projet entier
COPY . .

# collect static
RUN python manage.py collectstatic --noinput

# exposer le port utilisé par Daphne
EXPOSE 8000

# lancer le serveur ASGI pour channels
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "djangochat.asgi:application"]

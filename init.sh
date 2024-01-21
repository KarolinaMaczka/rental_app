#!/bin/bash

VENV_NAME="venv"

if [ ! -d "$VENV_NAME" ]; then
    echo "Tworzenie środowiska: $VENV_NAME"
    python3 -m venv $VENV_NAME
else
    echo "Środowisko już istnieje."
fi

echo "Aktywacja środowiska"
source $VENV_NAME/bin/activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

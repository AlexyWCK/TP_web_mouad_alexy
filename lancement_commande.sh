#!/bin/bash

if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Activation de l'environnement virtuel..."

echo "Installation des dépendances..."
pip install blinker==1.8.2
pip install Bootstrap-Flask==2.4.0
pip install click==8.1.7
pip install Flask==3.0.3
pip install Flask-Login==0.6.3
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-WTF==1.2.1
pip install greenlet==3.1.0
pip install itsdangerous==2.2.0
pip install Jinja2==3.1.4
pip install MarkupSafe==2.1.5
pip install python-dotenv==1.0.1
pip install PyYAML==6.0.2
pip install SQLAlchemy==2.0.35
pip install typing_extensions==4.12.2
pip install Werkzeug==3.0.4
pip install WTForms==3.1.2

echo "Démarrage de l'application Flask..."
cd tuto/ 
flask run

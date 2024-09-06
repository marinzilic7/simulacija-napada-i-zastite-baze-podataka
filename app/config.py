import os

# config.py
class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  # Ostavite prazno ako niste postavili lozinku za root korisnika
    MYSQL_DB = 'projekt'
    SECRET_KEY = 'ovo-je-moj-tajni-kljuc'  # Unesite ime vaše baze podataka

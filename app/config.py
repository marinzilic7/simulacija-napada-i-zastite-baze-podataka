import os

# config.py
# class Config:
#     MYSQL_HOST = 'mysql'
#     MYSQL_USER = 'projekt'
#     MYSQL_PASSWORD = 'projekt123'  # Ostavite prazno ako niste postavili lozinku za root korisnika
#     MYSQL_DB = 'projekt'
#     SECRET_KEY = 'ovo-je-moj-tajni-kljuc'


class Config:
    MYSQL_HOST = 'localhost'  # XAMPP koristi 'localhost' kao host
    MYSQL_USER = 'root'  # Zadani korisnik za XAMPP je 'root'
    MYSQL_PASSWORD = ''  # Obično nema lozinke za 'root' korisnika u XAMPP-u
    MYSQL_DB = 'projekt'  # Naziv baze podataka koju si kreirao u phpMyAdminu
    SECRET_KEY = 'ovo-je-moj-tajni-kljuc'
  
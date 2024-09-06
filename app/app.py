# app.py
import logging
from flask import Flask, render_template, request, redirect, url_for, flash,session
import MySQLdb
from config import Config
import os 
import time

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'ovo-je-moj-tajni-kljuc'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#Pohrana podataka o neuspjelim pokušajima prijave
failed_login_attempts = {}

# Funkcija za uspostavu veze s bazom podataka
def get_db_connection():
    connection = MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )
    return connection


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/registerUser', methods=['POST'])
def register_user():
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    email = request.form['email']
    password = request.form['password']

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        #Zaštita od SQL injekcija.  
        #Zaštita od SQL injekcija jer podaci nisu uključeni u SQL kod, već su odvojeni.  
        #Metoda za zaštitu baza podataka koja sprječava napade unošenjem malicioznih SQL kodova u upite.
        #Ovdje %s su mjesta rezervirana za parametre koje će cursor.execute automatski zamijeniti s vrijednostima (first_name, last_name, email, password).                                                                                               
        cursor.execute("INSERT INTO users (firstName, lastName, email, password) VALUES (%s, %s, %s, %s)", 
                       (first_name, last_name, email, password))
        connection.commit()
        flash('Korisnik uspješno registriran', 'success')
    except Exception as e:
        flash('An error occurred: ' + str(e), 'danger')
    finally:
        connection.close()

    return redirect(url_for('index'))


# Ovaj kod ispod za prijavu korisnika je ranjiv na SQL injekcije, testiranje SQL injekcije pomocu koje brišemo tablicu users; 
# Za upotrebu SQL injekcije, u polje za unos imena korisnika unesemo: " ' OR '1'='1  " a za lozinku "  '; DROP TABLE users; -- "
# Nakon toga pritisnemo gumb za prijavu i tablica users će biti obrisana.


@app.route('/loginUser', methods=['POST'])
def log_user():
    first_name = request.form['firstName']
    password = request.form['password']
    logging.debug(f"Login attempt with firstName='{first_name}' and password='{password}'")
    connection = get_db_connection()
    cursor = connection.cursor()

    # Neposveđeni SQL upit za testiranje
    query = f"SELECT * FROM users WHERE firstName='{first_name}' AND password='{password}'"
    logging.debug(f"SQL Query: {query}")
    cursor.execute(query)
    user = cursor.fetchone()
    
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        logging.debug(f"Query result: {user}")
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        user = None

    connection.close()

    if user:
        session['user_name'] = user[1]  # Pretpostavlja da je `firstName` na indeksu 1
        session['user_id'] = user[0]    # Pretpostavlja da je `ID_user` na indeksu 0
        return redirect(url_for('home'))
    else:
        flash('Neuspjesna prijava', 'danger')
        return redirect(url_for('login'))
    
# Zastita od SQL injekcija je u sljedecem dijelu koda.

@app.route('/loginUserSafe', methods=['POST'])
def log_user_safe():
    first_name = request.form['firstName']
    password = request.form['password']
    ip_address = request.remote_addr
    current_time = time.time()


    #Bruce Force zastita
    #Provjerava je li IP adresa korisnika prisutna u failed_login_attempts.
    #Ako jest, provjerava broj pokušaja i vrijeme posljednjeg pokušaja. Ako je broj pokušaja >= 5 i manje od jedne minute prošlo od posljednjeg pokušaja, prikazuje poruku o blokadi.


    if ip_address in failed_login_attempts:
        attempts, last_attempt_time = failed_login_attempts[ip_address]
        if attempts >= 5 and (current_time - last_attempt_time) < 60:
            # Izračunaj preostalo vrijeme
            counter = 60 - (current_time - last_attempt_time)
            flash(f'Previše neuspješnih pokušaja prijave. Pokušajte ponovno za {counter:.0f} sekundi.', 'danger')
            return redirect(url_for('login'))

    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE firstName=%s AND password=%s"
    cursor.execute(query, (first_name, password))
    user = cursor.fetchone()

    if user:
        session['user_name'] = user[1]  # Pretpostavlja da je `firstName` na indeksu 1
        session['user_id'] = user[0]    # Pretpostavlja da je `ID_user` na indeksu 0
        failed_login_attempts.pop(ip_address, None)
        connection.close()
        return redirect(url_for('home'))
    else:
        if ip_address in failed_login_attempts:
            failed_login_attempts[ip_address][0] += 1
        else:
            failed_login_attempts[ip_address] = [1, current_time]

        flash('Neuspješna prijava', 'danger')
        connection.close()
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Uklanja korisničke podatke iz sesije
    session.pop('user_name', None)
    session.pop('user_id', None)
    
    # Preusmjerava na početnu stranicu
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

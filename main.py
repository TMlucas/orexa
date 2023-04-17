# -*- coding: utf-8 -*-
from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite
from datetime import datetime as dt

# ------------------
# application Flask
# ------------------

app = Flask(__name__)

# ---------------------------------------
# fonction pour la gestion 
# ---------------------------------------

# connecte à la BDD, affecte le mode dictionnaire aux résultats de requêtes et renvoie un curseur
def connection_bdd():
	
	con = lite.connect('exemples.db')
	con.row_factory = lite.Row
	
	return con

# connecte à la BDD et renvoie toutes les lignes de la table commande
def selection_commande():
	
	conn = connection_bdd()
	cur = conn.cursor()
	
	cur.execute("SELECT nom, prenom, role FROM personnes")
	
	lignes = cur.fetchall()
	
	conn.close()
	
	return lignes

# connecte à la BDD et insère une nouvelle ligne avec les valeurs de la commande
def insertion_commande(numero, typev, option, date):
	
	try:
		conn = connection_bdd()
		cur = conn.cursor()
		
		cur.execute("INSERT INTO personnes('nom', 'prenom', 'role') VALUES (?,?,?,?)", (numero, type, option, date))
		
		conn.commit()
		
		conn.close()
		
		return True
		
	except lite.Error:
		
		return False

# ---------------------------------------
# les différentes pages (fonctions VUES)
# ---------------------------------------

#Page d'accueil
@app.route('/')
def index():
    return render_template('main.html')

#Vérification des identifiants
@app.route('/check', methods=['GET'])
def check():
    contenu=''
    identifiant, mdp = request.args.get('identifiant'), request.args.get('mdp')
    if (identifiant=='agilean' and mdp=='agilean'):
        contenu+="<meta http-equiv='refresh' content ='0; /agilean' />"
    elif (identifiant=='agilog' and mdp=='agilog'):
        contenu+="<meta http-equiv='refresh' content ='0; /agilog' />"
    else :
        contenu+="<meta http-equiv='refresh' content ='0; /' />"
    return contenu


@app.route('/agilean')
def agilean():
    return render_template('agilean.html')

@app.route('/agilean_commande', methods=['GET'])
def agilean_commande():
    numero=request.args.get('numero-commande', '')
    typev=request.args.get('type-commande', '')
    option = request.args.getlist('options')
    date=request.args.get('date', '')
    print (numero, typev, option)
    
    return contenu

@app.route('/agilean_contrats')
def agilean_contrats():
    lignes=selection_commande()
    return render_template('agilean_contrats.html', commandes=lignes)

@app.route('/agilog')
def agilog():
    return render_template('agilog.html')

@app.route('/agilog_contrats')
def agilog_contrats():
    return render_template('agilog_contrats.html')

# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug=True)
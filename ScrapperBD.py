import sqlite3

def creation_BD():
    conn=sqlite3.connect('gestion_scrapper.db')
    cur= conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS table_site(
                    identifiant_site INTEGER PRIMARY KEY AUTOINCREMENT,
                    lien_du_site TEXT NOT NULL,
                    nom_du_site TEXT NOT NULL
                    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS actualiter(
                    identifiant_de_actualite INTEGER PRIMARY KEY AUTOINCREMENT,
                    titre_actualiter TEXT NOT NULL,
                    nom_auteur TEXT NOT NULL,
                    date_publication TEXT NOT NULL,
                    description_actualite TEXT NOT NULL,
                    date_entrer_base_de_donne DATE,
                    identifiant_site INTEGER NOT NULL,
                    FOREIGN KEY(identifiant_site) REFERENCES table_site(identifiant_site)
                    )''')
    conn.close()
def ajout_de_site_wakasera(url):
    creation_BD()
    conn=sqlite3.connect('gestion_scrapper.db')
    conn.commit()


    cur= conn.cursor()
    cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'wakatsera'))
    """cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'burkinademain'))
    cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'burkina24'))
    cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'fasozine'))
    cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'lefaso'))"""

    conn.commit()
def ajout_de_site_burkinademain(url):
    creation_BD()
    conn=sqlite3.connect('gestion_scrapper.db')
    conn.commit()


    cur= conn.cursor()
    #cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'wakatsera'))
    cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'burkinademain'))
    """cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'burkina24'))
    cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'fasozine'))
    cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'lefaso'))"""

    conn.commit()
def ajout_de_site_burkina24(url):
    creation_BD()
    conn=sqlite3.connect('gestion_scrapper.db')
    conn.commit()


    cur= conn.cursor()
    #cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'wakatsera'))
    #cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'burkinademain'))
    cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'burkina24'))
    """cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'fasozine'))
    cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'lefaso'))"""

    conn.commit()
def ajout_de_site_fasozine(url):
    creation_BD()
    conn=sqlite3.connect('gestion_scrapper.db')
    conn.commit()


    cur= conn.cursor()
    #cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'wakatsera'))
    #cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'burkinademain'))
    #cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'burkina24'))
    cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'fasozine'))
    """cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'lefaso'))"""

    conn.commit()
def ajout_de_site_lefaso(url):
    creation_BD()
    conn=sqlite3.connect('gestion_scrapper.db')
    conn.commit()


    cur= conn.cursor()
    #cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'wakatsera'))
    #cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'burkinademain'))
    #cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'burkina24'))
    #cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'fasozine'))
    cur.execute("INSERT INTO table_site(lien_du_site,nom_du_site) VALUES (?,?)",(url,'lefaso'))

    conn.commit()
def enregistrer(titre, auteur, date, description, date_entrer, identifiant_site):
    conn = sqlite3.connect('gestion_scrapper.db')
    creation_BD()
    cur = conn.cursor()
    
    conn.commit()
    
    terme = (titre, auteur, date, description, date_entrer)

    cur.execute("INSERT INTO actualiter(titre_actualiter, nom_auteur, date_publication, description_actualite, date_entrer_base_de_donne, identifiant_site) VALUES (?, ?, ?, ?, ?, ?)", terme + (identifiant_site,))
    conn.commit()
    conn.close()


def retouver_id(url):
    conn = sqlite3.connect('gestion_scrapper.db')
    cur = conn.cursor()

    # Pas besoin de créer la BD à cet endroit
    # creation_BD()

    id = url

    # Utilisez fetchone() pour récupérer la première ligne de la requête
    cur.execute("SELECT identifiant_site FROM table_site WHERE lien_du_site=?", (id,))
    val = cur.fetchone()

    # Fermez la connexion après avoir récupéré la valeur
    conn.close()

    # Vérifiez si val est vide avant de retourner
    return val[0] if val else None
def recuperer_derniers_resultats(url):
    creation_BD()
    conn=sqlite3.connect('gestion_scrapper.db')
    conn.commit()
    cur = conn.cursor()

    # Requête pour récupérer les deux derniers résultats en fonction de l'URL
def recuperer_derniers_resultats(url):
    creation_BD()
    conn = sqlite3.connect('gestion_scrapper.db')
    conn.commit()
    cur = conn.cursor()
        
        # Requête pour récupérer les deux derniers résultats en fonction de l'URL
    cur.execute('''SELECT a.titre_actualiter, a.nom_auteur, a.date_publication, a.description_actualite
                FROM actualiter a
                JOIN table_site s ON a.identifiant_site = s.identifiant_site
                WHERE s.lien_du_site = ?
                ORDER BY a.date_entrer_base_de_donne DESC
                LIMIT 2''', (url,))
    resultats = cur.fetchall()

    conn.close()

    return resultats





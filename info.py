from tkinter import *
import sqlite3
from tkinter.messagebox import showinfo, showerror
import ScrapperBD
import wakasera
import fasozine
import List_URL_BURKINA24
import List_URL_BURKINADEMain
import Lefaso

def valider():
    url_saisie = entree.get()
    if url_saisie in ["https://www.wakatsera.com/", "https://fasozine.com/", "https://burkina24.com/", "https://www.burkinademain.com/", "https://lefaso.net/"]:
        conn = sqlite3.connect('gestion_scrapper.db')
        cur = conn.cursor()
        cur.execute("SELECT lien_du_site FROM table_site WHERE lien_du_site=?", (url_saisie,))
        result = cur.fetchone()
        if result:
            showinfo(title="Info", message="L'URL est déjà dans la base de données.")
        else:
            if url_saisie == "https://www.wakatsera.com/":
                cur.execute("INSERT INTO table_site (lien_du_site,nom_du_site) VALUES (?,?)", (url_saisie,"wakatsera"))
            elif url_saisie == "https://fasozine.com/":
                #url_saisie="https://fasozine.com/actualite/"
                cur.execute("INSERT INTO table_site (lien_du_site,nom_du_site) VALUES (?,?)", (url_saisie,"fasozine"))
            elif url_saisie == "https://burkina24.com/":
                 cur.execute("INSERT INTO table_site (lien_du_site,nom_du_site) VALUES (?,?)", (url_saisie,"burkina24"))
            elif url_saisie == "https://www.burkinademain.com/":
                cur.execute("INSERT INTO table_site (lien_du_site,nom_du_site) VALUES (?,?)", (url_saisie,"burkina_demain"))
            elif url_saisie == "https://lefaso.net/":
                cur.execute("INSERT INTO table_site (lien_du_site,nom_du_site) VALUES (?,?)", (url_saisie,"lefaso"))
            conn.commit()
            conn.close()
        #actualiter_afficher(url_saisie)
    else:
        showerror(title="Erreur", message="Url non valide.")

def actualiter_afficher(url_recuper):
    resultat = None
    try:
        if url_recuper == "https://www.wakatsera.com/":
            #identifiant_site = ScrapperBD.ajout_de_site_wakasera(url_recuper)
            wakasera.requete_b24()
            resultat = ScrapperBD.recuperer_derniers_resultats("https://www.wakatsera.com/")
        elif url_recuper == "https://fasozine.com/":
            #identifiant_site = ScrapperBD.ajout_de_site_fasozine(url_recuper)
            fasozine.requete_b24()
            resultat = ScrapperBD.recuperer_derniers_resultats("https://fasozine.com/")
        elif url_recuper == "https://burkina24.com/":
            #identifiant_site = ScrapperBD.ajout_de_site_burkina24(url_recuper)
            List_URL_BURKINA24.requete_b24()
            resultat = ScrapperBD.recuperer_derniers_resultats("https://burkina24.com/")
        elif url_recuper == "https://www.burkinademain.com/":
            #identifiant_site = ScrapperBD.ajout_de_site_burkinademain(url_recuper)
            List_URL_BURKINADEMain.requete_b24()
            resultat = ScrapperBD.recuperer_derniers_resultats("https://www.burkinademain.com/")
        elif url_recuper == "https://lefaso.net/":
            #identifiant_site = ScrapperBD.ajout_de_site_lefaso(url_recuper)
            Lefaso.requete_b24()
            resultat = ScrapperBD.recuperer_derniers_resultats("https://lefaso.net/")
        else:
            showerror(title="Erreur", message="Url non valide.")
    except Exception as e:
        showerror(title="Erreur", message=str(e))
    if resultat:
        # Convertir resultat en une chaîne de caractères si c'est une liste
        ancien_contenu = resultat_text.get("1.0", "end-1c")
        ancien_contenu_str = "".join(ancien_contenu)

        if isinstance(resultat, list):
            resultat_str = "\n".join(str(item) for item in resultat)
        else:
            resultat_str = str(resultat)

        resultat_text.delete("1.0", "end")
        resultat_text.insert("end", ancien_contenu_str + "\n" + resultat_str)

    else:
        showerror(title="Erreur", message="Impossible de récupérer les résultats.")

def supprimer_dans_base(selection):
    conn = sqlite3.connect('gestion_scrapper.db')
    cur = conn.cursor()
    cur.execute("SELECT identifiant_site FROM table_site WHERE lien_du_site=?", (selection,))
    identifiant = cur.fetchone()[0]
    cur.execute("DELETE FROM table_site WHERE lien_du_site=?", (selection,))
    cur.execute("DELETE FROM actualiter WHERE identifiant_site=?", (identifiant,))
    conn.commit()
    conn.close()

def fonction_de_suppression(url):
    supprimer_dans_base(url)
    list_titre()

def valider_modification(selection, nouvelle_url):
    conn = sqlite3.connect('gestion_scrapper.db')
    cur = conn.cursor()
    cur.execute("UPDATE table_site SET lien_du_site=? WHERE lien_du_site=?", (nouvelle_url, selection))
    conn.commit()
    conn.close()
    #list_titre()

def modifier_url(url):
    modal = Toplevel(fenetre)
    modal.title("Modifier l'URL")
    value_modal = StringVar()
    value_modal.set(url)
    entree_modal = Entry(modal, textvariable=value_modal, width=30)
    entree_modal.pack()
    def valider_modif():
        nouvelle_url = entree_modal.get()
        valider_modification(url, nouvelle_url)
        modal.destroy()
    bouton_valider = Button(modal, text="Valider", command=valider_modif)
    bouton_valider.pack()

def afficher_boutons(frame, url):
    Button(frame, text="Modifier", command=lambda: modifier_url(url)).pack(side=LEFT)
    Button(frame, text="Supprimer", command=lambda: fonction_de_suppression(url)).pack(side=LEFT)

def list_titre():
    for widget in l2.winfo_children():
        widget.destroy()
    resultats = recherche_titre()
    for resultat in resultats:
        frame = Frame(l2)
        frame.pack(side=TOP, padx=15, pady=20)
        Label(frame, text=resultat[0]).pack(side=LEFT)
        afficher_boutons(frame, resultat[0])

def recherche_titre():
    conn = sqlite3.connect('gestion_scrapper.db')
    cur = conn.cursor()
    cur.execute("SELECT lien_du_site FROM table_site ")
    val = cur.fetchall()
    conn.close()
    return val

fenetre = Tk()
fenetre.title('Scraping des Sites')
fenetre.geometry("800x600")
fenetre.config(background='#CCCCCC')

# Frame pour le renseignement de l'url (en haut à gauche)
l = LabelFrame(fenetre, text="Renseignement de l'url", width=400, height=200)
l.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

# Frame pour les résultats (sur le côté à droite)
l1 = LabelFrame(fenetre, text="Résultat", width=400, height=400)
l1.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

l2 = LabelFrame(fenetre, text="Résultats Affichés", width=400, height=400)
l2.grid(row=0, column=3, padx=10, pady=10, sticky="nw")

Label(l, text="Veuillez remplir tous les champs").grid(row=0, column=0, padx=10, pady=10)
value = StringVar() 
value.set("Entrer votre URL")
entree = Entry(l, textvariable=value, width=30)
entree.grid(row=1, column=0, padx=10, pady=10)

resultat_text = Text(l1, wrap=WORD)
resultat_text.grid(row=0, column=0, padx=10, pady=10)

bouton = Button(l, text="Afficher", command=list_titre)
bouton.grid(row=2, column=0, padx=10, pady=10)

bouton = Button(l, text="Valider", command=valider)
bouton.grid(row=3, column=0, padx=10, pady=10)

bouton = Button(l, text="Rechercher", command=lambda: actualiter_afficher(entree.get()))
bouton.grid(row=4, column=0, padx=10, pady=10)

fenetre.mainloop()
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import ScrapperBD
import os

def get_url(ex):
    liens=[]
    if ex:
        for e in ex:
            liens.append(e.get('href'))
        return liens
    else:
        return None

def get_text(ex):
    texte=[]
    if ex:
        for e in ex:
            texte.append(e.text)
        return texte
    else:
        return None
    
def requete_b24():
    HEADERS= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    urls=[]
    titres=[]
    dates_de_sortie=[]
    auteurs_articles=[]
    i= 1
    j=1
    burkina24_url="https://www.burkinademain.com/"
    response=requests.get(burkina24_url, headers=HEADERS)
    response.encoding=response.apparent_encoding

    if response.status_code==200:
        html=response.text
        fichier=open("burkina_demain.html","w",encoding='utf-8')
        fichier.write(html)
        fichier.close()
        
        donnee=BeautifulSoup(html,"html5lib")
        container=donnee.find("div", class_="wpb_wrapper")
        
        if container != None:
            recup_url=container.find_all("a")
            list_urls=get_url(recup_url)
            list_titres=get_text(recup_url)
            for l in list_titres:
                if l not in titres and l !="":
                    titres.append(l)
                    
            for titre in titres:
                if titre!="":
                    if j<3:
                        nomdufichier="Burkinademain_fichier_titre"+str(j)+".txt"
                        with open(nomdufichier, "w", encoding="UTF-8") as fichier:
                            fichier.write(titre) 
                j=j+1
            
            
            for list_url in list_urls:
                if list_url not in urls:
                    urls.append(list_url)
            
            for url in urls:
                if url:
                    if url!="#":
                        if i< 3:
                            response1=requests.get(url, headers=HEADERS)
                            if response1.status_code==200:
                                print("Fichier ",i)
                                nomdufichier="Burkinademain_fichier"+str(i)+".txt"
                                htlm_url=response1.text
                                donne_url=BeautifulSoup(htlm_url,"html5lib")
                                div_content=donne_url.find("div", class_="td-post-content tagdiv-type")
                                div_date=donne_url.find("span", class_="td-post-date")
                                div_auteur=donne_url.find("div", class_="td-post-author-name")

                                if div_date!=None and div_auteur!=None:
                                    dates=get_text(div_date)
                                    auteurs=get_text(div_auteur)
                                    auteur_final=""
                                    for auteur in auteurs:
                                        if auteur!=""and auteur!=" - " and auteur not in auteurs_articles:
                                            auteur_final=auteur_final+auteur
                                    auteurs_articles.append(auteur_final)
                                    for date in dates:
                                        if date!="" and date not in dates_de_sortie:
                                            dates_de_sortie.append(date)
                                
                                for auteur_article in auteurs_articles:
                                    nomdufichier_auteur="Burkinademain_fichier_auteur"+str(i)+".txt"
                                    with open(nomdufichier_auteur, "w", encoding="UTF-8") as fichier:
                                        fichier.write(auteur_article)
                                
                                for date_de_sortie in dates_de_sortie:
                                    nomdufichier_date="Burkinademain_fichier_date"+str(i)+".txt"
                                    with open(nomdufichier_date, "w", encoding="UTF-8") as fichier:
                                        fichier.write(date_de_sortie)
                                            
                                if os.path.exists(nomdufichier):
                                    os.remove(nomdufichier)
                                if div_content!=None:
                                    descriptions=get_text(div_content.find_all("p"))
                                    for description in descriptions:
                                        if os.path.exists(nomdufichier):
                                            with open(nomdufichier, "a", encoding="UTF-8") as fichier:
                                                fichier.write(description + "\n")
                                        else:
                                            with open(nomdufichier, "w", encoding="UTF-8") as fichier:
                                                fichier.write(description + "\n")               
                                
                                
                            else:
                                print("erreur au niveau de ",list_url,"avec le code erreur de:",response.status_code)
                            
                            i=i+1
                        
    else:
        print("erreur: ",response.status_code)
    
    def lire_et_inserer():
        for i in range(1, 3):  # Boucler sur les fichiers de 1 à 2
            # Lire le titre depuis le fichier
            with open(f'Burkinademain_fichier_titre{i}.txt', 'r', encoding='utf-8') as file:
                titre = file.read().strip()

            # Lire l'auteur depuis le fichier
            with open(f'Burkinademain_fichier_auteur{i}.txt', 'r', encoding='utf-8') as file:
                auteur = file.read().strip()

            # Lire la date depuis le fichier
            with open(f'Burkinademain_fichier_date{i}.txt', 'r', encoding='utf-8') as file:
                date_sortie = file.read().strip()

            # Lire la description depuis le fichier
            with open(f'Burkinademain_fichier{i}.txt', 'r', encoding='utf-8') as file:
                description = file.read().strip()

            # Récupérer l'ID correspondant à l'URL
            ide = ScrapperBD.retouver_id(burkina24_url)

            # Insérer les données dans la base de données
            ScrapperBD.enregistrer(titre, auteur, date_sortie, description, datetime.now(), ide)

# Appeler la fonction pour lire et insérer les données
    lire_et_inserer()

        
        


#requete_b24()

 

        
        




print("FIN")


# coding: utf-8
'''
Mini projet du choixpeau magique avec bonus sur l'entrée d'un profil soi-même

Auteurs : JACQ--BODET Malo
          ROCHER Salomé
          FEFEU Marie
          
'''
# import des modules
import csv
from collections import Counter
from ast import literal_eval
# définition des constantes

K_NEIGHBORS = 5 # nombre de voisins les plus proches

# définition des fonctions

def read_csv_file(file_name):
    """ 
    Ouvre et lit un fichier csv et renvoie un tableau avec le contenu du fichier.
    
    Entrée : file_name, nom du fichier csv
    Sortie : tab, table des éléments du fichier
    """
    with open(file_name, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        tab = [{key : value.replace('\xa0', ' ') for key, value in element.items()} for element in reader]
    return tab

def merge_tables(characters, characteristics):
    """
    Fusion des tableaux personnages et caractéristiques

    Entrées : characters, tableau des personnages 
             characteristics, tableau des caractéristiques
    Sortie : poudlard_characters, tableau indexé avec les deux tables fusionnées
    """
    poudlard_characters = []

    for poudlard_character in characteristics:
        for kaggle_character in characters:
            if poudlard_character['Name'] == kaggle_character['Name']:
                poudlard_character.update(kaggle_character)
                poudlard_characters.append(poudlard_character) 
    return poudlard_characters

def create_indexid(merged_table):
    """
    Indexe le tableau des personnages

    Entrée : merged_table, tableau de caractéristiques des personnages
    Sortie : dictionnaire avec les personnages et leurs identifiants
    """
    return {int(character['Id']): character for character in merged_table}

def distance_calculation(poudlard_characters, profile):
    """
    Calcule la distance euclidienne entre le profil mis en paramètres 
    et chaque sorcier

    Entrées : poudlard_characters, table des personnages et leurs caractériqtiques
             profile, tuple
             
    Sortie : distances, tableau trié de toutes les distances
    """
    index_id_characteristics = {int(character['Id']): 
                                (int(character['Courage']),
                                int(character['Ambition']),
                                int(character['Intelligence']),
                                int(character['Good'])) 
                                for character in poudlard_characters}
    liste_keys = []
    for element in index_id_characteristics.keys():
        liste_keys.append(element)

    distances = []
    p = 0
    res= []
    for element in index_id_characteristics.values():
        for i in range(len(element)):    
            res.append((element[i] - profile[i])**2)
        distances.append((liste_keys[p], sum(res)**0.5))
        p = p + 1
        res = []
    distances.sort(key=lambda x: x[1])
    return distances

def neighbors_index(k, tab):
    """
    Renvoie les k voisins les plus proches

    Entrées : k, entier 
             tab, tableau des distances
             
    Sortie : liste_neighbors_index, tableau des indices
    """
    assert tab != []
    minimal_distance = []
    liste_neighbors_index = []
    minimal_distance.extend(tab[0:k])
    for i in minimal_distance:            
        liste_neighbors_index.append(i[0])
    return liste_neighbors_index


def most_frequent1(list):
    '''
    Renvoie la maison la plus fréquente
    Entrée : list, liste comprenant les k plus proches maisons
    Sortie : maison_finale, liste comprenant la maison attribuée à l'utilisateur
    '''
    houses_dic = {'Gryffindor': 0,
                  'Ravenclaw': 0,
                  'Slytherin': 0,
                  'Hufflepuff': 0}
    for i in list:
        if i == 'Gryffindor':
            houses_dic['Gryffindor'] += 1 
        if i == 'Ravenclaw':
            houses_dic['Ravenclaw'] += 1
        if i == 'Slytherin':
            houses_dic['Slytherin'] += 1
        if i == 'Hufflepuff':
            houses_dic['Hufflepuff'] += 1
    maison_finale = []
    maximum = 0
    for item in houses_dic.items():
        if item[1] > maximum:
            maximum = item[1]
            maison_finale = [item[0]]
        elif item[1] == maximum:
            maison_finale.append(item[0])
    return maison_finale

def fonction_finale(profil):
    '''
    Renvoie les plus proches voisins, leurs maisons et la maison attibuée
    Entrée : profil, liste contenant les différentes valuers des qualités
    Sortie : reponse, litse contenant les plus proches voisins, leurs maisons et la maison attibuée
    '''
    characters_tab = read_csv_file("Characters.csv")
    characteristics_tab = read_csv_file("Caracteristiques_des_persos.csv")
    characters = merge_tables(characters_tab, characteristics_tab)
    index_id = create_indexid(characters) 
    distance = distance_calculation(characters, profil) # Calcul des distances euclidiennes
    index = neighbors_index(K_NEIGHBORS, distance)
    houses = []
    for i in index:
        houses.append(index_id[i]['House']) # Détermine la maison à attribuer   
    final_house = (most_frequent1(houses))
    response = []
    for i in index:
        response.append((index_id[i]['Name'], index_id[i]['House']))
    reponse = []
    reponse.append(final_house)
    reponse.append(response)
    return reponse

def formation_profil(profil_temporaire):
    '''
    Transforme une liste de listes de chaines de caractères ressemblant à un liste de listes de 
    tuples, exemple : [['(5,0,0,5)'], ['(2,5,0,0)']]
    Entrée : profil_temporaire, liste contenant les différentes réponses de l'utilisateur
    Sortie : profil, tableau contenant les valeurs des qualités modifiées
    '''
    profil = []
    courage = 0
    ambition = 0
    intelligence = 0
    good = 0
    l = []
    for j in profil_temporaire[1:]:
        for i in j:            
            l.append(literal_eval(i))   # Permet de transformer en tuple
    for i in l:              # Ici on fait la somme de touts les valeurs
        courage += i[0]    
        ambition += i[1]
        intelligence += i[2]
        good += i[3]
    profil = [courage, ambition, intelligence, good]
    for i in range(len(profil)):
        if profil[i] < 0:
            profil[i] = 0
        if profil[i] > 9:
            profil[i] = 9    
    return profil


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


def most_frequent(list):
    """
    Renvoie le premier élément le plus fréquent. S'il y a égalité, il 
    renvoie le premier de la liste, soit le plus proche du profil de départ

    Entrée : list, liste de maisons
    Sortie : out[0],  élément le plus fréquent de la liste
    """

    counts = Counter(list)
    max_count = counts.most_common(1)[0][1]
    out = [value for value, count in counts.most_common() if count == max_count]

    return out[0]


def determination_personality(profile):
    """
    Associe les valeurs des caractéristiques à leur élément 

    Entrée : profile, tuple
    Sortie : profile_values, tableau de caractéristiques mis à jour
    """
    profile_values = []
    profile_values.append(('Courage', profile[0]))
    profile_values.append(('Ambition', profile[1])), 
    profile_values.append(('Intelligence', profile[2])) 
    profile_values.append(('Tendance au bien', profile[3]))
    return profile_values

def ask_profile():
    """
    Demande à l'utilisateur de séléctionner un profil parmis les 5 existants ou de sélectionner son propre profil
 
    Sortie : profil, tuple de 4 entiers représentant les caractéristiques du profil
    """
    profil = None
    
    first_choice = input("Voulez-vous tester un des profils par défaut (1) ou saisir le votre (2) ? ")

    if first_choice == "1":
        profil1 = (9, 2, 8, 9)
        profil2 = (6, 7, 9, 7)
        profil3 = (3, 8, 6, 3)
        profil4 = (2, 3, 7, 8)
        profil5 = (3, 4, 8, 8)

        answer = input("""Quel profil voulez vous tester ?
                Il y a le profil 1 avec 9 de courage, 2 d'ambition, 8 d'intelligence et 9 de tendance au bien ;
                    le profil 2 avec 6 de courage, 7 d'ambition, 9 d'intelligence et 7 de tendance au bien ;
                    le profil 3 avec 3 de courage, 8 d'ambition, 6 d'intelligence et 3 de tendance au bien ;
                    le profil 4 avec 2 de courage, 3 d'ambition, 7 d'intelligence et 8 de tendance au bien ;
                    ou bien le profil 5 avec 3 de courage, 4 d'ambition, 8 d'intelligence et 8 de tendance au bien
                Tapez le numéro du profil pour savoir à quel maison le choixpeau l'envoie""")

        if answer.isdigit():
            answer = int(answer)
            if answer == 1:
                profil = profil1
            elif answer == 2:
                profil = profil2
            elif answer == 3:
                profil = profil3
            elif answer == 4:
                profil = profil4
            elif answer == 5:
                profil = profil5

    elif first_choice == "2":
        answer = input("""Entrez 4 chiffres de 1 à 9 séparés par un espace qui corresponderont respectivement :
                        au courage,
                        à l'ambition,
                        à l'intelligence
                        et la tendance au bien.""").split()
        answer = list(map(int, answer))
        if (len(answer) == 4):
            profil = tuple(answer)

    return profil

def display_profile(values):
    """
    Affichage du profil

    Entrée : values, tableau (représentant le profil)
    """
    print("Voici votre profil : ")
    for element in values:    
        print(f"Vous avez comme {element[0]} un niveau équivalent à {element[1]}")

def display_neighbors(values):
    """
    Affichage des voisins

    Entrée : values, tableau (représentant le profil) 
    """
    print("Vos voisins les plus proches sont : ")
    for element in values:
        print(f"{element[0]} qui a comme maison {element[1]}")

def display_house(house):
    """
    Affichage de la maison à laquelle le personnage est finalement affecté

    Entrée : house, tableau (représentant le profil) 
    """
    print(f"En fonction de ces voisins, il s'est donc avéré que vous étiez {house}")


# Programme principal avec appel des fonctions

characters_tab = read_csv_file("Characters.csv")
characteristics_tab = read_csv_file("Caracteristiques_des_persos.csv")
characters = merge_tables(characters_tab, characteristics_tab)
index_id = create_indexid(characters)

profil = ask_profile()
if profil == None:
    print("Vous n'avez pas saisi la/les bonnes valeurs. "          "Veuillez recommencer") 
else:         
    distance = distance_calculation(characters, profil) # Calcul des distances euclidiennes

    index = neighbors_index(K_NEIGHBORS, distance)

    houses = []
    for i in index:
        houses.append(index_id[i]['House']) # Détermine la maison à attribuer
    
    final_house = (most_frequent(houses))

    profil_values = determination_personality(profil)

    response = []
    for i in index:
        response.append((index_id[i]['Name'], index_id[i]['House']))
    
    display_profile(profil_values)
    display_neighbors(response)
    display_house(final_house)



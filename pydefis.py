"""Challenges from https://pydefis.callicode.fr
"""
import random
import string
import re
import os.path
import datetime
from locale import setlocale, LC_TIME
import json
import requests
from math import dist, sqrt
from time import sleep
from operator import itemgetter
import unicodedata

from PIL import Image



def lion_nemme() -> str:
    """https://pydefis.callicode.fr/defis/Herculito01Lion/txt
    """
    def valeur(divinite: str) -> int:
        """Compute value of a word from its letters
        A=1, B=2, C=3, etc.
        """
        somme = 0
        for lettre in divinite.upper():
            somme += ord(lettre) - 64

        return somme

    divinites = [
        "ARTEMIS", "ASCLEPIOS", "ATHENA", "ATLAS", "CHARON", "CHIRON", "CRONOS", "DEMETER", "EOS", "ERIS",
        "EROS", "GAIA", "HADES", "HECATE", "HEPHAISTOS", "HERA", "HERMES", "HESTIA", "HYGIE", "LETO", "MAIA",
        "METIS", "MNEMOSYNE", "NYX", "OCEANOS", "OURANOS", "PAN", "PERSEPHONE", "POSEIDON", "RHADAMANTHE",
        "SELENE", "THEMIS", "THETIS", "TRITON", "ZEUS",
    ]
    valeurs_cadran = {}
    for divinite in divinites:
        valeurs_cadran[divinite] = valeur(divinite)

    valeurs_trie = dict(sorted(valeurs_cadran.items(), key=lambda x: x[1]))

    resultat = " ".join(valeurs_trie.keys())
    return resultat


def hen_llinge_obfusque(message: str) -> str:
    """https://pydefis.callicode.fr/defis/C22_Obfuscate01/txt
    - message: message to decrypt
    """
    message_nettoye = message
    l_avant, l_apres = 0, 1

    while l_avant != l_apres:
        l_avant = len(message_nettoye)
        for lettre in string.ascii_lowercase:
            message_nettoye = message_nettoye.replace(
                f'{lettre}{lettre.upper()}', "")
        l_apres = len(message_nettoye)

    return message_nettoye


def lapin_cretin(phrase: str) -> str:
    """https://pydefis.callicode.fr/defis/C22_BwaCode01/txt
    - phrase: text to decrypt
    """
    result = re.sub(pattern="BWA.A", repl="", string=phrase)

    return result


def sudokteur(tableau: str) -> str:
    """https://pydefis.callicode.fr/defis/C23_Sudokteur/txt
    - tableau: digit array to analyze\n
    Return a string
    """
    chiffres = {}
    for i in string.digits:
        chiffres[i] = tableau.count(i)

    nombre_max = max(chiffres.values())
    result = ""
    for x in chiffres:
        result += x * (nombre_max - chiffres[x])

    return result


def pestage_ascii_art() -> None:
    """https://pydefis.callicode.fr/defis/PestageAsciiArt/txt
    The source file, stored in the subfolder /pestage_ascii_art/, must end with a /n, otherwise a bug will be raised.
    The output files will also be stored in /pestage_ascii_art/.
    """
    EMPTY_STRING = ""

    if os.path.isdir("./pestage_ascii_art/"):
        try:
            # store input data in a list
            with open(file="./pestage_ascii_art/pestage_ascii_art.txt", mode="r", encoding="utf-8") as f:
                pestage = f.readlines()
        except FileExistsError as e:
            raise e(
                "Error: 'pestage_ascii_art.txt' not found in './pestage_ascii_art/'.")
        except Exception as g:
            raise g(f"{g.__str__()}.")
    else:
        raise IsADirectoryError(
            "Error: no subfolder '/pestage_ascii_art/' found.")

    # length of each line of input data
    longueur = len(pestage[0])
    # each resulting portrait will be stored in this list, at its own index
    portraits = [EMPTY_STRING, EMPTY_STRING, EMPTY_STRING, EMPTY_STRING]
    for ligne,  chaine in enumerate(pestage):
        for col in range(longueur):
            # compute index pf the portrait
            index = (ligne & 1) + ((col & 1) << 1)
            # add the read character to the portrait
            portraits[index] += chaine[col]

        # create a newline at end of the second even index, the first even index has its own newline
        portraits[index + 2] += "/n"

    # write portraits to text files
    for i in range(4):
        fw = open(
            file=f"./pestage_ascii_art/portrait_{i}.txt", mode="w", encoding="utf-8")
        fw.write(portraits[i])
        fw.close()

    print('End of program.')


def les_hybrides_s01e09() -> str:
    """https://pydefis.callicode.fr/defis/C24_LesHybrides/txt
    """
    bases = {
        "0001": "A",
        "1010": "T",
        "1100": "G",
        "0011": "C",
    }

    # loading DNA sequences
    with open("./les_hybrides_s01e09/sequence_entrees.txt", "r", encoding="utf-8") as f:
        sequences = f.readlines()

    # cleaning list
    for idx, ligne in enumerate(sequences):
        sequences[idx] = ligne.split()[-1]

    result = ""

    # processing
    for idx, ligne in enumerate(sequences, 1):
        for pos in range(0, len(ligne) - 1, 4):
            mot = ligne[pos: pos + 4]
            if mot not in bases:
                result += f'{idx}, '

    result = result[:-2]
    return result


def mots_alpha() -> int:
    """https://pydefis.callicode.fr/defis/C23_MotsAlpha/txt
    Return number of words having letters alphabetically ordered
    """
    def analyse_mot(mots_alpha: list[str | None], mot: str) -> list[str]:
        """Test if letters of mot are in alphabetical order.
        - mots_alpha : list of words having letters alphabetically ordered
        - mot : word to analyse/n
        Return list of words having letters alphabetically ordered
        """
        res = 1
        compare = list(mot.lower())
        for idx, x in enumerate(compare):
            if x in convert:
                compare[idx] = convert[x]
        compare = "".join(compare)

        for x in range(1, len(compare)):
            if compare[x].lower() < compare[x - 1]:
                res = 0
                break

        if res and len(mot) >= 3:
            mots_alpha.append(mot)

        return mots_alpha

    # load list of words
    with open(file="./mots_alpha/liste_donna.txt", mode="r", encoding="utf-8") as f:
        liste_donna = f.readlines()

    mots_alpha = []
    convert = {
        "à": "a",
        "â": "a",
        "é": "e",
        "è": "e",
        "ë": "e",
        "ê": "e",
        "î": "i",
        "ï": "i",
        "ö": "o",
        "ô": "o",
        "ü": "u",
        "û": "u",
        "ÿ": "y",
    }

    for mot in liste_donna:
        mots_alpha = analyse_mot(mots_alpha, mot[:-1])

    return len(mots_alpha)


def les_noms_ont_de_l_importance() -> str:
    """https://pydefis.callicode.fr/defis/C23_NomsEspeces/txt
    """
    with open(file="./les_noms_ont_de_l_importance/liste_especes.txt", mode="r", encoding="utf-8") as f:
        liste_especes = f.readlines()

    especes = []
    for idx, item in enumerate(liste_especes):
        liste_especes[idx] = item[:-1]
        chaine = list(liste_especes[idx].lower())
        while chaine.count(" "):
            chaine.remove(" ")

        long = len(set(chaine))
        especes.append((item[:-1], long, long / len(chaine)))

    especes_triees = sorted(especes, key=itemgetter(2, 0))
    resultat = ""
    for x in range(10):
        resultat += f'{especes_triees[x][0]}, '

    return resultat[:-2]


def fake_news_dalek() -> None:
    """https://pydefis.callicode.fr/defis/C23_FakeNewsDalek/txt
    """
    with open("C:/Users/kobay/OneDrive/Documents/_Formation/_python/\
              udemy_101_exercices_algorithmes_python_corrigés/fake_news_dalek/message_dalek.mp3", mode="rb") as f:
        binaire = f.read()

    message = {}
    message_decode = ""
    idx = 0
    for pos in range(25, 310, 3):
        valeur = binaire[pos: pos + 3]
        dec = int(valeur, 16)
        lettre = str(binaire[dec: dec + 1])[2:3]
        message[idx] = {"hexa": valeur, "dec": dec, "lettre": lettre}
        message_decode += lettre
        idx += 1

    print(message_decode)


def code_konami() -> str:
    """https://pydefis.callicode.fr/defis/C22_KonamiCode/txt
    """
    with open(file="./code_konami/code_et_message.txt", mode="r", encoding="utf-8") as f:
        contenu = f.readlines()

    # clean data
    for i, x in enumerate(contenu):
        contenu[i] = x[:-1]

    # isolate the message
    separation = contenu.index("-------------------------------------")

    # build a dict with signs and alphabet
    alphabet = contenu[:separation]
    dico = {}
    for elem in alphabet:
        result = elem.split(" -> ")
        dico[result[0]] = result[1]

    # build the message
    message = "".join(contenu[separation + 1:])

    print(dico)
    print()
    print(message)

    sixth_test = ""
    for i in range(0, len(message), 2):
        sixth_test += dico[message[i: i + 2]]

    return sixth_test


def calcul_jours_magiques() -> int:
    """https://pydefis.callicode.fr/defis/JourMagique/txt
    Return number of magic dates between 2000-01-01 and today both included
    """
    setlocale(LC_TIME, 'fr_FR.UTF-8')

    la_date = datetime.datetime(2000, 1, 1)
    dates_magiques = []
    while la_date <= datetime.datetime.today():
        jour = la_date.strftime("%A")
        if (len(jour) + la_date.day) % 10 == 0:
            dates_magiques.append(la_date)

        la_date += datetime.timedelta(1)

    return len(dates_magiques)


def un_mail_anodin() -> str:
    """https://pydefis.callicode.fr/defis/SteganoUnicode/txt
    """
    with open(file="./un_mail_anodin/entree.txt", mode="r", encoding="utf-8") as f:
        contenu = f.read()

    accentues = list("Àäàâéèëêïîöôùûü«»ç")
    message = ""
    for car in contenu:
        if car not in string.printable and car not in accentues:
            message += car

    return message


def insaisissable_matrice(etapes: int) -> int:
    """https://pydefis.callicode.fr/defis/AlgoMat/txt
    """
    def formule(nombre: int) -> int:
        """Formula to be applied to nombre.
        - nombre: integer on which to apply formula\n
        Return computed value
        """
        return (9 * nombre + 3) % 19

    source = [
        [17, 3, 4, 14, 5, 17],
        [8, 16, 3, 17, 14, 12],
        [13, 5, 15, 4, 16, 3],
        [14, 7, 3, 16, 3, 2],
        [6, 1, 16, 10, 5, 13],
        [11, 1, 9, 11, 18, 8]
    ]
    matrice = [item for row in source for item in row]
    result = matrice.copy()

    for _ in range(etapes):
        for idx in range(len(result)):
            result[idx] = formule(result[idx])

    return sum(result)


def chiffres_preferes() -> None:
    """https://pydefis.callicode.fr/defis/ChiffresPreferes/txt
    Pour relever ce défi, vous devez calculer et fournir la somme des nombres compris
    entre deux bornes qui contiennent le chiffre 1 ou le chiffre 6 (ou les deux).
    Les deux bornes, qui sont les entrées du problème, sont à inclure dans la somme
    si elles contiennent l'un des chiffres.
    """
    mini, maxi, liste_chiffres = 143, 941, []
    for chiffre in range(mini, maxi + 1):
        if "1" in str(chiffre) or "6" in str(chiffre):
            liste_chiffres.append(chiffre)

    print(liste_chiffres)
    print(f'Résultat = {sum(liste_chiffres)}')


def professeur_guique() -> None:
    """https://pydefis.callicode.fr/defis/Algorithme/txt
    initialiser a, b, c, k et n respectivement à 1, 4, 3, 1 et 0
    répéter tant que k est strictement inférieur à 1000-n
        a ← b
        b ← c + a
        c ← -4*c - 3*a - b
        n ← a + b
        augmenter k de 1
    fin répéter
    """
    a, b, c, k, n = 1, 4, 3, 1, 0
    while k < (1000 - n):
        a = b
        b = c + a
        c = -4 * c - 3 * a - b
        n = a + b

        k += 1

    print(f'{a}, {b}, {c}')


def constante_de_champernowne() -> int:
    """https://pydefis.callicode.fr/defis/Champernowne/txt
    """
    champernowne = ""
    idx = 1
    while len(champernowne) < 500:
        champernowne += str(idx)
        idx += 1

    print(champernowne)

    total = 0
    n1 = 424
    n2 = 493
    for idx, c in enumerate(champernowne[n1 - 1: n2 + 1], start=n1):
        valeur = int(c)
        total += valeur
        print(f'{idx:>3} {valeur} {total:>5}')

    return total


def mon_beau_miroir() -> str:
    """https://pydefis.callicode.fr/defis/MiroirAjout/txt
    """
    def palidrome(nombre: int) -> bool:
        """Check if nombre is a palindrom.
        - nombre: number to check
        Return boolean
        """
        mirror = str(nombre)[::-1]
        return str(nombre) == mirror

    tableau_result = []
    entree = [396, 294, 290, 861, 481, 194, 570, 463, 265, 935]
    for x in entree:
        i = x
        idx = 0
        while 1:
            miroir = int(str(i)[::-1])
            suivant = i + miroir
            idx += 1
            if palidrome(suivant):
                tableau_result.append([suivant, idx])
                break
            else:
                i = suivant

    chaine = "["
    for i in tableau_result:
        chaine += f"[{str(i[0])}, {str(i[1])}] , "

    return f'{chaine[:-3]}]'


def ocean_liquide_mimas() -> None:
    """https://pydefis.callicode.fr/defis/C24_Mimas/txt
    """
    def minimums(profondeurs: list[float], prof_min :float) -> tuple[int , int]:
        """Find minimum of ligne and colonne.
        - profondeurs: list of depths
        - prof_min: minimum depth to search for\n
        Return row and column indexes where prof_min has been found
        """
        for ligne in range(1, hauteur - 1):
            for colonne in range(1, largeur - 1):
                total = 0
                for y in range(-1, 2):
                    for x in range(-1, 2):
                        total += cartes[carte][ligne + y][colonne + x]
                moyenne = total / 9
                profondeurs[ligne][colonne] = round(moyenne, 1)

                if profondeurs[ligne][colonne] < prof_min:
                    prof_min = profondeurs[ligne][colonne]
                    min_ligne = ligne
                    min_colonne = colonne

        return min_ligne, min_colonne

    def get_max_depth() -> tuple[int, int]:
        """Find the deepest point around a given point (y, x).
        Return row and column of that deepest point.
        """
        profondeurs = [[100.0] * hauteur for _ in range(largeur)]
        prof_min = 100.0

        return minimums(profondeurs, prof_min)

    url_get = "https://pydefis.callicode.fr/defis/C24_Mimas/get/Kobaya/a1f1c"
    url_post = "https://pydefis.callicode.fr/defis/C24_Mimas/post/Kobaya/a1f1c"
    objet_cartes = requests.get(url_get, verify=True)
    objet_cartes_json = objet_cartes.json()
    dict_result = {}

    # filter dictionary to keep only keys starting with 'carte'
    # thanks to dictionary comprehension
    cartes = {key: value for key, value in objet_cartes_json.items() if key.startswith('carte')}

    for carte in cartes:
        hauteur = len(cartes[carte])
        largeur = len(cartes[carte][0])
        dict_result[f'trou{carte[-2:]}'] = get_max_depth()

    dict_result['signature'] = objet_cartes_json['signature']
    retour = requests.post(url_post, json=dict_result, verify=True)
    print(retour.json())


def surveillance() -> str:
    """https://pydefis.callicode.fr/defis/C24_Surveillance_1/txt
    """
    with open("./surveillance/entree.txt", mode="r", encoding="utf-8") as f:
        donnees = f.readlines()

    # create list
    coordonnees = []
    for x in donnees:
        coordonnees.append([int(x.split(", ")[0]), int(x.split(", ")[1])])

    del x, donnees, f

    # compute distances between agents
    surveil = []
    for i, agent_1 in enumerate(coordonnees):
        mini = 10**10
        idx_mini = 0
        for j, agent_2 in enumerate(coordonnees):
            if i != j:
                distance = dist(agent_1, agent_2)
                if distance < mini:
                    mini = distance
                    idx_mini = j

        surveil.append(idx_mini)

    liste_result = []
    for i in range(len(coordonnees)):
        if i not in surveil:
            liste_result.append(i)

    liste_result.sort()
    resultat = ""
    for x in liste_result:
        resultat += f'{x}, '

    return resultat[:-2]


def analyse_de_sequences_1_2() -> int:
    """https://pydefis.callicode.fr/defis/C24_AcidesNucleiques_01/txt
    """
    symboles = {
        "A": ["A"],
        "C": ["C"],
        "G": ["G"],
        "U": ["U"],
        "R": ["A", "G"],
        "Y": ["C", "U"],
        "K": ["G", "U"],
        "M": ["A", "C"],
        "S": ["C", "G"],
        "W": ["A", "U"],
        "B": ["C", "G", "U"],
        "D": ["A", "G", "U"],
        "H": ["A", "C", "U"],
        "V": ["A", "C", "G"],
        "N": ["A", "C", "G", "U"]
    }

    entree = "NDNKCNVNUGYWRGCNABGSNCRACGSHWNNCYBCSNVUAAGDCMNKNYNNBNCGUBHUNRANDGDMDRSYMGSNWHNDNCVCMAMCANWKYRKVMWMKC"
    nb_sequences = 1
    for x in entree:
        nb_sequences *= len(symboles[x])

    return str(nb_sequences)[-5:]


def analyse_de_sequences_2_2() -> int:
    """https://pydefis.callicode.fr/defis/C24_AcidesNucleiques_02/txt
    """
    def corresp(sequence: str) -> int:
        """Check if sequence matches motif.
        - sequence: sequence to decrypt\n
        Return 0 if sequence doesn't match motif, else 1
        """
        result = 1
        for idx, lettre in enumerate(sequence):
            if lettre not in symboles[motif[idx]]:
                result = 0
                break

        return result

    with open("./analyse_de_sequences_2_2/symboles.json") as f:
        symboles = json.load(f)

    with open("./analyse_de_sequences_2_2/entree.txt") as f:
        entree = f.read()

    liste_entree = entree.split('\n')
    motif = liste_entree[0]

    total = 0
    for x in liste_entree[2:]:
        total += corresp(x)

    return total


def des_lettres_bien_rangees()-> int:
    """https://pydefis.callicode.fr/defis/C23_MotsAlpha/txt
    """
    with open('./des_lettres_bien_rangees/dico_accentues.json', mode="r", encoding="utf-8") as f:
        dico_accentues = json.load(f)
    with open('./des_lettres_bien_rangees/liste_mots_donna.txt', mode="r", encoding="utf-8") as f:
        liste_mots = f.readlines()
    # remove trailing /n on each line
    # and remove from list items whose lenght is less than 3
    idx = 0
    while idx < len(liste_mots):
        if len(liste_mots[idx]) > 3:
            liste_mots[idx] = liste_mots[idx][:-1]
            idx += 1
        else:
            liste_mots.pop(idx)

    result = 0
    for mot in liste_mots:
        temp = ""
        for pos in range(len(mot)):
            if mot[pos] in dico_accentues:
                temp += dico_accentues[mot[pos]]
            else:
                temp += mot[pos].lower()

            if pos > 0 and temp[pos] < temp[pos -1]:
                break
        else:
            result += 1

    return result


def monnaie() -> str:
    """https://pydefis.callicode.fr/defis/Monnaie/txt
    """
    pieces = (50, 20, 10, 5, 2, 1)
    pieces_utilisees = [0, 0, 0, 0, 0, 0]
    rembourse = (47, 13, 19, 62, 84, 32, 50, 42, 91, 93, 34, 19, 92, 35, 19, 4, 17)

    for remb in rembourse:
        somme = 0
        i = 0
        while somme < remb:
            while pieces[i] <= (remb - somme):
                if somme + pieces[i] <= remb:
                    somme += pieces[i]
                    pieces_utilisees[i] += 1

            i += 1

    result = "("
    for i in pieces_utilisees:
        result += f'{i}, '
    result = result[:-2]
    result += ")"

    return result


def des_lettres_bien_rangees_2() -> int:
    """https://pydefis.callicode.fr/defis/C23_MotsAlpha/txt
    Wrongly refectored by Copilot !
    """
    def load_words(file_path: str) -> list[str]:
        """Load words from file while ignoring those whose length is less than 3.
        - file_path: path to file\n
        Return list of words
        """
        with open(file_path, mode="r", encoding="utf-8") as f:
            words = f.readlines()
        return [word.strip() for word in words if len(word.strip()) > 3]


    def normalize_word(word: str, accent_map: dict[str, str]) -> str:
        """Normalize word by removing accents and converting to lowercase.
        - word: word to normalize
        - accent_map: dictionary of accents to remove
        Return normalized word
        """
        normalized = ""
        for char in word:
            if char in accent_map:
                normalized += accent_map[char]
            else:
                normalized += char.lower()
        return normalized


    def is_alphabetical(word: str) -> bool:
        """Check if letters of word are in alphabetical order.
        - word: word to analyze
        Return boolean
        """
        for i in range(1, len(word)):
            if word[i] < word[i - 1]:
                return False
        return True

    accent_map = {
        'à': 'a', 'é': 'e', 'è': 'e', 'ë': 'e', 'ê': 'e',
        'ì': 'i', 'ï': 'i', 'î': 'i', 'ò': 'o', 'ö': 'o',
        'ô': 'o', 'ù': 'u', 'û': 'u', 'ü': 'u', 'ÿ': 'y'
    }
    file_path = './des_lettres_bien_rangees/liste_mots_donna.txt'
    words = load_words(file_path)

    count = 0
    for word in words:
        normalized_word = normalize_word(word, accent_map)
        if is_alphabetical(normalized_word):
            count += 1

    return count


def persistance(nombre_1: int, nombre_2: int) -> list[int]:
    """https://pydefis.callicode.fr/defis/Persistance/txt
    """
    result = [0] * 10

    def calcul_persistance(nombre: int) -> int:
        """Calculate the persistence of a number.
        - nombre: number to analyze\n
        Return persistence
        """
        while nombre > 9:
            produit = 1
            for chiffre in str(nombre):
                produit *= int(chiffre)
            nombre = produit

        return produit

    for i in range(nombre_1, nombre_2 + 1):
        result[calcul_persistance(i)] += 1

    # ignore first element 0
    return result[1:]


def exemple_url_1() -> None:
    """https://pydefis.callicode.fr/defis/ExempleURL/txt
    """
    from defis_url import DefisUrl

    d = DefisUrl("https://pydefis.callicode.fr/defis/ExempleURL/get/Kobaya/96190", verify=True)
    lignes = d.get()
    somme = int(lignes[0]) + int(lignes[1])

    retour = d.post(somme)

    print(retour)

    del DefisUrl


def exemple_url_2() -> None:
    """https://pydefis.callicode.fr/defis/ExempleURL/txt
    """
    url_get = "https://pydefis.callicode.fr/defis/ExempleURL/get/Kobaya/96190"
    url_post = "https://pydefis.callicode.fr/defis/ExempleURL/post/Kobaya/96190"

    res = requests.get(url_get, verify=True)
    lignes = res.text.split("\n")
    somme = int(lignes[1]) + int(lignes[2])
    ret = requests.post(url_post, verify=True, data={"sig": lignes[0], "rep": somme})
    print(ret.text)


def nombres_riches(mini: int, maxi: int) -> list[int]:
    """https://pydefis.callicode.fr/defis/NombresRiches/txt
    """
    def tous_les_chiffres(chiffres: list[int]) -> bool:
        """Check if all digits are present in chiffres.
        - chiffres: list of digits\n
        Return boolean
        """
        for chiffre in chiffres:
            if chiffre == 0:
                return False

        return True

    result = []
    for x in range(mini, maxi + 1):
        chiffres = [0] * 10

        carre = str(x ** 2)
        cube = str(x ** 3)

        for chiffre in carre + cube:
            chiffres[int(chiffre)] += 1

        if tous_les_chiffres(chiffres):
            result.append(x)

    return result


def message_de_l_espace() -> list[int]:
    """https://pydefis.callicode.fr/defis/C24_Seti/txt
    """
    import zipfile
    from os import remove
    from glob import glob

    def detecte_doublons(enregistrements: list[str]) -> int:
        """Detect if characters are duplicated in a string.
        If no duplicates in a string, then it is a "rare sequence".
        - enregistrements: list of strings\n
        Returns number of rare sequences in enregistrements
        """
        nb_sequences_rares = 0
        for sequence in enregistrements:
            mots = analyse_bloc_4_lettres(sequence)

            if sum(mots.values()) == 48:
                nb_sequences_rares += 1

        return nb_sequences_rares

    def analyse_bloc_4_lettres(sequence: str) -> dict[str, int]:
        """Analyse a sequence of 4 letters.
        - sequence: string of 15 letters\n
        Returns a dictionary of 4-letter words with their count of unique letters
        """
        mots = {}
        for i in range(len(sequence) - 4):
            bloc_4_lettres = sequence[i: i + 4]
            quatres_lettres = {}
            for j in range(4):
                if quatres_lettres.get(bloc_4_lettres[j]):
                    quatres_lettres[bloc_4_lettres[j]] += 1
                else:
                    quatres_lettres[bloc_4_lettres[j]] = 1
            mots[bloc_4_lettres] = len(quatres_lettres)

        return mots

    my_zip_file = "./message_de_l_espace/radio_enregistrements.zip"
    destination_folder = "./message_de_l_espace"

    files = glob("./message_de_l_espace/*.txt")
    for file in files:
        remove(file)

    with zipfile.ZipFile(my_zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)

    result = []
    files = glob("./message_de_l_espace/*.txt")
    for file in files:
        with open(file, mode="r", encoding="utf-8") as f:
            enregistrements = f.readlines()

        numero_fic = re.search(r"(\d{3})", file).group(1)
        n = detecte_doublons(enregistrements)
        if n < 172 or n > 235:
            result.append(int(numero_fic))

        print(f"Fichier {numero_fic}")
        print(result)

    del remove, glob, zipfile

    return result


def les_cartes_chocogrenouille_a_trier() -> str:
    """https://pydefis.callicode.fr/defis/MLPotter01/txt
    """
    url_carte = (
        "https://pydefis.callicode.fr/defis/MLPotter01/intern/"
        "aMI7JVIH+mN1UYdSNih7hMO9A0wstHyI2QyDe7tkV2RmjDs3/card.png"
    )
    url_nom_personnage = (
        "https://pydefis.callicode.fr/defis/MLPotter01/intern/"
        "aMI7JVIH+mN1UYdSNih7hMO9A0wstHyI2QyDe7tkV2RmjDs3/reponse"
    )

    personnages = ["harry", "hermione", "ron", "luna", "neville", "ginny", "fred", "george", "dobby", "hedwige"]

    idx = 1
    while idx <= 100:
        reponse = requests.get(url_carte, verify=True)
        image = reponse.text
        idhr = image.find("IHDR")
        image = image[idhr:]
        image = "\x80\x50\x4E\x47\x0D\x0A\x1A\x0A" + image
        if reponse.text.startswith("Password"):
            mot_de_passe = reponse.text.split(": ")[1]
            break

        alea = random.randint(0, len(personnages) - 1)
        sleep(1)
        retour = requests.get(f'{url_nom_personnage}/{personnages[alea]}', verify=True)
        print(f'{idx:>3} {retour.text[:-1]}')

        with open(f"./les_cartes_chocogrenouille/{idx:0>3}_{retour.text[1:-2]}.png", "wb") as f:
            f.write(image.encode())

        idx += 1

    return mot_de_passe


def sa_legende_est_son_anagramme() -> None:
    """https://pydefis.callicode.fr/defis/NomAnagramme1/txt"""
    def remove_accents(input_str: str) -> str:
        """Normalized the chain using the form NFD (normalization form decomposition) which breaks down
        the characterized characters into basic characters + accents
        Args:
            input_str (str): string to process
        Returns:
            str: processed string
        """
        normalized_str = unicodedata.normalize('NFD', input_str)
        # remove all characters of category "Mn" (Mark, Nonspacing), which are accents,
        # using comprehension list
        return ''.join(
            char for char in normalized_str
            if unicodedata.category(char) != 'Mn'
        )

    agent = "Pierre Maréchal"
    with open(file="./sa_legende_est_son_anagramme/texte.txt", mode="r", encoding="utf-8") as f:
        noms = f.readlines()

    # get rid of accent
    lettres_agent = remove_accents(agent)
    # get rid of spaces and put all characters in lower case
    lettres_agent = lettres_agent.replace(" ", "").lower()
    # sort letters for future comparison
    lettres_agent = sorted(lettres_agent)
    # browse all names in the file
    for n in noms:
        # get rid of accent and final newline
        nom = remove_accents(n[:-1])
        nom = nom.replace(" ", "").lower()
        nom = sorted(nom)
        if nom == lettres_agent:
            print(n)
            break


def desamorcage_d_un_explosif_1() -> None:
    """https://pydefis.callicode.fr/defis/Desamorcage01/txt"""
    entree = "797114"
    u = entree[:3]
    n = entree[3:]

    res = int(u)
    for i in range(1, int(n) + 1):
        res *= 13
        res = int(str(res)[-3:])
        print(f"{i:>3} {res}")

    print(res)


def sequence_cesar() -> None:
    """https://pydefis.callicode.fr/defis/Sequence_Cesar/txt"""
    def decode_cesar(seq: str, dec: int) -> str:
        """Returns seq shifted by dec.
        Args:
            seq (str): sequence to be shifted
            dec (int): number of shift
        Returns:
            str: shifted sequence
        """
        res = ""
        for l in seq:
            decalage = (ord(l) - 65 + dec) % 26
            res += chr(decalage + 65)

        return res


    with open(file="./sequences_cesar/sequences.txt", mode="r", encoding="utf-8") as f:
        sequences = f.readlines()

    indices = ["SECRET", "TROUVER"]
    end = False

    for i, seq in enumerate(iterable=sequences, start=1):
        for dec in range(1, 25):
            seq_decode = decode_cesar(seq[:-1], dec)
            if indices[0] in seq_decode and indices[1] in seq_decode:
                print(f"{i} {seq_decode}")
                end = True
                break
        if end:
            break


def  le_sanglier_d_erymanthe() -> None:
    """https://pydefis.callicode.fr/defis/Herculito04Sanglier/txt"""
    def calcul(point_haut: int, point_bas: int) -> int:
        """Compute number of throwed stones.
        Args:
            point_haut (int): higher altitude
            point_bas (int): lower altitude
        Returns:
            int: number of throwed stones
        """
        return int((point_haut - point_bas) / 10) + 1


    entree = [
        0, 20, 10, 120, 40, 170, 40, 60, 50, 100,
        50, 180, 170, 180, 80, 130, 10, 150, 120, 130,
        80, 170, 60, 110, 10, 60, 20, 180, 40, 50,
        10, 70, 40, 190, 80, 130, 110, 190, 60, 170,
        10, 200, 20, 50, 20, 180, 30, 70, 30, 130,
        80, 120, 100, 140, 100, 110, 70, 170, 160, 180,
        170, 200, 50, 170, 100, 130, 60, 70, 10, 180, 150,
        180, 100, 140, 110, 120, 60, 100, 90, 180, 160, 190,
        80, 90, 80, 90, 60, 90, 30, 80, 70, 110, 10, 110,
        60, 70, 50, 180, 90, 140, 70, 160, 90, 200, 110,
        160, 110, 150, 30, 100, 50, 120, 30, 160, 150, 200,
        40, 120, 40, 90, 50, 170, 60, 140, 60, 150, 110,
        200, 120, 130, 20, 110, 100, 170, 20, 200, 130, 180,
        70, 140, 20, 30, 20, 90, 50, 80, 60, 110, 50, 120,
        30, 180, 160, 170, 140, 180, 100, 170, 20, 130, 50,
        100, 70, 190, 170, 200, 180, 190, 30, 50, 30, 40,
        30, 150, 30, 70, 20, 180, 40, 60, 50, 190, 70, 170,
        90, 150, 30, 100, 60, 100, 10, 60, 20, 150, 130,
        180, 140, 190, 70, 150, 140, 180, 0
    ]
    nb_cailloux = 0
    for i in range(1, len(entree)):
        if entree[i] < entree[i - 1]:
            nb_cailloux += calcul(entree[i - 1], entree[i])

    print(f"\nRésultat = {nb_cailloux}")


def herculito_xi() -> None:
    """https://pydefis.callicode.fr/defis/Herculito11Pommes/txt"""
    total_pommes = 0
    for x in range(1, 51):
        nb_pommes = x * x
        res__complet = nb_pommes / 3
        res_entier = nb_pommes // 3
        if res__complet == res_entier:
            total_pommes += nb_pommes
        print(x, nb_pommes, total_pommes)

    print(f"Résultat = {total_pommes}")


def desamorcage_a_la_tony_stark() -> None:
    """https://pydefis.callicode.fr/defis/SpymasterBomb/txt"""
    def multiple(chiffre: int) -> int:
        """Check if chiffre is a multiple of 3 or 5.
        Args:
            chiffre (int): number to test
        Returns: chiffre if multiple of 3 or 5, otherwise 0
        """
        res = (chiffre / 3 == chiffre // 3) or (chiffre / 5 == chiffre // 5)
        return chiffre if res else 0

    entree = 1435
    res = 0
    loo = entree - 1
    while loo:
        res += multiple(loo)
        loo -= 1

    print(f"Résultat={res}")


def le_message_pour_queulorior() -> None:
    """https://pydefis.callicode.fr/defis/Queulorior/txt"""
    entree = """NNEESOOESEENNEEOOSEOSEEENNESENSSENNEESSOOEEE
    NNEEOOSEOSEEENEENOOEESOOSEEEEEEENONSESENNSSENNEESSOOEEEN
    NSSEENNSSEEENOONEEOOSEESEEEENNEESSOOEEENNEESOOEESENNESEN
    SSEEENOONEEOOSEESEEEENNSSEEENNEESOOEESEEEENNEEOOSEOSEEEN
    NEESSOOEEENNEESOOESEENNEEOOSEOSEEEENNOEEOSSEEEEENNEESOOE
    ESOOEEENNEESOOESEENNSSEENNSSENNESNESSENNEEOOSEOSEEENNSSE
    ENNSSEEENOONEEOOSEESENNEEOOSEOSEEEEEENNEESSOOEEENNEEOOSE
    OSEEENNESNESSENNEESOOEESENNSSENNESENSS"""
    import tkinter
    import turtle

    turtle.teleport(-800, 0)

    for l in entree:
        if l =="N":
            turtle.setheading(90)
        elif l == "E":
            turtle.setheading(0)
        elif l == "S":
            turtle.setheading(270)
        elif l == "O":
            turtle.setheading(180)

        turtle.forward(10)

    _ = input()


def sw_iv_on_passe_en_vitesse_lumiere() -> None:
    """https://pydefis.callicode.fr/defis/VitesseLumiere/txt
    Calculate navi-components.
    """
    entree = (997, 312, 663)
    x = entree[0]
    y = entree[1]
    z = entree[2]
    while 10 * x > y :
        x = (y * z) % 10000
        y = (3 * z) % 10000
        z = (7 * z) % 10000

    print(f"Résultat = {x}, {y}, {z}")


def les_victimes_de_tooms_1() -> None:
    """https://pydefis.callicode.fr/defis/C24_DentToomsEasy/txt"""
    def multiple(dt: list[float], dif: float) -> bool:
        """Check if dt is a kind of multiple of tooms.
        Args:
            dt (list[float]): toothprint
            dif (float): difference between first elements
        Returns:
            bool: True if it's a Tooms' toothprint otherwise False
        """
        res = True
        for idx, val in enumerate(dt):
            if (val - dif) != tooms[idx]:
                res = False

        return res

    with open("./les_victimes_de_tooms_1/empreintes.txt") as f:
        raw = f.readlines()

    tooms = [10, 12, 6, 9, 18.5, 22, 7, 4, 9, 10]
    data = []
    result = []

    # split data
    for x in raw:
        splt = x.split(" - ")
        emp = splt[1][:-1].split(", ")
        # transform text to float
        data.append([float(x) for x in emp])

    # search for tooms in data
    for idx, x in enumerate(data, 1):
        diff = round(x[0] - tooms[0], 2)
        if x == tooms or multiple(x, diff):
            result.append(idx)

    print("résultat =", sum(result))


def meli_melo_d_adresses() -> str:
    """https://pydefis.callicode.fr/defis/C24_HashNewton/txt
    Returns:
        str: adresse
    """
    def encode_adr(adresse: str) -> str:
        """Encode adresse counting numbers of occurences of each letter.
        Args:
            adresse (str): address to encode
        Returns adresse encoded
        """
        dico_lettres = {}
        for l in adresse:
            if l in string.ascii_lowercase:
                if l in dico_lettres:
                    dico_lettres[l] += 1
                else:
                    dico_lettres[l] = 1

        # order alphabetically
        dico_lettres = dict(sorted(dico_lettres.items()))
        resu = ""
        for x in dico_lettres:
            resu += f"{dico_lettres[x]}{x}"

        return resu

    entree = "1a6e1g1i1l1m1n1o2r2s2u1y"
    with open("./meli_melo_d_adresses/adresses.txt", mode="r", encoding="utf-8") as f:
        adresses = f.readlines()

    for idx, ad in enumerate(adresses):
        # remove LF
        adresses[idx] = ad[:-1]

        encoded_adr = encode_adr(adresses[idx])
        if encoded_adr == entree:
            return adresses[idx]


def le_jour_de_la_serviette() -> None:
    """https://pydefis.callicode.fr/defis/C25_4_42/txt"""
    FICHIER = "./le_jour_de_la_serviette/resultat.txt"

    def create_result_file() -> None:
        """Create a file containing tuples of figures where
        (a + b + c) = 444 or a * b * c = 444
        """
        f = open(file=FICHIER, encoding="utf-8", mode="w")
        print("\033[1J")

        for a in range(1, 1000):
            for b in range(1, 1000):
                print(f"\033[1;1Ha={a} b={b}")
                for c in range(1, 1000):
                    somme_str = str(a + b + c)
                    produit_str = str(a * b * c)
                    if set(somme_str).issubset(ref) and set(produit_str).issubset(ref):
                        f.write(f"{str((a, b, c))}\n")
            f.flush()

        f.close()

    def find_max_4(list_tuples: list) -> tuple[int, int, int]:
        """Which tuple in list_tuples is the one for which the three numbers most often contain the number 4?
        Args:
            list_tuples (list): list of tuples
        Returns:
            tuple[int, int, int]: the three numbers
        """
        max_4 = 0
        max_tuple = ()
        for t in list_tuples:
            tup = t[1:-1].split(", ")
            count_4 = 0
            for c in tup:
                count_4 += str(c).count("4")

            if count_4 > max_4:
                max_4 = count_4
                max_tuple = t

        return max_tuple


    ref = {"2", "4"}
    if not os.path.exists(FICHIER):
        create_result_file()

    # open result file
    f = open(file=FICHIER, encoding="utf-8", mode="r")
    list_tuples = f.readlines()
    # removing LF
    for idx, l in enumerate(list_tuples):
        list_tuples[idx] = l[:-1]

    print(f"Résultat find_max_4() = {find_max_4(list_tuples)}")


def compter_les_etoiles_chaudes() -> None:
    """https://pydefis.callicode.fr/defis/C23_CompteEtoiles/txt"""
    # open image
    img = Image.open('./compter_les_etoiles_chaudes/ciel.png')
    rgb_img = img.convert('RGB')
    nb_hot_stars = 0
    # browse pixels
    for x in range(rgb_img.width):
        for y in range(rgb_img.height):
            r, g, b = rgb_img.getpixel((x, y))
            if b > r and b > g:
                print(f"x={x:>4} y={y:>4}, r={r:>3} g={g:>3} b={b:>3}")
                nb_hot_stars += 1

    print("Resultat ", nb_hot_stars)


def l_enregistreur_cache_1() -> None:
    """https://pydefis.callicode.fr/defis/C24_MicroCache1/txt"""
    import wave
    from pydub import AudioSegment

    sound1 = AudioSegment.from_file("./l_enregistreeur_cache_1/enregistrement_01a.wav", format="wav")
    sound2 = AudioSegment.from_file("./l_enregistreeur_cache_1/enregistrement_01b.wav", format="wav")

    # sound1 6 dB louder
    louder = sound1 + 6

    # Overlay sound2 over sound1 at position 0 (use louder instead of sound1 to use the louder version)
    overlay_1 = sound1.overlay(sound2, position=0)

    # simple export
    _ = overlay_1.export("output.wav", format="wav")

    del wave


def portrait_colore() -> None:
    """https://pydefis.callicode.fr/defis/LePortraitColore/txt"""
    fichier = "./portrait_colore/portrait.png"
    # charger l'image
    image = Image.open(fichier)
    pixels = image.load()
    largeur, hauteur = image.size

    for y in range(hauteur):
        for x in range(largeur):
            r, g, b = pixels[x, y]
            r_bin = format(r, "b")
            r_bin_rev = r_bin[::-1]
            new_r = int(r_bin_rev, 2)
            g_bin = format(g, "b")
            g_bin_rev = g_bin[::-1]
            new_g = int(g_bin_rev, 2)
            b_bin = format(b, "b")
            b_bin_rev = b_bin[::-1]
            new_b = int(b_bin_rev, 2)

            pixels[x, y] = (new_r, new_g, new_b)

    image.save("./portrait_colore/portrait_verlan.png")
    print("Terminé")


def l_ordre_66_ne_vaut_pas_66() -> bool:
    """https://pydefis.callicode.fr/defis/Ordre66/txt"""
    def impairs(nombre: int) -> bool:
        """Checks if nombre contains only odd figures.
        Args:
            nombre (int): number to check
        Returns:
            bool: True if nombre contains only odd figure, otherwise False
        """
        nombre_str = str(nombre)
        impair = True
        for x in nombre_str:
            chiffre = int(x)
            if chiffre / 2 == chiffre // 2:
                impair = False
                break

        return impair

    def plus_petit(nombre: int) -> bool:
        """Checks if every figure of nombre is strictly smaller than the next one.
        Args:
            nombre (int): number to check
        Returns:
            bool: True if nombre contains only odd figure, otherwise False
        """
        nombre_str = str(nombre)
        plus_petit = True
        taille = len(nombre_str) - 1
        for x in range(taille):
            if nombre_str[x] >= nombre_str[x + 1]:
                plus_petit = False
                break

        return plus_petit

    def produit_pair(nombre: int) -> bool:
        """Checks if the product of figures in nombre only contains odd figures.
        Args:
            nombre (int): number to check
        Returns:
            bool: True if product of figures in nombre only contains odd figures
        """
        nombre_str = str(nombre)
        produit  = 1
        for x in nombre_str:
            produit *= int(x)

        impair = True
        produit_str = str(produit)
        for x in produit_str:
            chiffre = int(x)
            if chiffre / 2 == chiffre // 2:
                impair = False
                break

        return impair

    def somme_pair(nombre: int) -> bool:
        """Checks if the sum of figures in nombre only contains odd figures.
        Args:
            nombre (int): number to check
        Returns:
            bool: True if sum of figures in nombre only contains odd figures
        """
        nombre_str = str(nombre)
        somme  = 0
        for x in nombre_str:
            somme += int(x)

        pair = True
        somme_str = str(somme)
        for x in somme_str:
            chiffre = int(x)
            if chiffre / 2 != chiffre // 2:
                pair = False
                break

        return pair

    for x in range(1111, 10000, 2):
        impair = impairs(x)
        petit = plus_petit(x)
        prod = produit_pair(x)
        som = somme_pair(x)
        if impair or petit or prod or som:
            print(f"{x:>4} {impair:>6} {petit:>6} {prod:>6} {som:>6}")
        if impair and petit and prod and som:
            break


def les_pouvoirs_psychiques_de_psystigri() -> None:
    """https://pydefis.callicode.fr/defis/PsystigriPsy/txt"""
    energie = 78
    objets = [
        -98, -66, 74, -85, 97, 38, 34, -14, 29, -58, 21, 2, 1, 35, 32, 50, -52, 3, -73,
        -13, -99, 86, -71, -86, 50, 8, -78, 89, -41, 77, 34, -59, -57, 49, 43, 100, 25,
        14, -80, -17, 42, -73, -81, 19, -77, -85, -100, 3, 17, 72, 9, 34, 11, 1, 60, 96,
        40, 54, 76, -77, -52, 19, -54, -92, -92, 27, 48, -43, 59, 94, 72, -17, -88, 18,
        2, -77, 86, 66, -67, 51, 14, 79, -58, -1, -21, 76, 60, 51, -26, -91, 32, 79, 36,
        11, -9, 34, -95, -92, -89, -76, 55, 69, -21, -1, 51, 85, 28, 15, -70, 15, 4, -72,
        70, -86, 57, -22, -53, -64, 9, 63, 26, 30, -71, -67, -94, 9, 53, -80, 55, -52,
        -30, 55, 11, 99, 51, -48, 46, -56, -64, 50, -38, 34, 64, 71, -92, 79, -53, -2, 88,
        -8, 96, 14, 14, -89, -90, -19, -26, 17, 97, 70, 62, 83, 28, 96, -55, -72, -37, 20,
        -12, -49, 65, 28, -11, -40, 61, -67, 7, -32, 13, -81, -53, -92, 43, -92, -3, 1,
        -15, -72, 64, -53, -16, 90, -47, -91, 68, 78, -67, 15, -68, -92, -97, -18, -6, 10,
        -37, -47, 60, -17, -2, -51, -46, 65, 81, 46, 33, -15, 82, 96, 28, -21, -41, -87,
        -52, -68, 55, -75, 57, -94, -16, -1, -28, 67, 35, 81, 78, -47, 93, -1, 52, -53,
        14, 2, -15, 14, -82, 43, -48, -53, 52, -7, -27, -89, 80, 22, 90, -29, -53, -22,
        -42, 35, -9, 36, 29, -85, 19, -20, 33, -93, 50, 36, -37, -28, -94, -61, -32, -53,
        -30, -97, -4, -100, -88, -44, 68, 29, -2, 53, -62, -81, -89, 74, 80, 80, 88, -13,
        -90, 15, 1, -45, 3, 4, 81, 55, -94, -91, -62, -60, -52, 45, -52, 77, 10, -63, 43,
        -36, -90, 58, 26, -76, -2, -76, -51, 60, 64, 5, 32, 14, 22, 1, -80, -52, -33, 39,
        74, -60, 32, 42, -83, -62, 0, -43, -61, 77, -96, -63, -60, 92, 68, -53, -53, 5,
        39, -4, 51, 72, -23, 86, 31, 70, 77, 38, -51, 25, -51, 33, -94, -17, 20, -47, 93,
        60, 61, 80, -54, -54, -88, -75, 34, 11, 53, 7, -2, 2, -55, -78, 23, -78, -31, -7,
        10, 85, 41, 20, -93, -7, -31, 55, -62, -54, -35, -66, -70, -98, -13, 98, -15, 70,
        78, 21, -87, -79, -67, 22, 89, 84, -49, 96, 63, 94, 74, 46, 82, -34, 73, 42, 70,
        26, -2, 68, -48, -63, -86, 55, 42, 16, -32, -98, 14, 70, -68, -88, -21, 75, 45,
        18, 10, 71, 93, 99, -58, 42, 14
    ]
    for idx, objet in enumerate(objets, 1):
        if abs(objet) <= energie:
            energie -= 1
        if energie <= 0:
            break

    print(f"Résultat = {idx}")


def le_plus_rare_de_tous() -> None:
    """https://pydefis.callicode.fr/defis/PokePlusRare2/txt"""
    with open(file="./le_plus_rare_de_tous/positions.txt", mode="r", encoding="utf-8") as f:
        positions = f.readlines()

    liste_pokemons = []
    liste_positions = []
    for x in positions:
        val = x[:-1]
        split = val.split(',')
        liste_pokemons.append(split[0])
        liste_positions.append(f"{split[1]},{split[2]}")

    dico_pokemons = {}
    for nom in liste_pokemons:
        trouve = dico_pokemons.get(nom, "erreur")
        if trouve == "erreur":
            dico_pokemons[nom] = 1
        else:
            dico_pokemons[nom] = dico_pokemons[nom] + 1

    m = min(dico_pokemons.items(), key=lambda t: t[1])
    print(f"Résultat = {m}")


def photo_de_vacances() -> None:
    """https://pydefis.callicode.fr/defis/MultiFile01/txt
    Solution : renommer le fichier "photo_000.png" en "photo_000.png.jar" et l'ouvrir...
    """


def les_oiseaux_du_lac_de_stymphale() -> None:
    """https://pydefis.callicode.fr/defis/Herculito06Oiseaux/txt"""
    fichier = "./les_oiseaux_du_lac_de_stymphale/lake.png"
    # charger l'image
    image = Image.open(fichier)
    pixels = image.load()
    largeur, hauteur = image.size

    nb_fleches = 0
    for y in range(hauteur):
        for x in range(largeur):
            val = pixels[x, y]
            nb_fleches += val

    print(f"Résultat = {nb_fleches}")


def cerbere() -> None:
    """https://pydefis.callicode.fr/defis/Herculito12Cerbere/txt"""
    from math import sqrt, floor, ceil

    entree = 13979
    entree_carre = entree**2
    for a in range(1, 13979):
        a_c = a**2

        b = sqrt(entree_carre - a_c)
        b = ceil(b)
        if floor(a_c + b**2) == entree_carre:
            print(f"{a:>5} {b:>5} {floor(a_c + b**2):>12} {entree_carre:>12}")
    print("Terminé.")


def thor_le_narcissique() -> None:
    """https://pydefis.callicode.fr/defis/ThorNarcissique/txt"""
    with open("./thor_le_narcissique/liste_mots.txt", "r", encoding="utf-8") as f:
        mots = f.readlines()

    mots_convenables = 0
    for mot in mots:
        t = mot.count("t")
        h = mot.count("h")
        o = mot.count("o")
        r = mot.count("r")

        if t == 1 and h == 1 and o == 1 and r == 1:
            mots_convenables += 1

    print(f"Résultat = {mots_convenables}")


def le_coffre_d_electro() -> None:
    """https://pydefis.callicode.fr/defis/UrlElectro/txt"""
    HTTPS = "https://"
    url_get = "https://pydefis.callicode.fr/defis/UrlElectro/intern/code/03fCF23cfE"

    while url_get:
        rep = requests.get(url_get, verify=True)
        rep_str = str(rep.content)
        https_count = rep_str.count(HTTPS)
        https = rep_str.find(HTTPS)
        if https_count == 2:
            https = rep_str.find(HTTPS, https + 8)

        fin = rep_str.find(" ", https)
        if fin == -1:
            fin = rep_str.find("'", https)

        url_get = rep_str[https:fin]
        print(url_get)


def la_biche_de_cyrenee() -> None:
    """https://pydefis.callicode.fr/defis/Herculito03Biche/txt"""
    with open(file="./la_biche_de_cyrenee/coordonees.txt", mode="r", encoding="utf-8") as f:
        coordonees = f.read()
    liste_coord_str = coordonees.split(", ")
    liste_coord = [int(l) for l in liste_coord_str]

    distance = 0
    nb_coord = len(liste_coord)
    x = liste_coord[0]
    y = liste_coord[1]
    for coord in range(2, nb_coord, 2):
        nx = liste_coord[coord]
        ny = liste_coord[coord + 1]

        if x == nx:
            distance += abs(ny - y)
        else:
            distance += abs(nx - x)

        x = nx
        y = ny

    print(f"Distance = {distance}")


def balade_sur_un_echiquier() -> None:
    """https://pydefis.callicode.fr/defis/BaladeEchiquier/txt"""
    recup_entree = "https://pydefis.callicode.fr/defis/BaladeEchiquier/get/Kobaya/d2488"
    soumission_rep = "https://pydefis.callicode.fr/defis/BaladeEchiquier/post/Kobaya/d2488"
    ordres = requests.get(recup_entree, verify=True)

    rep = str(ordres.content)
    rep = rep.split("\\n")
    # direction horizontale
    x = 0
    # direction verticale
    y = 1
    # positions de départ
    col = 1
    ligne = 1
    cases_visitees = {}
    cases_visitees[(col, ligne)] = 1

    for ordre in rep[1]:
        if ordre == "A":
            col += x
            ligne += y

            if cases_visitees.get((col, ligne)):
                cases_visitees[(col, ligne)] += 1
            else:
                cases_visitees[(col, ligne)] = 1

        # direction nord
        elif ordre == "D" and x == 0 and y == 1:
            x = 1
            y = 0
        elif ordre == "G" and x == 0 and y == 1:
            x = -1
            y = 0
        # direction est
        elif ordre == "D" and x == 1 and y == 0:
            x = 0
            y = -1
        elif ordre == "G" and x == 1 and y == 0:
            x = 0
            y = 1
        # direction sud
        elif ordre == "D" and x == 0 and y == -1:
            x = -1
            y = 0
        elif ordre == "G" and x == 0 and y == -1:
            x = 1
            y = 0
        # direction ouest
        elif ordre == "D" and x == -1 and y == 0:
            x = 0
            y = 1
        elif ordre == "G" and x == -1 and y == 0:
            x = 0
            y = -1

    reponse = f"{str(len(cases_visitees))}{chr(col + 64)}{ligne}"
    retour = requests.post(soumission_rep, verify=True, data={"sig": rep[0][2:], "rep": reponse})
    print(f"Résultat = {retour.content.decode("utf-8")}")


def toc_boum() -> None:
    """https://pydefis.callicode.fr/defis/TocBoum/txt"""
    nombre = 3188
    resultats = []
    for a in range(1, nombre):
        for b in range(1, nombre):
            if (13 * a + 7 * b == nombre):
                resultats.append((a, b, abs(a - b)))
                print(f"a={a}, b={b}")

    resultats.sort(key=lambda l: l[2])
    print(f"Résultat={resultats[0]}")


def meli_melo_binaire_de_nombres() -> None:
    """https://pydefis.callicode.fr/defis/MelangeBinaire/txt"""
    u = 53
    n = 21

    binaire = bin(u)[2:]
    for _ in range(n):
        nb_un = binaire.count("1")
        binaire += bin(nb_un)[2:]

    print(f"Résultat={int(binaire, 2)}")


def les_chiffres_de_fibonacci() -> None:
    """https://pydefis.callicode.fr/defis/FiboChiffres/txt"""
    entree = 61
    fibo = [0, 1]
    i = 1
    while i:
        new = sum(fibo[-2:])
        somme = 0
        for x in str(new):
            somme += int(x)

        fibo.append(new)
        i += 1

        if somme == entree:
            break


    print(f"Résultat = {new}")


def meli_melo_de_nombres() -> None:
    """https://pydefis.callicode.fr/defis/Melange/txt
    Tout d'abord, on sépare les 2 derniers chiffres des deux premiers, ce qui donne deux nombres: 96 et 97, qu'on ajoute ; nous obtenons 193.
    Puis, on multiplie ce résultat par 188, et on ajoute 188, ce qui donne 36472.
    Enfin, on calcule le reste de la division entière de 36472 par 9973, ce qui donne 6553.
    """
    u = 2963
    n = 105

    while n:
        u_str = str(u)
        u_str = u_str.zfill(4)
        premiers = u_str[:2]
        derniers = u_str[-2:]
        calcul = (int(premiers) + int(derniers)) * 188 + 188
        u = calcul % 9973

        n -= 1

    print(f"Résultat = {u}")


def sommes_de_trois_carres() -> None:
    """https://pydefis.callicode.fr/defis/Somme3Carres/txt
    Beaucoup de nombres peuvent s'écrire comme la somme de 3 carrés.
    Par exemple, 6² = 2² + 3² + 7² et 8 = 2² + 0² + 2². Certains ne peuvent pas, comme 7.
    Combien de nombres inférieurs ou égaux à 10000 ne peuvent pas s'écrire comme somme de 3 carrés ?
    2025-07-12 non résolu
    """
    resultats = {}
    for i in range(10001):
        mini = round(sqrt(i))
        carre = result = 0
        trois = 3
        liste = []
        passage_triple = 0

        while trois:
            result = mini**2
            if (carre + result) <= i:
                carre += result
                liste.append(mini)
                trois -= 1
            if passage_triple > 3:
                passage_triple = 0
                if mini >= 1:
                    mini -= 1
            else:
                passage_triple += 1

        if carre == i:
            resultats[i] = liste
            print(f"{i:>5} {resultats[i]}")

    print(f"Résultat = {len(resultats)}")


def l_hydre_de_lerne() -> None:
    """https://pydefis.callicode.fr/defis/Herculito02Hydre/txt
    - À chaque coup d'épée, Hercule coupait la moitié des têtes restantes.
    - Si après une coupe, il restait un nombre impair de têtes, alors le nombre de têtes restantes triplait instantanément,
    et une tête supplémentaire repoussait encore.
    - Si à un moment l'Hydre ne possédait plus qu'une seule tête, Hercule pouvait l'achever d'un coup d'épée supplémentaire.
    """
    nb_tetes = 8188
    coups_epee = 0
    while nb_tetes:
        coups_epee += 1
        nb_tetes /= 2
        if nb_tetes == 1:
            coups_epee += 1
            nb_tetes = 0
        elif nb_tetes / 2 != nb_tetes // 2:
            nb_tetes *= 3
            nb_tetes += 1

    print(f"Coup d'épée nécessaires = {coups_epee}")


def les_noms_des_ewoks() -> None:
    """https://pydefis.callicode.fr/defis/EwoksSansA/txt"""
    with open(file="./les_noms_des_ewoks/noms_ewoks.txt", mode="r", encoding="utf-8") as f:
        noms = f.readlines()

    noms_sans_a = 0
    for nom in noms:
        if "a" not in nom and "A" not in nom:
            noms_sans_a += 1

    print(f"Résultat = {noms_sans_a}")


def les_noms_des_ewoks_2() -> None:
    """https://pydefis.callicode.fr/defis/EwoksVoyelle/txt"""
    with open(file="./les_noms_des_ewoks_2/noms.txt", mode="r", encoding="utf-8") as f:
        noms = f.readlines()

    voyelles = ["A","E","I","O","U","Y","a","e","i","o","u","y"]
    resultat = 0
    for nom in noms:
        nb_voyelles = 0
        for lettre in nom:
            if lettre in voyelles:
                nb_voyelles += 1

        nb_consonnes = len(nom) - 1 - nb_voyelles
        if nb_consonnes == (nb_voyelles * 2):
            resultat += 1

    print(f"Résultat = {resultat}")


def bombe_a_desamorcer() -> None:
    """https://pydefis.callicode.fr/defis/Desamorcage03/txt"""
    defaut = "34125"
    permutations = [
        25, 31, 43, 12, 12, 43, 31, 35, 54, 23, 12, 23, 12, 21, 45, 43, 41, 45, 43, 45,
        35, 15, 53, 41, 51, 45, 12, 31, 14, 45, 12, 24, 32, 24, 21, 21, 51, 31, 53, 25,
        12, 43, 35, 13, 23, 54, 34, 32, 23, 15, 23, 42, 41, 43, 13, 14, 52, 14, 53, 41,
        14, 43, 35, 42, 32, 21, 51, 52, 24, 51, 12, 12, 52, 34, 35, 54, 21, 41, 32, 32,
        34, 12, 41, 34, 43, 41, 35, 12, 32, 51, 34, 15, 25, 43, 45, 45, 45, 52, 31, 43
    ]

    for id, perm in enumerate(permutations, 1):
        nouveau = ""
        perm_str = str(perm)
        for idx, l in enumerate(defaut):
            if str(idx + 1) == perm_str[0]:
                nouveau += defaut[int(perm_str[1]) - 1]
            elif str(idx + 1) == perm_str[1]:
                nouveau += defaut[int(perm_str[0]) - 1]
            else:
                nouveau += defaut[idx]

        defaut = nouveau
        print(f"{id}/100 - {defaut}")

    print(f"Résultat = {defaut}")


def la_chambre_des_pairs() -> None:
    """https://pydefis.callicode.fr/defis/ChambrePairs/txt
    2025-07-13 non résolu
    """
    alpha_austin = {
        "A": 0,
        "B": 1,
        "M": 2,
        "D": 3,
        "E": 4,
        "F": 5,
        "L": 6,
        "H": 7,
        "I": 8,
        "J": 9,
        "R": 10,
        "G": 11,
        "N": 12,
        "C": 13,
        "O": 14,
        "Q": 15,
        "P": 16,
        "K": 17,
        "S": 18,
        "Y": 19,
        "U": 20,
        "V": 21,
        "W": 22,
        "X": 23,
        "T": 24,
        "Z": 25
    }
    with open(file="./la_chambre_des_pairs/texte.txt", mode="r", encoding="utf-8") as f:
        texte = f.read()

    dates = re.findall(f"AUSTINPOWERSN.+LE\d{2}(PLUS|MOINS)\d{2}AUMOIS\d{2}(PLUS|MOINS)\d{2}EN\d{4}(PLUS|MOINS)\d{2}ANNEES", texte)

    sequences = []
    sequence = ""
    for dat in dates:
        pos = texte.find(dat[0])
        for idx in range(idx_texte, pos):
            if texte[idx] in string.digits:
                if sequence not in ("MOISAUSEINUNEMATERNELLE", "OURSAUSEINUNEMATERNELLE"):
                    sequences.append(sequence)
                sequence = ""
            elif int(alpha_austin[texte[idx]]) % 2 == 0:
                sequence += texte[idx]

        # traitement dates
        chiffres = dat[0].split(dat[1])
        if dat[1] == "PLUS":
            la_date = int(chiffres[0]) + int(chiffres[1])
        elif dat[1] == "MOINS":
            la_date = int(chiffres[0]) - int(chiffres[1])

        sequence += f" {la_date} "
        idx_texte = pos + len(dat[0])

    plus_long = len(max(sequences))
    for seq in sequences:
        if len(seq) == plus_long:
            print(f"Plus longue séquence = {seq}")


def les_ecailles_du_dragon() -> None:
    """https://pydefis.callicode.fr/defis/C22_Dungeons/txt"""
    fichier = "./les_ecailles_du_dragon/dungeons_portal_enc.png"
    # charger l'image
    image = Image.open(fichier)
    pixels = image.load()
    largeur, hauteur = image.size
    n = 10000

    for y in range(hauteur):
        for x in range(largeur):
            val = pixels[x, y]
            # niveau de gris inférieur à 128) ((x^3 + y^7) xor n) % 256
            if val < 128:
                pixels[x, y] = ((x**3 + y**7) ^ n) % 256
            else:
                pixels[x, y] = random.randint(0, 255)

    image.save("./les_ecailles_du_dragon/dungeons_portal_decoded_10000.png")

    print("Fin")

def carte_du_marauder():
    """https://pydefis.callicode.fr/defis/MaraudeurConfusio/txt"""
    fichier = "./carte_du_marauder/maraudeur_cr.png"
    cible = "./carte_du_marauder/maraudeur_cr.png"
    # charger l'image
    image_fichier = Image.open(fichier)
    pixels_fichier = image_fichier.load()
    hauteur, largeur = image_fichier.size

    image_cible = Image.open(cible)
    pixels_cible = image_cible.load()

    a = 53911
    b = 15677
    n = largeur * hauteur
    # (a * i + b) % n
    for x in range(hauteur):
        for y in range(largeur):
            no_pixel = x * (y * largeur)
            new_pos = (a * no_pixel + b) % n
            new_x = new_pos % largeur
            new_y = new_pos % hauteur
            # source color is mode RGBA, so ignore last value (canal alpha)
            pixels_cible[new_x, new_y] = pixels_fichier[x, y][:3]

    image_cible.save("./carte_du_marauder/maraudeur_decrypte.png")
    print("Fin.")


if __name__ == "__main__":
    carte_du_marauder()

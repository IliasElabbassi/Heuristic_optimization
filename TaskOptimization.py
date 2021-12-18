'''
Chaque fichier d'instances contient les n+1 lignes suivantes :
- la première ligne indique le nombre de tâches n
- Chacune des n lignes suivantes (i : {1..n}) contient trois valeurs correspondant respectivement à 
pi (le temps d'execution),
wi (le poids) et
di (la date limite), de la tâche i.
'''

'''
lis l'instance
recrée l'instance dans un ordre aléatoire
calculer le tableau Cj : temps d'éxécution de la tache j
calculer la somme des poids*retard (fct objectif)
'''
import random
import copy
import sys

sys.setrecursionlimit(3000)

class Tache:
    def __init__(self, temps, poids, date_limite):
        self.pi = temps
        self.wi = poids
        self.di = date_limite

# instance un tableau de Tache

def heuristique(instance):
    temps_exec = 0
    somme_poid_retard = 0

    for i in instance:
        temps_exec += i.pi
        somme_poid_retard += max(temps_exec-i.di, 0)*i.wi

    return somme_poid_retard

def recherche_retard(instance, temps_exec):
    tab_retard = []
    for i in instance:
        retard = max(temps_exec-i.di, 0)*i.wi
        if retard > temps_exec:
            tab_retard.append(i)
            instance.remove(i)
    
    for i in instance:
        tab_retard.append(i)
    
    return tab_retard

'''
éxécute la premier valeur de l'instance
pour ensuite réaranger l'instance

cad, que le réarangement ce fais en choisisant toutes les taches en retard
pour les mettre en premier dans l'instance
'''
def heuristique_constuctif(instance):
    temps_exec = 0
    somme_poid_retard = 0
    vide = False

    while not vide:
        if not instance:
            vide = True
        else:
            ele = instance.pop(0)
            temps_exec += ele.pi
            somme_poid_retard += max(temps_exec-ele.di, 0)*ele.wi
            if instance:
                instance = recherche_retard(instance, temps_exec)

    return somme_poid_retard

def aleatoire(instance):
    n = len(instance)
    new = []

    for i in range(n):
        rand = random.choice(instance)
        new.append(rand)
        instance.remove(rand)
    
    return new

def swap(i,j,arr):
    import copy

    c = copy.copy(arr)

    temp = c[i]
    c[i] = c[j]
    c[j] = temp

    return c

def voisin_swap(instance):
    voisins = []

    for i in range(0, len(instance)):
        tache = instance[i]
        if i+1 < len(instance):
            for j in range(i+1, len(instance)):
                voisins.append(swap(
                        i,j,
                        instance
                ))

    return voisins    

'''
On swap les elements et on prend la premiere instance ayant un retard plus petit
'''
def recherche_local(instance):
    print("----- local ------")
    s = ""
    for x in instance:
        s += str(x.pi)
        s+= " "
    print(s)
    result = heuristique(instance)
    print(result)

    voisins = voisin_swap(instance)
    
    for voisin in voisins:
        new_r = heuristique(voisin)
        if new_r < result:
            return recherche_local(voisin)

    return instance

def recherche_local(instance):
    print("----- local ------")
    s = ""
    for x in instance:
        s += str(x.pi)
        s+= " "
    print(s)
    result = heuristique(instance)
    print(result)

    voisins = voisin_swap(instance)
    max = []
    
    for voisin in voisins:
        new_r = heuristique(voisin)
        if new_r < result:
            return recherche_local(voisin)

    return instance
    
def tri(instance):
    return sorted(instance, key=lambda x:(x.pi/x.wi))


if __name__ == "__main__":
    f = open("./inst/n100_15_b.txt", "r")
    n = f.readline()
    instance = []

    for i in range(int(n)):
        line = f.readline()
        var = line.split()
        t = Tache(
            int(var[0]),
            int(var[1]),
            int(var[2])
            )
        instance.append(t)

    to_alea = copy.copy(instance)
    to_sorted = copy.copy(instance)
    inst = copy.copy(instance)

    alea = aleatoire(to_alea)
    sorted = tri(to_sorted)
    alea2 = copy.copy(alea)

    sorted2 = copy.copy(sorted)
    
    print("aleatoire : {0}".format(heuristique(alea)))
    print("trié par temps/poids : {0}".format(heuristique(sorted))) # heuristique sorted by increasing p/w
    print("heuristique constructif : {0}".format(heuristique_constuctif(sorted2))) # sorted + reindex the array with late task first inside the array
    rech_l = recherche_local(alea)
    print("recherche local : {0}".format(heuristique(rech_l)))

    # import random
    # tab_test = []
    # s = ""

    # print("----random test tab----------")
    # for i in range(0,10):
    #     tab_test.append(
    #         random.choice(instance)
    #     )
    #     s += str(tab_test[-1].pi)
    #     s+= " "
    
    # print(s)

    # test_voisins = voisin_swap(tab_test)

    # for t in test_voisins:
    #     print("----- swap ------")
    #     s = ""
    #     for x in t:
    #         s += str(x.pi)
    #         s+= " "
    #     print(s)

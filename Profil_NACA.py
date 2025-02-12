import numpy as np
from matplotlib import pyplot as plt


"""
On demande à l'utilisateur d'entrer le profil voulu, la longueur de corde,
le nombre de points à tracer et la distribution souhaitée. Si l'utilisateur
entre une mauvaise valeur, on boucle jusqu'à ce qu'il en entre une bonne.
"""

while True:

    profil = input('Entrez un profil NACAXXXX : ').lower()

    if len(profil) == 8 and profil[0:4] == 'naca':
        profil = profil[4:8]

    if len(profil) == 4:
        try:
            profil = int(profil)
        except:
            print('Entrée invalide, essayez à nouveau.')
            continue
        break
    else:
        print('Entrée invalide, essayez à nouveau.')

while True:

    corde = input('Entrez la corde en mètre : ')

    try:
        corde = int(corde)
    except:
        print('Entrée invalide, essayez à nouveau.')
        continue
    break

while True:

    nombre_de_points = input('Entrez le nombre de points à tracer pour chaque côté : ')

    try:
        nombre_de_points = int(nombre_de_points)
    except:
        print('Entrée invalide, essayez à nouveau.')
        continue
    break

while True:

    distribution = input('Entrez la distribution voulue entre [G]lauert ou [S]tandard : ').lower()

    if distribution == 'g' or distribution == 's':
        break
    else:
        print('Entrée invalide, essayez à nouveau.')

# On trouve nos paramètres de profil selon le choix de l'utilisateur
m = (profil // 1000) / 100  # Cambrure maximale
profil -= m * 100000
p = (profil // 100) / 10    # Position de la cambrure maximale
profil -= p * 1000
t = profil/100              # Épaisseur max du profil

# On initialise notre x en mode standard
x = np.linspace(0, 1, num = nombre_de_points)

# On applique la transformée de Glauert si désiré par l'utilisateur
if distribution == 'g':
    glauert = np.linspace(0, np.pi, num = nombre_de_points)

    for i in range(nombre_de_points):
        x[i-1] = 0.5*(1-np.cos(glauert[i-1]))

# On initialise nos NDArrays principaux
up = np.zeros((nombre_de_points, 2))
cambrure = np.zeros(nombre_de_points)
up[:, 0] = x.copy()
down = up.copy()

# On calcul notre cambrure
for i in range(nombre_de_points):

    if down[i-1, 0] <= p:
        cambrure[i - 1] = (m / p ** 2) * (2 * p * down[i-1, 0] - down[i-1, 0] ** 2)
    else:
        cambrure[i - 1] = (m / (1 - p) ** 2) * ((1 - 2 * p) + 2 * p * down[i-1, 0] - down[i-1, 0] ** 2)

# On calcul notre profil en incluant la cambrure
for i in range(nombre_de_points):

    up[i-1, 1] = 5 * t * (0.2969 * up[i-1, 0] ** 0.5 - 0.1260 * up[i-1, 0] - 0.3516 * up[i-1, 0] ** 2 +
                0.2843 * up[i-1, 0] ** 3 - 0.1036 * up[i-1, 0] ** 4) + cambrure[i - 1]

    down[i-1, 1] = - 5 * t * (0.2969 * down[i-1, 0] ** 0.5 - 0.1260 * down[i-1, 0] - 0.3516 * down[i-1, 0] ** 2 +
                    0.2843 * down[i-1, 0] ** 3 - 0.1036 * down[i-1, 0] ** 4) + cambrure[i - 1]

# On applique la longueur de corde
up *= corde
down *= corde

# On trouve l'épaisseur max et la position de l'épaisseur max
epaisseur_max = 0
position_epaisseur_max = 0
for i in range(nombre_de_points):
    if up[i-1, 1] - down[i-1, 1] > epaisseur_max:
        epaisseur_max = up[i-1, 1] - down[i-1, 1]
        position_epaisseur_max = up[i-1, 0]
print('Épaisseur maximale = ' + str(epaisseur_max) + ' m')
print('Position de l\'épaisseur maximale = ' + str(position_epaisseur_max) + ' m')
print('Épaisseur maximale adimentionnée (t/c) = ' + str(epaisseur_max/corde))
print('Position de l\'épaisseur maximale adimentionnée (x/c) = ' + str(position_epaisseur_max/corde))

# On définit quelques paramètres pour le graphique
plt.rcParams['font.size'] = 14
plt.rcParams['figure.dpi'] = 200

# On trace le profil
plt.plot(up[:, 0],up[:, 1],label='Extrados', color=(0, 0, 1))
plt.plot(down[:, 0],down[:, 1],label='Intrados', color=(1, 0, 0))
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.title('Profil NACA' + str(int(m*100)) + str(int(p*10)) + str(int(t*100)))
plt.xlim(-corde*0.1, corde*1.1)
plt.ylim(-corde*0.6, corde*0.6)
plt.show()
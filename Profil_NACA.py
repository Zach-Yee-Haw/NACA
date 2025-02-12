import numpy as np
from matplotlib import pyplot as plt


"""
On demande à l'utilisateur d'entrer le profil voulu, la longueur de corde,
le nombre de points à tracer et la distribution souhaitée. Si l'utilisateur
entre une mauvaise valeur, on boucle jusqu'à ce qu'il en entre une bonne.
"""

while True:

    profil = input('Entrez un profil NACAXXXX : ')

    if len(profil) == 8:
        profil = profil[3:7]

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

m = (profil // 1000) / 100
profil -= m * 100000
p = (profil // 100) / 10
profil -= p * 1000
t = profil/100


xdown = np.linspace(0, 1, num = nombre_de_points)

if distribution == 'g':
    glauert = np.linspace(0, np.pi, num = nombre_de_points)

    for i in range(nombre_de_points):
        xdown[i-1] = 0.5*(1-np.cos(glauert[i-1]))

xup = xdown

cambrure = np.zeros(nombre_de_points)
yup = cambrure
ydown = cambrure

for i in range(nombre_de_points):

    if xdown[i-1] <= p:
        cambrure[i - 1] = (m / p ** 2) * (2 * p * xdown[i - 1] - xdown[i - 1] ** 2)
    else:
        cambrure[i - 1] = (m / (1 - p) ** 2) * ((1 - 2 * p) + 2 * p * xdown[i - 1] - xdown[i - 1] ** 2)

for i in range(nombre_de_points):

    yup[i - 1] = 5 * t * (0.2969 * xup[i - 1] ** 0.5 - 0.1260 * xup[i - 1] - 0.3516 * xup[i - 1] ** 2 +
                0.2843 * xup[i - 1] ** 3 - 0.1036 * xup[i - 1] ** 4) + cambrure[i - 1]

    ydown[i - 1] = - 5 * t * (0.2969 * xdown[i - 1] ** 0.5 - 0.1260 * xdown[i - 1] - 0.3516 * xdown[i - 1] ** 2 +
                    0.2843 * xdown[i - 1] ** 3 - 0.1036 * xdown[i - 1] ** 4) + cambrure[i - 1]

# quelques paramètres pour le graphique
plt.rcParams['font.size'] = 14
plt.rcParams['figure.dpi'] = 100

# Bloc de code pour le tracé
plt.plot(xup,yup,label='Extrados', color=(0, 0, 1))
plt.plot(xup,ydown,label='Intrados', color=(1, 0, 0))
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.title('Profil NACA' + str(int(m*100)) + str(int(p*10)) + str(int(t*100)))
plt.xlim(-corde*0.1, corde*1.1)
plt.ylim(-corde*0.5, corde*0.5)
plt.show()
# Jeu de Stratégie 2D

## **Description**
Un jeu de stratégie au tour par tour où deux joueurs s’affrontent en sélectionnant leurs héros et en utilisant leurs compétences stratégiquement pour vaincre l'adversaire. Le jeu propose une carte avec obstacles et des héros aux compétences variées, équilibrant attaque et défense.

---

## **Comment jouer ?**

### **Début du jeu**
1. **Choix des noms des joueurs** :  
   - Chaque joueur commence par **saisir son nom** en appuyant sur **Entrée** après l’avoir écrit.  

2. **Sélection des héros** :  
   - Chaque joueur sélectionne **3 héros** parmi les 6 disponibles :  
     - **Erza**
     - **Gray**
     - **Natsu**
     - **Kansuke**
     - **Gowther**
     - **Heisuke**

---

### **Compétences des héros**
Chaque héros dispose de compétences variées pour **équilibrer le gameplay** :
- **Santé** : Certains héros ont plus de points de vie, les rendant plus résistants.  
- **Réduction des dégâts** : Les héros peuvent réduire un **pourcentage des dégâts** reçus lorsqu’ils sont attaqués.  
- **Attaque** :  
  - Certains héros possèdent des attaques avec une **grande portée**, leur permettant d'attaquer à distance.  
  - D'autres privilégient des attaques ayant une **grande zone d’effet**, où les dégâts varient selon la position des cibles :  
    - **Cible principale (au centre)** : Subit **100% des dégâts**.  
    - **Cibles secondaires (autour)** : Subissent **50% des dégâts**.  

Les compétences sont conçues pour maintenir un équilibre entre les héros, évitant qu’un héros soit trop puissant ou trop faible.

---

### **Contrôles**
- **Attaques** :  
  - **C** : Effectuer la **première attaque** de l’unité.  
  - **V** : Effectuer la **deuxième attaque** de l’unité.  

- **Défense** :  
  - **A** : Activer la compétence de **défense**.  

---

### **Carte et Obstacles**
La carte contient **3 types d’obstacles** qui influencent les déplacements et la stratégie :  
1. **Lava** :  
   - Seul **Natsu** peut traverser la lave. Les autres héros meurent instantanément en essayant.  
2. **Ice** :  
   - Seul **Gray** peut traverser la glace.  
3. **Objets fixes** (maisons, arbres) :  
   - Ces obstacles sont infranchissables pour tous les héros.  

---

### **Déroulement du jeu**
1. Les joueurs attaquent à tour de rôle.  
2. Chaque joueur sélectionne une unité parmi les 3 héros choisis, puis choisit l’une des **deux attaques disponibles** :  
   - Une **zone d’effet** est générée autour de la cible.  
     - La **cible principale** subit **100% des dégâts**.  
     - Les **autres cibles** dans la zone d’effet subissent **50% des dégâts**.  

3. **Défense automatique** : Lorsqu’une unité est attaquée, sa compétence de défense s’active automatiquement, réduisant les dégâts subis.  

4. Après chaque action, le **tour passe à l’unité suivante**, alternant les joueurs.

---

### **Conditions de victoire**
- Un joueur gagne lorsque **tous les héros adverses** sont vaincus.  
- Le dernier joueur ayant encore des héros en vie remporte la partie.  

---

## Lancement du jeu

Pour lancer le jeu, assurez-vous d'abord d'installer toutes les dépendances, pour cela, tapez la commande suivante dans le répertoire `Game_Python` contenant le fichier `requirements.txt`:
`pip install -r requirements.txt`

Maintenant que les dépendances sont satisfaites, positionnez-vous dans le fichier `Game_Python>tests>main.py` et lancez-le.

:warning: Si vous êtes sur VScode, il est très probable que vous ayez un problème lié aux chemis d'accès aux ressources, dans ce cas, pensez à modifier le champ `path` de la classe `Settings` situöe dans le dossier `src`, à substituer par l'une de ces valeurs `self.path = ''` ou `self.path = '../'`.

Si jamais le problème persiste ou que vous n'arrivez pas à lancer le jeu pour x raison, n'hésitez pas à nous contacter via :
:e-mail: alicia.berrouane@etu.sorbonne-universite.fr
:e-mail: zakaria.allouche@etu.sorbonne-universite.fr
:e-mail: amine.nait_si_ahmed@etu.sorbonne-universite.fr

---

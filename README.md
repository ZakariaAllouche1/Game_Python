# Game_Python

# Explication du jeu

Le jeu se joue entre deux joueurs, chacun devant choisir **3 héros** parmi les 6 disponibles : **Erza**, **Gray**, **Natsu**, **Kansuke**, **Gowther**, et **Heisuke**.  

## Compétences des héros :  
Chaque héros possède **différentes compétences**, qui influencent :  
- **Santé** : Certains héros ont plus de points de vie, les rendant plus résistants.  
- **Réduction des dégâts** : Chaque héros peut réduire un pourcentage des dégâts reçus lors des attaques ennemies, grâce à leurs capacités défensives.  
- **Style d’attaque** :  
  - Certains héros possèdent des attaques avec une **grande portée**, leur permettant d'attaquer à distance.  
  - D'autres privilégient des attaques ayant une **grande zone d’effet**, où les dégâts varient selon la position des cibles :  
    - **Cible principale (au centre)** : Subit **100% des dégâts**.  
    - **Cibles secondaires (autour)** : Subissent **50% des dégâts**.  

Les compétences sont réparties de manière à **équilibrer le jeu** entre les héros. Ainsi, aucun héros n’est trop puissant ou trop faible, encourageant une stratégie variée et équilibrée entre les joueurs.  

## La carte et les obstacles :  
La carte contient **3 types d’obstacles** qui influencent la stratégie des joueurs :  
- **Lava** : Seul **Natsu** peut traverser la lave sans danger. Tous les autres héros meurent en tentant de le faire.  
- **Ice** : Seul **Gray** peut traverser la glace.  
- **Objets fixes (maisons, arbres)** : Ces obstacles sont infranchissables pour tous les héros.  

## Déroulement du jeu :  
Une fois les héros choisis, le jeu commence. Les joueurs attaquent à tour de rôle, en sélectionnant une unité et en choisissant une de ses **deux attaques disponibles**.  

### Mécanique des attaques :  
- Lorsqu’un joueur attaque un adversaire, une **zone d’effet** est générée autour de la cible.  
  - **La cible principale**, située au centre, subit **100% des dégâts**.  
  - **Les autres adversaires** présents dans la zone d’effet reçoivent **50% des dégâts**.  
- Chaque attaque déclenche automatiquement la **défense** des cibles affectées, réduisant les dégâts reçus selon leur pourcentage de réduction.  

Après chaque attaque, le tour passe à l’unité suivante, permettant aux joueurs d'alterner leurs actions.  

## Conditions de victoire :  
Le jeu continue jusqu'à ce qu’un des deux joueurs perde **tous ses héros**. Le joueur ayant encore au moins un héros en vie remporte la partie.  

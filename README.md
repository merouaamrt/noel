# 🎄 Projet TD7 – Traitement d’Images (OpenCV)

## 📌 Description

L’objectif est de mettre en pratique les traitements d’images et de vidéos en utilisant le flux vidéo d’une webcam.

Le thème choisi pour ce projet est **Noël**.

---

## 🎯 Objectifs du projet
- Récupérer le flux vidéo de la webcam
- Détecter le visage de l’utilisateur
- Appliquer des filtres sur la vidéo
- Incruster des images sur le visage 
- Ajouter un objet interactif en arrière-plan
- Détecter le sourire de l’utilisateur
- Proposer un menu interactif pour activer/désactiver les effets

---

## 🧩 Fonctionnalités implémentées

### 1️⃣ Détection du visage
- Utilisation de la cascade de Haar :
  - `haarcascade_frontalface_default.xml`
- Le visage est détecté en temps réel via la webcam.

### 2️⃣ Manipulation de l’image vidéo
#### Filtre
- Application d’un **filtre sépia** sur toute l’image.
- Les images utilisées ont un **fond noir** pour faciliter l’incrustation.

### 3️⃣ Image interactive en arrière-plan
#### a. Objet en mouvement
- Des flocons de neige tombent du haut vers le bas de la vidéo.

#### b. Interaction avec le visage
- La couleur du flocon change lorsqu’il entre en collision avec la tête de l’utilisateur.

#### c. Détection du sourire
- Utilisation de `haarcascade_smile.xml`
- Un **rectangle bleu ciel** apparaît uniquement lorsque l’utilisateur sourit.

### 4️⃣ Menu interactif
Un menu clavier permet d’activer ou désactiver les éléments suivants :
- Filtre
- Chapeau
- Lunettes
- Moustache
- Neige

Touches utilisées :
- `f` : filtre
- `h` : chapeau
- `g` : lunettes
- `m` : moustache
- `n` : neige
- `q` : quitter

---

## 🛠️ Technologies utilisées
- Python 3
- OpenCV
- NumPy

---

## 📁 Contenu du dépôt
- `td7_projet.py` : code principal du projet
- Images (.jpeg / .png) : chapeau, lunettes, moustache, neige
- Cascades Haar :
  - `haarcascade_frontalface_default.xml`
  - `haarcascade_smile.xml`


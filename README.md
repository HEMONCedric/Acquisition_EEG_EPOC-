# Acquisition de données brutes sur casque EPOC+.

  Création d'un code permettant l'acquisition des sigaux brutes EEG sur un casque EPOC+ depuis Matlab sans licence EPOC+.
 Pour cette méthode rien de plus simple, il suffit de télécharger le dossier contenant les codes Python et Matlab et les bibliothèques :
Les fichiers nous intéressant dans ce dossier sont probar.m et addpath-recurse.m: 

   -Le fichier addpath-recurse.m permet de changer le chemin d’accès du compilateur python depuis matlab. Le seul changement nécessaire s’effectuera ici, il suffit de modifier la variable root-path en mettant le chemin d’accès du dossier téléchargée.
  
  -Le fichier probar.m va appeler les fonctions CyKITv2.py et eeg.py permettant la connexion au casque et l’extraction des données à l’aide de get-data, ensuite la boucle while permet d’écrire le nombre d’échantillons que l’on souhaite et de les enregistrer dans une matrice b. Les lignes correpondant à nos électrodes se trouvent des colonnes 3 à 16 de la matrice b.

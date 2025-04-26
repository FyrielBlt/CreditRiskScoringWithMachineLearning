# creditscoring
📚 Introduction
Notre projet, mené au sein d'une entreprise de technologies financières, vise à améliorer la prise de décision d'octroi de crédit en utilisant des techniques de machine learning.
En exploitant les données de la Banque Centrale de Madagascar et en suivant la méthodologie CRISP-DM, nous avons développé des modèles capables de classifier les demandes de crédit en trois catégories : saines, en souffrance et douteuses, tout en fournissant un score de probabilité pour chaque classe.

Nous avons effectué un traitement approfondi des données pour construire ces modèles. Finalement, nous avons constaté que le modèle XGBoost donnait les meilleurs résultats. Nous l'avons donc intégré dans notre application Flask pour une mise en œuvre pratique.

Mots-clés : Risque de crédit, Credit scoring, Apprentissage automatique, Modélisation prédictive, Classification, Méthodologie CRISP-DM.
📊 Analyse, traitement des données et développement des modèles
Vous trouverez l'intégralité de l'analyse, du traitement des données ainsi que du développement des modèles dans le fichier :
👉 Untitled63 (1) (1).ipynb

🚀 Déploiement du modèle avec Flask
Nous avons également développé une application Flask pour déployer notre modèle, que vous pouvez retrouver dans le dossier :
👉 Predict/

Quelques précisions :
Environnement de développement utilisé : Visual Studio Code, qui a facilité la création et la gestion de notre application de manière efficace et structurée.

Fonctionnement de l'application :

Les utilisateurs peuvent charger un fichier CSV contenant les données d'entrée.

L'application utilise le modèle pré-entraîné pour prédire les risques associés à chaque dossier de crédit.

Grâce à des routes Flask configurées, l'application peut traiter plusieurs dossiers simultanément, offrant ainsi une classification précise basée sur les prédictions du modèle et des règles établies.

Lorsqu'un utilisateur accède à l'application :

Il est d'abord dirigé vers une page d'accueil.

Il peut ensuite naviguer vers l'interface "À Propos" pour comprendre les fonctionnalités et l'objectif du projet.

![Aperçu de l'application](https://github.com/FyrielBlt/creditscoring/blob/main/c1.PNG)

![Aperçu de l'application](https://github.com/FyrielBlt/creditscoring/blob/main/c2.PNG)
Une fois prêt, l'utilisateur peut télécharger un fichier de données au format CSV qu'il soumet à
l'application pour évaluer les scores de crédit. 
En option, il peut également utiliser un fichier existant comme test pour évaluer la performance
du modèle.
![Aperçu de l'application](https://github.com/FyrielBlt/creditscoring/blob/main/c3.PNG)
Une fois le calcul effectué, l'utilisateur reçoit les scores de probabilité indiquant l'appartenance de
l'emprunteur à chaque classe. Les résultats peuvent être filtrés selon les critères désirés : affichage
uniquement des dossiers acceptés, refusés, ou les deux simultanément. Les dossiers acceptés sont
marqués en vert tandis que les dossiers refusés sont indiqués en rouge pour une visualisation claire
et rapide. De plus, l'application permet une recherche efficace par référence de dossier, offrant
ainsi une expérience utilisateur fluide et personnalisée.
![Aperçu de l'application](https://github.com/FyrielBlt/creditscoring/blob/main/c4.PNG)
L’utilisateur a également la possibilité de contacter le groupe BFI pour plus d'informations ou
d'assistance.
![Aperçu de l'application](https://github.com/FyrielBlt/creditscoring/blob/main/c5.PNG)
📚 Conclusion 
Après une immersion approfondie dans le domaine métier et les concepts clés, nous avons procédé
au traitement des données en sélectionnant avec rigueur les variables les plus pertinentes à l'aide
de tests statistiques tels que le test du chi2 et le test de Kruskal-Wallis. L'utilisation de techniques
comme l'arbre de décision nous a permis d'identifier les variables les plus influentes pour prédire
le risque de crédit, tout en incluant l'encodage, l'équilibrage et la standardisation des données.
Dans cette démarche, nous avons exploré et comparé cinq modèles de machine learning essentiels
la régression logistique, le SVM, le Random Forest, les réseaux de neurones artificiels et Xgboost.
Après une évaluation approfondie, le modèle Xgboost s'est distingué par son efficacité dans la
prédiction des scores de crédit dans notre application déployée.
L'application développée utilise Flask pour le déploiement du modèle, offrant ainsi une interface
conviviale aux utilisateurs pour interagir avec le système de prédiction de crédit via un simple
navigateur web.
Pour l'avenir, notre projet se concentrera sur l'optimisation continue de ces modèles, l'intégration
de nouvelles sources de données pertinentes. Cette stratégie vise à renforcer la gestion des risques,
offrant des avantages tangibles tant pour les institutions financières que pour les emprunteurs,
garantissant ainsi des décisions plus précises et efficaces.

# Analyse-des-ventes-MaroMarche

📱 Application Streamlit – Tableau de bord MaroMarché  
Cette application web interactive développée avec **Streamlit** permet d’analyser les données de vente de MaroMarché à travers plusieurs dimensions : **produits**, **clients** et **périodes de vente**.

Elle propose à la fois une **analyse descriptive** et **prédictive**, avec des modèles de Machine Learning intégrés.

---

🛠️ Technologies utilisées

- **Streamlit** – Interface web  
- **Python** – Langage principal  
- **Pandas / Numpy** – Manipulation de données  
- **Plotly / Matplotlib / Seaborn** – Visualisations  
- **Facebook Prophet** – Prévision des ventes et des clients  
- **Random Forest Regressor** – Prédiction de la demande produit  
- **CSS** – Personnalisation de l’interface  
- **Streamlit Authentication** – Sécurisation par mot de passe

---

🔐 Accès sécurisé  
L’utilisateur doit se connecter pour accéder à l’application.  
L’authentification est gérée via le fichier `auth.py`.

---

📁 Structure du projet

🔹 **Fichiers principaux**  
- `main.py` : Point d’entrée de l’application (tableau de bord global)

🔹 **Dossier `pages/`**  
- `1_analyse_vente.py`  
  - Analyse descriptive des ventes (CA, top produits, tendances)  
  - Analyse prédictive avec **Facebook Prophet**  
  - ✅ **Téléchargement possible des résultats filtrés**

- `2_analyse_produit.py`  
  - Analyse des performances produit  
  - Prédiction avec **Random Forest Regression**  
  - ✅ **Téléchargement possible des résultats filtrés**

- `3_analyse_client.py`  
  - Analyse des profils clients (âge, genre…)  
  - Prévision de fréquentation avec **Facebook Prophet**  
  - ✅ **Téléchargement possible des résultats filtrés**

🔹 **Dossier `outils/`**  
- `auth.py` : Authentification utilisateur  
- `data_loader.py` : Chargement des données  
- `ui_style.py` : Personnalisation CSS

🔹 **Dossier `data/`**  
- `dataset_final.csv` : Données utilisées dans l’application

---

✅ Fonctionnalités clés

- 🔑 Authentification sécurisée  
- 📊 Tableaux de bord dynamiques & multi-pages  
- 📈 Analyses descriptives et prédictives  
- 🧠 Intégration de modèles Machine Learning  
- 🎨 Interface customisée (CSS)  
- 📥 **Téléchargement des données filtrées disponible**

---

🚀 Lancer l'application

```bash
streamlit run main.py

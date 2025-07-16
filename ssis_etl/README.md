# 📦 SSIS - Processus ETL (Extract, Transform, Load)

Ce dossier contient les captures des flux de données développés avec SQL Server Integration Services (SSIS) pour alimenter le Data Warehouse du projet MaroMarché.

Chaque flux de données a été conçu pour enrichir les données en amont avant leur insertion dans les tables de la base de données **Dest_MaroMarche**.

---

## 📊 Flux de données et enrichissements

### 🧾 `flux_vente.png`  
**Chargement vers la table `FaitVente`**

✔️ Colonnes ajoutées :
- `prix_unitaire_formate` → Ajout du symbole *MAD* (ex : `35 MAD`)
- `montant_total` → Calcul : `quantité * prix unitaire`
- `montant_total_formate` → Ajout du symbole *MAD*
- `categorie_prix` → Catégorisation du prix (`Bas`, `Moyen`, `Élevé`)

---

### 🛍️ `flux_produit.png`  
**Chargement vers la table `DimProduit`**

✔️ Colonnes ajoutées :
- `origine_simplifiee` → Valeur normalisée : *Local* ou *Importé*
- `prix_categorie` → Classification du prix (`Bas`, `Moyen`, `Élevé`)
- `prix_unitaire_text` → Formatage du prix avec *MAD*

---

### 👥 `flux_client.png`  
**Chargement vers la table `DimClient`**

✔️ Colonnes ajoutées :
- `NomComplet` → Fusion du prénom et du nom
- `TrancheAge` → Classification (`Jeune`, `Adulte`, `Senior`)
- `GenreText` → Texte lisible (`Homme` pour `H`, `Femme` pour `F`)

---

### 📅 `flux_date.png`  
**Chargement vers la table `DimDate`**

✔️ Colonnes ajoutées :
- `mois_fr` → Nom du mois en français (ex : *Janvier*)
- `jour_fr` → Nom du jour en français (ex : *Lundi*)
- `est_weekend` → Booléen indiquant si la date tombe un week-end (`Oui` / `Non`)

---

## 🛠️ Outils utilisés

- SQL Server Integration Services (SSIS)
- Expressions et colonnes dérivées
- Flux de données et transformations conditionnelles

---

> Ces enrichissements ont permis d’augmenter la lisibilité des données, de faciliter l’analyse dans Power BI, et de créer des indicateurs plus pertinents pour les décisions commerciales.

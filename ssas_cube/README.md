# 🧊 SSAS - Cube d'analyse multidimensionnelle

Ce dossier contient des captures d'écran du cube SSAS (SQL Server Analysis Services) utilisé dans le projet **MaroMarché**.

---

## 📐 Structure du cube

Le cube est construit à partir de la base de données **Dest_MaroMarche**, avec :

- **Dimensions** :
  - DimClient
  - DimProduit
  - DimDate
- **Table de faits** :
  - FaitVente



## 📏 Mesures créées dans le cube (SSAS)

Les mesures suivantes ont été créées directement dans SSAS pour faciliter l'analyse :

- `Quantité Totale`
- `Prix Unitaire Moyen`
- `Montant Total`
- `Nombre de Ventes`

---

## 🧮 Mesures supplémentaires (Power BI)

D'autres indicateurs calculés ont été ajoutés dans Power BI, après connexion en mode **importation**, pour enrichir l'analyse :

- `Montant Total Formaté`
- `Prix Unitaire Formaté`
- `Nombre de Clients`
- `Nombre de Produits`
- Indicateurs personnalisés (par exemple, segmentation ou tendances)

---

## 📸 Captures disponibles

- structure_cube.png → Structure globale du cube
- mesures_cube.png → Liste des mesures dans SSAS
- exploration_cube.png → Exemple d’analyse avec les mesures

---

> ✅ Ces mesures permettent des tableaux de bord interactifs, rapides et dynamiques dans Power BI, tout en s’appuyant sur des calculs précalculés dans SSAS.

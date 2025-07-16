import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.ui_style import set_background, custom_sidebar_style
from utils.auth import check_authentication
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sns




# Authentification
check_authentication()

# Style
set_background()
custom_sidebar_style()






st.title("🧑‍💼 Analyse du Comportement des Clients – MaroMarché")

# Chargement des données
df = load_data()
df["date_complete"] = pd.to_datetime(df["date_complete"])

# Vérification colonne client
if "client_id" not in df.columns or "montant_total" not in df.columns:
    st.error("⚠️ Le jeu de données doit contenir les colonnes 'client_id', 'prenom', 'nom' et 'montant_total'.")
    st.stop()

#filtre  dynamique

st.sidebar.header("🎯 Filtres clients")

annees = sorted(df["date_complete"].dt.year.unique())
villes = sorted(df["ville"].dropna().unique()) if "ville" in df.columns else []

selected_annee = st.sidebar.selectbox("📅 Année :", ["Toutes"] + annees)
selected_ville = st.sidebar.selectbox("🏙️ Ville :", ["Toutes"] + villes) if villes else None

# Application des filtres
df_filtered = df.copy()

if selected_annee != "Toutes":
    df_filtered = df_filtered[df_filtered["date_complete"].dt.year == selected_annee]

if selected_ville and selected_ville != "Toutes":
    df_filtered = df_filtered[df_filtered["ville"] == selected_ville]



# 🔍 Analyse RFM

st.subheader("📊 Analyse RFM des clients")

# Agrégation RFM
df_clients = df_filtered.groupby(["client_id", "prenom", "nom"]).agg(
    derniere_achat=('date_complete', 'max'),
    frequence=('date_complete', 'count'),
    montant=('montant_total', 'sum')
).reset_index()

# Calcul de la récence
df_clients["recence"] = (pd.to_datetime("today") - df_clients["derniere_achat"]).dt.days

# Concaténation du nom complet
df_clients["nom_complet"] = df_clients["prenom"] + " " + df_clients["nom"]

# Affichage du tableau RFM
st.dataframe(df_clients[["nom_complet", "frequence", "montant", "recence"]].sort_values(by="montant", ascending=False))


# ===== Télécharger les données filtrées (RFM) =====
st.markdown("### 📥 Export des données clients filtrés (RFM)")

if not df_clients.empty:
    with st.expander("🔍 Aperçu des données RFM"):
        st.dataframe(df_clients, use_container_width=True)

    if st.button("✅ Préparer le fichier CSV des clients"):
        st.success("✅ Le fichier est prêt à être téléchargé ci-dessous ⬇️")

        csv_clients = df_clients.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Télécharger les données RFM (CSV)",
            data=csv_clients,
            file_name="clients_rfm.csv",
            mime="text/csv"
        )
else:
    st.info("ℹ️ Aucune donnée client à exporter pour les filtres actuels.")




# 🏅 Top clients par montant

st.subheader("🏅 Top 10 clients par montant total")

top_clients = df_clients.sort_values(by="montant", ascending=False).head(10)

st.bar_chart(top_clients.set_index("nom_complet")["montant"])


# ========== 📈 Évolution des clients actifs ==========
st.subheader("📊 Évolution du nombre de clients actifs par mois")

# Extraire mois/année
df_filtered["mois_annee"] = df_filtered["date_complete"].dt.to_period("M").astype(str)

# Supprimer les doublons client par mois
clients_par_mois = df_filtered.groupby("mois_annee")["client_id"].nunique().reset_index()
clients_par_mois.columns = ["mois", "nb_clients"]

st.line_chart(data=clients_par_mois.set_index("mois"))





# prediction

from prophet import Prophet
import matplotlib.pyplot as plt

st.subheader("🔮 Prévision du nombre de clients – MaroMarché")

# Préparation des données pour Prophet
df["mois"] = df["date_complete"].dt.to_period("M")
clients_mensuels = df.groupby("mois")["client_id"].nunique().reset_index()
clients_mensuels["mois"] = clients_mensuels["mois"].dt.to_timestamp()
df_prophet = clients_mensuels.rename(columns={"mois": "ds", "client_id": "y"})

# Sélection utilisateur : durée
n_mois = st.selectbox("📆 Durée de la prévision :", options=["Tous"] + list(range(1, 13)), index=0)

if n_mois == "Tous":
    st.info("📌 Veuillez sélectionner une durée (en mois) pour lancer la prévision.")
else:
    n_mois = int(n_mois)

    # Création et entraînement du modèle Prophet
    model = Prophet()
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=n_mois, freq="M")
    forecast = model.predict(future)

    # Récupération des données prédites
    future_pred = forecast.tail(n_mois)
    total_clients_pred = int(future_pred["yhat"].sum())

    # ✅ Résultat chiffré avant le graphe
    st.success(f"👥 Nombre total de clients prédits sur {n_mois} mois : **{total_clients_pred} clients**")

    # 🔽 Graphique de prévision
    st.subheader("📈 Prévision mensuelle du nombre de clients")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(forecast["ds"], forecast["yhat"], label="Prévision", color="green")
    ax.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], color="lightgreen", alpha=0.4, label="Intervalle de confiance")
    ax.set_xlabel("Date")
    ax.set_ylabel("Nombre de clients")
    ax.set_title("Prévision des clients actifs")
    ax.legend()
    st.pyplot(fig)

    # 📥 Bouton de téléchargement
    st.markdown("### 📤 Exporter les données de prévision")
    if st.button("✅ Préparer le fichier CSV des prévisions"):
        st.success("✅ Le fichier est prêt à être téléchargé ⬇️")

        csv_data = future_pred[["ds", "yhat", "yhat_lower", "yhat_upper"]].rename(columns={
            "ds": "Date",
            "yhat": "Prédiction",
            "yhat_lower": "Intervalle_inférieur",
            "yhat_upper": "Intervalle_supérieur"
        }).to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Télécharger les prévisions (CSV)",
            data=csv_data,
            file_name="previsions_clients.csv",
            mime="text/csv"
        )



# segmentation clinte RFM + Kmean


st.header("🧠 Segmentation des Clients par RFM + KMeans")
st.title("🧩 Segmentation des Clients – MaroMarché")

# Chargement des données
df = load_data()
df["date_complete"] = pd.to_datetime(df["date_complete"])

# Vérification des colonnes
required_cols = ["client_id", "montant_total", "date_complete"]
if not all(col in df.columns for col in required_cols):
    st.error("Le jeu de données doit contenir les colonnes : client_id, montant_total, date_complete.")
    st.stop()

# ==== Calcul RFM ====
df_rfm = df.groupby("client_id").agg({
    "date_complete": "max",
    "montant_total": "sum",
    "client_id": "count"
}).rename(columns={
    "date_complete": "dernier_achat",
    "montant_total": "montant",
    "client_id": "frequence"
})

df_rfm["recence"] = (pd.to_datetime("today") - df_rfm["dernier_achat"]).dt.days

# Clustering
rfm_features = df_rfm[["recence", "frequence", "montant"]]
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_features)

k = st.slider("🎯 Nombre de segments (k)", min_value=2, max_value=6, value=3)
kmeans = KMeans(n_clusters=k, random_state=42)
df_rfm["segment"] = kmeans.fit_predict(rfm_scaled)

# Donner un nom aux segments
segment_labels = {}
profil_segments = df_rfm.groupby("segment")[["recence", "frequence", "montant"]].mean().round(1)

for i, row in profil_segments.iterrows():
    if row["recence"] > 1000:
        label = "Clients Perdus"
    elif row["recence"] > 600 and row["montant"] < 12000:
        label = "Clients Inactifs"
    elif row["recence"] > 600 and row["montant"] >= 12000:
        label = "Clients Fidèles"
    else:
        label = "Clients à Potentiel"
    segment_labels[i] = f"Segment {i} – {label}"

df_rfm["segment_nom"] = df_rfm["segment"].map(segment_labels)

# 📊 Distribution
st.subheader("📊 Répartition des clients par segment")
segment_counts = df_rfm["segment_nom"].value_counts()
st.bar_chart(segment_counts)

# 📈 Moyennes
st.subheader("📈 Profil moyen des segments (moyennes RFM)")
profil_segments["Nom du segment"] = profil_segments.index.map(segment_labels)
st.dataframe(profil_segments.reset_index()[["segment", "Nom du segment", "recence", "frequence", "montant"]])

# 🧭 Scatter
st.subheader("🧭 Visualisation des segments (Récence vs Montant)")
fig, ax = plt.subplots(figsize=(8, 4))
sns.scatterplot(data=df_rfm, x="recence", y="montant", hue="segment_nom", palette="tab10", ax=ax)
plt.title("Visualisation des segments clients")
st.pyplot(fig)

# ==============================
# 🎛️ Filtres et Export
# ==============================

st.markdown("## 🎛️ Analyse détaillée par segment")
options = ["Tous"] + sorted(df_rfm["segment_nom"].unique())
selected_segment = st.selectbox("🧬 Sélectionner un segment :", options=options)

# Fusionner avec les prénoms/noms pour affichage
df_noms = df[["client_id", "prenom", "nom"]].drop_duplicates()
df_rfm = df_rfm.reset_index().merge(df_noms, on="client_id", how="left")
df_rfm["nom_complet"] = df_rfm["prenom"].fillna("") + " " + df_rfm["nom"].fillna("")

# Appliquer le filtre
if selected_segment == "Tous":
    df_segment_filtered = df_rfm
else:
    df_segment_filtered = df_rfm[df_rfm["segment_nom"] == selected_segment]

# Affichage
st.markdown(f"### 👥 Détails des clients ({selected_segment})")
colonnes_affichage = ["nom_complet", "client_id", "segment_nom", "recence", "frequence", "montant"]
st.dataframe(df_segment_filtered[colonnes_affichage], use_container_width=True)

# Export CSV
if not df_segment_filtered.empty:
    st.markdown("#### 📦 Exporter les données")
    if st.button("✅ Préparer le fichier CSV"):
        csv_data = df_segment_filtered[colonnes_affichage].to_csv(index=False).encode("utf-8")
        st.success("📁 Le fichier est prêt à être téléchargé ⬇️")
        st.download_button(
            label=f"📥 Télécharger les clients ({selected_segment})",
            data=csv_data,
            file_name=f"clients_segment_{selected_segment}.csv",
            mime="text/csv"
        )
else:
    st.info("Aucun client dans ce segment.")

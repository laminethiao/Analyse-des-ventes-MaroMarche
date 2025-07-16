import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analyse Produits – MaroMarché", layout="wide")


from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from utils.data_loader import load_data
from utils.ui_style import set_background, custom_sidebar_style
from utils.auth import check_authentication
# Authentification
check_authentication()



# Configuration de la page

st.title("📦 Analyse des Produits – MaroMarché")


set_background()
custom_sidebar_style()

# --- 1. Chargement des données ---
df = load_data()

# --- 2. Préparation colonnes temporelles ---
# --- Préparation des colonnes temporelles ---
df["date_complete"] = pd.to_datetime(df["date_complete"])
df["mois"] = df["date_complete"].dt.month
df["annee"] = df["date_complete"].dt.year

# --- Filtres dynamiques ---
st.sidebar.header("🎛️ Filtres Produits")

annees = sorted(df["annee"].dropna().unique())
mois = sorted(df["mois"].dropna().unique())
villes = sorted(df["ville"].dropna().unique())
categories = sorted(df["categorie"].dropna().unique())

selected_annee = st.sidebar.selectbox("📅 Année :", options=["Toutes"] + annees, key="annee_filter")
selected_mois = st.sidebar.selectbox("📆 Mois :", options=["Toutes"] + mois, key="mois_filter")
selected_ville = st.sidebar.selectbox("🏙️ Ville :", options=["Toutes"] + villes)
selected_categorie = st.sidebar.selectbox("🗂️ Catégorie :", options=["Toutes"] + categories)

# --- Application des filtres ---
df_filtered = df.copy()

if selected_annee != "Toutes":
    df_filtered = df_filtered[df_filtered["annee"] == selected_annee]

if selected_mois != "Toutes":
    df_filtered = df_filtered[df_filtered["mois"] == selected_mois]

if selected_ville != "Toutes":
    df_filtered = df_filtered[df_filtered["ville"] == selected_ville]

if selected_categorie != "Toutes":
    df_filtered = df_filtered[df_filtered["categorie"] == selected_categorie]

# --- Résultat : Top produits ---
if df_filtered.empty:
    st.warning("Aucune donnée disponible pour cette combinaison de filtres.")
else:
    titre = "🎯 Top produits vendus"
    if selected_annee != "Toutes":
        titre += f" – {selected_annee}"
    if selected_mois != "Toutes":
        titre += f"/{selected_mois}"

    st.subheader(titre)

    produit_stats = (
        df_filtered.groupby("nom_produit")["quantite"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    st.dataframe(produit_stats.head(10), use_container_width=True)

    st.bar_chart(
        produit_stats.set_index("nom_produit").head(10),
        use_container_width=True
    )
#telecharger le filtre
# ========== Export des données filtrées ==========

st.markdown("### 📥 Export des données filtrées")

filtres_appliques = (
    selected_annee != "Toutes"
    or selected_mois != "Toutes"
    or selected_ville != "Toutes"
    or selected_categorie != "Toutes"
)

if filtres_appliques and not df_filtered.empty:
    with st.expander("🔍 Afficher les données filtrées avant téléchargement"):
        st.dataframe(df_filtered, use_container_width=True)

    if st.button("✅ Préparer le fichier CSV des produits"):
        st.success("✅ Le fichier est prêt à être téléchargé ci-dessous ⬇️")

        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger les données produits filtrées (CSV)",
            data=csv_data,
            file_name="produits_filtrés.csv",
            mime="text/csv"
        )
else:
    st.info("🔎 Veuillez appliquer au moins un filtre pour activer l'affichage et le téléchargement des données.")



st.title("📦 Analyse Prédictive des Produits – MaroMarché")

# --- Charger les données ---
df = load_data()

# --- Sélection utilisateur ---
st.markdown("### 🔍 Estimation de la quantité vendue")

# Champs avec options dynamiques (valeurs uniques du dataset)
# --- Sélections utilisateur ---
ville_input = st.selectbox("🏙️ Ville :", ["Sélectionnez..."] + sorted(df["ville"].dropna().unique()))
categorie_input = st.selectbox("📂 Catégorie :", ["Sélectionnez..."] + sorted(df["categorie"].dropna().unique()))
produit_input = st.selectbox("🛒 Produit :", ["Sélectionnez..."] + sorted(df["nom_produit"].dropna().unique()))
annee_input = st.selectbox("📅 Année :", ["Sélectionnez..."] + sorted(df["annee"].dropna().unique()))
mois_input = st.selectbox("🗓️ Mois :", ["Sélectionnez..."] + sorted(df["mois"].dropna().unique()))

# --- Appliquer les filtres ---
df_filtered = df.copy()
filtres_appliqués = 0  # Compteur

if ville_input != "Sélectionnez...":
    df_filtered = df_filtered[df_filtered["ville"] == ville_input]
    filtres_appliqués += 1
if categorie_input != "Sélectionnez...":
    df_filtered = df_filtered[df_filtered["categorie"] == categorie_input]
    filtres_appliqués += 1
if produit_input != "Sélectionnez...":
    df_filtered = df_filtered[df_filtered["nom_produit"] == produit_input]
    filtres_appliqués += 1
if annee_input != "Sélectionnez...":
    df_filtered = df_filtered[df_filtered["annee"] == annee_input]
    filtres_appliqués += 1
if mois_input != "Sélectionnez...":
    df_filtered = df_filtered[df_filtered["mois"] == mois_input]
    filtres_appliqués += 1


# --- Résultat final + courbe d’évolution ---

if filtres_appliqués >= 2 and not df_filtered.empty:
    st.subheader("📈 Évolution mensuelle des ventes (historique)")

    # Préparer l'évolution mensuelle
    df_filtered["date_complete"] = pd.to_datetime(df_filtered["date_complete"])
    evolution_mensuelle = df_filtered.groupby(df_filtered["date_complete"].dt.to_period("M"))["quantite"].sum().reset_index()
    evolution_mensuelle["date_complete"] = evolution_mensuelle["date_complete"].dt.to_timestamp()

    # Afficher la courbe
    st.line_chart(evolution_mensuelle.set_index("date_complete"))

    # Résumés
    quantite_totale = int(df_filtered["quantite"].sum())
    montant_total = int(df_filtered["montant_total"].sum())
    st.success(f"📦 Quantité totale vendue : **{quantite_totale} unités**")
    st.success(f"💰 Montant total estimé : **{montant_total:,.0f} MAD**")
else:
    st.info("ℹ️ Veuillez sélectionner **au moins 2 critères** pour afficher les résultats.")

#ajouter

# Champ utilisateur : nombre de mois à prédire
n_mois_input = st.selectbox("📅 Durée de la prévision (en mois) :", options=["Sélectionnez..."] + list(range(1, 13)))

if n_mois_input != "Sélectionnez...":
    n_mois = int(n_mois_input)

    # Préparation des données
    df_filtered["date_complete"] = pd.to_datetime(df_filtered["date_complete"])
    df_monthly = df_filtered.groupby(df_filtered["date_complete"].dt.to_period("M"))["quantite"].sum().reset_index()
    df_monthly["date_complete"] = df_monthly["date_complete"].dt.to_timestamp()
    df_prophet = df_monthly.rename(columns={"date_complete": "ds", "quantite": "y"})

    # Modélisation avec Prophet
    model = Prophet()
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=n_mois, freq='M')
    forecast = model.predict(future)

    # Affichage
    st.subheader(f"🔮 Prévision des quantités vendues sur {n_mois} mois")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(forecast["ds"], forecast["yhat"], label="Prévision", color="green")
    ax.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], color="lightgreen", alpha=0.5, label="Intervalle de confiance")

    ax.set_xlabel("Date")
    ax.set_ylabel("Quantité")
    ax.set_title("Prévision de la quantité vendue")
    ax.legend(loc="lower right")
    plt.tight_layout()

    st.pyplot(fig)
else:
    st.info("ℹ️ Veuillez sélectionner une **durée en mois** pour lancer la prévision.")

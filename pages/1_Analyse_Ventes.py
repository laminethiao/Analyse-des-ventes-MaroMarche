import streamlit as st
import pandas as pd
from prophet import Prophet
from utils.data_loader import load_data
from utils.ui_style import set_background, custom_sidebar_style
from utils.auth import check_authentication
# Authentification
check_authentication()


# --- Charger les données ---
df = load_data()

# --- Préparation ---
df["date_complete"] = pd.to_datetime(df["date_complete"])
df_monthly = df.groupby(df["date_complete"].dt.to_period("M"))["montant_total"].sum().reset_index()
df_monthly["date_complete"] = df_monthly["date_complete"].dt.to_timestamp()
df_prophet = df_monthly.rename(columns={"date_complete": "ds", "montant_total": "y"})

# filtre celon la ville ou anne
st.sidebar.header("🎛️ Filtres Analyse Historique")
annees = sorted(df["annee"].dropna().unique())
villes = sorted(df["ville"].dropna().unique())

selected_year = st.sidebar.selectbox("📅 Année :", ["Toutes"] + annees)
selected_ville = st.sidebar.selectbox("🏙️ Ville :", ["Toutes"] + villes)

# Appliquer les filtres
df_filtered = df.copy()
if selected_year != "Toutes":
    df_filtered = df_filtered[df_filtered["annee"] == selected_year]
if selected_ville != "Toutes":
    df_filtered = df_filtered[df_filtered["ville"] == selected_ville]

# affiche le histogramme

st.header("📊 Analyse Historique des Ventes")

set_background()
custom_sidebar_style()

# Courbe des ventes par mois
df_historique = df_filtered.groupby(df_filtered["date_complete"].dt.to_period("M"))["montant_total"].sum().reset_index()
df_historique["date_complete"] = df_historique["date_complete"].dt.to_timestamp()

st.subheader("🗓️ Ventes par mois")
st.line_chart(df_historique.set_index("date_complete"))

# categorie les plus vendue
st.subheader("🏙️ Top villes par montant total (historique)")
top_villes = df_filtered.groupby("ville")["montant_total"].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_villes)

# telecharger le filtre applique
# ========== Téléchargement des données filtrées ==========

filtres_appliques = (selected_year != "Toutes" or selected_ville != "Toutes") and not df_filtered.empty

if filtres_appliques:
    with st.expander("🔍 Afficher les données filtrées avant téléchargement"):
        st.dataframe(df_filtered, use_container_width=True)

    if st.button("✅ Préparer le fichier CSV"):
        st.success("✅ Le fichier est prêt à être téléchargé ci-dessous ⬇️")

        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger les données filtrées (CSV)",
            data=csv,
            file_name="ventes_filtrees.csv",
            mime="text/csv"
        )
else:
    st.info("ℹ️ Appliquez un filtre (année ou ville) pour activer l'affichage et le téléchargement des données.")



st.title("📈 Analyse Prédictive des Ventes – MaroMarché")


# --- Choix utilisateur ---
st.sidebar.header("Paramètres de Prévision")

choix_mois = st.sidebar.selectbox("🔧 Mois à prédire :", options=["Sélectionnez...", 3, 6, 9, 12], index=0)
choix_annee = st.sidebar.selectbox("📅 Années à prédire :", options=["Sélectionnez...", 1, 2, 3], index=0)

# --- Logique de sélection ---
n_months = None
titre = ""

if choix_annee != "Sélectionnez...":
    n_months = int(choix_annee) * 12
    titre = f"{choix_annee} an(s)"
elif choix_mois != "Sélectionnez...":
    n_months = int(choix_mois)
    titre = f"{n_months} mois"
else:
    st.warning("❗ Veuillez sélectionner une période (mois ou années) pour lancer la prévision.")
    st.stop()

# --- Modélisation ---
model = Prophet()
model.fit(df_prophet)

future = model.make_future_dataframe(periods=n_months, freq='M')
forecast = model.predict(future)

# --- Affichage graphique principal ---
st.subheader(f"🔮 Prévision des ventes pour les {titre}")
forecast_vis = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].set_index("ds")
forecast_vis = forecast_vis.rename(columns={
    "yhat": "Prévision",
    "yhat_lower": "Prévision Basse",
    "yhat_upper": "Prévision Haute"
})

st.line_chart(forecast_vis)


# --- Montant total prédit ---
future_pred = forecast.tail(n_months)
total_predicted = future_pred["yhat"].sum()
st.success(f"📢 Montant total prédit sur {titre} : {total_predicted:,.0f} MAD")

# --- Graphique en barres ---
bar_data = future_pred[["ds", "yhat"]].copy()
bar_data["Mois"] = bar_data["ds"].dt.strftime("%b %Y")
bar_data = bar_data.set_index("Mois")

st.subheader("📊 Détail mensuel des prévisions")
st.bar_chart(bar_data["yhat"])

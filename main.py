
import streamlit as st
st.set_page_config(page_title="Tableau de bord analytique – MaroMarché", layout="wide")

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Morocco.svg", width=100)
# Afficher le logo tout en haut de la barre latérale



import pandas as pd
import matplotlib.pyplot as plt
from utils.data_loader import load_data
from utils.ui_style import set_background, custom_sidebar_style
from utils.auth import check_authentication

import io




# Authentification
check_authentication()


# Configuration de la page

set_background()
custom_sidebar_style()



# Titre principal
st.title("📊 Tableau de bord analytique – MaroMarché")

# Charger les données
df = load_data()

# ========== Filtres ==========
st.sidebar.header("🎯 Filtres")

villes = df['ville'].dropna().unique()
produits = df['nom_produit'].dropna().unique()
annees = df['annee'].dropna().unique()

ville_selection = st.sidebar.selectbox("Sélectionner une ville", options=["Toutes"] + list(sorted(villes)))
produit_selection = st.sidebar.selectbox("Sélectionner un produit", options=["Tous"] + list(sorted(produits)))
annee_selection = st.sidebar.selectbox("Sélectionner une année", options=["Toutes"] + sorted(annees))

# Appliquer les filtres
df_filtered = df.copy()
if ville_selection != "Toutes":
    df_filtered = df_filtered[df_filtered['ville'] == ville_selection]
if produit_selection != "Tous":
    df_filtered = df_filtered[df_filtered['nom_produit'] == produit_selection]
if annee_selection != "Toutes":
    df_filtered = df_filtered[df_filtered['annee'] == annee_selection]



# ========== KPIs ==========
st.markdown("## 📌 <span style='color:#006400;'>Indicateurs clés</span>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**<span style='color:#333;'>Nombre total de ventes</span>**", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#228B22;'>{df_filtered.shape[0]}</h3>", unsafe_allow_html=True)  # Vert

with col2:
    montant_total = df_filtered["montant_total"].sum()
    st.markdown("**<span style='color:#333;'>Montant total des ventes</span>**", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#228B22;'>{montant_total:,.0f} MAD</h3>", unsafe_allow_html=True)  # Vert

with col3:
    top_produit = df_filtered["nom_produit"].value_counts().idxmax() if not df_filtered.empty else "Aucun"
    st.markdown("**<span style='color:#333;'>Produit le plus vendu</span>**", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#228B22;'>{top_produit}</h3>", unsafe_allow_html=True)  # Bleu

with col4:
    top_ville = df_filtered["ville"].value_counts().idxmax() if not df_filtered.empty else "Aucune"
    st.markdown("**<span style='color:#333;'>Ville </span>**", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#228B22;'>{top_ville}</h3>", unsafe_allow_html=True)  # Bleu

# ========== Graphique ==========
st.subheader("📈 Top produits les plus vendus")

if not df_filtered.empty:
    top_produits = df_filtered['nom_produit'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(6, 3))
    top_produits.plot(kind='bar', ax=ax, color='lightgreen')
    ax.set_ylabel("Nombre de ventes",fontsize=10)
    ax.set_xlabel("Produit",fontsize=10)
    ax.set_title("Top 10 des produits les plus vendus")
    st.pyplot(fig)

    # ========== Téléchargement des données filtrées ==========
    # ========== Affichage du tableau filtré et téléchargement ==========
    filtres_appliques = (
            ville_selection != "Toutes"
            or produit_selection != "Tous"
            or annee_selection != "Toutes"
    )

    if filtres_appliques and not df_filtered.empty:
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
        st.info("🔎 Veuillez appliquer au moins un filtre pour activer l'affichage et le téléchargement des données.")




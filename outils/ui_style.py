
import streamlit as st
def set_background():
    st.markdown(
        """
        <style>
        /* Fond global rose clair */
        .stApp {
            background-color: #ffcccc;
        }

        /* Texte des liens principaux du menu */
        section[data-testid="stSidebar"] div.css-1v0mbdj,
        section[data-testid="stSidebar"] div.css-1wvskn5 {
            color: #ffcccc !important;
            font-weight: 600;
            font-size: 18px;
        }

        /* Ne pas changer la couleur des flèches / icônes */
        section[data-testid="stSidebar"] svg {
            color: inherit !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def custom_sidebar_style():
    st.markdown("""
        <style>
        /* Fond de la sidebar */
        section[data-testid="stSidebar"] {
            background-color: #1a1a2e;  /* Bleu nuit */
            padding: 20px;
        }

        /* Styles des liens dans le menu */
        section[data-testid="stSidebar"] ul {
            padding-left: 0;
        }

        section[data-testid="stSidebar"] ul li {
            list-style-type: none;
            margin-bottom: 10px;
        }

        section[data-testid="stSidebar"] ul li a {
            display: block;
            background-color: #e94560;  /* Rouge-rose pour bouton */
            color: white !important;
            padding: 10px 15px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }

        /* Hover effect */
        section[data-testid="stSidebar"] ul li a:hover {
            background-color: #f1c40f;  /* Jaune clair */
            color: #1a1a2e !important;  /* Texte sombre */
        }

        /* Titre sidebar + titres des champs */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] label {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

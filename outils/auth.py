import streamlit as st
from utils.ui_style import set_background, custom_sidebar_style


#st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Morocco.svg", width=200)

def login():
    set_background()
    custom_sidebar_style()
    users = {
        "admin": "lamine123",
        "user1": "passe123"
    }

    if st.session_state.get("logged_out_user"):
        st.warning(f"ℹ️ {st.session_state['logged_out_user']} vous avez été déconnecté de l'application Analyse de ventes de MaroMarché.")
        del st.session_state["logged_out_user"]  # On efface le message après l'avoir affiché

    st.sidebar.header("🔐 Connexion requise")
    username = st.sidebar.text_input("Nom d'utilisateur")
    password = st.sidebar.text_input("Mot de passe", type="password")
    login_btn = st.sidebar.button("Se connecter")

    if login_btn:
        if username in users and users[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("❌ Identifiants incorrects.")

def check_authentication():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login()
        st.stop()
    else:
        st.sidebar.success(f"✅ Connecté en tant que : {st.session_state.get('username', 'utilisateur')}")

        if st.sidebar.button("🔓 Se déconnecter"):
            # Sauvegarder l’utilisateur déconnecté
            st.session_state["logged_out_user"] = st.session_state.get("username", "utilisateur")
            st.session_state["authenticated"] = False
            st.session_state["username"] = ""
            st.rerun()



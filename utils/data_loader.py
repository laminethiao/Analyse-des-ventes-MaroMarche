

import pandas as pd
import streamlit as st  # ⚠️ à ne pas oublier

@st.cache_data
def load_data():
    df = pd.read_csv("data/dataset_final.csv", encoding='utf-8')
    return df

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os

# --- CONEXÃO (Cache Resource: Guarda a conexão aberta) ---
@st.cache_resource
def conectar_google_sheets():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    # 1. LOCAL (PC)
    if os.path.exists("credentials.json"):
        try:
            creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
            client = gspread.authorize(creds)
            return client.open("Sistema_Monitoramento_UBS")
        except Exception as e:
            st.error(f"⚠️ Erro local: {e}")
            return None

    # 2. NUVEM (SECRETS)
    try:
        if hasattr(st, "secrets") and "gcp_service_account" in st.secrets:
            cred = dict(st.secrets["gcp_service_account"])
            if "private_key" in cred:
                cred["private_key"] = cred["private_key"].replace("\\n", "\n")
            creds = Credentials.from_service_account_info(cred, scopes=scope)
            client = gspread.authorize(creds)
            return client.open("Sistema_Monitoramento_UBS")
    except:
        pass
    
    return None

# --- LEITURA (Cache Data: Guarda os dados por 60s) ---
@st.cache_data(ttl=60)
def ler_dados(nome_aba):
    planilha = conectar_google_sheets()
    if planilha:
        try:
            aba = planilha.worksheet(nome_aba)
            return aba.get_all_records()
        except:
            return []
    return []

# --- LIMPEZA DE CACHE (Para usar após salvar) ---
def limpar_cache():
    ler_dados.clear()
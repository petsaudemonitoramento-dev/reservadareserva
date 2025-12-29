import streamlit as st
import pandas as pd
from cryptography.fernet import Fernet

# --- CONFIGURAÇÃO DA CHAVE ---
def obter_cipher():
    # Pega a chave do arquivo .streamlit/secrets.toml ou da Nuvem
    chave = st.secrets.get("general", {}).get("ENCRYPTION_KEY")
    if not chave: return None
    try:
        return Fernet(chave.encode())
    except:
        return None

# --- FUNÇÕES DE TRANSFORMAÇÃO ---
def encriptar(dado):
    """Recebe 'Maria', retorna 'gAAAA...'"""
    if pd.isna(dado) or str(dado).strip() == "": return ""
    cipher = obter_cipher()
    if cipher:
        try:
            return cipher.encrypt(str(dado).encode()).decode()
        except Exception as e:
            st.error(f"Erro de Criptografia: {e}")
            return str(dado)
    return str(dado)

def decriptar(dado_cifrado):
    """Recebe 'gAAAA...', retorna 'Maria'"""
    if pd.isna(dado_cifrado) or str(dado_cifrado).strip() == "": return ""
    cipher = obter_cipher()
    if cipher:
        try:
            # Tenta descriptografar. 
            return cipher.decrypt(str(dado_cifrado).encode()).decode()
        except:
            # Se falhar (ex: é um dado antigo que não foi criptografado), retorna o original
            return str(dado_cifrado)
    return str(dado_cifrado)
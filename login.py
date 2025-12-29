import streamlit as st
import os
from cryptography.fernet import Fernet
from conexao import conectar_google_sheets, ler_dados

# --- CONFIGURAÇÃO DE CRIPTOGRAFIA ---
def obter_cipher():
    # Tenta pegar a chave dos secrets
    chave = st.secrets.get("general", {}).get("ENCRYPTION_KEY")
    
    if not chave:
        st.error("⚠️ ERRO CRÍTICO: Chave de criptografia não encontrada no secrets.toml!")
        return None
    
    try:
        return Fernet(chave.encode())
    except Exception as e:
        st.error(f"Erro na chave de criptografia: {e}")
        return None

def criptografar(senha_texto):
    cipher = obter_cipher()
    if cipher:
        return cipher.encrypt(senha_texto.encode()).decode()
    return senha_texto

def descriptografar(senha_cifrada):
    cipher = obter_cipher()
    if cipher:
        try:
            return cipher.decrypt(senha_cifrada.encode()).decode()
        except:
            # Se der erro (ex: senha antiga não criptografada), retorna ela mesma
            return senha_cifrada
    return senha_cifrada

def tela_login():
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        # Carrega as imagens corretamente
        if os.path.exists("LOGO_PET.png"): 
            st.image("LOGO_PET.png", width=400)
        elif os.path.exists("favicon_pet128x128.png"): 
            st.image("favicon_pet128x128.png", width=400)

    st.markdown("<h1 style='text-align:center;'>Acesso Restrito - UBS Romualdo Brito</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Cadastrar"])
    
    # --- ABA DE LOGIN ---
    with tab1:
        user = st.text_input("Usuário")
        senha_input = st.text_input("Senha", type="password")
        
        if st.button("ENTRAR", type="primary", use_container_width=True):
            regs = ler_dados("Usuarios")
            found = False
            
            if regs:
                for r in regs:
                    u_banco = str(r.get('Usuario'))
                    s_banco_cifrada = str(r.get('Senha'))
                    
                    if u_banco == user:
                        s_banco_real = descriptografar(s_banco_cifrada)
                        
                        if s_banco_real == senha_input:
                            st.session_state.update({'logado': True, 'usuario': user, 'perfil': r.get('Perfil')})
                            found = True
                            st.rerun()
                        else:
                            st.error("Senha incorreta.")
                        break
            
            if not found and user and not st.session_state.get('logado'):
                st.error("Usuário não encontrado.")

    # --- ABA DE CADASTRO ---
    with tab2:
        st.info("Cadastro de novos usuários")
        n_user = st.text_input("Novo Usuário")
        n_pass = st.text_input("Nova Senha", type="password")
        n_perf = st.selectbox("Função", ["Equipe UBS", "ACS", "Aluno"])
        
        if st.button("CADASTRAR", use_container_width=True):
            planilha = conectar_google_sheets()
            if planilha and n_user and n_pass:
                try:
                    sheet = planilha.worksheet("Usuarios")
                    existentes = sheet.col_values(1)
                    if n_user in existentes:
                        st.error("❌ Usuário já existe.")
                    else:
                        senha_segura = criptografar(n_pass)
                        sheet.append_row([n_user, senha_segura, n_perf])
                        st.success("✅ Usuário cadastrado! Siga para o login!")
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")

    st.write("") 
    st.write("") 
    st.markdown(
        """
        <div style='text-align: center; font-size: 12px; color: grey; margin-top: 30px;'>
            Desenvolvido por <b>Lucca Araujo</b><br>
            © 2025 PET Saúde Digital/UFCG
        </div>
        """, 
        unsafe_allow_html=True
    )

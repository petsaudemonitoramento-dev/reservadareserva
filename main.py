import streamlit as st
import os
from PIL import Image  

# --- IMPORTAÇÃO DOS MÓDULOS ---
from login import tela_login 
from telas_cadastro import form_clinico
from telas_acs import form_acs
from telas_risco import pagina_classificacao_risco
from meus_pacientes import visualizar_registros

# --- CONFIGURAÇÃO DA PÁGINA E ÍCONE ---
# 2. Carrega a sua logo (certifique-se que o arquivo está na pasta)
favicon = Image.open("favicon_pet128x128.png")

st.markdown("""
    <style>
    /* Esconde indicadores técnicos e menus padrão */
    div[data-testid="stStatusWidget"] { visibility: hidden; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Estilização Profissional */
    .stButton > button { border-radius: 8px; }
    .stSpinner > div { border-top-color: #004b8d !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Define a logo como ícone da página
st.set_page_config(page_title="Monitoramento UBS", page_icon=favicon, layout="wide")

# --- REMOVER ITENS PADRÃO DO STREAMLIT (CSS) ---
# Isso remove o rodapé (Hosted with...), a marca d'água e o menu do topo
hide_styles = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_styles, unsafe_allow_html=True)

# --- CONTROLE DE SESSÃO ---
if 'logado' not in st.session_state: 
    st.session_state['logado'] = False

# --- LÓGICA PRINCIPAL ---
if not st.session_state['logado']:
    tela_login() 
else:
    # BARRA LATERAL (SIDEBAR)
    with st.sidebar:
        # Exibição do Logo interna (na barra lateral) Pode substituir por foto de perfil um dia
        if os.path.exists("LOGO_PET.png"): 
            st.image("LOGO_PET.png", width=120)
        elif os.path.exists("LOGO_PET.jpeg"): 
            st.image("LOGO_PET.jpeg", width=120)
        
        # Informação do Usuário
        st.sidebar.title(f"Bem-vindo, {st.session_state.get('usuario', 'Usuário')}")
        
        # Definição do Menu baseado no Perfil
        opcoes = ["Meus Pacientes"]
        if st.session_state['perfil'] == "Equipe UBS": 
            opcoes = ["Novo Cadastro", "Meus Pacientes", "Classificação de Risco"]
        if st.session_state['perfil'] == "ACS": 
            opcoes = ["Novo Relatório", "Meus Pacientes"]
        if st.session_state['perfil'] == "Aluno": 
            opcoes = ["Painel Geral"]
        
        # Lógica de Redirecionamento
        idx_padrao = 0
        if 'menu_temp_override' in st.session_state and st.session_state['menu_temp_override'] in opcoes:
            idx_padrao = opcoes.index(st.session_state['menu_temp_override'])
            del st.session_state['menu_temp_override']
            
        menu = st.radio("Menu", opcoes, index=idx_padrao)
        
        st.divider()
        
        # Botão de Sair
        if st.button("SAIR", type="primary", use_container_width=True):
            st.session_state['logado'] = False
            st.rerun()

        # --- RODAPÉ DE AUTORIA ---
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; font-size: 12px; color: grey;'>
                Desenvolvido por <b>Lucca Araujo</b><br>
                © 2025 PET Saúde Digital/UFCG
            </div>
            """, 
            unsafe_allow_html=True
        )
            
    # ROTEAMENTO DAS TELAS
    if menu == "Novo Cadastro": 
        form_clinico()
    elif menu == "Novo Relatório": 
        form_acs()
    elif menu in ["Meus Pacientes", "Painel Geral"]: 
        visualizar_registros()
    elif menu == "Classificação de Risco": 
        pagina_classificacao_risco()

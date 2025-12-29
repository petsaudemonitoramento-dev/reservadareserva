import streamlit as st
from conexao import conectar_google_sheets, limpar_cache

def form_acs():
    st.subheader("🏘️ Relatório ACS")
    
    # Controle de estado para mensagem de sucesso
    if 'form_acs_sucesso' not in st.session_state: st.session_state['form_acs_sucesso'] = False
        
    if st.session_state['form_acs_sucesso']:
        st.success("✅ Relatório enviado com sucesso!")
        if st.button("🆕 Novo Relatório", type="primary"):
            st.session_state['form_acs_sucesso'] = False
            st.rerun()
        return

    # Formulário otimizado (não recarrega a cada clique)
    with st.form("form_acs_diario", clear_on_submit=False):
        micro = st.selectbox("Microárea", ["07", "08", "09", "10"])
        
        c1, c2 = st.columns(2)
        q_gest = c1.number_input("Total Gestantes", 0, step=1)
        q_cons = c2.number_input("Consultas Realizadas", 0, step=1)
        q_falt = c1.number_input("Faltas", 0, step=1)
        q_risc = c2.number_input("Gestantes de Alto Risco", 0, step=1)
        
        st.write("")
        submitted = st.form_submit_button("ENVIAR RELATÓRIO", type="primary", use_container_width=True)
    
    if submitted:
        planilha = conectar_google_sheets()
        if planilha:
            try:
                # Envia para a aba 'Dados_ACS'
                planilha.worksheet("Dados_ACS").append_row([
                    micro, q_gest, q_cons, q_falt, q_risc, st.session_state['usuario']
                ])
                
                # Garante que o painel de visualização veja os dados novos
                limpar_cache()
                
                st.session_state['form_acs_sucesso'] = True
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

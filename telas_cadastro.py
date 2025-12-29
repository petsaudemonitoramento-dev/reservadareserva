import streamlit as st
from datetime import datetime
from conexao import conectar_google_sheets, limpar_cache
from calculos import EXAMES_TRIMESTRE
from seguranca import encriptar

def form_clinico():
    st.subheader("🩺 Gestão de Ingressos - Pré-Natal")
    
    # Inicializa a lista de datas na sessão para persistência durante a interação
    if 'temp_datas_cad' not in st.session_state:
        st.session_state['temp_datas_cad'] = []

    # Organização principal em abas
    tab_manual, tab_importar = st.tabs(["📝 Cadastro Manual", "📤 Importar Planilha (PEC)"])

    # --- ABA 1: CADASTRO MANUAL ---
    with tab_manual:
        # Mensagem de sucesso após salvamento
        if st.session_state.get('form_clinico_sucesso'):
            st.success("✅ Paciente cadastrada com sucesso!")
            if st.button("🆕 Iniciar Novo Cadastro"):
                st.session_state['form_clinico_sucesso'] = False
                st.session_state['temp_datas_cad'] = [] # Limpa as datas para o novo formulário
                st.rerun()
            return

        # --- 1. DADOS DE IDENTIFICAÇÃO ---
        st.markdown("### 1. Dados da Gestante")
        col1, col2, col3 = st.columns(3)
        id_gestante = col1.text_input("ID Gestante / Nome", placeholder="Ex: Maria Silva ou CNS")
        microarea = col2.selectbox("Microárea", ["07", "08", "09", "10"])
        data_inicio = col3.date_input("Início do Pré-Natal", format="DD/MM/YYYY")

        st.markdown("---")

        # --- 2. ACOMPANHAMENTO E DESFECHO ---
        st.markdown("### 2. Status do Acompanhamento")
        c_ig, c_p = st.columns([1, 2])
        ig_v = c_ig.number_input("Idade Gestacional Atual (Semanas)", 0, 42)
        ja_teve_parto = c_p.radio("Já teve o parto?", ["Não", "Sim"], horizontal=True)
        
        # Lógica Condicional: Campos de parto aparecem apenas se "Sim"
        tipo_p = "-"
        dt_parto = None
        if ja_teve_parto == "Sim":
            with st.container(border=True):
                st.markdown("✨ **Informações do Parto**")
                col_p1, col_p2 = st.columns(2)
                tipo_p = col_p1.selectbox("Tipo de Parto", ["Normal", "Cesárea"])
                dt_parto = col_p2.date_input("Data da Ocorrência", format="DD/MM/YYYY")
        
        puerperio = st.radio("Paciente em Puerpério?", ["Não", "Sim"], horizontal=True)

        st.markdown("---")

        # --- 3. HISTÓRICO DE CONSULTAS (LAYOUT ALINHADO) ---
        st.markdown("### 📅 3. Datas de Consultas Realizadas")
        with st.container(border=True):
            # Resumo visual das datas adicionadas
            if st.session_state['temp_datas_cad']:
                st.info(f"**Datas registradas:** {', '.join(st.session_state['temp_datas_cad'])}")
            else:
                st.caption("Nenhuma consulta extra adicionada ainda.")

            # Colunas para alinhamento horizontal perfeito
            c_date, c_add, c_remove = st.columns([2, 1, 1])
            
            nova_data = c_date.date_input("Selecionar Data:", format="DD/MM/YYYY")
            
            # Ajuste CSS para alinhar botões verticalmente com o campo de data
            st.markdown("""<style> div.stButton { margin-top: 28px; } </style>""", unsafe_allow_html=True)
            
            if c_add.button("➕ Adicionar", use_container_width=True):
                data_fmt = nova_data.strftime("%d/%m/%Y")
                if data_fmt not in st.session_state['temp_datas_cad']:
                    st.session_state['temp_datas_cad'].append(data_fmt)
                    st.rerun()
            
            # Apaga data por data (do último para o primeiro)
            if c_remove.button("🔙 Apagar Última", use_container_width=True):
                if st.session_state['temp_datas_cad']:
                    st.session_state['temp_datas_cad'].pop()
                    st.rerun()

        st.markdown("---")

        # --- 4. EXAMES E PROCEDIMENTOS (VISUAL 2.0 RESTAURADO) ---
        st.subheader("🧪 4. Exames e Procedimentos")
        t1, t2, t3 = st.tabs(["1º Trimestre", "2º Trimestre", "3º Trimestre"])
        
        # Função para marcar/desmarcar todos os itens da aba
        def toggle_all_exams(trimestre, lista):
            chave_mestre = f"all_{trimestre}"
            estado = st.session_state.get(chave_mestre, False)
            for i in range(len(lista)):
                st.session_state[f"chk_{trimestre}_{i}"] = estado

        abas_config = {"1º Trimestre": t1, "2º Trimestre": t2, "3º Trimestre": t3}
        
        for nome_tri, aba_obj in abas_config.items():
            with aba_obj:
                lista_limpa = [ex for ex in EXAMES_TRIMESTRE.get(nome_tri, []) if ex != "Vacinação em dia"]
                
                # Checkbox de seleção em massa
                st.checkbox("✅ Marcar Todas deste trimestre", key=f"all_{nome_tri}", 
                            on_change=toggle_all_exams, args=(nome_tri, lista_limpa))
                
                st.divider()
                
                # Layout em duas colunas para os exames
                cols_exames = st.columns(2)
                for i, exame in enumerate(lista_limpa):
                    cols_exames[i % 2].checkbox(exame, key=f"chk_{nome_tri}_{i}")

        st.markdown("---")

        # --- AÇÃO FINAL: SALVAMENTO ---
        if st.button("💾 SALVAR CADASTRO COMPLETO", type="primary", use_container_width=True):
            if not id_gestante:
                st.error("O campo 'ID Gestante' é obrigatório.")
            else:
                planilha = conectar_google_sheets()
                if planilha:
                    # 1. Compila os exames marcados em string organizada
                    exames_final = []
                    for nt in ["1º Trimestre", "2º Trimestre", "3º Trimestre"]:
                        lst = [ex for i, ex in enumerate(EXAMES_TRIMESTRE.get(nt, [])) if ex != "Vacinação em dia"]
                        selecionados = [ex for i, ex in enumerate(lst) if st.session_state.get(f"chk_{nt}_{i}")]
                        if selecionados:
                            exames_final.append(f"[{nt}]: " + ", ".join(selecionados))
                    
                    # 2. Prepara a linha conforme as 14 colunas (A até N)
                    list_consultas = st.session_state['temp_datas_cad']
                    id_seguro = encriptar(id_gestante)
                    
                    nova_linha = [
                        id_seguro,                          # A: Agora salva criptografado (gAAAA...)
                        microarea,                          # B: Microárea
                        data_inicio.strftime("%d/%m/%Y"),   # C: Início PN
                        len(list_consultas) + 1,            # D: Total Consultas (Cadastro + Extras)
                        ", ".join(list_consultas),          # E: Histórico Datas
                        "\n".join(exames_final),            # F: Exames_Trimestre
                        "Verificar Risco",                  # G: Fatores_Risco (Default)
                        ig_v,                               # H: Tempo_Gestação
                        ja_teve_parto,                      # I: Teve_Parto
                        tipo_p,                             # J: Tipo_Parto
                        (dt_parto.strftime("%d/%m/%Y") if dt_parto else "-"), # K: Data_Parto
                        puerperio,                          # L: Puerpério
                        st.session_state['usuario'],        # M: Responsável
                        datetime.now().strftime("%d/%m/%Y") # N: Data Atualização
                    ]
                    
                    try:
                        planilha.worksheet("Dados_Clinicos").append_row(nova_linha)
                        limpar_cache()
                        st.session_state['form_clinico_sucesso'] = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao conectar com a planilha: {e}")

    # --- ABA 2: IMPORTAR PLANILHA (PREPARADA) ---
    with tab_importar:
        st.subheader("📤 Importação de Dados do e-SUS PEC")
        st.write("Selecione o arquivo exportado para cadastrar múltiplas gestantes automaticamente.")
        
        upload_pec = st.file_uploader("Arraste sua planilha (.xlsx ou .csv)", type=["xlsx", "csv"])
        
        if st.button("🚀 Processar Planilha PEC", type="primary"):
            if upload_pec:
                st.info("⚠️ Funcionalidade pronta para mapeamento de colunas assim que o modelo for fornecido.")
            else:
                st.error("Por favor, selecione um arquivo primeiro.")
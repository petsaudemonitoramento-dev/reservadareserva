import streamlit as st
import pandas as pd
from datetime import datetime
from conexao import conectar_google_sheets, ler_dados, limpar_cache
from calculos import calcular_gestacao_atual, pegar_cor_sem, EXAMES_TRIMESTRE
from graficos import criar_grafico_captacao_precoce, criar_grafico_meta_consultas, criar_grafico_riscos_ubs
from seguranca import decriptar, encriptar  # Importamos a segurança

def restaurar_estado_exames(texto_banco):
    if not texto_banco or texto_banco == "-": return
    for k in list(st.session_state.keys()):
        if k.startswith("chk_upd_"): del st.session_state[k]
    linhas = str(texto_banco).split('\n')
    for linha in linhas:
        for nt in ["1º Trimestre", "2º Trimestre", "3º Trimestre"]:
            if f"[{nt}]" in linha:
                itens = [i.strip() for i in linha.replace(f"[{nt}]: ", "").split(',')]
                lista_p = [ex for ex in EXAMES_TRIMESTRE.get(nt, []) if ex != "Vacinação em dia"]
                for i, ex_p in enumerate(lista_p):
                    if ex_p in itens: st.session_state[f"chk_upd_{nt}_{i}"] = True

def exibir_dashboard_gerencial(df_completo):
    st.markdown("### 🏥 Painel de Indicadores (Rede Alyne & Previne)")
    col_sel1, col_sel2 = st.columns([1, 3])
    with col_sel1:
        visao = st.radio("Visão:", ["Minha Produção", "Geral"], horizontal=True)
    
    df_dash = df_completo
    if visao == "Minha Produção":
        df_dash = df_completo[df_completo['Responsavel_Registro'] == st.session_state['usuario']]

    if df_dash.empty: return st.info("Sem dados.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Gestantes", len(df_dash))
    alto_risco = len(df_dash[df_dash['Fatores_Risco'].apply(lambda x: str(x) not in ['Nenhum', '-', 'Verificar Classificação de Risco', ''])])
    c2.metric("Alto Risco", alto_risco)
    media_cons = pd.to_numeric(df_dash['Total_Consultas'], errors='coerce').mean()
    c3.metric("Média Consultas", f"{media_cons:.1f}")

    st.markdown("---")
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        st.plotly_chart(criar_grafico_captacao_precoce(df_dash), use_container_width=True)
    with col_g2:
        st.plotly_chart(criar_grafico_meta_consultas(df_dash), use_container_width=True)
    with col_g3:
        st.plotly_chart(criar_grafico_riscos_ubs(df_dash), use_container_width=True)

def form_gerenciar_paciente(id_p_cripto, dados, modo):
    # --- NOVO: Mostra o nome real descriptografado no título ---
    nome_visual = decriptar(id_p_cripto)
    st.subheader(f"⚙️ {modo.upper()}: {nome_visual}")
    
    if 'carregou_dados' not in st.session_state:
        restaurar_estado_exames(dados.get('Exames_Trimestre', ''))
        st.session_state['carregou_dados'] = True
        st.session_state['temp_datas_upd'] = [d.strip() for d in str(dados.get('Historico_Datas', '')).split(',') if d.strip()]

    bloqueado = (modo == 'atualizar')
    col1, col2, col3 = st.columns(3)
    
    # --- CORREÇÃO DO ERRO DE INT() ---
    # Tenta converter para número. Se for "Pós-parto" ou texto, assume 0.
    try:
        ig_padrao = int(dados.get('Tempo_Gestação', 0))
    except:
        ig_padrao = 0
    
    # Tenta converter microárea (caso venha vazia)
    try:
        idx_micro = int(dados.get('Microarea', 7)) - 7
    except:
        idx_micro = 0

    micro = col1.selectbox("Microárea", ["07", "08", "09", "10"], index=idx_micro, disabled=bloqueado)
    ig = col2.slider("IG Atual", 0, 42, ig_padrao) # Usa o valor tratado
    parto = col3.radio("Parto?", ["Não", "Sim"], index=0 if dados.get('Teve_Parto') == "Não" else 1)

    st.markdown("---")
    st.subheader("🧪 Atualizar Exames e Procedimentos")
    tab1, tab2, tab3 = st.tabs(["1º Trimestre", "2º Trimestre", "3º Trimestre"])
    def toggle_upd(nt, lst):
        est = st.session_state.get(f"all_upd_{nt}", False)
        for i in range(len(lst)): st.session_state[f"chk_upd_{nt}_{i}"] = est

    for nt, aba in {"1º Trimestre": tab1, "2º Trimestre": tab2, "3º Trimestre": tab3}.items():
        with aba:
            lst = [ex for ex in EXAMES_TRIMESTRE.get(nt, []) if ex != "Vacinação em dia"]
            st.checkbox("Marcar Todos", key=f"all_upd_{nt}", on_change=toggle_upd, args=(nt, lst))
            cols = st.columns(2)
            for i, ex in enumerate(lst):
                st.checkbox(ex, key=f"chk_upd_{nt}_{i}")

    if st.button("💾 SALVAR ALTERAÇÕES", type="primary", use_container_width=True):
        planilha = conectar_google_sheets()
        if planilha:
            aba = planilha.worksheet("Dados_Clinicos")
            
            # --- NOVO: Procura pelo ID CRIPTOGRAFADO (Original) ---
            cell = aba.find(str(id_p_cripto))
            
            if cell:
                ex_txt = []
                for nt in ["1º Trimestre", "2º Trimestre", "3º Trimestre"]:
                    lst = [ex for ex in EXAMES_TRIMESTRE.get(nt, []) if ex != "Vacinação em dia"]
                    sel = [ex for i, ex in enumerate(lst) if st.session_state.get(f"chk_upd_{nt}_{i}")]
                    if sel: ex_txt.append(f"[{nt}]: " + ", ".join(sel))
                
                # Mapeamento 14 colunas
                aba.update_cell(cell.row, 2, micro) # B
                aba.update_cell(cell.row, 4, len(st.session_state['temp_datas_upd'])+1) # D
                aba.update_cell(cell.row, 6, "\n".join(ex_txt)) # F
                aba.update_cell(cell.row, 8, ig) # H
                aba.update_cell(cell.row, 9, parto) # I
                limpar_cache()
                st.success("Sincronizado!")
                del st.session_state['editando_paciente']
                if 'carregou_dados' in st.session_state: del st.session_state['carregou_dados']
                st.rerun()
            else:
                st.error("Erro crítico: Paciente não encontrada na planilha. O ID foi alterado externamente?")

def visualizar_registros():
    if st.session_state.get('editando_paciente'):
        form_gerenciar_paciente(st.session_state['id_edit'], st.session_state['dados_edit'], st.session_state['modo_edit'])
    else:
        st.title("📋 Painel de Monitoramento")
        dados = ler_dados("Dados_Clinicos")
        if not dados: return st.warning("Sem dados.")
        df = pd.DataFrame(dados)

        # --- NOVO: Cria coluna Visual (Descriptografada) para exibir na tela ---
        if 'ID_Gestante' in df.columns:
            df['Nome_Visual'] = df['ID_Gestante'].apply(decriptar)
        else:
            df['Nome_Visual'] = df.get('ID_Gestante', '-')

        # --- DASHBOARD RESTAURADO NO TOPO ---
        with st.expander("📈 Dashboard de Indicadores e Gráficos", expanded=False):
            exibir_dashboard_gerencial(df)
            
        st.markdown("### 🤰 Fichas das Pacientes")
        st.divider()

        df_cards = df
        if st.session_state['perfil'] == "ACS":
            df_cards = df[df['Responsavel_Registro'] == st.session_state['usuario']]

        cols = st.columns(3)
        for idx, row in df_cards.iterrows():
            with cols[idx % 3]:
                res_ig = calcular_gestacao_atual(row)
                cor_topo = pegar_cor_sem(res_ig)
                
                # --- CORREÇÃO AQUI: HTML COLADO NA ESQUERDA ---
                st.markdown(f"""
<div style="border: 1px solid #ddd; border-radius: 10px; padding: 0px; background-color: white; margin-bottom: 20px;">
    <div style="background-color: {cor_topo}; height: 8px; border-radius: 10px 10px 0 0;"></div>
    <div style="padding: 15px;">
        <h3 style="margin: 0 0 5px 0;">{row['Nome_Visual']}</h3>
        <p style="font-size:10px; color:gray; margin-bottom:15px;">ID Seguro: {str(row['ID_Gestante'])[:10]}...</p>
        <p style="margin: 5px 0;">📍 <b>Microárea:</b> {row['Microarea']}</p>
        <p style="margin: 5px 0;">🔢 <b>Consultas:</b> {row['Total_Consultas']}</p>
        <div style="background-color: #fff9db; padding: 5px 10px; border-radius: 15px; display: inline-block; margin-top: 10px;">
            🤰 <b>Gestante</b> | IG Registro: {row['Tempo_Gestação']} Sem
        </div>
    </div>
    <hr style="margin: 0;"><div style="padding: 15px;">
        <h4 style="margin: 0 0 10px 0;">🩺 Dados Clínicos</h4>
        <p style="font-size: 0.9em; color: #555;"><b>Exames:</b> {str(row['Exames_Trimestre'])[:110]}...</p>
    </div>
</div>
""", unsafe_allow_html=True)
                
                riscos = str(row['Fatores_Risco'])
                if riscos not in ["-", "Nenhum", "Verificar Classificação de Risco", ""]:
                    st.error(f"⚠️ Riscos: {riscos}")

                c1, c2 = st.columns(2)
                if c1.button("✏️ Editar", key=f"ed_{idx}", use_container_width=True):
                    st.session_state.update({
                        'editando_paciente': True, 
                        'id_edit': row['ID_Gestante'], 
                        'dados_edit': row.to_dict(), 
                        'modo_edit': 'editar'
                    })
                    st.rerun()
                if c2.button("⚠️ Classificar", key=f"rs_{idx}", type="primary", use_container_width=True):
                    st.session_state['id_selecionado_dashboard'] = str(row['ID_Gestante'])
                    st.session_state['menu_temp_override'] = "Classificação de Risco"
                    st.rerun()
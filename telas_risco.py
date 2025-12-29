import streamlit as st
import pandas as pd
from datetime import datetime
from conexao import conectar_google_sheets, ler_dados, limpar_cache
from calculos import calcular_score_risco_complexo, GRUPO_1, GRUPO_3, GRUPO_4, GRUPO_5
from utils import gerar_docx_memoria

def pagina_classificacao_risco():
    st.header("⚠ Classificação de Risco Gestacional")
    
    # --- 1. CARREGAMENTO E SEGURANÇA ---
    dados_brutos = ler_dados("Dados_Clinicos")
    if not dados_brutos:
        st.warning("Cadastre gestantes primeiro.")
        return
    
    df = pd.DataFrame(dados_brutos)
    df["ID_Gestante"] = df["ID_Gestante"].astype(str)
    ids = sorted(df["ID_Gestante"].unique().tolist())
    
    index_p = 0
    id_sessao = st.session_state.get('id_selecionado_dashboard')
    if id_sessao in ids:
        index_p = ids.index(id_sessao)
        
    id_sel = st.selectbox("Selecione a Gestante:", ids, index=index_p)
    trimestre_relatorio = st.radio("Período do Relatório:", ["1º Trimestre", "2º Trimestre", "3º Trimestre"], horizontal=True)

    # Busca exames para a lógica de autopreenchimento do Grupo 5
    df_f = df[df["ID_Gestante"] == str(id_sel)]
    exames_previos = str(df_f.iloc[0].get("Exames_Trimestre", "")).lower() if not df_f.empty else ""

    st.markdown("---")

    # --- 2. AVALIAÇÃO NUTRICIONAL (GRUPO 2) ---
    st.subheader("📊 2. Avaliação Nutricional")
    st.info("ℹ️ **Nota:** Digite os valores. A pontuação é automática. A soma de Baixo Peso e Sobrepeso (exceto Obesidade Mórbida) gera atenção diferenciada na APS, não Alto Risco imediato.")
    
    c1, c2 = st.columns(2)
    peso_txt = c1.text_input("Peso Atual (kg)", placeholder="Ex: 70.5")
    altura_txt = c2.text_input("Altura (m ou cm)", placeholder="Ex: 1.65")
    
    try: peso = float(peso_txt.replace(",", ".")) if peso_txt else 0.0
    except: peso = 0.0
    try: altura = float(altura_txt.replace(",", ".")) if altura_txt else 0.0
    except: altura = 0.0
    
    st.markdown("---")

    # --- 3. CHECKLIST DE RISCOS ---
    sel_g1, sel_g3, sel_g4, sel_g5 = [], [], [], []

    with st.expander("👤 1. Características Individuais", expanded=False):
        cols1 = st.columns(2)
        for i, (item, pts) in enumerate(GRUPO_1.items()):
            if cols1[i % 2].checkbox(f"{item} (+{pts} pts)", key=f"g1_{i}"):
                sel_g1.append(item)

    with st.expander("🏥 3. Comorbidades Prévias", expanded=False):
        cols3 = st.columns(2)
        for i, (item, pts) in enumerate(GRUPO_3.items()):
            label = item.split(" (")[0]
            help_txt = f"Pontuação: {pts} pts\nCritério: {item}"
            if cols3[i % 2].checkbox(label, key=f"g3_{i}", help=help_txt):
                sel_g3.append(item)

    with st.expander("📅 4. Histórico Obstétrico Anterior", expanded=False):
        cols4 = st.columns(2)
        for i, (item, pts) in enumerate(GRUPO_4.items()):
            if cols4[i % 2].checkbox(item, key=f"g4_{i}"):
                sel_g4.append(item)

    with st.expander("🤰 5. Intercorrências Atuais (Com Autopreenchimento)", expanded=False):
        cols5 = st.columns(2)
        for i, (item, pts) in enumerate(GRUPO_5.items()):
            termo = item.split(" - ")[0].split(" (")[0].lower()
            ja_detectado = (termo in exames_previos) and (len(termo) > 3)
            
            help_auto = f"Pontuação: {pts} pts"
            if ja_detectado:
                help_auto += "\n\nℹ️ Marcado automaticamente via Cadastro Clínico."
            
            if cols5[i % 2].checkbox(item.split(" - ")[0], value=ja_detectado, key=f"g5_{i}", help=help_auto):
                sel_g5.append(item)

    st.markdown("---")

    # --- 4. BOTÃO DE CÁLCULO E RESULTADO ---
    if st.button("🧮 CALCULAR CLASSIFICAÇÃO DE RISCO", type="primary", use_container_width=True):
        dados_input = {"peso": peso, "altura": altura, "g1": sel_g1, "g3": sel_g3, "g4": sel_g4, "g5": sel_g5}
        resultado = calcular_score_risco_complexo(dados_input)
        
        st.session_state['resultado_risco'] = {
            **resultado, 
            "id": id_sel, 
            "profissional": st.session_state['usuario'], 
            "trimestre": trimestre_relatorio
        }

    # Exibição do Resultado e Resumo de Fatores
    if 'resultado_risco' in st.session_state:
        res = st.session_state['resultado_risco']
        cor = "#2ecc71" if "Habitual" in res['Classificacao'] else "#f1c40f" if "Médio" in res['Classificacao'] else "#e74c3c"
        
        st.markdown(f"""
            <div style='background-color:{cor}; padding:20px; border-radius:10px; color:black; text-align:center;'>
                <h2 style='margin:0;'>RESULTADO: {res['Classificacao']}</h2>
                <h3 style='margin:5px 0;'>Pontuação Total: {res['Score']}</h3>
                <p><b>IMC:</b> {res['IMC']} ({res['Desc_IMC']})</p>
            </div>
        """, unsafe_allow_html=True)
        
        # --- RESUMO DO PORQUÊ FOI CLASSIFICADO ---
        with st.container(border=True):
            st.markdown("#### 🔍 Fatores Identificados:")
            if res['Fatores']:
                for fator in res['Fatores']:
                    st.markdown(f"• {fator}")
            else:
                st.write("Nenhum fator de risco pontuado.")
        
        st.info(f"**📋 CONDUTA SUGERIDA:** {res['Conclusao']}")

        st.markdown("---")
        c_docx, c_save = st.columns(2)
        
        docx_buffer = gerar_docx_memoria(res)
        if docx_buffer:
            c_docx.download_button("📄 Baixar Relatório (Word)", docx_buffer, f"Risco_{id_sel}.docx", use_container_width=True)
        
        if c_save.button("💾 Salvar Classificação no Painel", use_container_width=True):
            planilha = conectar_google_sheets()
            if planilha:
                try:
                    fatores_txt = ", ".join(res['Fatores']) if res['Fatores'] else "Nenhum"
                    aba_h = planilha.worksheet("Classificacao_Risco")
                    aba_h.append_row([res['id'], res['trimestre'], fatores_txt, res['Score'], res['Classificacao'], res['profissional'], datetime.now().strftime("%d/%m/%Y")])
                    
                    aba_c = planilha.worksheet("Dados_Clinicos")
                    cell = aba_c.find(str(res['id']))
                    if cell:
                        aba_c.update_cell(cell.row, 7, fatores_txt)
                        limpar_cache()
                        st.success("✅ Classificação salva e Painel atualizado!")
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
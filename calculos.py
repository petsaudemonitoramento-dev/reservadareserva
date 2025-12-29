from datetime import datetime

# --- GRUPO 1: Características Individuais e Socioeconômicas ---
GRUPO_1 = {
    "<=15 anos": 3,
    ">=40 anos": 3,
    "Não aceitação da gravidez": 3,
    "Indícios de Violência Doméstica": 2,
    "Situação de rua/ indígena ou quilombola": 2,
    "Sem escolaridade": 1,
    "Tabagista ativo": 2,
    "Raça negra": 1
}

# --- GRUPO 2: Avaliação Nutricional ---
# (A lógica deste grupo está dentro da função calcular_score_risco_complexo)

# --- GRUPO 3: Comorbidades Prévias ---
GRUPO_3 = {
    "AIDS/HIV": 10,
    "Alterações da tireoide (hipotireoidismo sem controle e hipertireoidismo)": 10,
    "Diabetes Mellitus": 10,
    "Endocrinopatias sem controle": 10,
    "Cardiopatia": 10,
    "Câncer materno": 10,
    "Cirurgia Bariátrica há menos de 6 meses": 10,
    "Doenças Autoimunes (colagenose)": 10,
    "Doenças Psiquiátricas (Encaminhar ao CAPS)": 5,
    "Doença Renal Grave": 10,
    "Dependência de Drogas (Encaminhar ao CAPS)": 10,
    "Epilepsia e doenças neurológicas graves de difícil controle": 10,
    "Hepatites (encaminhar ao infectologista)": 5,
    "HAS crônica controlada": 5,
    "HAS crônica complicada": 10,
    "Ginecopatia (Miomatose > 7cm, malformação uterina)": 5,
    "Pneumopatia grave de difícil controle": 10,
    "Tuberculose em tratamento ou com diagnostico na gestação (Encaminhar ao Pneumologista)": 10,
    "Trombofilia ou Tromboembolia": 10,
    "Uso de medicações com potencial efeito teratogênico": 5,
    "Varizes acentuadas": 1,
    "Doenças hematológicas (PTI, Anemia Falciforme, PTT, Coagulopatias, talassemias)": 10,
    "Transplante": 10
}

# --- GRUPO 4: Condições clínicas específicas e relacionadas às gestações prévias ---
GRUPO_4 = {
    "2 abortamentos espontâneos consecutivos ou 3 não consecutivos": 5,
    "3 ou mais abortamentos espontâneos consecutivos": 10,
    "Mais de um Prematuro com menos de 36 semanas": 10,
    "Óbito Fetal sem causa determinada": 10,
    "Pré-eclâmpsia ou Pré-eclâmpsia superposta": 10,
    "Eclâmpsia": 10,
    "Hipertensão Gestacional": 5,
    "Acretismo placentário": 7,
    "Descolamento prematuro de placenta": 5,
    "Insuficiência Istmo Cervical": 10,
    "Restrição de Crescimento Intrauterino": 2,
    "História de malformação Fetal complexa": 2,
    "Isoimunização em gestação anterior": 10,
    "Diabetes gestacional": 2,
    "Psicose Puerperal": 5,
    "História de tromboembolia": 10
}

# --- GRUPO 5: Condições clínicas específicas e relacionadas à gestação atual (ATUALIZADO) ---
GRUPO_5 = {
    "Ameaça de aborto - Encaminhar URGENCIA": 2,
    "Acretismo Placentário": 10,
    "Placenta Prévia após 28 semanas": 10,
    "Anemia não responsiva à tratamento (Hb> - 8) e hemopatias": 10,
    "Citologia Cervical anormal (LIEAG) – Encaminhar para PTGI": 3,
    "Doenças da tireoide diagnosticada na gestação": 10,
    "Diabetes gestacional": 10,
    "Doença Hipertensiva na Gestação (Pré-eclâmpsia, Hipertensão gestacional e Pre-eclâmpsia superposta)": 10,
    "Alteração no doppler das Artérias uterinas (aumento da resistência) e/ou alto risco para Pré-eclâmpsia": 5,
    "Doença Hemolítica": 10,
    "Gemelar": 10,
    "Isoimunização Rh": 10,
    "Insuficiência Istmo cervical": 10,
    "Colo curto no morfológico 2T": 10,
    "Malformação Congênita Fetal": 10,
    "Neoplasia ginecológica ou Câncer diagnosticado na gestação": 10,
    "Polidrâmnio/ Oligodrâmnio": 10,
    "Restrição de crescimento fetal Intrauterino": 10,
    "Toxoplasmose": 10,
    "Sífilis terciária, Alterações ultrassonográficas sugestivas de sífilis neonatal ou resistência ao tratamento com Penicilina Benzatina": 10,
    "Infecção Urinária de repetição (pielonefrite ou ITU 3x ou mais)": 10,
    "HIV, HTLV ou Hepatites Agudas": 10,
    "Condiloma acuminado (no canal/vagina/colo ou lesões extensas em região genital/perianal) – Encaminhar para PTGI": 5,
    "Feto com percentil > P90 (GIG) ou entre P3 e P10, com doppler normal (PIG)": 5,
    "Hepatopatias (colestase ou aumento das transaminases)": 10,
    "Hanseníase diagnosticada na gestação": 10
}

# --- LISTAS DE EXAMES POR TRIMESTRE ---
EXAMES_TRIMESTRE = {
    "1º Trimestre": [
        "Hemograma completo", "Tipagem sanguínea e fator Rh", "Coombs indireto (se Rh-)",
        "Glicemia em jejum", "Teste rápido Sífilis/VDRL", "Teste rápido HIV",
        "Anti-HIV", "Toxoplasmose IgM e IgG", "Sorologia Hepatite B (HbsAg)",
        "Urocultura + Urina Tipo I", "Ultrassonografia obstétrica",
        "Citopatológico colo útero (se necessário)", "Exame secreção vaginal (se indicação)",
        "Parasitológico de fezes (se indicação)", "HTLV", "Odontologia (Avaliação)", "Vacinação em dia"
    ],
    "2º Trimestre": [
        "Teste Tolerância Glicose (TTOG 75g)", "Coombs indireto (se Rh-)",
        "Ultrassonografia Morfológica", "Vacinação (dTpa/Influenza)", "Odontologia (Acompanhamento)"
    ],
    "3º Trimestre": [
        "Hemograma completo", "Glicemia em jejum", "Coombs indireto (se Rh-)",
        "VDRL (Sífilis)", "Anti-HIV", "Sorologia Hepatite B (HbsAg)",
        "Toxoplasmose (se IgG não reagente)", "Urocultura + Urina Tipo I",
        "Vacinação", "Odontologia"
    ]
}

# --- FUNÇÕES GERAIS ---

def calcular_gestacao_atual(row):
    """Calcula a IG atualizada ou retorna Pós-parto"""
    teve_parto = str(row.get('Teve_Parto', '')).strip().lower()
    if teve_parto == 'sim': return "Pós-parto"
    
    tempo_str = str(row.get('Tempo_Gestação', row.get('Tempo_Gestacao', ''))).strip()
    if tempo_str.lower() == 'pós-parto': return "Pós-parto"

    semanas_iniciais = 0
    try: semanas_iniciais = int(float(tempo_str))
    except: return 0

    data_str = str(row.get('Data_Registro', '')).strip()
    if not data_str: return semanas_iniciais 
        
    dt_reg = None
    # Tenta ler a data em formatos variados
    for fmt in ["%d/%m/%Y", "%Y-%m-%d"]:
        try: 
            dt_reg = datetime.strptime(data_str.split(' ')[0], fmt)
            break
        except: pass
        
    if dt_reg:
        dt_hoje = datetime.now()
        diferenca_dias = (dt_hoje - dt_reg).days
        semanas_atualizadas = semanas_iniciais + (diferenca_dias // 7)
        return min(semanas_atualizadas, 42)
    else:
        return semanas_iniciais

def pegar_cor_sem(valor_ig):
    """Retorna cor hexadecimal baseada na IG"""
    if str(valor_ig).lower() == "pós-parto": return "#ADD8E6" 
    try:
        s = int(valor_ig)
        if s == 0: return "#ADD8E6"
        if s <= 13: return "#2ecc71"
        if s <= 27: return "#f1c40f"
        return "#e74c3c"
    except: return "#ffffff"

def calcular_score_risco_complexo(dados):
    peso = dados.get("peso", 0)
    altura = dados.get("altura", 0)
    lista_g1 = dados.get("g1", [])
    lista_g3 = dados.get("g3", [])
    lista_g4 = dados.get("g4", [])
    lista_g5 = dados.get("g5", [])
    
    # --- CORREÇÃO INTELIGENTE DA ALTURA ---
    if altura > 3.0:
        altura = altura / 100.0

    imc = 0
    pontos_imc = 0
    desc_imc = "Eutrófica"
    
    # LÓGICA DO GRUPO 2
    if peso > 0 and altura > 0:
        imc = peso / (altura ** 2)
        if imc < 18:
            pontos_imc = 2 
            desc_imc = "Baixo Peso"
        elif 18 <= imc <= 24.9:
            pontos_imc = 0
            desc_imc = "Eutrófica"
        elif 25 <= imc <= 29.9:
            pontos_imc = 1
            desc_imc = "Sobrepeso"
        elif 30 <= imc <= 39.9:
            pontos_imc = 5
            desc_imc = "Obesidade I/II"
        else: # >= 40
            pontos_imc = 10
            desc_imc = "Obesidade Mórbida"
            
    soma_g1 = sum([GRUPO_1.get(item, 0) for item in lista_g1])
    soma_clinica = sum([GRUPO_3.get(item, 0) for item in lista_g3]) + \
                   sum([GRUPO_4.get(item, 0) for item in lista_g4]) + \
                   sum([GRUPO_5.get(item, 0) for item in lista_g5])
                   
    score_total = soma_g1 + pontos_imc + soma_clinica
    
    # Lógica de Classificação
    classificacao = "Risco Habitual"
    conclusao = "Manter acompanhamento de rotina na UBS conforme calendário padrão do Ministério da Saúde."
    
    if 5 <= score_total <= 9: 
        classificacao = "Médio Risco"
        conclusao = "Manter acompanhamento na UBS com Atenção Diferenciada. Avaliar maior frequência de consultas e discussão de caso com equipe multi."
        
    if score_total >= 10: 
        classificacao = "Alto Risco"
        conclusao = "ENCAMINHAR ao Pré-Natal de Alto Risco (ISEA/Políclinica). Manter vínculo com a UBS."
    
    # REGRA DA NOTA ADICIONAL
    if score_total >= 10 and soma_clinica == 0:
        if imc >= 40:
            classificacao = "Alto Risco (Obesidade Mórbida)"
            conclusao = "Encaminhar devido à Obesidade Mórbida. Atenção nutricional prioritária."
        else:
            classificacao = "Médio Risco (Atenção Diferenciada na APS)"
            conclusao = "A pontuação elevada se deve a fatores sociais/nutricionais. Manter na UBS com atenção diferenciada, não necessita encaminhamento imediato"
            
    todos_fatores = lista_g1 + [f"IMC: {imc:.1f} ({desc_imc})"] + lista_g3 + lista_g4 + lista_g5
    
    return {
        "Score": score_total,
        "Classificacao": classificacao,
        "Conclusao": conclusao,
        "IMC": round(imc, 2),
        "Desc_IMC": desc_imc,
        "Fatores": todos_fatores,
        "Pontos_G1": soma_g1,
        "Pontos_G2": pontos_imc,
        "Pontos_Clinicos": soma_clinica,
        "Grupos": {"G1": lista_g1, "G3": lista_g3, "G4": lista_g4, "G5": lista_g5}
    }

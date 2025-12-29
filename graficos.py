import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# --- FUNÇÃO AUXILIAR DE DATAS ---
def calcular_dias_desde_inicio(data_inicio_str):
    try:
        dt_ini = datetime.strptime(str(data_inicio_str), "%d/%m/%Y")
        dt_hoje = datetime.now()
        return (dt_hoje - dt_ini).days
    except:
        return 0

# ==========================================
# 1. GRÁFICO: CAPTAÇÃO PRECOCE (IG < 12 SEMANAS)
# ==========================================
def criar_grafico_captacao_precoce(df):
    if df.empty: return None
    
    precoce = 0
    tardio = 0
    
    for _, row in df.iterrows():
        try:
            ig_atual = int(row.get('Tempo_Gestação', 0))
            data_ini = row.get('Inicio_Pre_Natal', '')
            
            # Matemática reversa para descobrir IG no dia da 1ª consulta
            dias_passados = calcular_dias_desde_inicio(data_ini)
            semanas_passadas = dias_passados // 7
            ig_inicio = ig_atual - semanas_passadas
            
            if ig_inicio < 0: ig_inicio = 0 # Correção de segurança
            
            if ig_inicio <= 12: precoce += 1
            else: tardio += 1
        except:
            tardio += 1
            
    labels = ['Precoce (≤12 sem)', 'Tardia (>12 sem)']
    values = [precoce, tardio]
    colors = ['#2ecc71', '#e74c3c'] 
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    fig.update_traces(marker=dict(colors=colors))
    fig.update_layout(
        height=220,
        margin=dict(t=30, b=10, l=10, r=10),
        legend=dict(orientation="h", y=-0.2)
    )
    return fig

# ==========================================
# 2. GRÁFICO: META DE CONSULTAS (ADESÃO)
# ==========================================
def criar_grafico_meta_consultas(df):
    if df.empty: return None

    def classificar(n):
        try: n = int(n)
        except: n = 0
        if n >= 7: return "Meta (7+)"
        if n >= 4: return "Médio (4-6)"
        return "Crítico (0-3)"

    df_temp = df.copy()
    df_temp['Status'] = df_temp['Total_Consultas'].apply(classificar)
    
    contagem = df_temp['Status'].value_counts()
    
    labels = ["Meta (7+)", "Médio (4-6)", "Crítico (0-3)"]
    values = [contagem.get(l, 0) for l in labels]
    colors = ['#2ecc71', '#f1c40f', '#e74c3c']
    
    fig = go.Figure([go.Bar(
        x=values, y=labels, orientation='h',
        text=values, textposition='auto', marker_color=colors
    )])
    
    fig.update_layout(
        height=220,
        margin=dict(t=30, b=10, l=10, r=10),
        xaxis=dict(visible=False)
    )
    return fig

# ==========================================
# 3. GRÁFICO: FATORES DE RISCO DA UBS
# ==========================================
def criar_grafico_riscos_ubs(df):
    if df.empty: return None

    todos_riscos = []
    for riscos_str in df['Fatores_Risco']:
        if str(riscos_str) in ["Nenhum", "-", "", "Verificar Classificação de Risco"]:
            continue
        lista = [r.strip() for r in str(riscos_str).split(',')]
        todos_riscos.extend(lista)
    
    if not todos_riscos: return None

    series_riscos = pd.Series(todos_riscos)
    contagem = series_riscos.value_counts().reset_index().head(5)
    contagem.columns = ['Fator', 'Qtd']
    
    fig = px.bar(contagem, x='Qtd', y='Fator', orientation='h', text='Qtd')
    fig.update_traces(marker_color='#e74c3c', textposition='outside')
    fig.update_layout(
        height=220,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(autorange="reversed")
    )
    return fig

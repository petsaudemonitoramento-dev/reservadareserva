from docxtpl import DocxTemplate
from io import BytesIO
from datetime import datetime

# --- MAPA DE CATEGORIAS (CÉREBRO DA ORGANIZAÇÃO) ---
CATEGORIAS_MAP = {
    # 1. IDADE MATERNA
    "<=15 anos": "Idade Materna",
    ">=40 anos": "Idade Materna",

    # 2. HÁBITOS DE VIDA / SOCIAL
    "Tabagista ativo": "Hábitos de Vida / Social",
    "Dependência de Drogas": "Hábitos de Vida / Social",
    "Não aceitação da gravidez": "Hábitos de Vida / Social",
    "Indícios de Violência Doméstica": "Hábitos de Vida / Social",
    "Situação de rua": "Hábitos de Vida / Social",
    "Sem escolaridade": "Hábitos de Vida / Social",
    "Raça negra": "Hábitos de Vida / Social",

    # 3. DOENÇAS CRÔNICAS
    "Diabetes Mellitus": "Doenças Crônicas",
    "Cardiopatia": "Doenças Crônicas",
    "Doença Renal Grave": "Doenças Crônicas",
    "Epilepsia": "Doenças Crônicas",
    "HAS crônica": "Doenças Crônicas",
    "Doenças Autoimunes": "Doenças Crônicas",
    "Alterações da tireoide": "Doenças Crônicas",
    "Endocrinopatias": "Doenças Crônicas",
    "Câncer materno": "Doenças Crônicas",
    "Pneumopatia grave": "Doenças Crônicas",
    "Doenças hematológicas": "Doenças Crônicas",
    "Transplante": "Doenças Crônicas",
    "Cirurgia Bariátrica": "Doenças Crônicas",
    "Varizes acentuadas": "Doenças Crônicas",
    "Doenças Psiquiátricas": "Doenças Crônicas",

    # 4. CONDIÇÕES INFECCIOSAS
    "AIDS/HIV": "Condições Infecciosas",
    "Hepatites": "Condições Infecciosas",
    "Tuberculose": "Condições Infecciosas",
    "Infecção Urinária de Repetição": "Condições Infecciosas",
    "Doenças infecciosas agudas": "Condições Infecciosas",

    # 5. HISTÓRICO OBSTÉTRICO
    "abortamentos": "Histórico Obstétrico",
    "Prematuro": "Histórico Obstétrico",
    "Óbito Fetal": "Histórico Obstétrico",
    "Pré-eclâmpsia": "Histórico Obstétrico",
    "Eclâmpsia": "Histórico Obstétrico",
    "Hipertensão Gestacional": "Histórico Obstétrico",
    "Acretismo placentário": "Histórico Obstétrico",
    "Descolamento prematuro": "Histórico Obstétrico",
    "Insuficiência Istmo Cervical": "Histórico Obstétrico",
    "Restrição de Crescimento Intrauterino": "Histórico Obstétrico",
    "História de malformação": "Histórico Obstétrico",
    "Isoimunização em gestação anterior": "Histórico Obstétrico",
    "Diabetes gestacional": "Histórico Obstétrico",
    "Psicose Puerperal": "Histórico Obstétrico",
    "História de tromboembolia": "Histórico Obstétrico",
    "Trombofilia": "Histórico Obstétrico",

    # 6. TIPO DE GESTAÇÃO / COMPLICAÇÕES ATUAIS
    "Gestação Múltipla": "Tipo de Gestação / Complicações Atuais",
    "Diabetes Gestacional (Atual)": "Tipo de Gestação / Complicações Atuais",
    "DHEG": "Tipo de Gestação / Complicações Atuais",
    "Sangramento vaginal": "Tipo de Gestação / Complicações Atuais",
    "Isoimunização Rh (Atual)": "Tipo de Gestação / Complicações Atuais",
    "Malformação Fetal (Atual)": "Tipo de Gestação / Complicações Atuais",
    "Polidrâmnio": "Tipo de Gestação / Complicações Atuais",
    "Crescimento fetal restrito (Atual)": "Tipo de Gestação / Complicações Atuais",
    "Placenta prévia": "Tipo de Gestação / Complicações Atuais",
    "Ameaça de parto prematuro": "Tipo de Gestação / Complicações Atuais",
    "Colo curto": "Tipo de Gestação / Complicações Atuais",
    "Uso de medicações": "Tipo de Gestação / Complicações Atuais",
    "Ginecopatia": "Tipo de Gestação / Complicações Atuais"
}

def gerar_docx_memoria(dados_rel):
    try:
        doc = DocxTemplate("template_relatorio.docx")
    except Exception:
        return None

    fatores_marcados = dados_rel.get('Fatores', [])

    grupos_formatados = {
        "Idade Materna": [],
        "Tipo de Gestação / Complicações Atuais": [],
        "Doenças Crônicas": [],
        "Histórico Obstétrico": [],
        "Condições Infecciosas": [],
        "Hábitos de Vida / Social": [],
        "Outros": []  
    }

    for fator in fatores_marcados:
        if "IMC:" in fator:
            continue

        categoria_encontrada = None
        for chave_mapa, nome_categoria in CATEGORIAS_MAP.items():
            if chave_mapa in fator:
                categoria_encontrada = nome_categoria
                break

        texto_limpo = fator.split(" :")[0] if " :" in fator else fator

        if categoria_encontrada:
            grupos_formatados[categoria_encontrada].append(texto_limpo)
        else:
            grupos_formatados["Outros"].append(texto_limpo)

    def formatar_lista(lista):
        if not lista:
            return "Nada consta."
        return "\n".join([f"• {item}" for item in lista])

    contexto = {
        'data': datetime.now().strftime('%d/%m/%Y'),
        'profissional': dados_rel.get('profissional', 'N/A'),
        'id': dados_rel.get('id', 'N/A'),
        'trimestre': dados_rel.get('trimestre', 'N/A'),

        'classificacao': dados_rel.get('Classificacao', 'N/A'),
        'score': dados_rel.get('Score', 0),
        'conclusao': dados_rel.get('Conclusao', ''),

        'imc': dados_rel.get('IMC', 0),
        'desc_imc': dados_rel.get('Desc_IMC', ''),

        'txt_idade': formatar_lista(grupos_formatados["Idade Materna"]),
        'txt_atual': formatar_lista(grupos_formatados["Tipo de Gestação / Complicações Atuais"]),
        'txt_cronicas': formatar_lista(grupos_formatados["Doenças Crônicas"]),
        'txt_obstetrico': formatar_lista(grupos_formatados["Histórico Obstétrico"]),
        'txt_infecciosas': formatar_lista(grupos_formatados["Condições Infecciosas"]),
        'txt_habitos': formatar_lista(grupos_formatados["Hábitos de Vida / Social"]),
        'txt_outros': formatar_lista(grupos_formatados["Outros"]),
    }

    doc.render(contexto)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

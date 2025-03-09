import streamlit as st
import google.generativeai as genai  

# Configuração do título da página
st.set_page_config(page_title="Assistente de Diagnóstico", page_icon="🩺")

st.title("🔍 Assistente de Diagnóstico")

# Link para gerar a chave API no Google Gemini
st.markdown(
    "[🔑 Clique aqui para obter sua chave API da Google Gemini](https://ai.google.dev/)",
    unsafe_allow_html=True
)

# Chave API
api_key = st.text_input("Digite sua chave da API Gemini:", type="password")

def get_best_model():
    """Escolhe um modelo Gemini compatível e ativo."""
    preferred_models = ["gemini-pro", "gemini 1.5", "gemini-2.0-flash"]  

    try:
        models = genai.list_models()
        available_models = [model.name for model in models]
       
        st.success(f"✅ Modelo selecionado: {model}")
        return model

        st.error("❌ Nenhum modelo compatível disponível. Verifique sua conta no Google Cloud.")
        return None

    except Exception as e:
        st.error(f"❌ Erro ao listar os modelos disponíveis: {e}")
        return None

# Verifica se a chave foi inserida
if api_key:
    st.success("✅ Chave API inserida com sucesso! Agora, preencha os dados do paciente.")

    genai.configure(api_key=api_key)  

    model_name = get_best_model()
    
    if model_name:
        with st.form("diagnostico_form"):
            st.subheader("📋 Dados do Paciente")

            idade = st.number_input("Idade do paciente:", min_value=0, max_value=120, step=1)
            genero = st.selectbox("Gênero:", ["Masculino", "Feminino", "Outro"])
            comorbidades = st.text_input("Comorbidades (ou 'sem comorbidades conhecidas'):") 

            st.subheader("🩺 Queixa Principal e Sintomas")
            queixa_principal = st.text_area("Queixa principal e duração:")
            sintomas = st.text_area("Liste os sintomas associados (separados por vírgula):")
            sinais_vitais = st.text_area("Sinais vitais (se disponíveis):")
            exame_fisico = st.text_area("Achados relevantes no exame físico:")
            exames = st.text_area("Exames laboratoriais ou de imagem (se disponíveis):")

            enviar = st.form_submit_button("🔎 Analisar")

        if enviar:
            prompt = f"""
            Analise a seguinte constelação de sintomas para um possível diagnóstico diferencial:

            Paciente: {idade} anos, {genero}, com {comorbidades}.

            Queixa principal: {queixa_principal}.

            Sintomas associados:
            - {sintomas.replace(',', '\n    - ')}

            Sinais vitais: {sinais_vitais}

            Achados relevantes no exame físico:
            - {exame_fisico}

            Exames laboratoriais ou de imagem (se disponíveis):
            - {exames}

            Por favor:
                1. Liste os diagnósticos diferenciais organizados por PROBABILIDADE, do mais provável ao menos provável, considerando os dados epidemiológicos e a apresentação clínica. Para cada diagnóstico, forneça uma breve justificativa baseada nos sintomas e sinais apresentados.
        
                2. Em seguida, reorganize os mesmos diagnósticos por GRAVIDADE, do mais grave (potencialmente fatal ou com necessidade de intervenção imediata) ao menos grave. Para cada diagnóstico, indique o tempo estimado para intervenção e possíveis complicações caso não seja tratado adequadamente.
        
                3. Sugira os próximos passos diagnósticos mais apropriados para confirmar ou descartar cada uma das hipóteses principais.
        
                4. Indique se há sinais de alarme ou 'red flags' na apresentação que exigiriam atenção imediata ou encaminhamento para emergência.
                """

            try:
                with st.spinner("🧠 Analisando..."):
                    model = genai.GenerativeModel(model_name)  # Usa apenas modelos compatíveis
                    response = model.generate_content(prompt)  

                    resposta = response.text  

                st.subheader("📄 Resultado da Análise:")
                st.markdown(resposta.replace("\n", "\n\n"))  
            
            except Exception as e:
                st.error(f"❌ Erro ao acessar a API Gemini: {e}")

else:
    st.warning("⚠️ Digite sua chave da API para começar.")

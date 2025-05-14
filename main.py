import streamlit as st
from openai import OpenAI
import json
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if "question" not in st.session_state:
    st.session_state.question = ""

if "system" not in st.session_state:
    st.session_state.system = "Você é um analista da qualidade de software senior e está encarregado de formular perguntas para estudantes"

if "html_markdown" not in st.session_state:
    st.session_state.html_markdown = ""

if "tamanho" not in st.session_state:
    st.session_state.tamanho = ""

if "questionario" not in st.session_state:
    st.session_state.questionario = ""

if "numero" not in st.session_state:
    st.session_state.numero = 1

if "imagem" not in st.session_state:
    st.session_state.imagem = ""

if "descricao" not in st.session_state:
    st.session_state.descricao = '''
                                # Tópico Principal
                                ## Subtópico 1
                                 - Ponto 1
                                  - Detalhe 1
                                  - Detalhe 2
                                 - Ponto 2
                                ## Subtópico 2
                                 - Ponto 1
                                 - Ponto 2
                                  - Detalhe 1
                                    - Subdetalhe 1
                                    - Subdetalhe 2
                                ## Subtópico 3
                                 - Ponto 1
                                 - Ponto 2
                                 - Ponto 3
                                ## Conclusão
                                 - Resumo dos tópicos
                                 - Considerações finais
                                '''

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "mindmap" not in st.session_state:
    st.session_state.mindmap = ""

if "conteudo" not in st.session_state:
    st.session_state.conteudo = '''O conteúdo será exibido aqui...'''

if "pergunta" not in st.session_state:
    st.session_state.pergunta = "Insira um assunto no sobre o CTFL para que a questão seja gerada..."

if "explicacao" not in st.session_state:
    st.session_state.explicacao = ""
    

assunto = ""
prompt = ""
system = st.session_state.system
client = OpenAI()

def ask_openai(system, assunto, prompt):
    
    if assunto == "":
        return "Como posso ajudá-lo?"
    try:
        print("Iniciando chat")
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (f"{system}")
                },
                {
                    "role": "user",
                    "content": (f"{prompt}")
                }
            ],

            temperature=1,
            max_tokens=5000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0

            )
        
        answer = completion.choices[0].message.content
        answer = answer.replace("`","").replace("json","") 
        print(f"answer: {answer}")
        return answer
    
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return None

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

with st.expander('Gerador de mindmap', expanded=True):
        #st.write('''
        #        <h2 class="cor">Gerador</h2>
        #        ''',unsafe_allow_html=True)
        with st.form("assunto"):
            assunto = st.text_area("Insira aqui o assunto")
            gerar_conteudo = st.form_submit_button("Gerar conteúdo",use_container_width=True)
            
            if assunto == "" and gerar_conteudo:
                st.warning("Adicione o assunto a ser abordado")
            else:    
                if gerar_conteudo:
                    system = st.session_state.system
                    prompt =f'''
                            Quero aprender sobre o texto abaixo: 
                                    {assunto}
                            Você é um programa que cria mindmaps utilizando o markmap e escreve somente texto em markdown seguindo o exemplo abaixo:
                                
                            Exemplo de input

                                Scenario 1: Yield Value has no FAIL 

                                Given an hourly check value that has no FAIL
                                When the table is rendered,
                                Then values are colored black by default to indicate the Yield is 100%

                                Scenario 2: Yield Value has a FAIL 
                                Given an hourly check value that has at least one FAIL
                                When the table is rendered,
                                Then values are highlighted (rectangular section with rounded corners) with a warning color (e.g., red) to indicate the Yield is less than 100%.

                                Scenario 3: Dropdown Hourly Check

                                Given that I see a dropdown filter is available above the hourly check table
                                When I select the dropdown
                                Then I see the dropdown with "All" selected by default, and the table should display all the data together.

                                Scenario 4: Filtering Yield Values via Dropdown

                                Given that I see a dropdown filter is available above the hourly check table
                                When I select "Failed" from the dropdown

                                Then the table should display only tester lines where there is at least one FAIL (warning/red rows), the tester lines with 100% yield must not be exhibited
                            
                            Exemplo de saida
                                # Raid Tracker  Hourly Check  Add color labels to Hourly Check page 
                                ## Cenário Positivo (Caminho Feliz)
                                ### O usuário acessa a tela de 'hourly check' e visualiza as configurações iniciais.
                                 - Validar que ao usuário iniciar a tela todos os horários serão exibidos inicialmente.
                                 - Validar que ao usuário iniciar a tela os horários que não possuem falhas permanecerão sem cor de fundo e letras pretas.
                                 - Validar que ao usuário iniciar a tela e visualizar um horário que possua 'falhas', a cor do fundo desse horário deverá estar vermelha com letras brancas.
                                 - Validar que ao usuário iniciar a tela, um campo inicialmente vazio de filtro com dropdown será exibido e terá duas opções:
                                  - Opções: 'all' e 'Failed'
                                ### O usuário deseja filtrar um determinado grupo de horários.
                                 - Validar que ao usuário selecionar a opção 'Failed' no menu dropdown do campo de filtro, serão exibidos somente os valores com falhas.
                                 - Validar que ao usuário selecionar a opção 'All' no menu dropdown do campo de filtro, todos os valores sejam exibidos. 
                                ## Caminho Alternativo
                                ### O usuário não consegue visualizar horários
                                 - Validar que se houver um erro no carregamento dos horários, uma mensagem de erro deverá ser exibida ao usuário, informando que os dados não puderam ser carregados.
                            '''
                    
                    st.session_state.descricao = ask_openai(system, assunto, prompt)
                    
                    if assunto != "":
                        
                        system = '''
                                    Você é um desenvolvedor que só responde em através de linguagem markdown.
                                     exemplo = #topico ##Subtopico
                                 '''
                        prompt = f'''
                                    Crie um resumo sobre o assunto abaixo:
                                    assunto = {assunto}
                                  '''
                        st.session_state.conteudo = ask_openai(system, assunto, prompt)
                        
                                
#Componente de mindmap e conteúdo

with st.container(border=True, key="container"):
    with st.expander("Mindmap", expanded=True):
        if st.session_state.conteudo != "":
            st.markdown('''<div class="pergunta2"> O mindmap aparecerá no campo abaixo </div>''',unsafe_allow_html=True)
            st.session_state.html_markdown ='''
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8" />
                            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                            <title>Markmap</title>
                            <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.16"></script>
                            <style>
                            svg.markmap {
                                width: 100%;
                                height: 100vh;
                                background-color: white;
                            }
                            
                            .node{
                                margin: 10px;
                            }
                            
                            #fullscreen-button {
                                position: absolute;
                                top: 10px;
                                right: 10px;
                                padding: 10px;
                                background-color: rgba(207,1,59);
                                color: white;
                                border: none;
                                cursor: pointer;
                                z-index: 1000;
                            }
                            
                            body, html {
                                margin: 0;
                                height: 100%;
                                overflow: hidden;
                            }

                            #mindmap-container {
                                height: calc(100% - 35px);
                                width: 100%;
                                transition: transform 0.3s ease;
                                display: flex;
                                justify-content: center;
                                align-items: center;
                            }
                            
                            </style>
                        </head>
                        <body>
                            <button id="fullscreen-button">Tela cheia</button>
                            <div id="mindmap-container" class="markmap node">
                                <script type="text/template">
                                    ---
                                    markmap:
                                    maxWidth: 400
                                    colorFreezeLevel: 2
                                    ---''' + f'''
                                    {st.session_state.descricao}
                                    ''' + '''
                                    
                                </script>
                            </div>
                        <script>
                            const fullscreenButton = document.getElementById('fullscreen-button');
                            const mindmapContainer = document.getElementById('mindmap-container');
                            
                            function updateButtonLabel() {
                                if (document.fullscreenElement) {
                                    fullscreenButton.textContent = 'Sair da Tela Cheia';
                                } else {
                                    fullscreenButton.textContent = 'Tela Cheia';
                                    mindmapContainer.style.transform = 'none';
                                }
                            }

                            fullscreenButton.addEventListener('click', () => {
                                const elem = document.documentElement;
                                if (!document.fullscreenElement) {
                                    elem.requestFullscreen().catch(err => {
                                        alert(`Error attempting to enable fullscreen mode: ${err.message} (${err.name})`);
                                    });
                                } else {
                                    document.exitFullscreen();
                                }
                            });
                            
                            document.addEventListener('fullscreenchange', updateButtonLabel);
                        </script>
                        </body>
                        </html>
                        '''    
            components.html(st.session_state.html_markdown, height=400)
            #st.markdown(st.session_state.descricao)
            #st.markdown(st.session_state.conteudo)

    
if assunto != "":
    
    conteudo = f"\n\n{st.session_state.conteudo}"
    print("================================================")
    print(f"{conteudo}")
    
    with st.expander("Resumo", expanded=True):
            st.write('''<div class="pergunta2">Resumo do assunto</div>''', unsafe_allow_html=True)
            st.markdown(f'''<div class="resposta">{conteudo}</div>''', unsafe_allow_html=True)

else:        
    with st.expander("Resumo", expanded=True):
            st.markdown('''<div class="pergunta2">Resumo do assunto</div>''', unsafe_allow_html=True)
            st.markdown(f'''<div class="resposta"><p>{st.session_state.conteudo} </p></div>''', unsafe_allow_html=True)
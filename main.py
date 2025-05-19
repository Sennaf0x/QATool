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
    st.session_state.system = "You are a senior software quality analyst and are in charge of formulating questions for students."

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
                                # Main Topic
                                ## Subtopic 1
                                 - Point 1
                                  - Detail 1
                                  - Detail 2
                                 - Point 2
                                ## Subtopic 2
                                 - Point 1
                                 - Point 2
                                  - Detail 1
                                   - Subdetail 1
                                   - Subdetail 2
                                ## Subtopic 3
                                 - Point 1
                                 - Point 2
                                 - Point 3
                                ## Conclusion
                                 - Summary of topics
                                 - Final considerations
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
            titulo = st.input_text("Nome da estória")
            gerar_conteudo = st.form_submit_button("Gerar conteúdo",use_container_width=True)
            
            if assunto == "" or gerar_conteudo or :
                st.warning("Adicione o assunto a ser abordado")
            else:    
                if gerar_conteudo:
                    system = st.session_state.system
                    prompt =f'''
                            I want to learn about the text below:
                                {assunto}
                                You are a program that creates mind maps using markmap and writes only text in markdown following the example below:
                            
                            Definitions
                                The happy path is the ideal interaction flow that a user follows to complete a task or goal without encountering errors, problems, or exceptions. In general, this is the most direct flow and is often the most desired and expected behavior of the system.
                                The alternative path is any interaction flow that deviates from the happy path. This includes scenarios where users may encounter errors, take different actions, or follow alternative decisions throughout the process.

                            Example of input

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
                            
                            Example of output

                                # Raid Tracker  Hourly Check  Add color labels to Hourly Check page 
                                ## Positive scenario (Happy path)
                                ### The user accessed the ‘hourly check’ page and viewed the initial settings.
                                 - Validate that when the user starts the hourly check page, all times will be specified initially.
                                 - Validate that when the user starts the hourly check page, times that do not have errors will remain without a background color and black letters.
                                 - Validate that when the user starts the hourly check page and views a time that has 'errors', the background color of that time should be red with white letters.
                                 - Validate that when the user starts the hourly check page, an initially empty filter field with a drop-down menu will be selected and will have two options:
                                  - Options: 'all' and 'Failure'
                                ### The user wants to filter a specific group of schedules on hourly check page.
                                 - Validate that when the user selects the 'Failed' option in the filter field dropdown menu, only the values ​​with failures will be displayed.
                                 - Validate that when the user selects the 'All' option in the filter field dropdown menu, all values ​​will be displayed.
                                ## Alternative Scenario
                                ### The user cannot view schedules
                                 - Validate that if there is an error loading the schedules, an error message should be displayed to the user, informing that the data could not be loaded.
                                ### The user returns to the main screen
                                 - Validate that when the user clicks the back button, he/she will be redirected to the previous screen
                            '''
                    
                    st.session_state.descricao = ask_openai(system, assunto, prompt)
                    
                    if assunto != "":
                        
                        system = '''
                                    You are a developer who only responds using markdown language. 
                                    Example = #topic ##Subtopic
                                 '''
                        prompt = f'''
                                    Create a summary about the topic below: 
                                    topic = {assunto}
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
                                height: 150vh;
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
                            
                            #exportButton {
                                position: absolute;
                                top: 10px;
                                right: 100px;
                                padding: 10px;
                                background-color: rgba(207,1,59);
                                color: white;
                                border: none;
                                cursor: pointer;
                                z-index: 700;
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
                            <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.16"></script>
                            <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
                        </head>
                        <body>
                            <button id="fullscreen-button">Tela cheia</button>
                            <button id="exportButton">Export as PNG</button>
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

                            document.getElementById('exportButton').addEventListener('click', function() {
                            html2canvas(document.querySelector("#mindmap-container"), {scale: 5}).then(canvas => {
                            var link = document.createElement('a');''' + f'''
                            link.download = 'mindmap.png';''' + '''
                            link.href = canvas.toDataURL();
                            link.click();
                            });
                            });
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
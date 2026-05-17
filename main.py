from argon2.exceptions import VerifyMismatchError
from argon2 import PasswordHasher
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st
import pandas as pd
import pyodbc
import time
import os
import re

load_dotenv()

try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={os.getenv("DB_SERVER")};"
        f"DATABASE={os.getenv("DB_NAME")};"
        f"UID={os.getenv("DB_USER")};"
        f"PWD={os.getenv("DB_PASSWORD")};"
        "Encrypt=yes;TrustServerCertificate=yes;"
    )
except Exception as e:
    st.write(f"Erro ao acessar banco de dados: {e}")
cursor = conn.cursor()

st.set_page_config(
    page_title="Lista de Tarefas",
    page_icon="📝",
    layout="wide"
)

st.markdown("""
            
            <style>
                .stColumn div[direction="column"] {
                    align-items: center;
                    justify-content: center;
                }
                
                .st-key-ContainerLogin div {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                
                .stToastContainer {
                    height: 80%;
                    display: flex;
                    justify-content: flex-end;
                }
            
            </style>
                        
            """, unsafe_allow_html=True)

ph = PasswordHasher()

if "sucessoLogin" not in st.session_state:
    st.session_state["sucessoLogin"] = False

def login():
    if len(st.session_state["loginData"]) == 0:
        st.toast("Preencha os campos vazios!", icon="❌")
    else:
        email = st.session_state["loginData"][0]
        password = st.session_state["loginData"][1]
        query = cursor.execute(f"SELECT ID_USER, username, e_mail, password FROM userdata WHERE e_mail = '{email}'").fetchall()
        
        if len(query) == 0:
            st.toast("E-mail ou senha incorretos!", icon="❌")
        else:
            try:
                verify = ph.verify(query[0][3], password)
                
                st.session_state["loginData"] = [query[0][0], query[0][1], query[0][2], query[0][3]]
                st.session_state["sucessoLogin"] = True if verify else False
            except:
                st.toast("E-mail ou senha incorretos!", icon="❌")
    

verificarLogin = st.session_state["sucessoLogin"]

if verificarLogin:
    st.markdown("""
                
                <style>
                    div[data-baseweb="input"] {
                        background-color: #33c2f600;
                        border: none;
                        border-bottom: 3px solid #262730;
                    }
                    
                    div[data-baseweb="input"] div {
                        background-color: #33c2f600;
                    }
                    
                    .stColumn div[direction="column"] {
                        align-items: center;
                        justify-content: space-around;
                    }
                    
                    .stCheckbox {
                        margin-top: 0rem;
                        margin-bottom: 0rem;
                    }
                    
                    label[data-baseweb="checkbox"] span {
                        margin: 0px;
                    }
                </style>
                
                """, unsafe_allow_html=True)
    
    def createNewTask():
        query = cursor.execute(f"""
                               
                               INSERT INTO task_table (status, task_name, description, initial_date, final_date, ID_USER)
                               VALUES
                               (NULL, NULL, NULL, NULL, NULL, {st.session_state["loginData"][0]})
                               
                               """)
        cursor.commit()
        
        st.toast("Tarefa criada com sucesso!!", icon="✅")
    
    st.title("Lista de Tarefas", text_alignment="center")

    tabela = pd.DataFrame({
        "Nome": ["Gabriel"],
        "Descrição": ["teste"],
        "Data Início": [datetime(2005, 12, 12, 10, 22)],
        "Data Conclusão": ["99/99/9999"],
        "Status": [True],
    })

    tasks = cursor.execute("SELECT ID_TAREFA, status, task_name, description, initial_date, final_date, ID_USER FROM task_table").fetchall()
    
    if len(tasks) == 0:
        with st.container(horizontal_alignment="center"):
            st.markdown("<p style='text-align: center;'>Não há tarefas cadastradas :(</p>", unsafe_allow_html=True)
    else:
        headerColumns = st.columns((1, 2, 2, 2, 2, 1), vertical_alignment="bottom", width=999999)

        with headerColumns[0]:
            st.subheader("Status", text_alignment="center", divider="grey")
        with headerColumns[1]:
            st.subheader("Nome", divider="grey")
        with headerColumns[2]:
            st.subheader("Descrição", divider="grey")
        with headerColumns[3]:
            st.subheader("Data Início", divider="grey")
        with headerColumns[4]:
            st.subheader("Data Final", divider="grey")
        with headerColumns[5]:
            st.subheader("Excluir", divider="grey")

        tableColumn = st.columns((1, 2, 2, 2, 2, 1))
        

        for task in tasks:
            st.session_state[f"taskInitialDate-{task[0]}"] = task[4]
            st.session_state[f"taskFinalDate-{task[0]}"] = task[5]
            
            initialDateSS = st.session_state[f"taskInitialDate-{task[0]}"]
            finalDateSS = st.session_state[f"taskFinalDate-{task[0]}"]
            
            def atualizarCampo(coluna, IDTarefa, IDUser, campo):
                fieldNames = ["status", "task_name", "description", "initial_date", "final_date"]
                novoValorCampo = st.session_state[campo]

                if coluna not in fieldNames:
                    st.error("Campo inválido")
                else:
                    query = f"UPDATE task_table SET {coluna} = ? WHERE ID_TAREFA = ? AND ID_USER = ?"
                    cursor.execute(query, (novoValorCampo, IDTarefa, IDUser))
                    cursor.commit()
            
            
            with tableColumn[0]:
                taskCheckbox = st.checkbox(
                    label=f"status-id{task[0]}",
                    label_visibility="collapsed",
                    value=task[1],
                    args=["status", task[0], task[6], f"task-status-{task[0]}"],
                    key=f"task-status-{task[0]}",
                    on_change=atualizarCampo)


            with tableColumn[1]:
                taskName = st.text_input(
                    label=f"nome-id{task[0]}",
                    label_visibility="collapsed",
                    value=task[2], max_chars=50,
                    args=["task_name", task[0], task[6], f"task_name-{task[0]}"],
                    key=f"task_name-{task[0]}",
                    on_change=atualizarCampo)
                    
                    
            with tableColumn[2]:
                taskDescription = st.text_input(
                    label=f"descricao-id{task[0]}",
                    label_visibility="collapsed",
                    value=task[3], max_chars=100,
                    args=["description", task[0], task[6], f"task-description-{task[0]}"],
                    key=f"task-description-{task[0]}",
                    on_change=atualizarCampo)
                    

            with tableColumn[3]:
                taskInitialDate = st.datetime_input(
                    label=f"datainicio-id{task[0]}",
                    label_visibility="collapsed",
                    format="DD/MM/YYYY", value=task[4],
                    args=["initial_date", task[0], task[6], f"task-initial_date-{task[0]}"],
                    key=f"task-initial_date-{task[0]}",
                    on_change=atualizarCampo)
                
                #if taskInitialDate != None:
                #    if taskInitialDate != initialDateSS:
                #        query = cursor.execute(f"UPDATE task_table SET initial_date = ? WHERE ID_TAREFA = ? AND ID_USER = ?", taskInitialDate, task[0], task[6])
                #        cursor.commit()
                #else:
                #        query = cursor.execute(f"UPDATE task_table SET initial_date = NULL WHERE ID_TAREFA = ? AND ID_USER = ?", task[0], task[6])
                #        cursor.commit()


            with tableColumn[4]:
                taskFinalDate = st.datetime_input(
                    label=f"datafinal-id{task[0]}",
                    label_visibility="collapsed",
                    format="DD/MM/YYYY", value=task[5],
                    args=["final_date", task[0], task[6], f"task-final_date-{task[0]}"],
                    key=f"task-final_date-{task[0]}",
                    on_change=atualizarCampo)

            def deleteTask(IDTarefa, IDUser):
                query = f"DELETE FROM task_table WHERE ID_TAREFA = ? AND ID_USER = ?"
                cursor.execute(query, (IDTarefa, IDUser))
                cursor.commit()
            
            with tableColumn[5]:
                taskTrash = st.button(
                    "🗑️",
                    args=[task[0], task[6]],
                    key=f"lixeira-id{task[0]}",
                    on_click=deleteTask)
        
    with st.container(horizontal_alignment="center"):
        st.button("Criar nova tarefa", on_click=createNewTask)
    
else:    
    if "toogleLoginCad" not in st.session_state:
        st.session_state["toogleLoginCad"] = "cadastro"
    
    def telaDeLogin():
        st.session_state["toogleLoginCad"] = "login"
    
    def telaDeCadastro():
        st.session_state["toogleLoginCad"] = "cadastro"
        
    def cadastrar():
        if len(st.session_state["cadData"]) == 0:
            st.toast("Preencha os campos vazios!", icon="❌")
        else:
            username = st.session_state["cadData"][0]
            email = st.session_state["cadData"][1]
            password = st.session_state["cadData"][2]
            query = cursor.execute(f"SELECT e_mail FROM userdata WHERE e_mail = '{email}'").fetchall()
            emailFormat = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,7}$"
            
            if len(query) != 0 or not re.fullmatch(emailFormat, email):
                st.toast("E-mail inválido", icon="❌")
            else:
                password = ph.hash(password)
                query = cursor.execute(f"INSERT INTO userdata (username, e_mail, password) VALUES ('{username}', '{email}', '{password}')")
                cursor.commit()
                del st.session_state["cadData"]

                st.session_state["toogleLoginCad"] = "login"
                
                st.toast("Cadastro realizado!", icon="✅")

    
    col1, col2, col3 = st.columns((0.7, 1, 0.7))
    with col2:
        st.header("Lista de Tarefas")
        with st.container(border=True):
            if st.session_state["toogleLoginCad"] == "cadastro":
                st.subheader("Cadastro")
                inputUsername = st.text_input(label="username", label_visibility="collapsed", placeholder="Nome e Sobrenome", max_chars=50)
                inputEmail = st.text_input(label="e_mail", label_visibility="collapsed", placeholder="E-mail", max_chars=100)
                inputPassword = st.text_input(label="password", label_visibility="collapsed", placeholder="Senha", type="password", max_chars=50)
                
                if len(inputUsername) != 0 and len(inputEmail) != 0 and len(inputPassword) != 0:
                    st.session_state["cadData"] = [inputUsername, inputEmail, inputPassword]
                else:
                    st.session_state["cadData"] = []
                
                with st.container(key="widgetsContainer", horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
                    st.button("Já tem uma conta?", type="tertiary", on_click=telaDeLogin)
                    st.button("Cadastrar", on_click=cadastrar)
                
                passwordFormat = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#]).{8,}$"
                if inputPassword and not re.fullmatch(passwordFormat, inputPassword):
                    st.warning("A senha deve possuir letras (maiúsculas e minúsculas), números, caracteres especiais e 8 caracteres no mínimo.", icon="⚠️")

            else:
                st.subheader("Login")
                inputEmail = st.text_input(label="e_mail", label_visibility="collapsed", placeholder="E-mail", max_chars=100)
                inputPassword = st.text_input(label="password", label_visibility="collapsed", placeholder="Senha", type="password", max_chars=50)
                
                if len(inputEmail) != 0 and len(inputPassword) != 0:
                    st.session_state["loginData"] = [inputEmail, inputPassword]
                else:
                    st.session_state["loginData"] = []
                
                with st.container(key="widgetsContainer", horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
                    st.button("Não tem uma conta? Cadastre-se", type="tertiary", on_click=telaDeCadastro)
                    st.button("Login", on_click=login)
                
# os.system("cls")
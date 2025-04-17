import streamlit as st
from PIL import Image
import datetime
import requests
import pandas as pd
import json

#---------------------------- Configuración -------------------------
API_BASE = "http://128.0.17.6:3000/data/"

#--------------------------------------------------------------------


#------------------------------- Estados ----------------------------
if "main" not in st.session_state:
    st.session_state.main = True

if "line" not in st.session_state:
    st.session_state.line = 0

if "json_data" not in st.session_state:
    st.session_state.json_data = None

if "date" not in st.session_state:
    st.session_state.date = None

if "time" not in st.session_state:
    st.session_state.time = None

if "post_status_code" not in st.session_state:
    st.session_state.post_status_code = None

if "post_status_text" not in st.session_state:
    st.session_state.post_status_text = None

if "especifica_delete_flag" not in st.session_state:
    st.session_state.especifica_delete_flag = False

#--------------------------------------------------------------------


#----------------------------- Funciones ----------------------------
def init_page():
    if st.session_state.main:
        st.markdown(
            """
            <style>
            /* Color de fondo claro */
            .stApp {La
            .stApp {La
                background-color: #f5f7fa;
            }
            
            /* Estilo para el título */
            .css-10trblm {
                color: #2c3e50;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                margin-bottom: 30px;
            }
            
            /* Estilo para el number input */
            .stNumberInput {
                max-width: 300px;
                margin: 0 auto;
            }
            
            .stNumberInput input {
                background-color: #ffffff;
                border: 1px solid #dfe6e9;
                border-radius: 8px;
                padding: 10px 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            
            /* Estilo para los botones */
            .stButton>button {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 500;
                transition: all 0.3s ease;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            
            .stButton>button:hover {
                background-color: #2980b9;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }
            
            /* Centrar el contenido principal */
            .css-1v0mbdj {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            
            /* Estilo para las columnas */
            .stColumns {
                margin-top: 30px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # Título de la aplicación
        st.markdown(
            """
            <h1 style='text-align: center;'>
                Frontend de Caycho
            </h1>
            """,
            unsafe_allow_html=True
        )

        number = st.number_input(
            "Ingrese el número de linea", 
            value=0, 
            placeholder="Type a number..."
        )

        left, middle, right = st.columns(3)
        # Botón debajo de la caja
        if middle.button("Iniciar", icon="▶️", use_container_width=True):
            st.session_state.line = number
            st.session_state.main = False
            st.rerun()

def sidebar():
    with st.sidebar:
        st.image("nettalco_logo2.png")

        # --- Fecha y hora ---
        st.markdown("---")
        now = datetime.datetime.now()
        st.write(f"**Fecha:** {st.session_state.date}")
        st.write(f"**Hora:** {st.session_state.time}")
        st.markdown("---")

        # --- Botón principal (destacado) ---
        if st.button(
            "🚀 EJECUTAR", 
            key="run",
            type="primary",  # Botón destacado en Streamlit >= 1.27
            use_container_width=True
        ):
            st.sidebar.success("Proceso ejecutado!")
        
        st.markdown("---")
        # --- Botón principal (destacado) ---
        if st.button(
            "⚡ Actualizar", 
            key="actualizar",
            use_container_width=True
        ):
            st.sidebar.success("Proceso ejecutado!")

        # Espacio para separar los botones secundarios
        st.markdown("<br>", unsafe_allow_html=True)  # Salto de línea

        # --- Botones secundarios (estilo menos prominente) ---
        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "📊 Datos", 
                key="data",
                use_container_width=True
            ):
                st.sidebar.info("Cargando datos...")

        with col2:
            if st.button(
                "📈 Gráfico", 
                key="chart",
                use_container_width=True
            ):
                st.sidebar.info("Generando gráfico...")
        
        if st.session_state.post_status_code != None:
            if st.session_state.post_status_code <= 205:
                st.success(st.session_state.post_status_text["message"])
            else:
                st.error(st.session_state.post_status_text["error"])
            st.session_state.post_status_code = None
            st.session_state.post_status_text = None
        



def especifica_buttons():
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "🗑️ Eliminar Específica", 
            key="especifica_delete",
            use_container_width=True
        ):
            #st.session_state.especifica_delete_flag = True
            #print(st.session_state.df_tickets)
            delete_especifica()

    with col2:
        if st.button(
            "✏️ Cambiar Específica", 
            key="especifica_change",
            use_container_width=True
        ):
                st.info("Cambiando Específica..")

def get_json_from_api():
    try:
        url = API_BASE + str(st.session_state.line)
        response = requests.get(url)
        
        response.raise_for_status() 
        
        data_json = response.json()
        
        st.session_state.json_data = data_json

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        data_json = None 

def set_date_time():
    st.session_state.date = st.session_state.json_data["fecha"].split(" ")[0]
    st.session_state.time = st.session_state.json_data["fecha"].split(" ")[1]

def set_dfs():
    df_tickets = pd.DataFrame(st.session_state.json_data["tickets"])
    df_tickets = df_tickets.rename(columns={"ORDEN_COSTURA" : "Orden de Costura", "PAQUETE" : "Paquete", "ESPECIFICA" : "Específica", "ESTILO_NETTALCO" : "Estilo Nettalco", "ESTILO_CLIENTE" : "Estilo Cliente", "TARIFADO" : "Tarifado", "FECHA_DESPACHO" : "Fecha de Despacho"})
    df_tickets = df_tickets[["Orden de Costura", "Paquete", "Específica", "Estilo Nettalco", "Estilo Cliente", "Tarifado", "Fecha de Despacho", "activo"]]
    st.session_state.df_tickets = df_tickets

    df_ordenes_costura = pd.DataFrame(st.session_state.json_data["ordenes_costura"]).T
    df_ordenes_costura = df_ordenes_costura.rename(columns={"id_orden_costura" : "Id", "id_estilo_nettalco" : "Estilo Nettalco", "fecha_despacho" : "Fecha de Despacho", "prioridad" : "Prioridad", "tiempo_estandar" : "Tiempo Estándar"})
    df_ordenes_costura = df_ordenes_costura[["Id", "Estilo Nettalco", "Fecha de Despacho", "Prioridad", "Tiempo Estándar", "activo"]]
    st.session_state.df_ordenes_costura = df_ordenes_costura

    df_estilos_nettalco = pd.DataFrame(st.session_state.json_data["estilos_nettalco"]).T
    df_estilos_nettalco = df_estilos_nettalco.rename(columns={"id_estilo_nettalco" : "Id", "id_tarifado" : "Tarifado", "id_estilo_cliente" : "Estilo Cliente"})
    df_estilos_nettalco = df_estilos_nettalco[["Id", "Tarifado", "Estilo Cliente", "activo"]]
    st.session_state.df_estilos_nettalco = df_estilos_nettalco

    df_estilos_cliente = pd.DataFrame(st.session_state.json_data["estilos_cliente"]).T
    df_estilos_cliente = df_estilos_cliente.rename(columns={"id_estilo_cliente" : "Id"})
    df_estilos_cliente = df_estilos_cliente[["Id", "activo"]]
    st.session_state.df_estilos_cliente = df_estilos_cliente

    df_operadores = pd.DataFrame(st.session_state.json_data["operadores"]).T
    df_operadores = df_operadores.rename(columns={"id_operador" : "Id", "nombre" : "Nombre"})
    df_operadores = df_operadores[["Id", "Nombre", "activo"]]
    st.session_state.df_operadores = df_operadores

    df_paquetes = pd.DataFrame(st.session_state.json_data["paquetes"]).T
    df_paquetes = df_paquetes.rename(columns={"id_paquete" : "Id", "id_orden_costura" : "Orden de Costura", "numero_prendas" : "Número de Prendas"})
    df_paquetes = df_paquetes[["Id", "Orden de Costura", "Número de Prendas", "activo"]]
    st.session_state.df_paquetes = df_paquetes

    df_tarifados = pd.DataFrame(st.session_state.json_data["tarifados"]).T
    df_tarifados = df_tarifados.rename(columns={"id_tarifado" : "Id"})
    df_tarifados = df_tarifados[["Id"]]
    st.session_state.df_tarifados = df_tarifados

    df_especificas = pd.DataFrame(st.session_state.json_data["especificas"]).T
    df_especificas = df_especificas.rename(columns={"id_especifica" : "Id", "descripcion" : "Descripción", "tiempo_estandar" : "Tiempo Estándar"})
    df_especificas = df_especificas[["Id", "Descripción", "Tiempo Estándar", "activo"]]
    st.session_state.df_especificas = df_especificas

    df_operador_especifica = pd.DataFrame(st.session_state.json_data["operador_especifica"])
    df_operador_especifica = df_operador_especifica.rename(columns={"id_operador" : "Operador", "id_especifica" : "Específica", "eficiencia" : "Eficiencia"})
    df_operador_especifica = df_operador_especifica[["Operador", "Específica", "Eficiencia", "activo"]]
    st.session_state.df_operador_especifica = df_operador_especifica

    # df_tarifado_especifica_siguiente = pd.DataFrame(st.session_state.json_data["tarifado_especifica_siguiente"])
    # df_tarifado_especifica_siguiente = df_tarifado_especifica_siguiente.rename(columns={"id_tarifado" : "Tarifado", "id_especifica" : "Específica", "id_especifica_siguiente" : "Específica Siguiente"})
    # df_tarifado_especifica_siguiente = df_tarifado_especifica_siguiente[["Tarifado", "Específica", "Específica Siguiente"]]
    # st.session_state.df_tarifado_especifica_siguiente = df_tarifado_especifica_siguiente

def delete_by_api(url, rows_to_delete):
    for id in rows_to_delete:
        response = requests.delete(url + str(id))
        if response.status_code == 200:
            print("borrado exitosamente")
        else:
            print("error en la llamada")
            #st.error(f"Error al eliminar ID {id}.")
    st.rerun()

def delete_by_api_operator_especifica(url, rows_to_delete):
    print(rows_to_delete)
    for rows in rows_to_delete.iterrows():
        operador = rows[1]["Operador"]
        especifica = rows[1]["Específica"]
        url = url + str(operador) + "/" + str(especifica)
        response = requests.delete(url)
        st.session_state.post_status_code = response.status_code
    # for id in rows_to_delete:
    #     response = requests.delete(url + str(id))
    #     if response.status_code == 200:
    #         print("borrado exitosamente")
    #     else:
    #         print("error en la llamada")
    #         #st.error(f"Error al eliminar ID {id}.")
    # st.rerun()

@st.dialog("Eliminar Específica")
def delete_especifica():
    id_especifica = st.text_input("Id Específica")
    if st.button("Submit"):
        st.session_state.df_tickets.loc[st.session_state.df_tickets["Específica"] == id_especifica, "activo"] = False
        st.rerun()

def post_by_api(url, data):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    st.session_state.post_status_code = response.status_code
    response = json.loads(response.text)
    st.session_state.post_status_text = response

@st.dialog("Agregar Operador")
def add_operator(url_api):
    id = st.text_input("Id")
    name = (st.text_input("Nombre")).upper()
    if st.button("Submit"):
        new_operator = {"id_operador": id, "nombre": name}
        post_by_api(url_api, new_operator)
        st.rerun()

@st.dialog("Agregar Operador - Especifica")
def add_operator_especifica(url_api):
    id_especifica = st.text_input("Id Específica")
    id_operador = (st.text_input("Id Operador")).upper()
    eficiencia = st.text_input("Eficiencia")
    if eficiencia != "":
        eficiencia = float(eficiencia)
    if st.button("Submit"):
        new_operator_especifica = {"id_especifica": id_especifica, "id_operador": id_operador, "eficiencia": eficiencia}
        post_by_api(url_api, new_operator_especifica)
        st.rerun()

def show_tables(line):
    HEIGHT_TABLE = 250
    st.markdown(
        """
        <h2 style='text-align: center;'>
            Tickets
        </h2>
        """,
        unsafe_allow_html=True
    )
    st.dataframe(st.session_state.df_tickets, hide_index=False, use_container_width=True)

    #Aqui falta poner lo de los errores

    st.divider()

    col1, col2 = st.columns([2, 1])
    with col1:
        subcol1, subcol2 = st.columns([6, 1])
        flag_delete_ordenes_costura = False
        with subcol1:
            st.markdown(
                """
                <h3 style='text-align: center;'>
                    Ordenes de Costura
                </h3>
                """,
                unsafe_allow_html=True
            )
        with subcol2:
            if st.button("🔄", help="Eliminar Órdenes de Costura Seleccionadas"):
                flag_delete_ordenes_costura = True
            
        #st.session_state.df_ordenes_costura['Eliminar'] = False
        edited_df_ordenes_costura = st.data_editor(st.session_state.df_ordenes_costura, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["Id", "Estilo Nettalco", "Fecha de Despacho", "Prioridad", "Tiempo Estándar"])

        if flag_delete_ordenes_costura:
            ORDENES_COSTURA_API_DELETE = API_BASE + str(line) + "/ordenes_costura/"
            #rows_to_delete_ordenes_costura = edited_df_ordenes_costura[edited_df_ordenes_costura["Eliminar"] == True]["Id"].tolist()
            #delete_by_api(ORDENES_COSTURA_API_DELETE, rows_to_delete_ordenes_costura)

    with col2:
        subcol1, subcol2 = st.columns([4, 1])
        flag_delete_estilos_nettalco = False
        with subcol1:
            st.markdown(
                """
                <h3 style='text-align: center;'>
                    Estilos Nettalco
                </h3>
                """,
                unsafe_allow_html=True
            )
        with subcol2:
            if st.button("🔄", help="Eliminar Estilos Nettalco Seleccionadas"):
                flag_delete_estilos_nettalco = True
            
        #st.session_state.df_estilos_nettalco['Eliminar'] = False
        edited_df_estilos_nettalco = st.data_editor(st.session_state.df_estilos_nettalco, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["Id", "Tarifado", "Estilo Cliente"])

        if flag_delete_estilos_nettalco:
            ESTILOS_NETTALCO_API_DELETE = API_BASE + str(line) + "/estilos_nettalco/"
            #rows_to_delete_estilos_nettalco = edited_df_estilos_nettalco[edited_df_estilos_nettalco["Eliminar"] == True]["Id"].tolist()
            #delete_by_api(ESTILOS_NETTALCO_API_DELETE, rows_to_delete_estilos_nettalco)
    
    col1, col2, col3 = st.columns([5, 4, 2])
    with col1:
        subcol1, subcol2, subcol3 = st.columns([4, 1, 1])
        flag_delete = False
        with subcol1:
            st.markdown(
                """
                <h3 style='text-align: center;'>
                    Operadores
                </h3>
                """,
                unsafe_allow_html=True
            )
        with subcol2:
            if st.button("➕", help="Agregar operador"):
                OPERATORS_API_POST = API_BASE + str(line) + "/operadores"
                add_operator(OPERATORS_API_POST)

        with subcol3:   
            if st.button("🔄", help="Eliminar Operadores Seleccionados"):
                flag_delete = True
            

        #st.session_state.df_operadores['Eliminar'] = False
        edited_df = st.data_editor(st.session_state.df_operadores, hide_index=True, use_container_width=True, height=HEIGHT_TABLE)

        if flag_delete:
            OPERATORS_API_DELETE = API_BASE + str(line) + "/operadores/"
            #rows_to_delete = edited_df[edited_df["Eliminar"] == True]["Id"].tolist()
            #delete_by_api(OPERATORS_API_DELETE, rows_to_delete)
        
    
    with col2:
        subcol1, subcol2 = st.columns([5, 1])
        flag_delete_paquetes = False
        with subcol1:
            st.markdown(
                """
                <h3 style='text-align: center;'>
                    Paquetes
                </h3>
                """,
                unsafe_allow_html=True
            )
        with subcol2:
            if st.button("🔄", help="Eliminar Paquetes Seleccionados"):
                flag_delete_paquetes = True
            
        #st.session_state.df_paquetes['Eliminar'] = False
        edited_df_paquetes = st.data_editor(st.session_state.df_paquetes, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["Id", "Orden de Costura", "Número de Prendas"])

        if flag_delete_paquetes:
            PAQUETES_API_DELETE = API_BASE + str(line) + "/paquetes/"
            #rows_to_delete_paquetes = edited_df_paquetes[edited_df_paquetes["Eliminar"] == True]["Id"].tolist()
            #delete_by_api(PAQUETES_API_DELETE, rows_to_delete_paquetes)

    with col3:
        st.markdown(
            """
            <h3 style='text-align: center;'>
                Tarifados
            </h3>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(st.session_state.df_tarifados, hide_index=True, use_container_width=True, height=HEIGHT_TABLE)

    col1, col2, col3 = st.columns([4, 4, 3])
    with col1:
        st.markdown(
            """
            <h3 style='text-align: center;'>
                Específicas
            </h3>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(st.session_state.df_especificas, hide_index=True, use_container_width=True, height=HEIGHT_TABLE)

    with col2:
        subcol1, subcol2, subcol3 = st.columns([4, 1, 1])
        flag_delete_operador_especifica = False
        with subcol1:
            st.markdown(
                """
                <h3 style='text-align: center;'>
                    Operador-Específica
                </h3>
                """,
                unsafe_allow_html=True
            )
        with subcol2:
            if st.button("➕", help="Agregar Estilo Cliente"):
                OPERATORS_API_POST = API_BASE + str(line) + "/operador_especifica"
                add_operator_especifica(OPERATORS_API_POST)
        with subcol3:
            if st.button("🔄", help="Eliminar Operador - Específica Seleccionadas"):
                flag_delete_operador_especifica = True
            
        #st.session_state.df_operador_especifica['Eliminar'] = False
        edited_df_operador_especifica = st.data_editor(st.session_state.df_operador_especifica, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["Id", "Orden de Costura", "Número de Prendas"])

        if flag_delete_operador_especifica:
            operador_especifica_API_DELETE = API_BASE + str(line) + "/operador_especifica/"
            #rows_to_delete_operador_especifica = edited_df_operador_especifica[edited_df_operador_especifica["Eliminar"] == True]
            #delete_by_api_operator_especifica(operador_especifica_API_DELETE, rows_to_delete_operador_especifica)

    with col3:
        subcol1, subcol2 = st.columns([6, 1])
        flag_delete_estilos_cliente = False
        with subcol1:
            st.markdown(
                """
                <h3 style='text-align: center;'>
                    Estilos Cliente
                </h3>
                """,
                unsafe_allow_html=True
            )
        with subcol2:
            if st.button("🔄", help="Eliminar Estilos de Cliente Seleccionados"):
                flag_delete_estilos_cliente = True
            
        #st.session_state.df_estilos_cliente['Eliminar'] = False
        edited_df_estilos_cliente = st.data_editor(st.session_state.df_estilos_cliente, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["Id", "Orden de Costura", "Número de Prendas"])

        if flag_delete_estilos_cliente:
            estilos_cliente_API_DELETE = API_BASE + str(line) + "/estilos_cliente/"
            #rows_to_delete_estilos_cliente = edited_df_estilos_cliente[edited_df_estilos_cliente["Eliminar"] == True]["Id"].tolist()
            #delete_by_api(estilos_cliente_API_DELETE, rows_to_delete_estilos_cliente)

    # with col3:
    #     st.markdown(
    #         """
    #         <h3 style='text-align: center;'>
    #             Tarifado - Específica Siguiente
    #         </h3>
    #         """,
    #         unsafe_allow_html=True
    #     )
    #     st.dataframe(st.session_state.df_tarifado_especifica_siguiente, hide_index=True, use_container_width=True, height=HEIGHT_TABLE)

def make_history():
    st.markdown(
        """
        <h2 style='text-align: center;'>
            Historial de Cambio de Específicas
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("Sin cambios de específicas")
#--------------------------------------------------------------------



#---------------------------- Página Inicial ------------------------
init_page()

#--------------------------------------------------------------------

#---------------------------- Página Principal ----------------------
if st.session_state.main == False:
    # --- Configuración inicial ---
    st.set_page_config(
        page_title="Frontend Caycho",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    with st.spinner("Un momento por favor..."):
        get_json_from_api()
        set_date_time()
        set_dfs()
        

    # --- Imagen circular en el sidebar ---
    sidebar()

    # --- Contenido principal ---
    st.title("Visualización de parámetros")
    especifica_buttons()
    
    show_tables(st.session_state.line)
    
    make_history()


#--------------------------------------------------------------------

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

if "disabled_execute_button" not in st.session_state:
    st.session_state.disabled_execute_button = True

if "disabled_graphic_button" not in st.session_state:
    st.session_state.disabled_graphic_button = True

#--------------------------------------------------------------------


#----------------------------- Funciones ----------------------------
def init_page():
    if st.session_state.main:
        st.markdown(
            """
            <style>
            /* Estilos base que funcionan en ambos modos (light/dark) */
            :root {
                --primary-color: #3498db;
                --primary-hover: #2980b9;
                --text-color: #2c3e50;
                --bg-color: #f5f7fa;
                --input-bg: #ffffff;
                --input-border: #dfe6e9;
                --shadow-sm: 0 2px 4px rgba(0,0,0,0.05);
                --shadow-md: 0 4px 8px rgba(0,0,0,0.15);
            }
            
            /* Ajustes para modo oscuro */
            @media (prefers-color-scheme: dark) {
                :root {
                    --text-color: #f0f0f0;
                    --bg-color: #1a1a1a;
                    --input-bg: #2d2d2d;
                    --input-border: #444;
                }
            }
            
            /* Aplicar estilos según el tema de Streamlit */
            .stApp {
                background-color: var(--bg-color);
            }
            
            /* Estilo para el título */
            .css-10trblm, h1 {
                color: var(--text-color) !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                margin-bottom: 30px;
            }
            
            /* Estilo para los inputs - solución para modo oscuro */
            .stNumberInput, .stTextInput, .stTextArea {
                max-width: 300px;
                margin: 0 auto;
            }
            
            .stNumberInput input, 
            .stTextInput input, 
            .stTextArea textarea {
                background-color: var(--input-bg) !important;
                color: var(--text-color) !important;
                border: 1px solid var(--input-border) !important;
                border-radius: 8px !important;
                padding: 10px 15px !important;
                box-shadow: var(--shadow-sm);
            }
            
            /* Placeholder visible en ambos modos */
            .stNumberInput input::placeholder,
            .stTextInput input::placeholder {
                color: #999 !important;
                opacity: 1 !important;
            }
            
            /* Estilo para los botones */
            .stButton>button {
                background-color: var(--primary-color);
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 12px 24px !important;
                font-weight: 500 !important;
                transition: all 0.3s ease !important;
                box-shadow: var(--shadow-sm);
            }
            
            .stButton>button:hover {
                background-color: var(--primary-hover) !important;
                transform: translateY(-2px) !important;
                box-shadow: var(--shadow-md) !important;
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
            
            /* Efecto moderno para las tarjetas */
            .st-bd, .st-cb {
                border-radius: 12px !important;
                box-shadow: var(--shadow-sm) !important;
                transition: transform 0.2s ease, box-shadow 0.2s ease !important;
            }
            
            .st-bd:hover, .st-cb:hover {
                transform: translateY(-3px) !important;
                box-shadow: 0 6px 12px rgba(0,0,0,0.1) !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # Título de la aplicación
        st.markdown(
            """
            <h1 style='text-align: center;'>
                Planificador de Específicas
            </h1>
            """,
            unsafe_allow_html=True
        )

        number = st.text_input(
            "Ingrese el número de linea", 
            placeholder="Type a number..."
        )

        left, middle, right = st.columns(3)
        # Botón debajo de la caja
        if middle.button("Iniciar", icon="▶️", use_container_width=True):
            with st.spinner("Procesando linea, espere por favor..."):
                st.session_state.line = number
                url = API_BASE + f"{number}/preprocesar"
                requests.get(url)
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
        # st.markdown("---")

        # # --- Botón principal (destacado) ---
        # if st.button(
        #     "⚡ COMPROBAR", 
        #     key="actualizar",
        #     use_container_width=True
        # ):
        #     st.sidebar.success("Proceso ejecutado!")

        # Espacio para separar los botones secundarios
        
        st.markdown("---")

        if len(st.session_state.df_especificas_fuera_tarifado) == 0 and len(st.session_state.df_especificas_sin_operario) == 0:
            st.success("Data ópmita", icon="✅")
            st.session_state.disabled_execute_button = False
        else:
            st.error("Hay errores por corregir", icon="⚠️")

        # --- Botón principal (destacado) ---
        if st.button(
            "🚀 EJECUTAR", 
            key="run",
            type="primary",  # Botón destacado en Streamlit >= 1.27
            disabled=st.session_state.disabled_execute_button,
            use_container_width=True
        ):
            with st.spinner("Ejecutando proceso, espere por favor..."):
                url = f"http://128.0.17.6:3000/ejecutar/{st.session_state.line}"
                requests.get(url)
                st.session_state.disabled_graphic_button = False
                st.sidebar.success("Gant Creado!")

        st.markdown("<br>", unsafe_allow_html=True)  # Salto de línea

        # --- Botones secundarios (estilo menos prominente) ---
        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "📊 Datos", 
                key="data",
                disabled=True,
                use_container_width=True
            ):
                st.sidebar.info("Cargando datos...")

        with col2:
            if st.button(
                "📈 Gráfico", 
                key="chart",
                disabled=st.session_state.disabled_graphic_button,
                use_container_width=True
            ):
                st.sidebar.info("Generando gráfico...")
        
        st.markdown("---")
        
        if st.session_state.post_status_code != None:
            if st.session_state.post_status_code <= 205:
                st.success(st.session_state.post_status_text["message"])
            else:
                st.error(st.session_state.post_status_text["error"])
            st.session_state.post_status_code = None
            st.session_state.post_status_text = None
        
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
    df_tickets = df_tickets.rename(columns={"ORDEN_COSTURA" : "OC", "ESPECIFICA" : "ESPECÍFICA", "DESCRIPCION" : "DESCRIPCIÓN", "ESTILO_NETTALCO" : "ESTILO NETTALCO", "ESTILO_CLIENTE" : "ESTILO CLIENTE", "FECHA_DESPACHO" : "FECHA DESPACHO", "activo" : "ACTIVO"})
    df_tickets = df_tickets[["OC", "PAQUETE", "ESPECÍFICA", "DESCRIPCIÓN", "ESTILO NETTALCO", "ESTILO CLIENTE", "TARIFADO", "FECHA DESPACHO", "ACTIVO"]]
    st.session_state.df_tickets = df_tickets
    st.session_state.df_ticket_especificas = st.session_state.json_data["ticket_especificas"]

    errors = st.session_state.json_data["errores"]
    df_especificas_fuera_tarifado = pd.DataFrame(errors["especificas_fuera_tarifado"])
    df_especificas_sin_operario = df_especificas_fuera_tarifado.rename(columns={"descripcion" : "DESCRIPCIÓN", "id_especifica" : "ESPECÍFICA", "id_estilo_cliente" : "ESTILO CLIENTE", "id_estilo_nettalco" : "ESTILO NETTALCO"})
    #df_especificas_sin_operario = df_especificas_fuera_tarifado[["DESCRIPCIÓN", "ESPECÍFICA", "ESTILO CLIENTE", "ESTILO NETTALCO"]]
    st.session_state.df_especificas_fuera_tarifado = df_especificas_fuera_tarifado

    df_especificas_sin_operario = pd.DataFrame(errors["especificas_sin_operario"])
    df_especificas_sin_operario = df_especificas_sin_operario.rename(columns={"descripcion" : "DESCRIPCIÓN", "id_especifica" : "ESPECÍFICA", "id_estilo_cliente" : "ESTILO CLIENTE", "id_estilo_nettalco" : "ESTILO NETTALCO"})
    #df_especificas_sin_operario = df_especificas_sin_operario[["DESCRIPCIÓN", "ESPECÍFICA", "ESTILO CLIENTE", "ESTILO NETTALCO"]]
    st.session_state.df_especificas_sin_operario = df_especificas_sin_operario

    df_ordenes_costura = pd.DataFrame(st.session_state.json_data["ordenes_costura"]).T
    df_ordenes_costura = df_ordenes_costura.rename(columns={"id_orden_costura" : "OC", "id_estilo_nettalco" : "ESTILO NETTALCO", "fecha_despacho" : "FECHA DESPACHO", "prioridad" : "PRIORIDAD", "tiempo_estandar" : "TIEMPO ESTÁNDAR", "activo" : "ACTIVO"})
    df_ordenes_costura = df_ordenes_costura[["PRIORIDAD", "FECHA DESPACHO", "OC", "ESTILO NETTALCO", "ACTIVO"]]
    st.session_state.df_ordenes_costura = df_ordenes_costura

    df_estilos_nettalco = pd.DataFrame(st.session_state.json_data["estilos_nettalco"]).T
    df_estilos_nettalco = df_estilos_nettalco.rename(columns={"id_estilo_nettalco" : "ESTILO NETTALCO", "id_tarifado" : "TARIFADO", "id_estilo_cliente" : "ESTILO CLIENTE", "activo" : "ACTIVO"})
    df_estilos_nettalco = df_estilos_nettalco[["ESTILO NETTALCO", "TARIFADO", "ESTILO CLIENTE", "ACTIVO"]]
    st.session_state.df_estilos_nettalco = df_estilos_nettalco

    df_estilos_cliente = pd.DataFrame(st.session_state.json_data["estilos_cliente"]).T
    df_estilos_cliente = df_estilos_cliente.rename(columns={"id_estilo_cliente" : "ESTILO CLIENTE", "activo" : "ACTIVO"})
    df_estilos_cliente = df_estilos_cliente[["ESTILO CLIENTE", "ACTIVO"]]
    st.session_state.df_estilos_cliente = df_estilos_cliente

    df_operadores = pd.DataFrame(st.session_state.json_data["operadores"]).T
    df_operadores = df_operadores.rename(columns={"id_operador" : "CÓDIGO", "nombre" : "NOMBRE", "activo" : "ACTIVO"})
    df_operadores = df_operadores[["CÓDIGO", "NOMBRE", "ACTIVO"]]
    st.session_state.df_operadores = df_operadores

    df_paquetes = pd.DataFrame(st.session_state.json_data["paquetes"]).T
    df_paquetes = df_paquetes.rename(columns={"id_paquete" : "OC_PACK", "id_orden_costura" : "OC", "numero_prendas" : "PRENDAS", "activo" : "ACTIVO"})
    df_paquetes = df_paquetes[["OC_PACK", "OC", "PRENDAS", "ACTIVO"]]
    st.session_state.df_paquetes = df_paquetes

    df_tarifados = pd.DataFrame(st.session_state.json_data["tarifados"]).T
    df_tarifados = df_tarifados.rename(columns={"id_tarifado" : "TARIFADO"})
    df_tarifados = df_tarifados[["TARIFADO"]]
    st.session_state.df_tarifados = df_tarifados

    df_especificas = pd.DataFrame(st.session_state.json_data["especificas"]).T
    df_especificas = df_especificas.rename(columns={"id_especifica" : "Id", "descripcion" : "Descripción", "tiempo_estandar" : "Tiempo Estándar"})
    df_especificas = df_especificas[["Id", "Descripción", "Tiempo Estándar"]]
    st.session_state.df_especificas = df_especificas

    df_operador_especifica = pd.DataFrame(st.session_state.json_data["operador_especifica"])
    df_operador_especifica = df_operador_especifica.rename(columns={"id_operador" : "OPERADOR", "nombre" : "NOMBRE", "id_especifica" : "ESPECÍFICA", "descripcion":"DESCRIPCIÓN", "eficiencia" : "EFICIENCIA", "activo" : "ACTIVO"})
    df_operador_especifica["EFICIENCIA"] = (df_operador_especifica["EFICIENCIA"] * 100).round(1).astype(str) + "%"
    df_operador_especifica = df_operador_especifica[["OPERADOR", "NOMBRE", "ESPECÍFICA", "DESCRIPCIÓN" ,"EFICIENCIA", "ACTIVO"]]
    st.session_state.df_operador_especifica = df_operador_especifica

    df_tarifado_especifica_siguiente = pd.DataFrame(st.session_state.json_data["tarifado_especifica_siguiente"])
    df_tarifado_especifica_siguiente = df_tarifado_especifica_siguiente.rename(columns={"id_tarifado" : "Tarifado", "id_especifica" : "Específica", "id_especifica_siguiente" : "Específica Siguiente"})
    df_tarifado_especifica_siguiente = df_tarifado_especifica_siguiente[["Tarifado", "Específica", "Específica Siguiente"]]
    st.session_state.df_tarifado_especifica_siguiente = df_tarifado_especifica_siguiente

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
def delete_especifica(line):
    id_especificas = st.session_state.df_tickets["ESPECÍFICA"].unique()
    #id_especificas = [item["id_especifica"] for item in st.session_state.df_ticket_especificas]
    id_especifica = st.selectbox("Específica", id_especificas)
    if st.button("Eliminar"):
        TICKETS_API_DELETE = API_BASE + str(line) + "/tickets/especificas/eliminar/"
        changed_rows_especifica_delete = st.session_state.df_tickets.loc[st.session_state.df_tickets["ESPECÍFICA"] == id_especifica]
        ids_especifica_delete = changed_rows_especifica_delete["ESPECÍFICA"].tolist()
        actives_especifica_delete = changed_rows_especifica_delete["ACTIVO"].tolist()
        update_active(TICKETS_API_DELETE, ids_especifica_delete, actives_especifica_delete)
        get_errors()
        st.rerun()

@st.dialog("Cambiar Específica de Ticket")
def change_especifica_ticket(line):
    id_especificas = st.session_state.df_tickets["ESPECÍFICA"].unique()
    descriptions = st.session_state.df_tickets["DESCRIPCIÓN"].unique()
    especificas_list = [f"{id_especifica} - {description}" for id_especifica, description in zip(id_especificas, descriptions)]
    old_especifica = st.selectbox("Específica", especificas_list).split(" - ")[0]
    active_especificas = st.session_state.df_especificas
    id_especifica = active_especificas["Id"].tolist()
    descriptions_especificas = active_especificas["Descripción"].tolist()
    especificas_list = []
    for i in range(len(id_especifica)):
        especificas_list.append(id_especifica[i] + " - " + descriptions_especificas[i])
    new_especifica = st.selectbox("Nueva Específica", especificas_list).split(" - ")[0]
    if st.button("Cambiar"):
        TICKETS_API_UPDATE = API_BASE + str(line) + "/tickets/especificas/cambiar/"
        changed_rows_especifica_update = st.session_state.df_tickets.loc[st.session_state.df_tickets["ESPECÍFICA"] == old_especifica]
        ids_especifica_update = changed_rows_especifica_update["ESPECÍFICA"].tolist()
        update_especifica_ticket(TICKETS_API_UPDATE, ids_especifica_update, new_especifica)
        get_errors()
        st.rerun()

@st.dialog("Cambiar Específica")
def change_especifica(line):
    id_especificas = st.session_state.df_especificas["Id"].unique()
    old_especifica = st.selectbox("Específica", id_especificas)
    new_id_especifica = st.text_input("Id de Esepcífica")
    new_description = st.text_input("Descripción")
    new_estandar_time = st.text_input("Tiempo Estándar")
    if st.button("Cambiar"):
        ESPECIFICAS_API_UPDATE = API_BASE + str(line) + "/especificas/"
        changed_especifica_update = st.session_state.df_especificas.loc[st.session_state.df_especificas["Id"] == old_especifica]
        ids_especifica_update = changed_especifica_update["Id"].tolist()[0]
        update_especifica(ESPECIFICAS_API_UPDATE, ids_especifica_update, new_id_especifica, new_description, new_estandar_time)
        get_errors()
        st.rerun()

@st.dialog("Recuperar Específica")
def recovery_especifica(line):
    id_especificas = st.session_state.df_tickets.loc[st.session_state.df_tickets["ACTIVO"] == False, "ESPECÍFICA"].unique()
    id_especifica = st.selectbox("Específica", id_especificas)
    if st.button("Recuperar"):
        TICKETS_API_UPDATE = API_BASE + str(line) + "/tickets/especificas/agregar/"
        changed_rows_especifica_delete = st.session_state.df_tickets.loc[st.session_state.df_tickets["ESPECÍFICA"] == id_especifica]
        ids_especifica_delete = changed_rows_especifica_delete["ESPECÍFICA"].tolist()
        actives_especifica_delete = changed_rows_especifica_delete["ACTIVO"].tolist()
        update_active(TICKETS_API_UPDATE, ids_especifica_delete, actives_especifica_delete)
        get_errors()
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
    codigo = st.text_input("Código")
    if st.button("Agregar"):
        new_operator = {"id_operador": codigo}
        post_by_api(url_api, new_operator)
        get_errors()
        st.rerun()

@st.dialog("Agregar Operador - Especifica")
def add_operator_especifica(url_api):
    active_operators = st.session_state.df_operadores[st.session_state.df_operadores["ACTIVO"] == True]
    id_operators = active_operators["CÓDIGO"].tolist()
    names_operadores = active_operators["NOMBRE"].tolist()
    operators_list = []
    for i in range(len(id_operators)):
        operators_list.append(id_operators[i] + " - " + names_operadores[i])
    id_operator = st.selectbox("OPERADOR", operators_list).split(" - ")[0]
    active_especificas = st.session_state.df_especificas
    id_especifica = active_especificas["Id"].tolist()
    descriptions_especificas = active_especificas["Descripción"].tolist()
    especificas_list = []
    for i in range(len(id_especifica)):
        especificas_list.append(id_especifica[i] + " - " + descriptions_especificas[i])
    id_especifica = st.selectbox("ESPECÍFICA", especificas_list).split(" - ")[0]
    eficiencia = st.text_input("Eficiencia -> poner en porcentaje ejemplo: 71.2%")
    if eficiencia != "":
        eficiencia = float(eficiencia.rstrip('%')) / 100
    if st.button("Agregar"):
        new_operator_especifica = {"id_especifica": id_especifica, "id_operador": id_operator, "eficiencia": eficiencia}
        post_by_api(url_api, new_operator_especifica)
        get_errors()
        st.rerun()

def update_especifica_ticket(url, old_especificas_list, new_especifica):
    if old_especificas_list:
        for old_especifica in old_especificas_list:
            update_url = url + str(old_especifica)
            payload = {
                "id_especifica": new_especifica
            }
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            response = requests.put(update_url, data=json.dumps(payload), headers=headers)
            st.session_state.post_status_code = response.status_code
            st.session_state.post_status_text = response.json()
            get_errors()
    st.rerun()

def update_especifica(url, old_id, new_id, new_description, new_estandar_time):
    if old_id:
        update_url = url + str(old_id)
        payload = {
            "descripcion": new_id,
            "id_especifica": new_description,
            "tiempo_estandar": float(new_estandar_time),
            "activo": True
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.put(update_url, data=json.dumps(payload), headers=headers)
        st.session_state.post_status_code = response.status_code
        st.session_state.post_status_text = response.json()
        get_errors()
    st.rerun()

def update_active(url, ids_list, activates_list):
    if ids_list and activates_list:
        for i in range (0, len(ids_list)):
            id = ids_list[i]
            activate = activates_list[i]
            update_url = url + str(id)
            payload = {
                "activo": activate
            }
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            response = requests.put(update_url, data=json.dumps(payload), headers=headers)
            st.session_state.post_status_code = response.status_code
            st.session_state.post_status_text = response.json()
            get_errors()
    st.rerun()

def update_active_oc(url, ids_list, prioridad, activates_list):
    if ids_list and activates_list:
        for i in range (0, len(ids_list)):
            id = ids_list[i]
            prio = prioridad[i]
            activate = activates_list[i]
            update_url = url + str(id)
            payload = {
                "prioridad": prio,
                "activo": activate
            }
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            response = requests.put(update_url, data=json.dumps(payload), headers=headers)
            st.session_state.post_status_code = response.status_code
            st.session_state.post_status_text = response.json()
            get_errors()
    st.rerun()

def update_active_op_esp(url, ops_ids, esps_ids, eficiencia, activates_list):
    if ops_ids and esps_ids and activates_list:
        for i in range (0, len(ops_ids)):
            operador_id = ops_ids[i]
            especifica_id = esps_ids[i]
            activate = activates_list[i]
            update_url = url + str(operador_id) + "/" + str(especifica_id)
            payload = {
                "eficiencia": eficiencia[i],
                "activo": activate
            }
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            response = requests.put(update_url, data=json.dumps(payload), headers=headers)
            st.session_state.post_status_code = response.status_code
            st.session_state.post_status_text = response.json()
            get_errors()
    st.rerun()

def get_errors():
    url = API_BASE + str(st.session_state.line) + "/errores"
    requests.get(url)

def especifica_buttons(line):
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(
            "🗑️ Eliminar Específica", 
            key="especifica_delete",
            use_container_width=True
        ):
            delete_especifica(line)

    with col2:
        if st.button(
            "✏️ Cambiar Específica", 
            key="especifica_change",
            use_container_width=True
        ):
            change_especifica_ticket(line)

    with col3:
        if st.button(
            "♻️ Recuperar Específica", 
            key="especifica_recovery",
            use_container_width=True
        ):
            recovery_especifica(line)

def write_history():
    print("guardado")

def show_tables(line):
    HEIGHT_TABLE = 250

    col1, col2, col3 = st.columns([3, 4, 2])
    with col1:
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
            if st.button("🔄", help="Refrescar Estilos de Cliente Seleccionados"):
                flag_delete_estilos_cliente = True
            
        #st.session_state.df_estilos_cliente['Eliminar'] = False
        edited_df_estilos_cliente = st.data_editor(st.session_state.df_estilos_cliente, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["ESTILO CLIENTE"])

        if flag_delete_estilos_cliente:
            ESTILOS_CLIENTE_API_UPDATE = API_BASE + str(line) + "/estilos_cliente/"
            changed_rows_estilos_cliente = edited_df_estilos_cliente[edited_df_estilos_cliente["ACTIVO"] != st.session_state.df_estilos_cliente["ACTIVO"]]
            ids_estilos_cliente = changed_rows_estilos_cliente["ESTILO CLIENTE"].tolist()
            actives_estilos_cliente = changed_rows_estilos_cliente["ACTIVO"].tolist()
            update_active(ESTILOS_CLIENTE_API_UPDATE, ids_estilos_cliente, actives_estilos_cliente)

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
            if st.button("🔄", help="Refrescar Estilos Nettalco Seleccionadas"):
                flag_delete_estilos_nettalco = True
            
        #st.session_state.df_estilos_nettalco['Eliminar'] = False
        edited_df_estilos_nettalco = st.data_editor(st.session_state.df_estilos_nettalco, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["ESTILO NETTALCO", "TARIFADO", "ESTILO CLIENTE"])

        if flag_delete_estilos_nettalco:
            ESTILOS_NETTALCO_API_UPDATE = API_BASE + str(line) + "/estilos_nettalco/"
            changed_rows_estilos_nettalco = edited_df_estilos_nettalco[edited_df_estilos_nettalco["ACTIVO"] != st.session_state.df_estilos_nettalco["ACTIVO"]]
            ids_estilos_nettalco = changed_rows_estilos_nettalco["ESTILO NETTALCO"].tolist()
            actives_estilos_nettalco = changed_rows_estilos_nettalco["ACTIVO"].tolist()
            update_active(ESTILOS_NETTALCO_API_UPDATE, ids_estilos_nettalco, actives_estilos_nettalco)

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

    #col1, col2= st.columns(1)
    #with col1:
    subcol1, subcol2, subcol3 = st.columns([8, 1, 1])
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
        if st.button("🔄", help="Refrescar Operadores Seleccionados"):
            flag_delete = True
        

    #st.session_state.df_operadores['Eliminar'] = False
    edited_df = st.data_editor(st.session_state.df_operadores, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["CÓDIGO", "NOMBRE"])

    if flag_delete:
        OPERATORS_API_UPDATE = API_BASE + str(line) + "/operadores/"
        changed_rows = edited_df[edited_df["ACTIVO"] != st.session_state.df_operadores["ACTIVO"]]
        ids_operadores = changed_rows["CÓDIGO"].tolist()
        actives_operadores = changed_rows["ACTIVO"].tolist()
        update_active(OPERATORS_API_UPDATE, ids_operadores, actives_operadores)
        
    
    # with col2:
    #     subcol1, subcol2 = st.columns([5, 2])
    #     with subcol1:
    #         st.markdown(
    #             """
    #             <h3 style='text-align: center;'>
    #                 Un toque
    #             </h3>
    #             """,
    #             unsafe_allow_html=True
    #         )
            
    #     with subcol2:
    #         if st.button("✏️ Cambiar", help="Cambiar Específica"):
    #             change_especifica(line)
    #     st.dataframe(st.session_state.df_especificas, hide_index=True, use_container_width=True, height=HEIGHT_TABLE)

    st.markdown(
        """
        <h2 style='text-align: center;'>
            Específicas
        </h2>
        """,
        unsafe_allow_html=True
    )
    especifica_buttons(st.session_state.line)
    # Agregamos los errores de especificas sin operario en esta tabla operador específica
    complete_df_tickets = st.session_state.df_tickets.copy()

    if not st.session_state.df_especificas_fuera_tarifado.empty:
        new_rows_especifica = st.session_state.df_especificas_fuera_tarifado[["id_especifica"]].drop_duplicates(subset=["id_especifica"]).copy()
        new_rows_especifica["ESPECÍFICA"] = new_rows_especifica["id_especifica"].astype(str) + " ⚠️"

        for col in complete_df_tickets.columns:
            if col not in new_rows_especifica.columns:
                new_rows_especifica[col] = None

        new_rows_especifica = new_rows_especifica[complete_df_tickets.columns]

        complete_df_tickets = pd.concat([new_rows_especifica, complete_df_tickets], ignore_index=True)

    st.dataframe(complete_df_tickets, hide_index=False, use_container_width=True)

    # col1, col2, col3= st.columns([1, 3, 1])
    # with col2:
    subcol1, subcol2, subcol3 = st.columns([8, 1, 1])
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
        if st.button("➕", help="Agregar Operador - Específica"):
            OPERATORS_API_POST = API_BASE + str(line) + "/operador_especifica"
            add_operator_especifica(OPERATORS_API_POST)
    with subcol3:
        if st.button("🔄", help="Refrescar Operador - Específica Seleccionadas"):
            flag_delete_operador_especifica = True
        
    #st.session_state.df_operador_especifica['Eliminar'] = False
    # Agregamos los errores de especificas sin operario en esta tabla operador específica
    complete_operators_especifica = st.session_state.df_operador_especifica.copy()

    if not st.session_state.df_especificas_sin_operario.empty:
        new_rows_operators_especifica = st.session_state.df_especificas_sin_operario[["ESPECÍFICA", "DESCRIPCIÓN"]].drop_duplicates(subset=["ESPECÍFICA"]).copy()
        new_rows_operators_especifica["ESPECÍFICA"] = new_rows_operators_especifica["ESPECÍFICA"].astype(str) + " ⚠️"

        for col in complete_operators_especifica.columns:
            if col not in new_rows_operators_especifica.columns:
                new_rows_operators_especifica[col] = None

        new_rows_operators_especifica = new_rows_operators_especifica[complete_operators_especifica.columns]

        complete_operators_especifica = pd.concat([new_rows_operators_especifica, complete_operators_especifica], ignore_index=True)

    #complete_operators_especifica = pd.concat([complete_operators_especifica, new_rows], ignore_index=True)
    edited_df_operador_especifica = st.data_editor(complete_operators_especifica, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["OPERADOR", "NOMBRE", "ESPECÍFICA", "DESCRIPCIÓN"])

    if flag_delete_operador_especifica:
        OPERADOR_ESPECIFICA_API_UPDATE = API_BASE + str(line) + "/operador_especifica/"
        eficiencia_changed_rows = edited_df_operador_especifica[
            edited_df_operador_especifica["EFICIENCIA"] != st.session_state.df_operador_especifica["EFICIENCIA"]
        ]

        changed_rows_operador_especifica = edited_df_operador_especifica[
            (edited_df_operador_especifica["ACTIVO"] != st.session_state.df_operador_especifica["ACTIVO"]) |
            (edited_df_operador_especifica["EFICIENCIA"] != st.session_state.df_operador_especifica["EFICIENCIA"])
        ]
        # Convert efficiency from percentage string to decimal float
        changed_rows_operador_especifica["EFICIENCIA"] = changed_rows_operador_especifica["EFICIENCIA"].str.rstrip('%').astype(float) / 100
        ids_operador= changed_rows_operador_especifica["OPERADOR"].tolist()
        ids_especificas = changed_rows_operador_especifica["ESPECÍFICA"].tolist()
        eficiencia= changed_rows_operador_especifica["EFICIENCIA"].tolist()
        actives_operador_especifica = changed_rows_operador_especifica["ACTIVO"].tolist()
        update_active_op_esp(OPERADOR_ESPECIFICA_API_UPDATE, ids_operador, ids_especificas, eficiencia, actives_operador_especifica)
        #write_history("Operador-Específica", eficiencia_changed_rows)

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
            if st.button("🔄", help="Refrescar Órdenes de Costura Seleccionadas"):
                flag_delete_ordenes_costura = True
            
        #st.session_state.df_ordenes_costura['Eliminar'] = False
        edited_df_ordenes_costura = st.data_editor(st.session_state.df_ordenes_costura, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["OC", "ESTILO NETTALCO", "FECHA DESPACHO"])

        if flag_delete_ordenes_costura:
            ORDENES_COSTURA_API_UPDATE = API_BASE + str(line) + "/ordenes_costura/"

            prioridad_changed_rows = edited_df_ordenes_costura[
                edited_df_ordenes_costura["PRIORIDAD"] != st.session_state.df_ordenes_costura["PRIORIDAD"]
            ]

            changed_rows_ordenes_costura= edited_df_ordenes_costura[
                (edited_df_ordenes_costura["ACTIVO"] != st.session_state.df_ordenes_costura["ACTIVO"]) |
                (edited_df_ordenes_costura["PRIORIDAD"] != st.session_state.df_ordenes_costura["PRIORIDAD"])
            ]

            # changed_rows_ordenes_costura = edited_df_ordenes_costura[edited_df_ordenes_costura["ACTIVO"] != st.session_state.df_ordenes_costura["ACTIVO"]]
            ids_ordenes_costura = changed_rows_ordenes_costura["OC"].tolist()
            prioridad = changed_rows_ordenes_costura["PRIORIDAD"].tolist()
            actives_ordenes_costura = changed_rows_ordenes_costura["ACTIVO"].tolist()
            update_active_oc(ORDENES_COSTURA_API_UPDATE, ids_ordenes_costura, prioridad, actives_ordenes_costura)

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
            if st.button("🔄", help="Refrescar Paquetes Seleccionados"):
                flag_delete_paquetes = True
            
        #st.session_state.df_paquetes['Eliminar'] = False
        edited_df_paquetes = st.data_editor(st.session_state.df_paquetes, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["OC_PACK", "OC", "PRENDAS"])

        if flag_delete_paquetes:
            PAQUETES_API_UPDATE = API_BASE + str(line) + "/paquetes/"
            changed_rows_paquetes = edited_df_paquetes[edited_df_paquetes["ACTIVO"] != st.session_state.df_paquetes["ACTIVO"]]
            ids_paquetes = changed_rows_paquetes["OC_PACK"].tolist()
            actives_paquetes = changed_rows_paquetes["ACTIVO"].tolist()
            update_active(PAQUETES_API_UPDATE, ids_paquetes, actives_paquetes)

    st.divider()
    # Tablas de errores
    # col1, col2 = st.columns([5, 8])
    # with col1:
    #     st.markdown(
    #         """
    #         <h3 style='text-align: center; color: salmon;'>
    #             Especificas Fuera del Tarifado
    #         </h3>
    #         """,
    #         unsafe_allow_html=True
    #     )
    #     st.dataframe(st.session_state.df_especificas_fuera_tarifado, hide_index=True, use_container_width=True)
    
    # with col2:
    #     st.markdown(
    #         """
    #         <h3 style='text-align: center; color: salmon;'>
    #             Especificas Sin Operario
    #         </h3>
    #         """,
    #         unsafe_allow_html=True
    #     )
    #     st.dataframe(st.session_state.df_especificas_sin_operario, hide_index=True, use_container_width=True)

    # st.divider()

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
            Historial De Cambios
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
        page_title="Configuración de Parámetros",
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
    st.markdown("""
    <style>
    .css-10trblm, h1 {
                color: var(--text-color) !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                margin-bottom: 30px;
            }

    .centered-title {
        text-align: center;
        font-size: 2em !important;
        font-weight: bold;
        margin-bottom: 30px;
    }
    </style>
    <h1 class="centered-title">CONFIGURACIÓN DE PARÁMETROS</h1>
    """, unsafe_allow_html=True)
        
    show_tables(st.session_state.line)
    
    make_history()


#--------------------------------------------------------------------

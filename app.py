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
                Planificador de Específicas
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
            disabled=True,
            use_container_width=True
        ):
            st.sidebar.success("Proceso ejecutado!")
        
        st.markdown("---")
        # --- Botón principal (destacado) ---
        if st.button(
            "⚡ COMPROBAR", 
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
    st.session_state.df_ticket_especificas = st.session_state.json_data["ticket_especificas"]

    errors = st.session_state.json_data["errores"]
    df_especificas_fuera_tarifado = pd.DataFrame(errors["especificas_fuera_tarifado"])
    #df_especificas_fuera_tarifado = df_especificas_fuera_tarifado.rename(columns={"ORDEN_COSTURA" : "Orden de Costura", "PAQUETE" : "Paquete", "ESPECIFICA" : "Específica", "ESTILO_NETTALCO" : "Estilo Nettalco", "ESTILO_CLIENTE" : "Estilo Cliente", "TARIFADO" : "Tarifado", "FECHA_DESPACHO" : "Fecha de Despacho"})
    #df_especificas_fuera_tarifado = df_especificas_fuera_tarifado[["Orden de Costura", "Paquete", "Específica", "Estilo Nettalco", "Estilo Cliente", "Tarifado", "Fecha de Despacho", "activo"]]
    st.session_state.df_especificas_fuera_tarifado = df_especificas_fuera_tarifado

    df_especificas_sin_operario = pd.DataFrame(errors["especificas_sin_operario"])
    #df_especificas_sin_operario = df_especificas_sin_operario.rename(columns={"ORDEN_COSTURA" : "Orden de Costura", "PAQUETE" : "Paquete", "ESPECIFICA" : "Específica", "ESTILO_NETTALCO" : "Estilo Nettalco", "ESTILO_CLIENTE" : "Estilo Cliente", "TARIFADO" : "Tarifado", "FECHA_DESPACHO" : "Fecha de Despacho"})
    #df_especificas_sin_operario = df_especificas_sin_operario[["Orden de Costura", "Paquete", "Específica", "Estilo Nettalco", "Estilo Cliente", "Tarifado", "Fecha de Despacho", "activo"]]
    st.session_state.df_especificas_sin_operario = df_especificas_sin_operario

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
    df_especificas = df_especificas[["Id", "Descripción", "Tiempo Estándar"]]
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
def delete_especifica(line):
    id_especificas = st.session_state.df_tickets["Específica"].unique()
    #id_especificas = [item["id_especifica"] for item in st.session_state.df_ticket_especificas]
    id_especifica = st.selectbox("Específica", id_especificas)
    if st.button("Eliminar"):
        TICKETS_API_DELETE = API_BASE + str(line) + "/tickets/especificas/eliminar/"
        changed_rows_especifica_delete = st.session_state.df_tickets.loc[st.session_state.df_tickets["Específica"] == id_especifica]
        ids_especifica_delete = changed_rows_especifica_delete["Específica"].tolist()
        actives_especifica_delete = changed_rows_especifica_delete["activo"].tolist()
        update_active(TICKETS_API_DELETE, ids_especifica_delete, actives_especifica_delete)
        print(changed_rows_especifica_delete)
        st.rerun()

@st.dialog("Cambiar Específica de Ticket")
def change_especifica_ticket(line):
    id_especificas = st.session_state.df_tickets["Específica"].unique()
    old_especifica = st.selectbox("Específica", id_especificas)
    active_especificas = st.session_state.df_especificas["Id"].tolist()
    new_especifica = st.selectbox("Nueva Específica", active_especificas)
    if st.button("Cambiar"):
        TICKETS_API_UPDATE = API_BASE + str(line) + "/tickets/especificas/cambiar/"
        changed_rows_especifica_update = st.session_state.df_tickets.loc[st.session_state.df_tickets["Específica"] == old_especifica]
        ids_especifica_update = changed_rows_especifica_update["Específica"].tolist()
        update_especifica_ticket(TICKETS_API_UPDATE, ids_especifica_update, new_especifica)
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
        st.rerun()

@st.dialog("Recuperar Específica")
def recovery_especifica(line):
    id_especificas = st.session_state.df_tickets.loc[st.session_state.df_tickets["activo"] == False, "Específica"].unique()
    id_especifica = st.selectbox("Específica", id_especificas)
    if st.button("Recuperar"):
        TICKETS_API_UPDATE = API_BASE + str(line) + "/tickets/especificas/agregar/"
        changed_rows_especifica_delete = st.session_state.df_tickets.loc[st.session_state.df_tickets["Específica"] == id_especifica]
        ids_especifica_delete = changed_rows_especifica_delete["Específica"].tolist()
        actives_especifica_delete = changed_rows_especifica_delete["activo"].tolist()
        update_active(TICKETS_API_UPDATE, ids_especifica_delete, actives_especifica_delete)
        print(changed_rows_especifica_delete)
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
    active_operators = st.session_state.df_operadores[st.session_state.df_operadores["activo"] == True]["Id"].tolist()
    id_operador = st.selectbox("Id Operador", active_operators)
    active_especificas = st.session_state.df_especificas["Id"].tolist()
    id_especifica = st.selectbox("Id Especifica", active_especificas)
    eficiencia = st.text_input("Eficiencia")
    if eficiencia != "":
        eficiencia = float(eficiencia)
    if st.button("Submit"):
        new_operator_especifica = {"id_especifica": id_especifica, "id_operador": id_operador, "eficiencia": eficiencia}
        post_by_api(url_api, new_operator_especifica)
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
    st.rerun()

def update_active(url, ids_list, activates_list):
    print(ids_list)
    if ids_list and activates_list:
        for i in range (0, len(ids_list)):
            print("-------- ", i)
            id = ids_list[i]
            activate = activates_list[i]
            update_url = url + str(id)
            print("id: ", id, " activate: ", activate)
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
    st.rerun()

def update_active_op_esp(url, ops_ids, esps_ids, eficiencia, activates_list):
    print(ops_ids)
    if ops_ids and esps_ids and activates_list:
        for i in range (0, len(ops_ids)):
            print("-------- ", i)
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
    st.rerun()

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
    col1, col2 = st.columns([5, 8])
    with col1:
        st.markdown(
            """
            <h3 style='text-align: center; color: salmon;'>
                Especificas Fuera del Tarifado
            </h3>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(st.session_state.df_especificas_fuera_tarifado, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown(
            """
            <h3 style='text-align: center; color: salmon;'>
                Especificas Sin Operario
            </h3>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(st.session_state.df_especificas_sin_operario, hide_index=True, use_container_width=True)

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
            if st.button("🔄", help="Refrescar Órdenes de Costura Seleccionadas"):
                flag_delete_ordenes_costura = True
            
        #st.session_state.df_ordenes_costura['Eliminar'] = False
        edited_df_ordenes_costura = st.data_editor(st.session_state.df_ordenes_costura, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["Id", "Estilo Nettalco", "Fecha de Despacho", "Prioridad", "Tiempo Estándar"])

        if flag_delete_ordenes_costura:
            ORDENES_COSTURA_API_UPDATE = API_BASE + str(line) + "/ordenes_costura/"
            changed_rows_ordenes_costura = edited_df_ordenes_costura[edited_df_ordenes_costura["activo"] != st.session_state.df_ordenes_costura["activo"]]
            ids_ordenes_costura = changed_rows_ordenes_costura["Id"].tolist()
            actives_ordenes_costura = changed_rows_ordenes_costura["activo"].tolist()
            update_active(ORDENES_COSTURA_API_UPDATE, ids_ordenes_costura, actives_ordenes_costura)

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
        edited_df_estilos_nettalco = st.data_editor(st.session_state.df_estilos_nettalco, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["Id", "Tarifado", "Estilo Cliente"])

        if flag_delete_estilos_nettalco:
            ESTILOS_NETTALCO_API_UPDATE = API_BASE + str(line) + "/estilos_nettalco/"
            changed_rows_estilos_nettalco = edited_df_estilos_nettalco[edited_df_estilos_nettalco["activo"] != st.session_state.df_estilos_nettalco["activo"]]
            ids_estilos_nettalco = changed_rows_estilos_nettalco["Id"].tolist()
            actives_estilos_nettalco = changed_rows_estilos_nettalco["activo"].tolist()
            update_active(ESTILOS_NETTALCO_API_UPDATE, ids_estilos_nettalco, actives_estilos_nettalco)

    
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
            if st.button("🔄", help="Refrescar Operadores Seleccionados"):
                flag_delete = True
            

        #st.session_state.df_operadores['Eliminar'] = False
        edited_df = st.data_editor(st.session_state.df_operadores, hide_index=True, use_container_width=True, height=HEIGHT_TABLE)

        if flag_delete:
            OPERATORS_API_UPDATE = API_BASE + str(line) + "/operadores/"
            changed_rows = edited_df[edited_df["activo"] != st.session_state.df_operadores["activo"]]
            ids_operadores = changed_rows["Id"].tolist()
            actives_operadores = changed_rows["activo"].tolist()
            update_active(OPERATORS_API_UPDATE, ids_operadores, actives_operadores)
        
    
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
        edited_df_paquetes = st.data_editor(st.session_state.df_paquetes, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["Id", "Orden de Costura", "Número de Prendas"])

        if flag_delete_paquetes:
            PAQUETES_API_UPDATE = API_BASE + str(line) + "/paquetes/"
            changed_rows_paquetes = edited_df_paquetes[edited_df_paquetes["activo"] != st.session_state.df_paquetes["activo"]]
            ids_paquetes = changed_rows_paquetes["Id"].tolist()
            actives_paquetes = changed_rows_paquetes["activo"].tolist()
            update_active(PAQUETES_API_UPDATE, ids_paquetes, actives_paquetes)

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
        subcol1, subcol2 = st.columns([5, 2])
        with subcol1:
            st.markdown(
                """
                <h3 style='text-align: center;'>
                    Específicas
                </h3>
                """,
                unsafe_allow_html=True
            )
            
        with subcol2:
            if st.button("✏️ Cambiar", help="Cambiar Específica"):
                change_especifica(line)
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
        edited_df_operador_especifica = st.data_editor(st.session_state.df_operador_especifica, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["Operador", "Específica"])

        if flag_delete_operador_especifica:
            OPERADOR_ESPECIFICA_API_UPDATE = API_BASE + str(line) + "/operador_especifica/"
            eficiencia_changed_rows = edited_df_operador_especifica[
                edited_df_operador_especifica["Eficiencia"] != st.session_state.df_operador_especifica["Eficiencia"]
            ]

            changed_rows_operador_especifica = edited_df_operador_especifica[
                (edited_df_operador_especifica["activo"] != st.session_state.df_operador_especifica["activo"]) |
                (edited_df_operador_especifica["Eficiencia"] != st.session_state.df_operador_especifica["Eficiencia"])
            ]
            ids_operador= changed_rows_operador_especifica["Operador"].tolist()
            ids_especificas = changed_rows_operador_especifica["Específica"].tolist()
            eficiencia= changed_rows_operador_especifica["Eficiencia"].tolist()
            actives_operador_especifica = changed_rows_operador_especifica["activo"].tolist()
            update_active_op_esp(OPERADOR_ESPECIFICA_API_UPDATE, ids_operador, ids_especificas, eficiencia, actives_operador_especifica)
            #write_history("Operador-Específica", eficiencia_changed_rows)

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
            if st.button("🔄", help="Refrescar Estilos de Cliente Seleccionados"):
                flag_delete_estilos_cliente = True
            
        #st.session_state.df_estilos_cliente['Eliminar'] = False
        edited_df_estilos_cliente = st.data_editor(st.session_state.df_estilos_cliente, hide_index=True, use_container_width=True, height=HEIGHT_TABLE, disabled=["Id", "Orden de Costura", "Número de Prendas"])

        if flag_delete_estilos_cliente:
            ESTILOS_CLIENTE_API_UPDATE = API_BASE + str(line) + "/estilos_cliente/"
            changed_rows_estilos_cliente = edited_df_estilos_cliente[edited_df_estilos_cliente["activo"] != st.session_state.df_estilos_cliente["activo"]]
            ids_estilos_cliente = changed_rows_estilos_cliente["Id"].tolist()
            actives_estilos_cliente = changed_rows_estilos_cliente["activo"].tolist()
            update_active(ESTILOS_CLIENTE_API_UPDATE, ids_estilos_cliente, actives_estilos_cliente)

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
    especifica_buttons(st.session_state.line)
    
    show_tables(st.session_state.line)
    
    make_history()


#--------------------------------------------------------------------

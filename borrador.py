import requests
import pandas as pd

try:
    url = "http://128.0.17.6:3000/data/61"
    response = requests.get(url)
    
    response.raise_for_status() 
    
    data_json = response.json()

except requests.exceptions.RequestException as e:
    print(f"Error al conectar con la API: {e}")
    data_json = None 

especificas = data_json["especificas"]

df_especificas = pd.DataFrame(especificas).T

print(df_especificas)
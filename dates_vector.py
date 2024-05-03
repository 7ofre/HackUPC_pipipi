import pandas as pd

# Supongamos que tienes un DataFrame llamado df con dos columnas de fechas llamadas 'fecha_inicio' y 'fecha_fin'
# Asegúrate de que estas columnas estén en el formato datetime

# Ejemplo de DataFrame
#data = {
#    'fecha_inicio': ['2024-01-01', '2024-02-01', '2024-03-01'],
#    'fecha_fin': ['2024-01-05', '2024-02-03', '2024-03-05']
#}

df = pd.read_csv("C:\\Users\\irina\\Downloads\\hackupc-travelperk-dataset.csv")

#df = pd.DataFrame(data)


df['Departure Date'] = pd.to_datetime(df['Departure Date'], dayfirst=True)
df['Return Date'] = pd.to_datetime(df['Return Date'], dayfirst=True)

# Función para generar todas las fechas entre dos fechas dadas
def obtener_fechas_entre(fecha_inicio, fecha_fin):
    return pd.date_range(start=fecha_inicio, end=fecha_fin)

df['Fechas Entre'] = df.apply(lambda x: obtener_fechas_entre(x['Departure Date'], x['Return Date']), axis=1)

# Mostrar el DataFrame resultante
print(df)
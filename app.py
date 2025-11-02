import streamlit as st
from faker import Faker
from datetime import date
from faker_vehicle import VehicleProvider
import pandas as pd
from io import BytesIO
import random

# Inicializar Faker
fake = Faker('es_ES')
fake.add_provider(VehicleProvider)
##fechas de la reparacion
FECHA_INICIO_OBJ = date(2018, 1, 1) # Año, Mes, Día
FECHA_FIN_OBJ = date(2024, 12, 31) # Año, Mes, Día
#ocupaciones especificas
# Define tu lista específica de trabajos de alta cualificación
OCUPACIONES_ESPECIFICAS = [
    'Ingeniero de Sistemas',
    'Abogado Corporativo',
    'Médico Cirujano',
    'Científico de Datos',
    'Arquitecto Principal',
    'Consultor Financiero',
    'Juez',
    'Profesor Universitario',
    'Ingeniero de minas',
    'Administrador'
]
# Diccionario de campos disponibles
Available_fields = {
    'Nombres': fake.name,
    'Dirección': fake.address,
    'Empresa': fake.company,
    'Ocupación': lambda: random.choice(OCUPACIONES_ESPECIFICAS),
    'Auto_reparado': fake.vehicle_make,
    'Fecha_rep': lambda: fake.date_between_dates(
        date_start=FECHA_INICIO_OBJ,
        date_end=FECHA_FIN_OBJ
    ),
    'Monto_Gastado': lambda: fake.pydecimal(
        left_digits=5,   # Máximo 3 dígitos antes del punto (e.g., 999)
        right_digits=2,  # 2 decimales
        min_value=5000,    # Gasto mínimo de 50.00
        max_value=9999    # Gasto máximo de 999.99
    ),
    'Divisa': lambda: 'PEN'

}

# Función para generar datos falsos
def generate_fake_data(fields, num_rows):
    data = {field: [func() for _ in range(num_rows)] for field, func in fields.items()}
    return pd.DataFrame(data)

# Interfaz Streamlit
st.title('Generador de datos de reparación de carros')
st.write('Selecciona los campos que quieres generar y la cantidad de datos')

selected_fields = st.multiselect(
    'Selecciona los campos a agregar:',
    options=list(Available_fields.keys()),
    default=list(Available_fields.keys())
)

num_rows = st.number_input('Cantidad de datos que quieres generar:', min_value=1, max_value=10000, value=100)

if st.button('Generar datos'):
    selected_funcs = {field: Available_fields[field] for field in selected_fields}
    df = generate_fake_data(selected_funcs, num_rows)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        writer.book.use_constant_memory = True
        df.to_excel(writer, index=False)

    output.seek(0)

    st.success('Datos generados con éxito')
    st.write(df)



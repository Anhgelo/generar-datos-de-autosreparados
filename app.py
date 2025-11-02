import streamlit as st
from faker import Faker
from faker_vehicle import VehicleProvider
import pandas as pd
from io import BytesIO

# Inicializar Faker
fake = Faker('es_ES')
fake.add_provider(VehicleProvider)
# Diccionario de campos disponibles
Available_fields = {
    'Nombres': fake.name,
    'Dirección': fake.address,
    'Empresa': fake.company,
    'Ocupación': fake.job,
    'Auto_reparado': fake.vehicle_make,
    'Fecha_rep': fake.date
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

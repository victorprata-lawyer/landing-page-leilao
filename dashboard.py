import streamlit as st
import sqlite3
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Dashboard Assets", page_icon="📊", layout="wide")

@st.cache_resource
def init_connection():
    return sqlite3.connect('assets.db', check_same_thread=False)

@st.cache_data
def get_columns(_conn):
    c = _conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'assets'")
    if not c.fetchone():
        return None
    c.execute("PRAGMA table_info(assets)")
    return [info[1] for info in c.fetchall()]

@st.cache_data
def get_unique_values(_conn, column: str):
    query = f"SELECT DISTINCT `{column}` FROM assets WHERE `{column}` IS NOT NULL ORDER BY `{column}`"
    df = pd.read_sql(query, _conn)
    return sorted(df[column].dropna().unique().tolist())

# Main app
conn = init_connection()
columns = get_columns(conn)

if columns is None:
    st.error("❌ A tabela 'assets' não existe no banco de dados 'assets.db'. Crie a tabela primeiro.")
    st.stop()

st.title("📊 Dashboard de Assets")

# Sidebar for filters
with st.sidebar:
    st.header("🔍 Filtros")
    
    search_term = ""
    if 'processo' in columns:
        search_term = st.text_input("Busca por Processo:")
    
    cidade_filtro = "Todas"
    if 'cidade' in columns:
        cidades = get_unique_values(conn, 'cidade')
        cidade_filtro = st.selectbox("Cidade:", ["Todas"] + cidades)
    
    status_filtro = "Todos"
    if 'status' in columns:
        status_list = get_unique_values(conn, 'status')
        status_filtro = st.selectbox("Status:", ["Todos"] + status_list)
    
    page_size = st.selectbox("Itens por página:", [10, 25, 50, 100], index=1)

# Build dynamic query
params = []
where_clauses = []
if search_term:
    where_clauses.append("processo LIKE ?")
    params.append(f"%{search_term}%")
if cidade_filtro != "Todas":
    where_clauses.append("cidade = ?")
    params.append(cidade_filtro)
if status_filtro != "Todos":
    where_clauses.append("status = ?")
    params.append(status_filtro)

where_str = " AND ".join(where_clauses) if where_clauses else "1=1"
base_query = f"SELECT * FROM assets WHERE {where_str}"

# Total count
count_query = base_query.replace("SELECT *", "SELECT COUNT(*)")
total_rows = pd.read_sql(count_query, conn, params=params).iloc[0, 0]

col1, col2 = st.columns([3, 1])
col1.metric("Total de Registros Filtrados", total_rows)

if total_rows == 0:
    st.info("ℹ️ Nenhum registro encontrado com os filtros aplicados.")
else:
    total_pages = (total_rows + page_size - 1) // page_size
    
    if 'page_num' not in st.session_state:
        st.session_state.page_num = 1
    
    page_num = st.number_input(
        "Página:",
        min_value=1,
        max_value=total_pages,
        value=st.session_state.page_num,
        key="page_selector"
    )
    st.session_state.page_num = page_num
    
    offset = (page_num - 1) * page_size
    paginated_query = f"{base_query} ORDER BY rowid DESC LIMIT {page_size} OFFSET {offset}"
    df = pd.read_sql(paginated_query, conn, params=params)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Export all filtered data
    full_query = f"{base_query} ORDER BY rowid DESC"
    df_full = pd.read_sql(full_query, conn, params=params)
    
    csv_buffer = StringIO()
    df_full.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Exportar CSV (todos os filtrados)",
        data=csv_buffer.getvalue().encode('utf-8'),
        file_name="assets_filtrados.csv",
        mime="text/csv"
    )
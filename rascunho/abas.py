import streamlit as st

st.time_input(
    "Hora Inicial", value=None, key="start_time2",
)


# Inicializando valores no session_state caso ainda não existam
if "start_date" not in st.session_state:
    st.session_state["start_date"] = None
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "end_date" not in st.session_state:
    st.session_state["end_date"] = None
if "end_time" not in st.session_state:
    st.session_state["end_time"] = None
if "option" not in st.session_state:
    st.session_state["option"] = "Opção A"
if "observations" not in st.session_state:
    st.session_state["observations"] = ""

# Criando abas
aba1, aba2 = st.tabs(["Configurações", "Observações"])

with aba1:
    st.header("Configurações de Data e Opções")

    col1, col2 = st.columns(2)

    with col1:
        st.date_input(
            "Data Inicial", value=st.session_state.get("start_date", None), key="start_date"
        )
        st.time_input(
            "Hora Inicial", value=st.session_state.get("start_time", None), key="start_time",
        )

    with col2:
        st.date_input(
            "Data Final", value=st.session_state["end_date"], key="end_date"
        )
        st.time_input(
            "Hora Final", value=st.session_state["end_time"], key="end_time"
        )

    st.radio(
        "Escolha uma opção:", ["Opção A", "Opção B"], index=0 if st.session_state["option"] == "Opção A" else 1, key="option"
    )

with aba2:
    st.header("Observações")

    st.text_area(
        "Digite suas observações:", value=st.session_state["observations"], key="observations"
    )

# Mostrando os valores no Session State (opcional para debug)
st.write("Session State:", st.session_state)

import streamlit as st

def main():
    # Inicializa o estado da aplicação
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'campo1' not in st.session_state:
        st.session_state.campo1 = ""
    if 'campo2' not in st.session_state:
        st.session_state.campo2 = ""
    if 'campo3' not in st.session_state:
        st.session_state.campo3 = ""

    # Funções para navegação entre steps
    def go_to_next_step():
        if st.session_state.current_step == 1:
            st.session_state.campo1 = st.session_state.input_campo1
        elif st.session_state.current_step == 2:
            st.session_state.campo2 = st.session_state.input_campo2
        if st.session_state.current_step < 3:
            st.session_state.current_step += 1

    def go_to_previous_step():
        if st.session_state.current_step == 2:
            st.session_state.campo1 = st.session_state.input_campo1
        elif st.session_state.current_step == 3:
            st.session_state.campo2 = st.session_state.input_campo2
        if st.session_state.current_step > 1:
            st.session_state.current_step -= 1

    # Stepper lógica
    current_step = st.session_state.current_step

    if current_step == 1:
        with st.form(key="form_step_1"):
            st.title("Step 1 de 3")
            st.session_state.input_campo1 = st.text_input("campo 1", value=st.session_state.campo1)
            st.form_submit_button("Salvar")
        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("Próximo"):
                go_to_next_step()

    elif current_step == 2:
        with st.form(key="form_step_2"):
            st.title("Step 2 de 3")
            st.session_state.input_campo2 = st.text_input("campo 2", value=st.session_state.campo2)
            st.form_submit_button("Salvar")
        col1, col2, col3 = st.columns([2, 6, 2])
        with col1:
            if st.button("Anterior"):
                go_to_previous_step()
        with col3:
            if st.button("Próximo"):
                go_to_next_step()

    elif current_step == 3:
        with st.form(key="form_step_3"):
            st.title("Step 3 de 3")
            st.session_state.input_campo3 = st.text_input("campo 3", value=st.session_state.campo3)
            st.form_submit_button("Salvar")
        col1, col2 = st.columns([2, 8])
        with col1:
            if st.button("Anterior"):
                go_to_previous_step()

if __name__ == "__main__":
    main()

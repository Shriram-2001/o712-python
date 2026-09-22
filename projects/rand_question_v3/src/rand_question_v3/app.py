import time

import streamlit as st

from rand_question_v3.selector import random_pair

st.set_page_config(page_title="Random Question Picker", page_icon="?")
st.title("Random Student & Question Picker")
st.caption("Build your lists, then draw a name and a question.")

if "names" not in st.session_state:
    st.session_state.names = []
if "questions" not in st.session_state:
    st.session_state.questions = []
if "drawn_names" not in st.session_state:
    st.session_state.drawn_names = []
if "drawn_questions" not in st.session_state:
    st.session_state.drawn_questions = []

def add_name():
    name = st.session_state.name_input.strip()
    if name:
        st.session_state.names.append(name)
        st.session_state.name_input = ""


def add_question():
    question = st.session_state.question_input.strip()
    if question:
        st.session_state.questions.append(question)
        st.session_state.question_input = ""

name_column, question_column = st.columns(2)
with name_column:
    with st.form("name_form", clear_on_submit=True):
        st.text_input("Name", key="name_input")
        st.form_submit_button("Add name", on_click=add_name, use_container_width=True)
    st.write("Names")
    st.write(st.session_state.names or "No names added yet.")

with question_column:
    with st.form("question_form", clear_on_submit=True):
        st.text_input("Question", key="question_input")
        st.form_submit_button("Add question", on_click=add_question, use_container_width=True)
    st.write("Questions")
    st.write(st.session_state.questions or "No questions added yet.")

no_repeats = st.checkbox("No repeats within this session")
drawn_name_pool = [name for name in st.session_state.names if name not in st.session_state.drawn_names]
drawn_question_pool = [
    question
    for question in st.session_state.questions
    if question not in st.session_state.drawn_questions
]

if st.button("Draw", type="primary", use_container_width=True):
    name_pool = drawn_name_pool if no_repeats else st.session_state.names
    question_pool = drawn_question_pool if no_repeats else st.session_state.questions

    if not name_pool or not question_pool:
        st.warning("Add at least one available name and one available question before drawing.")
    else:
        name, question = random_pair(name_pool, question_pool)
        placeholder = st.empty()
        for _ in range(15):
            flash_name, flash_question = random_pair(name_pool, question_pool)
            placeholder.info(f"{flash_name}\n\n{flash_question}")
            time.sleep(0.2)
        placeholder.success(f"{name}\n\n{question}")
        if no_repeats:
            st.session_state.drawn_names.append(name)
            st.session_state.drawn_questions.append(question)

if st.button("Reset session", use_container_width=True):
    st.session_state.drawn_names = []
    st.session_state.drawn_questions = []
    st.rerun()

import time

import streamlit as st

from rand_question_v3.selector import random_pair


st.set_page_config(page_title="Random Question Picker", page_icon="?")


def initialize_session():
    defaults = {
        "names": [],
        "questions": [],
        "used_names": [],
        "used_questions": [],
        "last_draw": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_name():
    value = st.session_state.name_entry.strip()
    if value:
        st.session_state.names.append(value)


def add_question():
    value = st.session_state.question_entry.strip()
    if value:
        st.session_state.questions.append(value)


def available_values(values, used_values, no_repeats):
    if not no_repeats:
        return values
    return [value for value in values if value not in used_values]


def draw_pair(name_pool, question_pool, no_repeats):
    name, question = random_pair(name_pool, question_pool)
    flash = st.empty()
    for _ in range(20):
        flash_name, flash_question = random_pair(name_pool, question_pool)
        flash.info(f"**{flash_name}**\n\n{flash_question}")
        time.sleep(0.15)
    flash.success(f"**{name}**\n\n{question}")
    st.session_state.last_draw = (name, question)
    if no_repeats:
        st.session_state.used_names.append(name)
        st.session_state.used_questions.append(question)


initialize_session()

st.title("Random Student & Question Picker")
st.write("Add names and questions, then draw a pair.")

name_column, question_column = st.columns(2)
with name_column:
    st.subheader("Names")
    with st.form("add_name_form", clear_on_submit=True):
        st.text_input("Name", key="name_entry")
        st.form_submit_button("Add", on_click=add_name, use_container_width=True)
    if st.session_state.names:
        st.markdown("\n".join(f"- {name}" for name in st.session_state.names))
    else:
        st.caption("No names added yet.")

with question_column:
    st.subheader("Questions")
    with st.form("add_question_form", clear_on_submit=True):
        st.text_input("Question", key="question_entry")
        st.form_submit_button("Add", on_click=add_question, use_container_width=True)
    if st.session_state.questions:
        st.markdown("\n".join(f"- {question}" for question in st.session_state.questions))
    else:
        st.caption("No questions added yet.")

st.divider()
no_repeats = st.checkbox("No repeats within this session")
name_pool = available_values(st.session_state.names, st.session_state.used_names, no_repeats)
question_pool = available_values(
    st.session_state.questions,
    st.session_state.used_questions,
    no_repeats,
)

draw_column, reset_column = st.columns(2)
with draw_column:
    if st.button("Draw", type="primary", use_container_width=True):
        if not name_pool or not question_pool:
            st.warning("Add an available name and question before drawing.")
        else:
            draw_pair(name_pool, question_pool, no_repeats)

with reset_column:
    if st.button("Reset session", use_container_width=True):
        st.session_state.used_names = []
        st.session_state.used_questions = []
        st.session_state.last_draw = None
        st.rerun()

if st.session_state.last_draw:
    name, question = st.session_state.last_draw
    st.subheader("Latest draw")
    st.success(f"**{name}**\n\n{question}")

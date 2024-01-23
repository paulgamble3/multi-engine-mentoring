import streamlit as st 
import pandas as pd
import ast
from firebase.firebase_utils import write_task_item

# wide
st.set_page_config(layout="wide")


data_fn = "mmem_1_17.csv"
DATASET = pd.read_csv(data_fn)

def process_conv(conv):
    conv = conv.split("[/INST]")
    conv = [c.split("[INST]") for c in conv]
    conv = [item for sublist in conv for item in sublist]

    conv_string = "\n\n".join(conv)
    conv_string = conv_string.replace("Patient:", "\n\nPatient:")
    conv_string = conv_string.replace("Nurse:", "\n\nNurse:")
    conv_string = conv_string.replace("[T", "\n\n**[T")
    conv_string = conv_string.replace("]", "]**")

    return conv_string

def sample_data_row(DATASET):
    row = DATASET.sample(n=1).iloc[0]
    PREAMBLE = row['checklist']
    RAW_TASKS = ast.literal_eval(row['tasks'])
    RAW_TASKS = sorted(RAW_TASKS, key=lambda k: k['pointer'])

    CONV = row['instruction']
    CONV = CONV.split('<</SYS>>')[-1]
    CONV = process_conv(CONV)

    RESPONSES = []

    # need to handle kickout checklist

    data_obj = {
        'PROMPT_ID': row['prompt_id'],
        'PREAMBLE': PREAMBLE,
        'RAW_TASKS': RAW_TASKS,
        'CONV': CONV
    }

    return data_obj



data_obj = sample_data_row(DATASET)

st.header("Myelin Engine Mentoring")
user_name = st.text_input("Enter your name:")

with st.expander("**Checklist**"):
    #st.subheader("Checklist")
    st.write(data_obj['PREAMBLE'])


col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("Conversation")
        st.write(data_obj['CONV'])

with col2:
    with st.container(border=True):
        st.subheader("Tasks")
        #st.write(TASKS)
        for task in data_obj['RAW_TASKS']:
            with st.container(border=True):
                st.write("**" + task['pointer'] + " " + task['engine'] + "**")
                st.write(task['content'])


with st.form(key='feedback', clear_on_submit=True):
    st.subheader("Feedback")
    #st.write("Please provide feedback on the conversation and tasks. What do you like? What do you not like? What would you change?")

    st.write("**Response 1:**")
    st.write("**Response 2:**")
    preference = st.radio("Which response do you prefer?", ("Response 1", "Response 2"))

    rewrite = st.text_area(label="Write the ideal response:", height=200)

    submitted = st.form_submit_button(label='Submit')

    if submitted:
        #st.write("Thank you for your feedback!")
        write_task_item(
            {
                "user_name": user_name,
                "data_obj": data_obj,
                "preference": preference,
                "rewrite": rewrite
            },
            "multi-engine-mentoring"
        )
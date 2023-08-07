import streamlit as st
import pandas as pd
# import uuid
# from utils.general_utils import load_vector_embeddings

def create_ask_deepy_bot():
    st.header('Q&A HR Chatbot')
    # vector_embeddings = load_vector_embeddings()

    st.markdown("""Hi there! my name is Deepy. I am here to answer any HR related questions you may have.""")
    upload_file = st.file_uploader("Upload CSV", type=['csv','xls','xlsx'], disabled=True)
    if upload_file is not None:
        dataframe = pd.read_csv(upload_file, encoding='latin-1')
        st.write(dataframe)
    # with st.form("user_input"):
    #     user_input = st.text_area("User Input:", key="input", placeholder="Enter your question...")
    #     submit_button = st.form_submit_button('Submit', use_container_width=True, type="primary")
    #     if submit_button:
    #         st.session_state.ext_interaction_id = str(uuid.uuid4())
    #         with st.spinner('Loading result...'):
    #             dc_client.set_tags({Tag.USER_INPUT: user_input, 
    #                                 Tag.USER_ID: 'user@deepchecks.com', 
    #                                 Tag.EXT_INTERACTION_ID: st.session_state.ext_interaction_id})
    #             result = generate_llm_response(user_input, vector_embeddings)
    #         llm_response = f"{result['answer'].replace('SOURCES:', '')}"
    #         st.session_state.llm_response = llm_response
    #         st.session_state.is_annotated = False

    # if user_input:
    #     if len(st.session_state.llm_response) > 0:
    #         st.info(st.session_state.llm_response, icon="🤖")
    #         if not st.session_state.is_annotated:
    #             placeholder_column = st.empty()
    #             columns = placeholder_column.columns(2)
    #             with columns[0]:
    #                 placeholder_good = st.empty()
    #                 good = placeholder_good.button('👍 Good', key='good_btn', use_container_width=True)

    #             with columns[1]:
    #                 placeholder_bad = st.empty()
    #                 bad = placeholder_bad.button('👎 Bad', key='bad_btn', use_container_width=True)

    #             if good or bad:
    #                 st.session_state.is_annotated = True
    #                 placeholder_good.empty()
    #                 placeholder_column.empty()
    #                 placeholder_bad.empty()
    #             if good:
    #                 st.session_state.annotation_message = "Good"
    #                 dc_client.annotate(ext_interaction_id=st.session_state.ext_interaction_id, annotation=AnnotationType.GOOD)
    #             elif bad:
    #                 st.session_state.annotation_message =  "Bad"            
    #                 dc_client.annotate(ext_interaction_id=st.session_state.ext_interaction_id, annotation=AnnotationType.BAD)

    # if not submit_button and st.session_state.is_annotated:
    #     if 'Bad' in st.session_state.annotation_message:
    #         st.button('👎 Bad', use_container_width=True)
    #         if st.session_state.is_annotated:
    #             st.markdown("""<style>
    #                             [data-testid=stVerticalBlock]>div>div>button,
    #                             [data-testid=stVerticalBlock]>div>div>button:hover,
    #                             [data-testid=stVerticalBlock]>div>div>button:active,
    #                             [data-testid=stVerticalBlock]>div>div>button:focus:not(:active) {
    #                                 background-color: #FC636B;
    #                                 border: 1px solid #FC636B;
    #                                 pointer-events: none;
    #                                 color: white;
    #                             }
    #                     </style>""", unsafe_allow_html=True)

    #     else:
    #         st.button('👍 Good', use_container_width=True)
    #         if st.session_state.is_annotated:
    #             st.markdown("""<style>
    #                             [data-testid=stVerticalBlock]>div>div>button,
    #                             [data-testid=stVerticalBlock]>div>div>button:hover,
    #                             [data-testid=stVerticalBlock]>div>div>button:active,
    #                             [data-testid=stVerticalBlock]>div>div>button:focus:not(:active) {
    #                                 background-color: #37A862;
    #                                 border: 1px solid #37A862;
    #                                 color: white;
    #                                 pointer-events: none;
    #                             }
    #                             </style>""", unsafe_allow_html=True)

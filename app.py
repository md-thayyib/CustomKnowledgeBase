import streamlit as st
from dotenv import load_dotenv
import openai
import os
from streamlit_chat import message
from query import generate_response
from ingest import create_vector
import time
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
try:
    if st.session_state["OPENAI_API_KEY"]:
        openai.api_key = st.session_state["OPENAI_API_KEY"]
except:
    pass



def main():
    st.set_page_config(page_title="CustomKnowledgeBase",page_icon=":pen:",layout='wide')
    st.markdown("<h1 style='text-align: center;'>Custom Knowledge Base 📘</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style ='text-align:center;'>Ask anything on documents</h5> ",unsafe_allow_html=True)

    

    # make a path for the files
    saved_path = "data"
    if not os.path.exists(saved_path):
        os.makedirs(saved_path)
    
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
            "2. Upload a pdf📄\n"
            "3. Click Submit\n"
            "4. Then ask any thing💬\n"
        )



        api_key_input = st.text_input(label="Paste your openai api key",
                                       type='password',
                                       placeholder="Paste your OpenAI API key here (sk-...)",
                                       help="You can get your API key from https://platform.openai.com/account/api-keys.",
                                       value=st.session_state.get("OPENAI_API_KEY", "")
                                       )
        
        
        try:
            if api_key_input !="":
                st.session_state['OPENAI_API_KEY'] = api_key_input
                os.environ["OPENAI_API_KEY"] = api_key_input
                openai.api_key = os.environ["OPENAI_API_KEY"]
        except:
            st.error("Key Error")
        # Upload the file
        uploaded_file = st.file_uploader("Choose a pdf file",type="pdf",accept_multiple_files=True)
        submit_data = st.button('Submit')

        
        st.markdown(
            """
            <div style="position: fixed; bottom: 0; width: 100%; text-align: left;">
             <h6 style ='text-align:left;font-size:12px'>Made by <a href = 'https://linkedin.com/in/md-thayyib'>md-thayyib</a> </h6> Contribute
                <a style = 'font-size:12px' href ='https://github.com/md-thayyib/CustomKnowledgeBase'>Github</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    def remove_existing_files(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    success_message = st.empty()
    # To read file as byte
    if uploaded_file is not None:

        # Remove existing files from directories
        try:
            remove_existing_files(saved_path)
        except:
            pass

        for file in uploaded_file:
            bytes_data = file.getvalue()

            #Save uploaded file into data folder
            with open(os.path.join(saved_path,file.name),'wb') as out_file:
                out_file.write(bytes_data)
        if submit_data and api_key_input !="":
            create_vector()
            success_message.success("Vector has been created")
            time.sleep(2)  # Delay for 2 seconds
            success_message.empty()
    

    # Initialise session state variables
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {"role": "system", "content": "You are a helpful assistant."}
    ]
        
    response_container = st.container()
    # container for text box
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            col1, col2 = st.columns([10,1])
            with col1:
                user_input = st.text_input("Hello", key='input',placeholder="Type your question \U0001F4E4",label_visibility="collapsed")
            with col2:
                submit_button = st.form_submit_button(label=':arrow_right:')
    


        if submit_button and user_input:
            output = generate_response(user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)
            #st.session_state['model_name'].append(model_name)
    
    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user1')
                message(st.session_state["generated"][i], key=str(i))

    col1, col2, = st.columns([3,1])


    with col2:
        if st.session_state['generated']:
            clear_button = st.button("Clear chat - Click Twice")
            if clear_button:
                del st.session_state['generated']





if __name__ == "__main__":
    main()

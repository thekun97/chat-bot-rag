import os
import pickle
from pathlib import Path

import openai
import streamlit as st
from llama_index import ServiceContext
from llama_index import SimpleDirectoryReader
from llama_index import VectorStoreIndex
from llama_index.llms import OpenAI
from llama_index.node_parser import (
    UnstructuredElementNodeParser,
)
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.readers.file.flat_reader import FlatReader
from llama_index.retrievers import RecursiveRetriever

from preprocessing_pdf import convert_pdf_to_html


@st.cache_resource(show_spinner=False)
def load_data(file_path, file_name):
    raw_name = file_name.replace('.pdf', '')
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="data", recursive=True)
        docs = reader.load_data()
        convert_pdf_to_html("./data/" + file_name)

        reader = FlatReader()
        file = reader.load_data(Path(f"result/{raw_name}.html"))

        node_parser = UnstructuredElementNodeParser()
        if not os.path.exists(f"{raw_name}.pkl"):
            file_raw_nodes = node_parser.get_nodes_from_documents(file)
            pickle.dump(file_raw_nodes, open(f"{raw_name}.pkl", "wb"))
        else:
            file_raw_nodes = pickle.load(open(f"{raw_name}.pkl", "wb"))

        base_nodes, node_mappings = node_parser.get_base_nodes_and_mappings(
            file_raw_nodes
        )

        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4-1106-vision-preview"))

        vector_index = VectorStoreIndex(base_nodes)
        vector_retriever = vector_index.as_retriever(similarity_top_k=3)
        recursive_retriever = RecursiveRetriever(
            "vector",
            retriever_dict={"vector": vector_retriever},
            node_dict=node_mappings,
            verbose=True,
        )
        query_engine = RetrieverQueryEngine.from_args(recursive_retriever, service_context=service_context)
        return query_engine


def main():
    st.set_page_config(page_title="Chat with your document",
                       page_icon="💬", layout="centered", initial_sidebar_state="auto", menu_items=None)

    openai.api_key = ""
    st.title("Chat with your document 💬")

    if "messages" not in st.session_state.keys():
        # Initialize the chat messages history
        st.session_state.messages = [
            {"role": "assistant", "content": "Hãy hỏi tôi !"}
        ]

    with st.sidebar:
        st.subheader("Your documents")
        uploaded_file = st.file_uploader(
            "Upload your PDF documents here and click on 'Process'", accept_multiple_files=True)
        if uploaded_file:
            save_path = save_file_locally(uploaded_file[0])
        if st.button("Process"):
            with st.spinner("Loading and indexing your docs – hang tight! This should take 1-2 minutes."):
                if uploaded_file is not None:
                    # index = load_data(save_path, uploaded_file[0].name)
                    query_engine = load_data(save_path, uploaded_file[0].name)

                    if "chat_engine" not in st.session_state.keys():
                        # Initialize the chat engine
                        st.session_state.query_engine = query_engine
                        # st.session_state.chat_engine = index.as_chat_engine(chat_mode="openai", verbose=True)

    if prompt := st.chat_input("Your question"):
        # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # response = st.session_state.chat_engine.chat(prompt)
                response = st.session_state.query_engine.query(prompt)
                str_response = str(response)
                st.write(str_response)
                message = {"role": "assistant", "content": str_response}
                st.session_state.messages.append(message)
                # Add response to message history


if __name__ == '__main__':
    main()

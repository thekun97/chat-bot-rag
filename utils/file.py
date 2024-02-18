import os
from llama_index.node_parser import SimpleNodeParser
from llama_index import SimpleDirectoryReader
from .conn import init_mongo
from llama_index.storage.docstore import MongoDocumentStore
from llama_index.storage.index_store import MongoIndexStore
from llama_index.storage.storage_context import StorageContext
from llama_index import (
    LLMPredictor,
    GPTVectorStoreIndex,
    GPTListIndex,
    GPTSimpleKeywordTableIndex,
    download_loader
)


def save_file_locally(uploaded_file, partner):
    save_folder = f"data/{partner}"
    os.makedirs(save_folder, exist_ok=True)
    filename = uploaded_file.name
    save_path = os.path.join(save_folder, filename)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return save_folder


async def indexing_to_mongo(partner_path):
    reader = SimpleDirectoryReader(input_dir=partner_path, recursive=True)
    docs = reader.load_data()
    nodes = SimpleNodeParser().get_nodes_from_documents(docs)

    # mongo_client, mongo_db = await init_mongo()

    storage_context = StorageContext.from_defaults(
        docstore=MongoDocumentStore.from_uri(uri=os.getenv("MONGO_URL"), db_name=os.getenv("MONGO_DBNAME")),
        index_store=MongoIndexStore.from_uri(uri=os.getenv("MONGO_URL"), db_name=os.getenv("MONGO_DBNAME")),
    )

    vector_index = GPTVectorStoreIndex(nodes, storage_context=storage_context)

    vector_response = vector_index.as_query_engine().query("APS khuyến nghị MUA cổ phiếu MBB với giá mục tiêu bao nhiêu ?")
    return vector_response

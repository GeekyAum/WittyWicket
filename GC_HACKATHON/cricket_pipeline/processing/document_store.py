from pathway.xpacks.llm.document_store import DocumentStore

class DocumentStoreManager:
    def __init__(self, parsed_data):
        self.parsed_data = parsed_data

    def setup_document_store(self):
        # Create and run the document store server.
        document_store = DocumentStore(
            documents=self.parsed_data,
            reference_id_col="doc_id",
            text_col="parsed_content.text",
            metadata_col=self.parsed_data.metadata,
        )
        document_store.run_server(
            host="0.0.0.0",
            port=8765,
            storage_backend="rocksdb",
            storage_path="./document_store"
        )

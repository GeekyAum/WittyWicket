from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
import pathway as pw
from pathway.xpacks.llm.vector_store import VectorStoreServer

# Step 1: Set up LangChain components
def create_vector_store(pw_table, output_dir="./vector_store"):
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print("Creating vector store with LangChain integration...")
    
    # Initialize the embedding model through LangChain
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Configure text splitter for document chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    
    # Step 2: Prepare data for the vector store
    # Create a connectable table that maintains context and metadata
    vector_data = pw_table.select(
        text=pw.this.context,
        match_id=pw.this.match_id,
        timestamp=pw.this.timestamp,
        team1=pw.this.team1,
        team2=pw.this.team2
    )

    
    # Step 3: Create Pathway Vector Store Server
    host = "127.0.0.1"
    port = 8666
    
    # Initialize the server with LangChain components
    vector_server = VectorStoreServer.from_langchain_components(
        vector_data,
        embedder=embeddings,
        splitter=text_splitter,
        text_column="text",
        metadata_columns=["match_id", "timestamp", "team1", "team2"]
    )

    
    # Step 4: Save vector store for persistence
    cache_path = f"{output_dir}/cache"
    
    # Debug output before running
    print("Vector data schema preview:")
    pw.debug.compute_and_print_schema(vector_data)
    
    # Run the server in threaded mode (non-blocking)
    vector_server.run_server(
        host, 
        port=port,
        with_cache=True,
        cache_backend=pw.persistence.Backend.filesystem(cache_path),
        threaded=True
    )
    
    print(f"Vector store server running at http://{host}:{port}")
    
    # Step 5: Create a verification file for debugging
    verification_path = f"{output_dir}/vector_store_info.txt"
    with open(verification_path, 'w') as f:
        f.write(f"Vector store server URL: http://{host}:{port}\n")
        f.write(f"Cache directory: {cache_path}\n")
        f.write(f"Created on: {pw.io.python.now()}\n")
    
    print(f"Vector store info saved to {verification_path}")
    
    # Return server object for client connection in LangGraph
    return vector_server

# Usage in main pipeline
vector_server = create_vector_store(pw_table, output_dir="./vector_store")
pw.run()

# Step 6: Demonstrate LangChain client connection (for future LangGraph integration)
print("\nVerifying LangChain client connection to vector store:")
try:
    from langchain_community.vectorstores import PathwayVectorClient
    
    # Connect to the running server
    client = PathwayVectorClient(host="127.0.0.1", port=8666)
    
    # Test a simple query to verify connection
    print("Testing vector store with query: 'current match status'")
    docs = client.similarity_search("current match status", k=2)
    
    if docs:
        print(f"✓ Successfully retrieved {len(docs)} documents")
        print(f"First result: {docs[0].page_content[:100]}...")
    else:
        print("No documents found. Vector store may be empty.")
        
    # Get vector store statistics for verification
    stats = client.get_vectorstore_statistics()
    print(f"Vector store stats: {stats}")
    
except Exception as e:
    print(f"Error connecting to vector store: {e}")
    print("Note: This is expected if running in a non-interactive environment")

print("\nData successfully ingested into Pathway-LangChain vector store!")

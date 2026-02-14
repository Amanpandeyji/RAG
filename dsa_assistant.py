"""
Beginner-Friendly DSA Assistant using RAG with Groq API
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

class DSAAssistant:
    def __init__(self, notes_file="dsa_notes.txt"):
        """Initialize the DSA Assistant with RAG capabilities"""
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Initialize Groq LLM
        self.llm = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name="llama-3.3-70b-versatile",  # Updated to currently supported model
            temperature=0  # Deterministic responses, no creativity
        )
        
        # Load and process DSA notes
        self.vectorstore = self._create_vectorstore(notes_file)
        
        # Create the RAG chain
        self.qa_chain = self._create_qa_chain()
    
    def _load_documents(self, file_path):
        """Load DSA notes from file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Notes file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    
    def _create_vectorstore(self, notes_file):
        """Create vector store from DSA notes"""
        print("📚 Loading DSA notes...")
        
        # Load the notes
        notes_content = self._load_documents(notes_file)
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""]
        )
        
        texts = text_splitter.split_text(notes_content)
        
        print(f"✂️  Split notes into {len(texts)} chunks")
        
        # Create embeddings (using free HuggingFace embeddings)
        print("🔢 Creating embeddings...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Create vector store
        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        
        print("✅ Vector store created successfully!")
        return vectorstore
    
    def _create_qa_chain(self):
        """Create the RAG QA chain with custom prompt"""
        
        # Custom prompt template following the user's rules
        template = """You are a beginner-friendly Data Structures and Algorithms (DSA) assistant
built using a Retrieval-Augmented Generation (RAG) model.

Your job is to help students understand DSA problems using ONLY the
information provided in the retrieved context.

Rules:
1. Use ONLY the given context.
2. Do NOT assume the student knows advanced concepts.
3. Explain in simple words.
4. If the answer is not in the context, say:
   "This information is not available in the provided notes."
5. Do NOT invent algorithms or shortcuts.
6. Follow the same language and examples from the context.

Context:
{context}

User Question:
{question}

Answer:"""

        prompt = ChatPromptTemplate.from_template(template)
        
        # Create retriever
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 3}  # Retrieve top 3 most relevant chunks
        )
        
        # Create the chain
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return rag_chain, retriever
    
    def ask(self, question):
        """Ask a question and get an answer"""
        print(f"\n❓ Question: {question}\n")
        print("🔍 Searching through DSA notes...")
        
        # Get answer from RAG chain
        rag_chain, retriever = self.qa_chain
        answer = rag_chain.invoke(question)
        source_docs = retriever.invoke(question)  # Updated method
        
        print(f"\n💡 Answer:\n{answer}\n")
        
        # Show which parts of notes were used
        if source_docs:
            print(f"📖 Retrieved {len(source_docs)} relevant sections from notes")
        
        return answer, source_docs
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("\n" + "="*60)
        print("🎓 Welcome to the DSA Learning Assistant!")
        print("="*60)
        print("\nI'm here to help you understand Data Structures and Algorithms.")
        print("Ask me anything about DSA concepts, and I'll explain in simple terms.")
        print("\nType 'exit' or 'quit' to end the session.\n")
        
        while True:
            try:
                question = input("Your question: ").strip()
                
                if question.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Happy learning! Goodbye!")
                    break
                
                if not question:
                    print("Please enter a question.\n")
                    continue
                
                self.ask(question)
                print("\n" + "-"*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Happy learning! Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")


def main():
    """Main function to run the DSA assistant"""
    try:
        # Initialize the assistant
        assistant = DSAAssistant()
        
        # Run in interactive mode
        assistant.interactive_mode()
        
    except Exception as e:
        print(f"❌ Error initializing assistant: {str(e)}")
        print("\nMake sure you have:")
        print("1. Installed all requirements: pip install -r requirements.txt")
        print("2. Created .env file with GROQ_API_KEY")
        print("3. Added dsa_notes.txt file")


if __name__ == "__main__":
    main()

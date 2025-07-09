import os
import tempfile
from typing import List, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
from PyPDF2 import PdfReader
import streamlit as st

class RAGEngine:
    """Engine de Recuperação e Geração Aumentada para EscritaComCiencia"""
    
    def __init__(self):
        """Inicializa o engine RAG"""
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.chain = None
        self.memory = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Inicializa os componentes do RAG"""
        try:
            # Configurar embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            
            # Configurar LLM (Google Gemini)
            google_api_key = os.getenv('GOOGLE_API_KEY')
            if not google_api_key:
                # Tentar obter da configuração do Streamlit
                try:
                    google_api_key = st.secrets.get("GOOGLE_API_KEY")
                except:
                    pass
            
            if google_api_key:
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash-exp",
                    google_api_key=google_api_key,
                    temperature=0.3,
                    convert_system_message_to_human=True
                )
            else:
                st.warning("⚠️ Chave da API do Google não encontrada. Configure GOOGLE_API_KEY.")
                return
            
            # Configurar memória
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
            
        except Exception as e:
            st.error(f"Erro ao inicializar componentes: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extrai texto de um arquivo PDF"""
        try:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Erro ao extrair texto do PDF: {str(e)}")
            return ""
    
    def split_text(self, text: str) -> List[Document]:
        """Divide o texto em chunks menores"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        
        chunks = text_splitter.split_text(text)
        documents = [Document(page_content=chunk) for chunk in chunks]
        return documents
    
    def create_vectorstore(self, documents: List[Document]) -> bool:
        """Cria o vectorstore a partir dos documentos"""
        try:
            if not self.embeddings:
                st.error("Embeddings não inicializados")
                return False
            
            self.vectorstore = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            return True
        except Exception as e:
            st.error(f"Erro ao criar vectorstore: {str(e)}")
            return False
    
    def setup_chain(self):
        """Configura a cadeia de conversação"""
        try:
            if not self.vectorstore or not self.llm or not self.memory:
                st.error("Componentes não inicializados")
                return False
            
            retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5}  # Aumentar para buscar mais contexto
            )
            
            # Prompt personalizado para o sistema
            from langchain.prompts import PromptTemplate
            
            custom_prompt = PromptTemplate(
                input_variables=["context", "question"],
                template="""
                Você é um assistente especializado no livro "Português Funcional" de Marcos Rogério Martins Costa e Iara da Silva Bezerra.
                
                INSTRUÇÕES CRÍTICAS:
                
                1. 🔍 ANÁLISE OBRIGATÓRIA: Examine cuidadosamente o contexto fornecido abaixo antes de responder.
                
                2. 📖 CONTEÚDO DISPONÍVEL: Use as informações do contexto que incluem:
                   - Gramática da língua portuguesa (orações subordinadas, concordância, regência)
                   - Técnicas de leitura e interpretação
                   - Estratégias de escrita e comunicação
                   - Exemplos práticos e exercícios
                
                3. ✅ QUANDO ENCONTRAR INFORMAÇÕES NO CONTEXTO:
                   - Use SEMPRE o conteúdo como base principal
                   - Cite exemplos e explicações encontradas
                   - Mantenha linguagem didática e clara
                   - Forneça definições completas
                
                4. 🎯 PARA TEMAS GRAMATICAIS (como orações subordinadas):
                   - Procure definições, classificações e exemplos no contexto
                   - Identifique regras e aplicações práticas
                   - Explique de forma educativa e acessível
                
                5. 📚 ESTRUTURA DA RESPOSTA:
                   - Comece com definição clara do conceito
                   - Inclua classificações quando relevantes
                   - Forneça exemplos práticos
                   - Use tom educativo dos autores
                
                6. ❌ NUNCA responda apenas "Não" ou "Não há informações":
                   - Sempre tente extrair informações relevantes do contexto
                   - Se o contexto for limitado, use o que estiver disponível
                   - Construa uma resposta educativa mesmo com informações parciais
                
                CONTEXTO DO LIVRO:
                {context}
                
                PERGUNTA: {question}
                
                Responda de forma completa e educativa com base no contexto fornecido:
                """
            )
            
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                memory=self.memory,
                return_source_documents=True,
                combine_docs_chain_kwargs={"prompt": custom_prompt},
                verbose=False
            )
            return True
        except Exception as e:
            st.error(f"Erro ao configurar cadeia: {str(e)}")
            return False
    
    def process_documents(self, pdf_files) -> bool:
        """Processa documentos PDF e cria o vectorstore"""
        try:
            all_documents = []
            
            for pdf_file in pdf_files:
                # Extrair texto
                text = self.extract_text_from_pdf(pdf_file)
                if not text.strip():
                    continue
                
                # Dividir em chunks
                documents = self.split_text(text)
                all_documents.extend(documents)
            
            if not all_documents:
                st.error("Nenhum texto foi extraído dos documentos")
                return False
            
            # Criar vectorstore
            if not self.create_vectorstore(all_documents):
                return False
            
            # Configurar cadeia
            if not self.setup_chain():
                return False
            
            return True
            
        except Exception as e:
            st.error(f"Erro ao processar documentos: {str(e)}")
            return False
    
    def get_response(self, question: str) -> str:
        """Gera resposta para uma pergunta"""
        try:
            if not self.chain:
                return "Desculpe, o sistema ainda não foi inicializado. Por favor, carregue um documento primeiro."
            
            # Usar o chain com prompt personalizado já configurado
            result = self.chain({"question": question})
            
            answer = result.get("answer", "Desculpe, não consegui gerar uma resposta.")
            
            # Personalizar a resposta com a identidade dos autores
            if answer and not answer.startswith("Desculpe"):
                answer = f"📚 **Português Funcional - Marcos Rogério & Iara Bezerra**\n\n{answer}"
            
            return answer
            
        except Exception as e:
            return f"Erro ao gerar resposta: {str(e)}"
    
    def clear_history(self):
        """Limpa o histórico da conversa"""
        if self.memory:
            self.memory.clear()
    
    def save_vectorstore(self, path: str):
        """Salva o vectorstore em disco"""
        try:
            if self.vectorstore:
                self.vectorstore.save_local(path)
                return True
        except Exception as e:
            st.error(f"Erro ao salvar vectorstore: {str(e)}")
        return False
    
    def load_vectorstore(self, path: str):
        """Carrega o vectorstore do disco"""
        try:
            if os.path.exists(path) and self.embeddings:
                self.vectorstore = FAISS.load_local(path, self.embeddings)
                self.setup_chain()
                return True
        except Exception as e:
            st.error(f"Erro ao carregar vectorstore: {str(e)}")
        return False
    
    def load_pdf(self, pdf_path: str) -> bool:
        """Carrega e processa um arquivo PDF específico"""
        try:
            if not os.path.exists(pdf_path):
                st.error(f"Arquivo não encontrado: {pdf_path}")
                return False
            
            with open(pdf_path, 'rb') as pdf_file:
                return self.process_documents([pdf_file])
                
        except Exception as e:
            st.error(f"Erro ao carregar PDF: {str(e)}")
            return False
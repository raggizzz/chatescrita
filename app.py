import streamlit as st
import base64
import os
from dotenv import load_dotenv
from rag_engine import RAGEngine

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="MARCOS & ERIKA - EscritaComCiencia",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para interface profissional
st.markdown("""
<style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Reset e configurações globais */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Fundo com tema claro */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        min-height: 100vh;
        color: #000000 !important;
    }
    
    /* Elementos específicos do Streamlit */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stText, .stTextInput label, .stSelectbox label, .stButton button,
    .element-container, .stAlert, .stSuccess, .stWarning, .stError {
        color: #000000 !important;
    }
    
    /* Ocultar elementos padrão do Streamlit */
    .stDeployButton,
    header[data-testid="stHeader"],
    footer,
    .stMainMenu,
    #MainMenu,
    .stActionButton {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Container principal */
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Layout centralizado removido - sem fundo branco */
    
    /* Wrapper da imagem dos personagens */
    .characters-wrapper {
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        animation: fadeInDown 1s ease-out;
    }
    
    /* Estilo da imagem dos personagens educadores - responsiva */
    .characters-image {
        max-width: 250px;
        width: 100%;
        height: auto;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        background: white;
        display: block;
        margin: 0 auto;
        animation: float 3s ease-in-out infinite;
    }
    
    .characters-image:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Responsividade para dispositivos móveis */
    @media (max-width: 768px) {
        .characters-image {
            max-width: 200px;
        }
        .names-title {
            font-size: 2.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .characters-image {
            max-width: 150px;
        }
        .names-title {
            font-size: 2rem;
        }
    }
    
    /* Título com os nomes */
    .names-title {
        font-size: 3rem;
        font-weight: 900;
        color: #000000 !important;
        margin: 1rem 0;
        text-align: center;
        letter-spacing: 3px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        line-height: 1.2;
        font-family: 'Inter', sans-serif;
        animation: fadeInUp 1s ease-out 0.3s both;
    }
    
    /* Balão de fala moderno */
    .speech-bubble {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px solid #e9ecef;
        border-radius: 25px;
        padding: 2rem 2.5rem;
        margin: 1rem auto 2rem;
        max-width: 500px;
        position: relative;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 1s ease-out 0.6s both;
    }
    
    .speech-bubble:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.12);
    }
    
    /* Seta do balão de fala apontando para cima */
    .speech-bubble::before {
        content: '';
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 0;
        border-left: 15px solid transparent;
        border-right: 15px solid transparent;
        border-bottom: 15px solid #e9ecef;
        z-index: 1;
    }
    
    .speech-bubble::after {
        content: '';
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 0;
        border-left: 13px solid transparent;
        border-right: 13px solid transparent;
        border-bottom: 13px solid #ffffff;
        z-index: 2;
    }
    
    /* Texto da mensagem de boas-vindas */
    .welcome-message {
        font-size: 1.2rem;
        color: #000000 !important;
        line-height: 1.6;
        margin: 0;
        font-weight: 500;
        text-align: center;
        font-family: 'Inter', sans-serif;
    }
    
    /* Área do chat */
    .chat-container {
        width: 100%;
        max-width: 800px;
        margin: 2rem auto;
        padding: 0 1rem;
        animation: fadeInUp 1s ease-out 0.9s both;
    }
    
    /* Input do chat */
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 2px solid #e9ecef !important;
        padding: 1rem 1.5rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #007bff !important;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1) !important;
    }
    
    /* Botão de enviar */
    .stButton > button {
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 123, 255, 0.4) !important;
    }
    
    /* Mensagens do chat */
    .chat-message {
        margin: 1rem 0;
        padding: 1rem 1.5rem;
        border-radius: 20px;
        max-width: 80%;
        animation: slideIn 0.5s ease-out;
    }
    
    .user-message {
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #1976d2 !important;
        margin-right: auto;
        border: 1px solid #dee2e6;
    }
    
    /* Animações */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Responsividade para dispositivos móveis */
    @media (max-width: 768px) {
        .characters-image {
            max-width: 300px;
        }
        
        .names-title {
            font-size: 2.5rem;
            letter-spacing: 2px;
        }
        
        .speech-bubble {
            padding: 1.5rem 2rem;
            border-radius: 20px;
        }
        
        .welcome-message {
            font-size: 1.1rem;
        }
        
        .chat-message {
            max-width: 90%;
        }
    }
    
    @media (max-width: 480px) {
        .characters-image {
            max-width: 250px;
        }
        
        .names-title {
            font-size: 2rem;
            letter-spacing: 1px;
        }
        
        .speech-bubble {
            padding: 1.2rem 1.5rem;
            border-radius: 18px;
        }
        
        .welcome-message {
            font-size: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def get_characters_image():
    """Retorna a imagem dos personagens educadores em base64"""
    try:
        with open("image.png", "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{img_data}"
    except FileNotFoundError:
        # Fallback: SVG com personagens educadores 3D estilizados
        svg_content = """
<svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ffffff;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f8f9fa;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="2" dy="4" stdDeviation="3" flood-color="rgba(0,0,0,0.15)"/>
    </filter>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Fundo -->
  <rect width="400" height="300" fill="url(#bg)" rx="20"/>
  
  <!-- Marcos (Homem) - Educador -->
  <g transform="translate(100, 50)" filter="url(#shadow)">
    <!-- Cabeça -->
    <ellipse cx="0" cy="40" rx="35" ry="38" fill="#fdbcb4"/>
    <!-- Cabelo profissional -->
    <path d="M -32 15 Q 0 5 32 15 Q 30 35 0 40 Q -30 35 -32 15" fill="#4a4a4a"/>
    <!-- Óculos -->
    <circle cx="-12" cy="35" r="8" fill="none" stroke="#333" stroke-width="2"/>
    <circle cx="12" cy="35" r="8" fill="none" stroke="#333" stroke-width="2"/>
    <line x1="-4" y1="35" x2="4" y2="35" stroke="#333" stroke-width="2"/>
    <!-- Olhos -->
    <circle cx="-12" cy="35" r="3" fill="#333"/>
    <circle cx="12" cy="35" r="3" fill="#333"/>
    <circle cx="-10" cy="33" r="1" fill="white"/>
    <circle cx="14" cy="33" r="1" fill="white"/>
    <!-- Nariz -->
    <ellipse cx="0" cy="42" rx="2" ry="3" fill="#f4a688"/>
    <!-- Sorriso amigável -->
    <path d="M -10 50 Q 0 58 10 50" stroke="#333" stroke-width="2" fill="none" stroke-linecap="round"/>
    <!-- Corpo profissional -->
    <rect x="-25" y="75" width="50" height="70" fill="#1976d2" rx="15"/>
    <!-- Gravata -->
    <polygon points="0,75 -5,90 5,90" fill="#c41e3a"/>
    <rect x="-2" y="75" width="4" height="20" fill="#c41e3a"/>
    <!-- Braços -->
    <ellipse cx="-35" cy="95" rx="10" ry="25" fill="#1976d2"/>
    <ellipse cx="35" cy="95" rx="10" ry="25" fill="#1976d2"/>
    <!-- Mãos -->
    <circle cx="-35" cy="120" r="8" fill="#fdbcb4"/>
    <circle cx="35" cy="120" r="8" fill="#fdbcb4"/>
  </g>
  
  <!-- Érika (Mulher) - Educadora -->
  <g transform="translate(300, 50)" filter="url(#shadow)">
    <!-- Cabeça -->
    <ellipse cx="0" cy="40" rx="35" ry="38" fill="#fdbcb4"/>
    <!-- Cabelo elegante -->
    <path d="M -35 10 Q 0 0 35 10 Q 32 55 0 60 Q -32 55 -35 10" fill="#8b4513"/>
    <!-- Olhos expressivos -->
    <circle cx="-12" cy="35" r="4" fill="#333"/>
    <circle cx="12" cy="35" r="4" fill="#333"/>
    <circle cx="-10" cy="33" r="1.5" fill="white"/>
    <circle cx="14" cy="33" r="1.5" fill="white"/>
    <!-- Cílios -->
    <path d="M -16 30 L -14 28 M -10 29 L -8 27 M -6 30 L -4 28" stroke="#333" stroke-width="1"/>
    <path d="M 8 28 L 10 27 M 14 29 L 16 27 M 18 30 L 20 28" stroke="#333" stroke-width="1"/>
    <!-- Nariz -->
    <ellipse cx="0" cy="42" rx="2" ry="3" fill="#f4a688"/>
    <!-- Sorriso caloroso -->
    <path d="M -10 50 Q 0 58 10 50" stroke="#333" stroke-width="2" fill="none" stroke-linecap="round"/>
    <!-- Corpo elegante -->
    <rect x="-25" y="75" width="50" height="70" fill="#e91e63" rx="15"/>
    <!-- Colar -->
    <circle cx="0" cy="85" r="5" fill="#ffd700" stroke="#ffb300" stroke-width="1"/>
    <!-- Braços -->
    <ellipse cx="-35" cy="95" rx="10" ry="25" fill="#e91e63"/>
    <ellipse cx="35" cy="95" rx="10" ry="25" fill="#e91e63"/>
    <!-- Mãos -->
    <circle cx="-35" cy="120" r="8" fill="#fdbcb4"/>
    <circle cx="35" cy="120" r="8" fill="#fdbcb4"/>
  </g>
  
  <!-- Elementos decorativos educacionais -->
  <g filter="url(#glow)">
    <circle cx="60" cy="60" r="2" fill="#ffd700" opacity="0.8"/>
    <circle cx="340" cy="70" r="2.5" fill="#ff6b6b" opacity="0.7"/>
    <circle cx="50" cy="220" r="1.5" fill="#4ecdc4" opacity="0.9"/>
    <circle cx="350" cy="210" r="2" fill="#45b7d1" opacity="0.8"/>
    <!-- Livros pequenos -->
    <rect x="30" y="250" width="8" height="12" fill="#007bff" opacity="0.6" rx="1"/>
    <rect x="360" y="240" width="8" height="12" fill="#28a745" opacity="0.6" rx="1"/>
  </g>
</svg>
"""
        return "data:image/svg+xml;base64," + base64.b64encode(svg_content.encode()).decode()

def initialize_rag_engine():
    """Inicializa o RAG engine com o arquivo LIVRO.pdf"""
    if 'rag_engine' not in st.session_state:
        try:
            st.session_state.rag_engine = RAGEngine()
            st.session_state.pdf_loaded = False
            
            # Verificar se o arquivo LIVRO.pdf existe
            if os.path.exists("LIVRO.pdf"):
                try:
                    st.session_state.rag_engine.load_pdf("LIVRO.pdf")
                    st.session_state.pdf_loaded = True
                except Exception as e:
                    st.session_state.pdf_loaded = False
                    st.session_state.pdf_error = f"Erro ao carregar PDF: {str(e)}"
            else:
                st.session_state.pdf_loaded = False
                st.session_state.pdf_error = "Arquivo LIVRO.pdf não encontrado"
        except Exception as e:
            st.session_state.rag_engine = None
            st.session_state.pdf_loaded = False
            st.session_state.pdf_error = f"Erro ao inicializar sistema: {str(e)}"

def main():
    """Função principal da aplicação"""
    # Inicializar o RAG engine
    initialize_rag_engine()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Imagem dos personagens educadores
    characters_img_src = get_characters_image()
    st.markdown(f'''
    <div class="characters-wrapper">
        <img src="{characters_img_src}" alt="Marcos e Erika - EscritaComCiencia" class="characters-image">
    </div>
    ''', unsafe_allow_html=True)
    
    # Título com os nomes
    st.markdown('<h1 class="names-title">MARCOS & ERIKA</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.5rem; color: #000000 !important; font-weight: 600; margin-top: -0.5rem;">EscritaComCiencia</p>', unsafe_allow_html=True)
    
    # Balão de fala com mensagem de boas-vindas
    st.markdown('''
    <div class="speech-bubble">
        <p class="welcome-message">Olá! Somos Marcos & Erika da EscritaComCiencia, especialistas em língua portuguesa. Como podemos ajudar você hoje?</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Área do chat
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Exibir mensagens do histórico
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Input do usuário
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Digite sua pergunta sobre língua portuguesa:",
            placeholder="Ex: Como usar corretamente a crase?",
            label_visibility="collapsed",
            key="user_input"
        )
    
    with col2:
        send_button = st.button("Enviar", type="primary")
    
    # Processar entrada do usuário
    if send_button and user_input:
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Gerar resposta usando RAG engine
        with st.spinner("Pensando..."):
            if st.session_state.pdf_loaded and st.session_state.rag_engine:
                response = st.session_state.rag_engine.get_response(user_input)
            else:
                if hasattr(st.session_state, 'pdf_error'):
                    response = f"Desculpe, houve um problema ao carregar nosso conhecimento especializado: {st.session_state.pdf_error}. Mesmo assim, como especialistas em língua portuguesa, posso ajudar com sua pergunta sobre '{user_input}'. Por favor, reformule sua pergunta e tentarei responder com base em meu conhecimento geral."
                else:
                    response = f"Olá! Recebi sua pergunta: '{user_input}'. Estou carregando nosso conhecimento especializado. Por favor, aguarde um momento e tente novamente."
        
        # Adicionar resposta do bot
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun para atualizar a interface
        st.rerun()
    
    # Botão para limpar conversa
    if st.session_state.messages:
        if st.button("🗑️ Limpar Conversa", help="Limpar todo o histórico de mensagens"):
            st.session_state.messages = []
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Fechar chat-container

if __name__ == "__main__":
    main()
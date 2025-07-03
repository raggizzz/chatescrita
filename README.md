# Chatbot Especialista em "Português Funcional"

## 📚 Descrição

Chatbot profissional especializado no livro "Português Funcional" de Marcos Rogério Martins Costa e Iara da Silva Bezerra. Interface moderna e responsiva que oferece orientação educacional baseada no conteúdo completo da obra, priorizando sempre uma visão holística dos 10 capítulos que tratam da língua portuguesa como ferramenta de transformação pessoal e profissional.

## ✨ Características da Interface

- **Design Profissional**: Interface limpa e moderna com tema claro
- **Personagens 3D**: Marcos e Érika, educadores amigáveis e sorridentes
- **Layout Responsivo**: Adaptável para desktop e dispositivos móveis
- **Animações Suaves**: Efeitos de hover e animações de entrada
- **Balão de Fala Moderno**: Mensagem de boas-vindas em português
- **Chat Interativo**: Interface de conversação em tempo real

## 🛠️ Tecnologias Utilizadas

- **Frontend**: Streamlit com CSS personalizado
- **Backend**: Python + LangChain para orquestração de IA
- **IA**: Google Gemini AI para geração de linguagem natural
- **Processamento de Documentos**: PyPDF2 para extração de texto
- **Busca Vetorial**: FAISS para recuperação de informações
- **Embeddings**: Sentence Transformers para representação vetorial

## 📋 Pré-requisitos

- Python 3.8+
- Chave de API do Google Gemini
- Arquivo `LIVRO.pdf` com conteúdo de referência

## 🚀 Instalação e Execução

1. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variáveis de ambiente** (IMPORTANTE - SEGURANÇA):
   ```bash
   # Copiar o arquivo de exemplo
   cp .env.example .env
   
   # Editar o arquivo .env com suas chaves reais
   # GOOGLE_API_KEY=sua_chave_google_gemini_aqui
   ```
   - ⚠️ **NUNCA** commitar o arquivo `.env` no Git
   - ⚠️ **NUNCA** colocar chaves de API diretamente no código
   - O arquivo `.env` já está no `.gitignore` para sua proteção
   - Use o `.env.example` como template

3. **Adicionar arquivo de referência**:
   - Colocar o arquivo `LIVRO.pdf` na raiz do projeto

4. **Executar a aplicação**:
   ```bash
   python -m streamlit run app.py
   ```

5. **Acessar no navegador**:
   - Local: http://localhost:8501

## 📁 Estrutura do Projeto

```
ChatBot-Escrita/
├── app.py              # Interface principal do Streamlit
├── rag_engine.py       # Engine de IA e processamento de documentos
├── requirements.txt    # Dependências do projeto
├── README.md          # Documentação
├── LIVRO.pdf          # Arquivo de referência (adicionar)
└── .env               # Variáveis de ambiente (criar)
```

## 🎯 Funcionalidades

- **Processamento de PDF**: Extração e indexação automática do conteúdo
- **Busca Semântica**: Recuperação inteligente de informações relevantes
- **Respostas Contextuais**: Respostas baseadas no conteúdo do documento
- **Histórico de Conversa**: Manutenção do contexto da conversa
- **Interface Multilíngue**: Suporte completo ao português
- **Design Responsivo**: Funciona em todos os dispositivos

## 🔧 Configuração Avançada

### Personalização da Interface
- Modificar cores e estilos no CSS do `app.py`
- Ajustar animações e efeitos visuais
- Personalizar mensagens e textos

### Configuração da IA
- Ajustar parâmetros do modelo no `rag_engine.py`
- Modificar estratégias de chunking de texto
- Configurar embeddings e busca vetorial

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar se todas as dependências estão instaladas
2. Confirmar se o arquivo `LIVRO.pdf` está presente
3. Validar a configuração da chave de API do Google Gemini

## 🎨 Características Visuais

- **Fonte**: Inter (moderna e legível)
- **Cores**: Tema claro com gradientes suaves
- **Animações**: Efeitos de flutuação e transições suaves
- **Responsividade**: Breakpoints para mobile e tablet
- **Acessibilidade**: Contraste adequado e navegação intuitiva

---

**Desenvolvido para oferecer uma experiência profissional e amigável no aprendizado da língua portuguesa.**
# Handover Documentation tool

The Handover Documentation Tool is an extension of AAS Manager that generates a Handover Documentation Submodel from a PDF file using LLMs.

## Usage
- Select **Tools → Handover Documentation tool**.
- Select the LLM provider and model.
- Provide credentials:
  - Cloud providers: enter the API key.
  - **Ollama (local)**: API key is not required; optionally enter a custom Ollama base URL (default: `http://localhost:11434`).
- Drag-and-drop or choose the PDF file.
- Check and adjust extracted data if needed.
- Finish to add the generated Handover Documentation Submodel to the current AAS file.

## Supported LLM providers
- OpenAI
- Anthropic
- Google Vertex
- Groq
- Mistral AI
- Ollama (local)

## Local LLM setup (Ollama)
1. Install and run [Ollama](https://ollama.com/).
2. Pull a chat model, for example:
   - `ollama pull llama3.1:8b`
3. Pull the embedding model used for RAG:
   - `ollama pull nomic-embed-text`
4. In the tool, choose **Ollama (local)** and set the model name (for example `llama3.1:8b`).
5. Leave the API key field empty to use `http://localhost:11434`, or provide a custom Ollama URL.

The tool uses [LangChain](https://python.langchain.com/docs/) for LLM interaction. It splits PDFs into chunks, stores embeddings in a vector store, and performs RAG querying for larger documents.

> Disclaimer: The Handover Documentation tool relies on LLMs for information extraction. LLM output can be incomplete or inaccurate. Always review the generated documentation before production or compliance use.

# Agentic Chatbot - LangGraph Day 4

A classroom-friendly end-to-end agentic chatbot built with:

- LangGraph for graph orchestration and the tool-use loop
- LangChain tools/messages/model integration
- OpenAI-compatible chat model (via Experiential Labs gateway)
- FastAPI backend
- Streamlit UI
- Docker + Docker Compose

## Architecture

Streamlit UI -> FastAPI /chat -> LangGraph agent -> LLM -> ToolNode -> tools -> LLM -> FastAPI -> Streamlit

## Tools

- calculator
- get_current_time
- get_weather (Open-Meteo, no separate weather API key)

## Local setup

1. Create a virtual environment.
2. Install `requirements.txt`.
3. Copy `.env.example` to `.env`.
4. Add your API key and base URL.
5. Run `uvicorn app.main:app --reload --port 8000`.
6. In another terminal run `streamlit run ui/streamlit_app.py`.

## Docker setup

1. Create `.env` from `.env.example`.
2. Build the image: `docker build -t agentic-chatbot:day4 .`
3. Start both services: `docker compose up --build`.
4. Open http://localhost:8501 and http://localhost:8000/docs.

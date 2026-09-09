# Ethabo — AI Study Companion

Ethabo (meaning "assistant" in Isoko) is an AI study app that turns your
own documents into an interactive study workspace — chat with your notes, generate quizzes,
build study plans, run research on gaps in your sources, and track your progress over time.

## Architecture

**Backend** (`backend/`) — Django + DRF, PostgreSQL with pgvector, a LangGraph multi-agent
system, Cohere for generation/embeddings/reranking, and Tavily as a web-search fallback.

**Frontend** (`study-companion/`) — Next.js (App Router), React, plain JavaScript, hand-built UI.

### The five agents
- **Tutor** — conversational Q&A over your uploaded sources
- **Quiz Generator** — generates questions from your notes, grades answers, tracks results
- **Study Planner** — builds a study plan from your sources
- **Research Assistant** — answers questions from your notes first, falls back to live web
  search (via Tavily) when the answer isn't in your notes
- **Progress Analysis** — summarizes quiz performance to highlight weak spots

### Retrieval pipeline
Documents are chunked and embedded, then retrieved via a hybrid approach — dense
(embedding similarity) + sparse (keyword) retrieval fused with Reciprocal Rank Fusion (RRF),
followed by Cohere reranking and context compression before being passed to an agent.

### Routing
A heuristic-first router classifies each request, falling back to an LLM classifier
(Cohere) when heuristics don't confidently match — defaulting to the Tutor agent on failure.

## Project structure

```
ai-study-companion/
├── backend/            # Django REST API + LangGraph agents
└── study-companion/    # Next.js frontend
```

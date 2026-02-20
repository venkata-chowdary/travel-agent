# Travel Agent AI ✈️

A CLI-based intelligent travel agent powered by Google's Gemini models. This application understands user travel requirements and generates detailed itineraries by simulating flight and hotel searches.

## 🚀 Features

- **Natural Language Understanding**: Uses Gemini 2.0 Flash (and fallback models) to interpret complex travel queries.
- **Guardrail Agent**: Intercepts and validates user queries before processing, blocking irrelevant questions to save tokens and prevent hallucinations.
- **Smart Balancing**: Agent logic naturally balances cost and ratings to find the "sweet spot" for accommodations and flights without exceeding budgets.
- **Tool Calling**: Agents can "call" tools to search for flights, hotels, and calculate costs (currently using mock data for demonstration).
- **Structured Output**: Guarantees valid JSON output matching a strict schema using Pydantic validation.
- **Resilience**: Built-in retry logic with exponential backoff for handling API rate limits and network instability.
- **Logging**: Comprehensive logging for tracing agent thought processes and debugging.

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **AI Model**: Google Gemini (via `google-genai` SDK)
- **Validation**: Pydantic
- **Configuration**: dotenv for environment management

## 📂 Project Structure

```
Travel Agent/
├── agent/
│   ├── agent.py           # Core GeminiAgent logic (tool calling, retry loop)
│   ├── guardrail_agent.py # Agent for validating prompt relevance
│   ├── prompts.py         # System prompts and instructions
│   └── tool.py            # Tool registration logic
├── schemas/
│   ├── output_parser.py # Pydantic parser for validating JSON response
│   ├── itinerary.py     # Data models for the itinerary
│   └── tool_schema.py   # Schemas for tool definitions
├── tools/
│   ├── flights.py      # Mock flight search tool
│   ├── hotels.py       # Mock hotel search tool
│   └── cost.py         # Cost calculation tool
├── utils/
│   └── logger.py       # Logging configuration
├── main.py             # Entry point of the application
├── config.py           # Configuration settings (Model names, timeouts)
└── .env                # Environment variables (API Keys)
```

## ⚡ Getting Started

### Prerequisites

- Python 3.8+
- A Google Cloud Project with the Gemini API enabled
- A [Google AI Studio API Key](https://aistudio.google.com/)

### Installation

1.  **Clone the repository**:

    ```bash
    git clone <repository-url>
    cd "Travel Agent"
    ```

2.  **Create a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:

    ```bash
    pip install google-genai python-dotenv pydantic exceptiongroup
    ```

4.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```env
    GEMINI_API_KEY=your_api_key_here
    LOG_LEVEL=INFO
    ```

### Usage

Run the main script to generate a sample itinerary:

```bash
python main.py
```

The application will:

1.  Initialize the Gemini Agent.
2.  Process the default query: _"Plan a 3-day trip to Goa from Delhi under ₹20,000 next weekend."_
3.  Simulate tool calls (searching flights/hotels).
4.  Generate and validate the final JSON itinerary.
5.  Print the result to the console.

## 📝 Current Status

- **Agent Logic**: Functional with multi-turn tool calling and query guardrails.
- **Tools**: `search_flights` and `search_hotels` are implemented with mock data.
- **Error Handling**: Robust against invalid queries, JSON parsing errors, and API timeouts.
- **Next Steps**:
    - Integrate real travel APIs (e.g., Skyscanner, Amadeus).
    - Add a frontend interface (Streamlit/React).
    - Support conversation history.

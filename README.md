### Kaitu ###

**Personal AI Assistant** — Version `0a2 - Foxy`

Kaitu is a modular Python personal assistant for Windows. It combines local models through Ollama, optional cloud models through Google Gemini and Groq, voice interaction, persistent facts, desktop commands, and modular skills.

> **Current Status:** `0a2`
> Experimental project under active development.

## Features ##

### Core

- Multi-provider AI: Ollama by default, with Groq and Gemini cloud options
- Persistent user facts and short-term conversation history
- Input routing for local responses, memory, math, commands, and AI fallback
- Deterministic local responses for common interactions

### Commands

- Open applications
- Close applications
- Launch websites
- Web search
- Windows application discovery
- Command aliases and natural-language command handling

### Voice

- Two-way voice conversation
- Text-to-Speech / read-aloud mode
- Speech-to-Text / dictation mode
- Voice input and output controls

### Skills

- Natural-language calculator
- Text/file reader

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| Local LLM | Ollama |
| Cloud LLMs | Groq, Google Gemini |
| Speech Recognition | faster-whisper |
| Text-to-Speech | Piper TTS |
| Memory | JSON facts + in-memory conversation history |
| Testing | pytest dependency (test files are gitignored locally) |
| Platform | Windows |


## Architecture

```text
main.py
  ├─ normalize input and detect voice mode
  ├─ audio.voice_talk (optional voice sessions)
  └─ router.route_input
       ├─ local_responses
       ├─ data.memory (fact commands and summary)
       ├─ skills.calculator
       ├─ command_engine (app control, web search, reading)
       └─ brain.ask_assistant
            └─ provider_manager
                 ├─ Ollama
                 ├─ Groq
                 └─ Gemini
```

The router handles farewells, local responses, memory, calculations, and recognized commands before falling back to an AI provider. Voice sessions use the same router.

| Prefix | Provider behavior |
|---|---|
| *(none)* | Ollama with `TALK_MODEL` |
| `cloud ` | Groq → Gemini → Ollama with `TALK_MODEL` |
| `think ` | Gemini → Ollama with `MEMORY_MODEL` |
| `ola ` | Ollama with `MEMORY_MODEL` |

### Project structure

```text
Kaitu/
├── main.py
├── router.py
├── brain.py
├── provider_manager.py
├── config.py
├── commands.py
├── command_engine.py
├── local_responses.py
├── aliases.py
├── app_discovery.py
├── data/
│   └── memory.py
├── providers/
│   ├── __init__.py
│   ├── ollama_provider.py
│   ├── groq_provider.py
│   └── gemini_provider.py
├── audio/
│   ├── __init__.py
│   ├── speech_input.py
│   ├── speech_output.py
│   ├── voice_processing.py
│   └── voice_talk.py
├── skills/
│   ├── calculator.py
│   └── reader.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Command phrases

`commands.py` is the phrase and response registry used by Kaitu's local interactions. It groups phrases by intent for greetings, farewells, identity, status, date, and time, and provides the corresponding local responses. It also defines phrase lists and related data for voice controls, wake words, pronunciation, and memory commands.

The modules that handle these features import the relevant constants from `commands.py`; phrase matching and command behavior are implemented in those modules.

## Memory

`data/memory.py` stores user facts in the ignored runtime file `data/memory.json`. The expected format is:

```json
{
  "memories": [
    {
      "memory_id": "mem_example",
      "memory": "I live in India",
      "created_at": "2026-01-01T12:00:00+05:30"
    }
  ]
}
```

Use explicit phrases such as `remember that I live in India`, `forget that I live in India`, or `what do you know about me`. Forgetting currently compares wording after trimming outer whitespace and ignoring capitalization; semantic matching is not implemented. Summaries are generated locally through Ollama.

Conversation history is kept in memory for the current process only, limited to the latest 10 messages. It is not saved across restarts. Cloud providers receive the saved memory context when used, so avoid storing sensitive information if you do not want it sent to a cloud service.

## Setup ##

## 1. Prerequisites

* Python 3.13+
* Windows
* Ollama
* Microphone for voice features
* CUDA-compatible GPU is optional and may improve Whisper performance


## 2. Clone the Repository

```powershell
git clone https://github.com/kunal0040/Kaitu.git
cd Kaitu
```


## 3. Create a Virtual Environment

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 4. Install Dependencies

```powershell
pip install -r requirements.txt
```


## 5. Configure cloud providers (optional)

Create a `.env` file in the project root and set the key(s) for the cloud provider(s) you plan to use:

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

Keep `.env` private; do not commit real API keys.

## 6. Install Ollama models

Example models:

```powershell
ollama pull phi4-mini
ollama pull huihui_ai/qwen3-abliterated:8b
```

The exact models can be changed through `config.py`.


## 7. Run Kaitu

```powershell
python main.py
```


## Usage Examples ##

You: hi
Kaitu: Hey {your_name}! ...

You: open chrome
Kaitu: Opening Google Chrome...

You: what is 25 percent of 80
Kaitu: The answer is 20.

You: remember that I live in India
Kaitu: Got it, {your_name}, I'll remember that for next time.

You: cloud explain this concept
→ Uses Groq, then Gemini, then local Ollama if needed

You: ola explain this concept
→ Uses the configured local Ollama memory model

You: let's talk
→ Enters two-way voice mode


## Configuration ##

Important settings are located in `config.py`.

Example settings:

```python
ASSISTANT_NAME = "Kaitu"
USER_NAME = "your_name"
ASSISTANT_VERSION = "0a2 - Foxy"
MODEL_NAME_GROQ = "openai/gpt-oss-120b"
MODEL_NAME_GEMINI = "gemini-3.5-flash"
TALK_MODEL = "phi4-mini"
MEMORY_MODEL = "huihui_ai/qwen3-abliterated:8b"
```


## Current Limitations ##

Kaitu `0a2` is an experimental release.


## Versioning ##

Current release:

**`0a2 - Foxy`**

This is an early experimental release. APIs, architecture, features, and internal components may change significantly in future versions.



# License

This is a personal experimental project created for learning and development.

Use and modify freely for learning and personal purposes.



## Author

**Kunal**

Built as a personal AI assistant project.

**Kaitu `0a2 - Foxy`**
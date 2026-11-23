### Kaitu ###

**Personal AI Assistant** — Version `0a3 - Foxy`

Kaitu is a modular Python personal assistant for Windows. It combines local models through Ollama, optional cloud models through Google Gemini and Groq, voice interaction, persistent facts, desktop commands, and modular skills.

> **Current Status:** `0a3`
> Experimental project under active development.

## Features ##

### Core

- Multi-provider AI: Ollama by default, with Groq and Gemini cloud options
- Persistent user facts and short-term conversation history
- Input routing for local responses, memory, math, commands, and AI fallback
- Deterministic local responses for common interactions
- Wake-word removal and fuzzy correction for command vocabulary
- Local greeting, identity, status, date, and time responses

### Commands

- Open applications
- Close applications
- Launch websites
- Web search
- Windows application discovery
- Command aliases and natural-language command handling
- Personal website shortcuts from `data/personal_webpages.json`

### Voice

- Two-way voice conversation
- Text-to-Speech / read-aloud mode
- Speech-to-Text / dictation mode
- Voice input and output controls
- Switchable male/female Piper voices and return-to-keyboard controls

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
| Platform | Windows |


## Architecture

```text
main.py
  ├─ normalize input and detect voice mode
  ├─ audio.voice_talk (optional voice sessions)
  └─ router.route_input
       ├─ local_response.input_analyzer
       ├─ data.memory (fact commands, summary and conversation logs)
       ├─ skills.calculator
       ├─ local_response.command_engine (app control, web search, reading)
       └─ brain.ask_assistant
            └─ providers.provider_manager
                 ├─ Ollama
                 └─ Gemini
                 └─ Groq
```

The router handles local responses, memory commands and recognized commands before falling back to an AI provider. Farewell responses are local, and the main loop exits after a farewell. Voice sessions use the same router.

Input handling removes a leading wake word. Local routing uses normalized text, while the AI fallback receives the original input with the wake word removed.

| Prefix | Provider behavior |
|---|---|
| *(none)* | Ollama with `TALK_MODEL` |
| `cloud ` | Gemini → Groq → Ollama with `TALK_MODEL` |
| `think ` | Gemini → Ollama with `MEMORY_MODEL` |
| `ola ` | Ollama with `MEMORY_MODEL` |

### Project structure

```text
Kaitu/
├── main.py
├── router.py
├── brain.py
├── config.py
├── data/
│   ├── __init__.py
│   ├── memory.py
│   └── logs/
│       └── conversation_logs.py
├── providers/
│   ├── __init__.py
│   ├── provider_manager.py
│   ├── ollama_provider.py
│   ├── groq_provider.py
│   └── gemini_provider.py
├── local_response/
│   ├── __init__.py
│   ├── aliases.py
│   ├── app_discovery.py
│   ├── command_engine.py
│   ├── commands.py
│   └── input_analyzer.py
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

`local_response/commands.py` is the phrase and response registry used by Kaitu's local interactions. It groups phrases by intent for greetings, farewells, identity, status and provides the corresponding local responses. It also defines phrase lists and related data for voice controls and other relevant commands.

### Personal webpage shortcuts

`data/personal_webpages.json` maps shortcut names to URLs under the `WEB_SITES` key. `local_response/command_engine.py` loads these shortcuts so a command such as `open github` opens its configured URL. This file is local and ignored by Git.

## Memory

`data/memory.py` stores user facts in the local runtime file `data/memory.json`. The expected format is:

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

Use explicit phrases such as `remember that I live in India`, `forget that I live in India`, or `what do you know about me`. Duplicate and forget matching normalize text (including case and punctuation), but do not infer semantic equivalence. Summaries are generated locally through Ollama.

Conversation context is kept in memory for the current process only, limited to the latest 20 messages.

### Conversation log

`data/logs/conversation_logs.py` loads and saves the persistent log at `data/logs/conversation_log.json`. Each entry records the original input, processed input, assistant response, and conversation time. The JSON file is generated locally and is separate from the short-term conversation context above.

AI providers receive saved memory context and in-process conversation history when used. Avoid storing sensitive information if you do not want it sent to a cloud provider.

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
→ Uses Gemini, then Groq, then local Ollama if needed

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
ASSISTANT_VERSION = "0a3 - Foxy"
MODEL_NAME_GROQ = "openai/gpt-oss-120b"
MODEL_NAME_GEMINI = "gemini-3.5-flash"
TALK_MODEL = "phi4-mini"
MEMORY_MODEL = "huihui_ai/qwen3-abliterated:8b"
```

---

### Model Architecture & Fine-Tuning

The core intelligence of Kaitu is powered by **`phi4:mini-kaitu`**, a custom fine-tuned model derived from Microsoft's Phi-4-mini (3.8B) using QLoRA and quantized to 4-bit `Q4_K_M GGUF` for low-latency local execution on Ollama.

- **Fine-Tuning Codebase & Benchmarks**: [kunal0040/Finetune-Phi4-mini](https://github.com/kunal0040/Finetune-Phi4-mini)
- **Benchmark History**: Evaluated across 500+ curated prompts through 8 full iterations (V1–V8).
- **Runtime Guards**: Features deterministic safety guards for command interception, syntax validation, and memory injection.

## Current Limitations ##

Kaitu `0a3 - Foxy` is an experimental release. Voice features require a working microphone and the Piper voice model files configured in `config.py`. Speech recognition tries the configured CUDA device and falls back to CPU if unavailable.


## Versioning ##

Current release:

**`0a3 - Foxy`**

This is an early experimental release. APIs, architecture, features, and internal components may change significantly in future versions.



# License

This is a personal experimental project created for learning and development.

Use and modify freely for learning and personal purposes.



## Author

**Kunal**

Built as a personal AI assistant project.

**Kaitu `0a3 - Foxy`**
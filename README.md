### Kaitu ###

**Personal AI Assistant** — Version `0a1`

Kaitu is a modular Python-based personal AI assistant designed to run locally on a Windows machine. It combines local LLMs through Ollama, optional cloud AI through Google Gemini, voice interaction, persistent memory, system commands, and modular skills into a single assistant.

> **Current Status:** Foxy (`0a1`)  
> Experimental project under active development.

## Features ##

### Core

- Multi-provider AI architecture using Ollama and Google Gemini
- Persistent memory system
- LLM-based memory relationship classification:
  - `new`
  - `duplicate`
  - `update`
  - `contradiction`
  - `uncertain`
- Modular input router
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
| Cloud LLM | Google Gemini |
| Speech Recognition | faster-whisper |
| Text-to-Speech | Piper TTS |
| Memory | JSON + LLM-based classification |
| Testing | pytest + pytest-cov |
| Platform | Windows |


## Architecture ##

Kaitu is organized into independent components so that individual systems can be developed and replaced without rewriting the entire assistant.

User Input
    │
    ▼
   Router
    │
    ├── Local Responses
    │
    ├── Memory Manager
    │
    ├── Command Engine
    │
    └── AI Brain
           │
           ├── Ollama
           └── Gemini

Additional Systems:
    ├── Voice
    ├── Memory
    ├── Skills
    └── Windows App Discovery

## Project Structure ##
 
Kaitu/
├── main.py
├── router.py
├── brain.py
├── config.py
├── memory.py
├── memory_manager.py
├── command_engine.py
├── local_responses.py
├── aliases.py
├── app_discovery.py
├── app_registry.py
├── provider_manager.py
│
├── providers/
│   ├── __init__.py
│   ├── gemini_provider.py
│   └── ollama_provider.py
│
├── audio/
│   ├── __init__.py
│   ├── speech_input.py
│   ├── speech_output.py
│   ├── voice_talk.py
│   └── voice_processing.py
│
├── skills/
│   ├── calculator.py
│   └── reader.py
│
├── requirements.txt
├── .gitignore
└── README.md

## Setup ##

## 1. Prerequisites

* Python 3.13+
* Windows
* Ollama
* Microphone for voice features
* CUDA-compatible GPU is optional and may improve Whisper performance


## 2. Clone the Repository

--bash--
git clone https://github.com/kunal0040/Kaitu.git
cd Kaitu



## 3. Create a Virtual Environment

### Windows PowerShell

python -m venv .venv
.venv\Scripts\Activate.ps1


## 4. Install Dependencies

pip install -r requirements.txt


## 5. Configure Gemini

Create a `.env` file in the project root:

GEMINI_API_KEY=your_gemini_api_key_here


## 6. Install Ollama Models

Example models:

ollama pull phi4-mini
ollama pull huihui_ai/qwen3-abliterated:8b

The exact models can be changed through `config.py`.


## 7. Run Kaitu


python main.py


## Usage Examples ##

You: hi
Kaitu: Hey Kunal! ...

You: open chrome
Kaitu: Opening Google Chrome...

You: what is 25 percent of 80
Kaitu: The answer is 20.

You: remember that I study VLSI Engineering
Kaitu: I'll remember that you study VLSI Engineering, Kunal!

You: let's talk
→ Enters two-way voice mode


## Configuration ##

Important settings are located in `config.py`.

Example:

ASSISTANT_NAME = "Kaitu"
USER_NAME = "Kunal"
ASSISTANT_VERSION = "0a1"

TALK_MODEL = "phi4-mini"
MEMORY_MODEL = "huihui_ai/qwen3-abliterated:8b"



## Current Limitations ##

Kaitu `0a1` is an experimental release.

Current limitations include:

* Memory currently requires explicit memory commands
* Automatic memory extraction from normal conversation is not yet implemented
* Web search and real-time information grounding are limited
* No screen awareness
* Windows-focused system control
* Calculator has some edge-case limitations
* Voice interaction is still under active development
* Cross-platform support is not currently available


## Roadmap ##

* [ ] Automatic memory extraction
* [ ] Web search tool
* [ ] Improved natural-language command parsing
* [ ] Better error handling and logging
* [ ] Additional modular skills
* [ ] Cross-platform support
* [ ] GUI / system tray interface
* [ ] Improved voice interruption handling


## Versioning ##

Current release:

**`0a1` — Foxy**

This is an early experimental release. APIs, architecture, features, and internal components may change significantly in future versions.



# License

This is a personal experimental project created for learning and development.

Use and modify freely for learning and personal purposes.



## Author

**Kunal**

Built as a personal AI assistant project.

**Kaitu `0a1` — Foxy**
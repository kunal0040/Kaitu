import requests
import json
from config import SYSTEM_PROMPT, OLLAMA_URL, MEMORY_MODEL
from memory import load_memory, get_conversation_history


def get_system_prompt(model_name):
    return SYSTEM_PROMPT + f"""

    Runtime information:
    You are currently running locally on the user's computer through Ollama.
    The underlying local model is {model_name}.
    You do not require cloud API credits for local inference.

    Do not identify the assistant as Qwen during normal conversation.

    If the user specifically asks about the underlying model, provider, or runtime,
    truthfully say that the current local model is {model_name} running through Ollama.
    """


def ask(prompt, model_name):

    memory = load_memory()

    memory_context = f"""
    Known information about the user:
    {memory}
    """

    history = get_conversation_history()

    messages = [
        {"role": "system", "content": get_system_prompt(model_name) + memory_context}
    ]

    messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model_name,
        "messages": messages,
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    response.raise_for_status()

    data = response.json()
    return data["message"]["content"]


def analyze_memory(new_fact, existing_facts, model_name=MEMORY_MODEL):

    memory_prompt = f"""
    You are an AI Memory Relationship Engine. Your sole function is to evaluate ONE new fact about the user against a list of existing facts and output a strict JSON classification.

    You evaluate the logical and semantic relationship based on Entity-Attribute-Value (EAV) extraction. You do not converse, summarize, or verify real-world truth.

    ### THE 5 RELATIONSHIP CLASSES

    1. "new"
    The new fact introduces independent, non-redundant information.
    Trigger "new" if:
    - Subject or Attribute is fundamentally different.
    - Granularity Addition: The new fact is a specific subset of an existing broad fact (e.g., existing: "I like programming", new: "I specialize in Python").
    - Collection Addition: The new fact adds an item to a plural/multi-value attribute (e.g., existing: "I visited Country A", new: "I visited Country B").
    - Historical/Static facts that do not overwrite each other.

    2. "duplicate"
    The new fact is semantically identical, logically equivalent, or entirely subsumed by an existing fact.
    Trigger "duplicate" if:
    - They share the exact same Entity + Attribute + Value meaning.
    - Synonyms & Abbreviations: The new fact uses a common abbreviation, nickname, or synonymous phrasing (e.g., "VS Code" == "Visual Studio Code"; "is my editor" == "I use for coding").
    - Subsumption: The new fact is a generic statement of a specific fact already known (e.g., existing: "I own a high-end gaming laptop", new: "I own a laptop").
    - Ignore differences in grammar, syntax, first-person phrasing, or temporal framing that implies the same current state.

    3. "update"
    The new fact provides a newer/current value for a STRICTLY MUTABLE, single-state attribute, or represents a progression in time.
    Trigger "update" if:
    - State Change: The text explicitly implies a transition, sale, or cessation (e.g., "sold my", "stopped playing", "now enjoy"). Stopping a habit or selling an item is an update, NOT a contradiction.
    - Single-State Overwrites: The attribute logically holds one primary value at a time (e.g., current residence/city, current favorite item, primary operating system, current field of study). Stating a new one implies replacing the old one.
    - Mutual Exclusivity via Time: Changing tools or physical states (e.g., switching from glasses to contact lenses) is an update.
    - Semantic change is required. If the new value means the exact same thing as the old, use "duplicate".

    4. "contradiction"
    The new fact logically denies an existing fact, and it cannot be explained by the standard passage of time.
    Trigger "contradiction" if:
    - Absolute Denial: The new fact denies ever having done or owned something currently in memory (e.g., "I have never lived in...", "I never built...").
    - Direct Negation: Stating the exact opposite of an active state without a transition verb (e.g., existing: "I know HTML", new: "I don't know HTML"; existing: "I have a sister", new: "I have no sister").
    - Do NOT use for standard progression (e.g., changing favorites or stopping a hobby is an "update").

    5. "uncertain"
    Trigger "uncertain" ONLY if:
    - The new fact is too vague to extract an Entity-Attribute-Value.
    - It is impossible to determine if a state change is an "update" or a "contradiction" without querying the user (e.g., ambiguous phrasing like "maybe", "perhaps").

    ### EVALUATION PROTOCOL (Run silently)
    1. Extract (Entity + Attribute + Value) from New Fact.
    2. Scan Existing Facts for the same Entity + Attribute.
    3. If no match -> "new".
    4. If match exists, compare Values:
    - Same meaning, subsumed, or abbreviation -> "duplicate"
    - Different meaning, attribute is single-state/mutable, or explicit cessation/change -> "update"
    - Different meaning, attribute is multi-state/collection -> "new"
    - Direct negation or absolute denial of past reality -> "contradiction"

    Existing memories: 
    {existing_facts}

    New fact: 
    {new_fact}

    ### OUTPUT CONSTRAINTS
    Return ONLY raw, valid JSON. 
    Do NOT wrap the output in markdown code blocks (no ```json or ```).
    Do NOT include any explanations, prefixes, or suffixes.

    {{
        "relationship": "new|duplicate|update|contradiction|uncertain",
        "matched_fact": "Exact text of the relevant existing memory, or null if relationship is 'new' or no single match exists."
    }}

    IMPORTANT DOMAIN RULES:
    - Tech & Tools vs. Languages: Coding languages (e.g., Python, Rust, Java) are learned skills. Software/Tools (e.g., VS Code, PyCharm, MacOS) are used to perform tasks. They operate independently.
    - Number Formatting: Word forms and numeric forms are identical (e.g., "Fourth" == "4").
    - Age/Time: "Turned 22 this year" is an update to an older age, but a duplicate if the system already knows they are 22.
    """

    MEMORY_SCHEMA = {
        "type": "object",
        "properties": {
            "relationship": {
                "type": "string",
                "enum": ["new", "duplicate", "update", "conflict", "uncertain"],
            },
            "matched_fact": {"type": ["string", "null"]},
        },
        "required": ["relationship", "matched_fact"],
    }

    payload = {
        "model": model_name,
        "prompt": memory_prompt,
        "stream": False,
        "format": MEMORY_SCHEMA,
        "options": {"temperature": 0, "seed": 42},
    }

    response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=300)
    response.raise_for_status()
    data = response.json()

    result = json.loads(data["response"])
    return result

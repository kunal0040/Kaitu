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

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    data = response.json()
    return data["message"]["content"]


def analyze_memory(new_fact, existing_facts, model_name=MEMORY_MODEL):

    memory_prompt = f"""
    You are Kaitu's Memory Relationship Engine. Your sole function is to evaluate ONE new fact about the user against a list of existing facts and output a strict JSON classification.

    You evaluate the logical and semantic relationship based on Entity-Attribute-Value (EAV) extraction. You do not converse, summarize, or verify real-world truth.

    ### THE 5 RELATIONSHIP CLASSES

    1. "new"
    The new fact introduces independent, non-redundant information.
    Trigger "new" if:
    - Subject or Attribute is fundamentally different.
    - Granularity Addition: The new fact is a specific subset of an existing broad fact (e.g., existing: "I like programming", new: "I specialize in Python").
    - Collection Addition: The new fact adds an item to a plural/multi-value attribute (e.g., existing: "I visited France", new: "I visited Japan").
    - Historical/Static facts that do not overwrite each other (e.g., owning two different laptops).

    2. "duplicate"
    The new fact is semantically identical or entirely subsumed by an existing fact.
    Trigger "duplicate" if:
    - They share the exact same Entity + Attribute + Value meaning.
    - Ignore differences in grammar, syntax, synonyms, first-person phrasing, or temporal framing that implies the same current state.
    - Examples: "I am a student" == "I study at school"; "I love dogs" == "Dogs are my favorite animals".

    3. "update"
    The new fact provides a newer/current value for a STRICTLY MUTABLE, single-state attribute.
    Trigger "update" if:
    - The attribute can logically only hold one primary value at a time (e.g., current age, current city, current semester, relationship status, active primary device).
    - The text implies a transition (e.g., "now", "moved to", "switched", "started").
    - Note: If the user explicitly states they have multiple of an item (e.g., two cars), treat as "new", not "update".
    - Semantic change is required. If the new value means the same thing as the old, use "duplicate".

    4. "conflict"
    The new fact logically contradicts an existing fact, and it cannot be explained by the passage of time (an update).
    Trigger "conflict" if:
    - Direct negation (e.g., "I have a sister" vs "I am an only child").
    - Mutually exclusive absolute claims (e.g., "I have never left the US" vs "I went to London").
    - Do NOT use for standard progression (e.g., Semester 3 -> Semester 4 is an "update").

    5. "uncertain"
    Trigger "uncertain" ONLY if:
    - The new fact is too vague to extract an Entity-Attribute-Value.
    - It is impossible to determine if a state change is an "update" or a "conflict" without querying the user.

    ### EVALUATION PROTOCOL (Run silently)
    1. Extract (Entity + Attribute + Value) from New Fact.
    2. Scan Existing Facts for the same Entity + Attribute.
    3. If no match -> "new".
    4. If match exists, compare Values:
    - Same meaning -> "duplicate"
    - Different meaning, attribute is single-state/mutable -> "update"
    - Different meaning, attribute is multi-state/collection -> "new"
    - Logical impossibility without time progression -> "conflict"

    Existing memories: 
    {existing_facts}

    New fact: 
    {new_fact}

    ### OUTPUT CONSTRAINTS
    Return ONLY raw, valid JSON. 
    Do NOT wrap the output in markdown code blocks (no ```json or ```).
    Do NOT include any explanations, prefixes, or suffixes.

    {{
        "relationship": "new|duplicate|update|conflict|uncertain",
        "matched_fact": "Exact text of the relevant existing memory, or null if relationship is 'new' or no single match exists."
    }}
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

    response = requests.post("http://localhost:11434/api/generate", json=payload)
    response.raise_for_status()
    data = response.json()

    result = json.loads(data["response"])
    return result

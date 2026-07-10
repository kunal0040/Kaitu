import requests
import json
import time
from config import SYSTEM_PROMPT
from memory import load_memory, get_conversation_history

OLLAMA_URL = "http://localhost:11434/api/chat"
FAST_MODEL = "qwen2.5:3b"
THINKING_MODEL = "dolphin3"
MEMORY_MODEL = "phi4-mini"

memory = load_memory()

memory_context = f"""
Known information about the user:
{memory}
"""


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


if __name__ == "__main__":

    tests = [
        # ==================== NEW ====================
        ("My mother's name is Pooja", ["My name is Kunal Bhargav"], "new"),
        ("I use VS Code for coding", ["I program in Python"], "new"),
        ("I have completed HTML", ["I am learning Python"], "new"),
        ("I enjoy story-driven games", ["I play badminton"], "new"),
        ("My laptop has 16 GB RAM", ["My laptop is an Asus TUF A15"], "new"),
        ("I am the class representative", ["I study VLSI Engineering"], "new"),
        ("I want to build a voice assistant", ["I built a banking system"], "new"),
        ("I usually code after midnight", ["I prefer studying at night"], "new"),
        ("I have played Red Dead Redemption 2", ["I play God of War"], "new"),
        ("I am interested in GATE preparation", ["My CGPA is 7.85"], "new"),
        # ================= DUPLICATE =================
        ("Python is a language I program in", ["I program in Python"], "duplicate"),
        (
            "I am pursuing a VLSI Engineering degree",
            ["I study VLSI Engineering"],
            "duplicate",
        ),
        (
            "My notebook computer is an Asus TUF A15",
            ["My laptop is an Asus TUF A15"],
            "duplicate",
        ),
        ("I like to play badminton", ["I enjoy playing badminton"], "duplicate"),
        (
            "I prefer doing my studies during nighttime",
            ["I prefer studying at night"],
            "duplicate",
        ),
        ("My CGPA currently stands at 7.85", ["My current CGPA is 7.85"], "duplicate"),
        (
            "I am currently a fourth-semester student",
            ["I am in Semester 4"],
            "duplicate",
        ),
        ("Kaitu was created by me", ["I created Kaitu"], "duplicate"),
        ("I use an Oppo K13 5G as my phone", ["My phone is Oppo K13 5G"], "duplicate"),
        (
            "Shanvi is my sibling and she is my sister",
            ["Shanvi is my sister"],
            "duplicate",
        ),
        # =================== UPDATE ==================
        ("My CGPA is now 8.3", ["My CGPA is 7.85"], "update"),
        ("I have moved to Delhi", ["I currently live in Patna"], "update"),
        ("I am now in Semester 5", ["I am in Semester 4"], "update"),
        (
            "I switched my primary phone to a Pixel 9",
            ["My current phone is Oppo K13 5G"],
            "update",
        ),
        (
            "I have finished building the Banking System",
            ["I am currently building the Banking System"],
            "update",
        ),
        (
            "I now study from 10 PM to 2 AM",
            ["I usually study from 9 PM to 12 AM"],
            "update",
        ),
        ("I stopped preparing for GATE", ["I am preparing for GATE"], "update"),
        (
            "I am now learning C++ instead of Python",
            ["I am currently focusing on learning Python"],
            "update",
        ),
        ("My current SGPA is 8.5", ["My current SGPA is 8.0"], "update"),
        (
            "I changed Kaitu's thinking model to Dolphin3",
            ["Kaitu's thinking model is Qwen3 4B"],
            "update",
        ),
        # ================= CONFLICT ==================
        ("I do not know Python", ["I program in Python"], "conflict"),
        ("I have never played badminton", ["I regularly play badminton"], "conflict"),
        ("I do not have a sister", ["Shanvi is my sister"], "conflict"),
        ("I did not create Kaitu", ["I created Kaitu"], "conflict"),
        (
            "I have never studied VLSI Engineering",
            ["I study VLSI Engineering"],
            "conflict",
        ),
        ("I own no computer", ["I own an Asus TUF A15 laptop"], "conflict"),
        ("I hate story-driven games", ["I love story-driven games"], "conflict"),
        ("I never study at night", ["I prefer studying at night"], "conflict"),
        ("My name is not Kunal", ["My name is Kunal"], "conflict"),
        ("I have never used VS Code", ["I use VS Code for coding"], "conflict"),
        # ================= UNCERTAIN =================
        ("Things are different now", ["I study VLSI Engineering"], "uncertain"),
        ("I changed it", ["My phone is Oppo K13 5G"], "uncertain"),
        ("Maybe I don't like it anymore", ["I enjoy badminton"], "uncertain"),
        ("My situation has changed", ["I live in Patna"], "uncertain"),
        ("That is no longer true", ["I am learning Python"], "uncertain"),
        # =============== MULTI-MEMORY ===============
        (
            "I built a Flask website",
            [
                "I program in Python",
                "I know HTML and CSS",
                "I play badminton",
                "I study VLSI Engineering",
            ],
            "new",
        ),
        (
            "I am pursuing VLSI Engineering",
            [
                "I program in Python",
                "I study VLSI Engineering",
                "I own an Asus TUF A15",
                "I play badminton",
            ],
            "duplicate",
        ),
        (
            "My CGPA has increased to 8.2",
            [
                "I study VLSI Engineering",
                "My CGPA is 7.85",
                "I am in Semester 4",
                "I play badminton",
            ],
            "update",
        ),
        (
            "I have never learned Python",
            [
                "I study VLSI Engineering",
                "I program in Python",
                "I know HTML and CSS",
                "I play badminton",
            ],
            "conflict",
        ),
        (
            "I recently changed that",
            [
                "My CGPA is 7.85",
                "My phone is Oppo K13 5G",
                "I am in Semester 4",
                "I study VLSI Engineering",
            ],
            "uncertain",
        ),
    ]
    correct = 0

    start_time = time.time()

    for new_fact, existing_facts, expected in tests:
        result = analyze_memory(
            new_fact,
            existing_facts,
        )

        action = result["relationship"]

        passed = action == expected

        if passed:
            correct += 1

        print(
            f"{'PASS' if passed else 'FAIL'} | "
            f"Expected: {expected} | "
            f"Got: {action}"
        )

    print(f"\nScore: {correct}/{len(tests)}")

    total_time = time.time() - start_time
    print(f"Total time: {total_time:.2f}s")

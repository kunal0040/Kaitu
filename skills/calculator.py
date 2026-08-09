import re
import random
from local_responses import normalize_input

SYMBOLS_REPLACEMENTS = {
    "plus": "+",
    "add": "+",
    "added to": "+",
    "minus": "-",
    "subtract": "-",
    "subtracted by": "-",
    "times": "*",
    "multiplied by": "*",
    "multiply by": "*",
    "divided by": "/",
    "divide by": "/",
    "over": "/",
    "to the power of": "**",
    "raised to the power of": "**",
    "power": "**",
    "squared": "**2",
    "cubed": "**3",
    "square root of": "**0.5",
    "percent of": "*0.01*",
    "percentage of": "*0.01*",
    "percent": "*0.01",
    "percentage": "*0.01",
}

MATH_ANSWER_PREFIXS = [
    "The answer is",
    "The final result is",
    "Therefore, we get",
    "Thus, the solution is",
    "Hence, the value is",
    "This simplifies to",
    "Evaluating this yields",
    "Which gives us",
    "The calculated value is",
    "The result evaluates to",
    "So, the answer is",
    "The mathematical solution is",
    "It follows that the answer is",
    "The computed result is",
]


def clean_math_expression(text: str) -> str:
    text = text.lower().strip()

    text = re.sub(
        r"(\d+\.?\d*)\s*(?:percent|percentage|%)\s+of\s+(\d+\.?\d*)",
        r"(\1*0.01*\2)",
        text,
    )

    text = re.sub(r"(\d+\.?\d*)\s*(?:percent|percentage)", r"(\1*0.01)", text)
    text = re.sub(r"(\d+\.?\d*)\s*%", r"(\1*0.01)", text)

    for word, symbol in sorted(
        SYMBOLS_REPLACEMENTS.items(), key=lambda x: len(x[0]), reverse=True
    ):
        text = re.sub(rf"\b{re.escape(word)}\b", symbol, text)

    return text


def execute_calculations(target: str) -> str:
    if not target or not str(target).strip():
        return "I didn't catch the numbers you wanted me to evaluate."

    expression = clean_math_expression(str(target))

    safe_expression = re.sub(r"[^0-9\+\-\*\/\(\)\.\s]", "", expression)

    safe_expression = re.sub(r"(\d)\s*\(", r"\1*(", safe_expression) 
    safe_expression = re.sub(r"\)\s*(\d)", r")*\1", safe_expression)  
    safe_expression = re.sub(r"\)\s*\(", r")*(", safe_expression)  
    safe_expression = re.sub(r"\s+", "", safe_expression)

    if not safe_expression:
        return "That doesn't sound like a valid math problem."

    prefix = random.choice(MATH_ANSWER_PREFIXS)

    try:
        result = eval(safe_expression, {"__builtins__": {}})

        if not isinstance(result, (int, float)):
            return "I couldn't compute that exact expression."

        if isinstance(result, float) and result.is_integer():
            result = int(result)
        elif isinstance(result, float):
            result = round(result, 10) 
            if result.is_integer():
                result = int(result)

        return f"{prefix} {result}."

    except ZeroDivisionError:
        return "I cannot divide by zero."
    except Exception:
        return "I couldn't compute that exact expression."


def looks_like_math_expression(user_input: str) -> bool:
    if not user_input:
        return False

    normalized = normalize_input(user_input)
    if not normalized:
        return False

    if not re.search(r"\d", normalized):
        return False

    if re.fullmatch(r"[\d\.\s\+\-\*/\(\)%=<>!]+", normalized):
        return True


    math_keywords = [
        "plus", "add", "minus", "subtract", "times", "multiplied", "multiply",
        "divided", "divide", "over", "power", "squared", "cubed", "square root",
        "percent", "percentage", "calculate", "what is", "what's", "compute",
        "equals", "equal to"
    ]

    has_keyword = any(keyword in normalized for keyword in math_keywords)
    has_operator = bool(re.search(r"[\+\-\*/%]", normalized))

    return has_keyword or has_operator
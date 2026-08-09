import re
import random
from local_responses import normalize_input

SYMBOLS_REPLACEMENTS = {
    "plus": "+",
    "add": "+",
    "minus": "-",
    "subtract": "-",
    "times": "*",
    "multiplied by": "*",
    "multiply by": "*",
    "divided by": "/",
    "divide by": "/",
    "over": "/",
    "to the power of": "**",
    "power": "**",
    "mod": "%",
    "modulo": "%",
    "squared": "**2",
    "cubed": "**3",
    "square root of": "**0.5",
    "percent": "/ 100",
    "equals": "==",
    "equal to": "==",
    "is equal to": "==",
    "not equal to": "!=",
    "is not equal to": "!=",
    "greater than": ">",
    "is greater than": ">",
    "less than": "<",
    "is less than": "<",
    "greater than or equal to": ">=",
    "less than or equal to": "<=",
    "equals sign": "=",
    "open parenthesis": "(",
    "open paren": "(",
    "close parenthesis": ")",
    "close paren": ")",
    "open bracket": "[",
    "close bracket": "]",
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
    text = text.lower()

    for word, symbol in SYMBOLS_REPLACEMENTS.items():
        text = re.sub(rf"\b{word}\b", symbol, text)

    return text


def execute_calculations(target: str) -> str:
    if not target:
        return "I didn't catch the numbers you wanted me to evaluate."

    expression = clean_math_expression(target)

    safe_expression = re.sub(r"[^0-9\+\-\*\/\(\)\.\% ]", "", expression)
    safe_expression = re.sub(r"(\d)\s*\(", r"\1*(", safe_expression)

    prefix = random.choice(MATH_ANSWER_PREFIXS)

    if not safe_expression.strip():
        return "That doesn't sound like a valid math problem."

    try:
        result = eval(safe_expression, {"__builtins__": {}})

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return f"{prefix} {result}."

    except ZeroDivisionError:
        return "I cannot divide by zero."

    except Exception:
        return "I couldn't compute that exact expression."


MATH_EXPRESSION_PATTERN = re.compile(r"^[\d\.\s\+\-\*/\(\)%=<>!]+$")


def looks_like_math_expression(user_input):
    normalized_input = normalize_input(user_input)

    if not normalized_input:
        return False

    if not re.search(r"\d", normalized_input):
        return False

    return bool(MATH_EXPRESSION_PATTERN.fullmatch(normalized_input))

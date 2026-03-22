import sys
import re
import math
import operator
# not using any LLM 
# python router.py "what's 3 * 4"
# # → Called multiply(3, 4) = 12

# python router.py "divide 10 by 2"
# # → Called divide(10, 2) = 5.0

# python router.py "add 100 and 250"
ROUTES = {
    ("add", "plus", "sum", "+"):                operator.add,
    ("subtract", "minus", "difference", "-"):   operator.sub,
    ("multiply", "times", "product", "*", "x"): operator.mul,
    ("divide", "divided", "quotient", "/"):     operator.truediv,
    ("power", "pow", "exponent", "**", "^"):    math.pow,
    ("sqrt", "square root"):                    lambda a, _: math.sqrt(a),
    ("log", "logarithm"):                       math.log,
    ("factorial",):                             lambda a, _: math.factorial(int(a)),
}

def extract_numbers(query: str) -> list[float]:
    return [float(n) for n in re.findall(r"-?\d+\.?\d*", query)]

def route(query: str):
    query_lower = query.lower()

    fn = None
    fn_label = None
    for keywords, func in ROUTES.items():
        if any(kw in query_lower for kw in keywords):
            fn = func
            fn_label = keywords[0]
            break

    if fn is None:
        print("Could not determine operation from query.")
        return

    numbers = extract_numbers(query)
    if len(numbers) < 1:
        print("Could not find any numbers in query.")
        return

    a = numbers[0]
    b = numbers[1] if len(numbers) > 1 else None

    a = int(a) if isinstance(a, float) and a.is_integer() else a
    if isinstance(b, float) and b is not None and b.is_integer():
        b = int(b)

    try:
        result = fn(a, b)
        args_str = f"{a}, {b}" if b is not None else f"{a}"
        print(f"→ Called {fn_label}({args_str}) = {result}")
        return result
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python router.py \"what's 3 * 4?\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    route(query)
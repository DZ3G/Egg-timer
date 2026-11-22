"""A simple command-line calculator.

Type expressions like `2 + 3 * (4 - 1)` and press Enter. Type `q` to quit.
Expressions are parsed with `ast`, so only arithmetic is allowed (no eval).
"""
import ast
import operator

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")


def calculate(expression: str):
    """Evaluate an arithmetic expression and return the result."""
    return _eval(ast.parse(expression, mode="eval"))


def main():
    print("Simple calculator. Operators: + - * / // % ** and parentheses. 'q' quits.")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.lower() in {"q", "quit", "exit"}:
            break
        if not line:
            continue
        try:
            print(calculate(line))
        except ZeroDivisionError:
            print("Error: division by zero")
        except (ValueError, SyntaxError, OverflowError):
            print("Error: invalid expression")


if __name__ == "__main__":
    main()

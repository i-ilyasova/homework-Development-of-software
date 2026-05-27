from fastapi import FastAPI, HTTPException
import re

app = FastAPI(title="Calculator API")

_state = {"expression": ""}


def _safe_eval(expression: str) -> float:
    if not re.fullmatch(r"[\d\s\+\-\*\/\.\(\)]+", expression):
        raise ValueError("Invalid characters in expression")
    return eval(expression)


@app.get("/add")
def add(a: float, b: float):
    return {"a": a, "b": b, "result": a + b}


@app.get("/subtract")
def subtract(a: float, b: float):
    return {"a": a, "b": b, "result": a - b}


@app.get("/multiply")
def multiply(a: float, b: float):
    return {"a": a, "b": b, "result": a * b}


@app.get("/divide")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    return {"a": a, "b": b, "result": a / b}


@app.get("/operate")
def operate(a: float, op: str, b: float):
    operations = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
    }
    if op not in operations:
        raise HTTPException(status_code=400, detail=f"Unknown operator '{op}'. Use: +, -, *, /")
    if op == "/" and b == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    return {"a": a, "op": op, "b": b, "result": operations[op](a, b)}


@app.get("/calculate")
def calculate(expression: str):
    try:
        result = _safe_eval(expression)
        return {"expression": expression, "result": result}
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Division by zero")
    except (ValueError, SyntaxError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/expression")
def set_expression(expression: str):
    _state["expression"] = expression
    return {"expression": _state["expression"]}


@app.get("/expression")
def get_expression():
    return {"expression": _state["expression"]}


@app.get("/expression/result")
def execute_expression():
    if not _state["expression"]:
        raise HTTPException(status_code=400, detail="Expression is not set")
    try:
        result = _safe_eval(_state["expression"])
        return {"expression": _state["expression"], "result": result}
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Division by zero")
    except (ValueError, SyntaxError) as e:
        raise HTTPException(status_code=400, detail=str(e))

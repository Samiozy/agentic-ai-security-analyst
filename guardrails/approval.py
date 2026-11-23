"""Human-in-the-loop gate. No action executes unless approval is typed.

Approval is per action, never cached, and remains separate from model output.
"""
def require_approval(description: str, *, input_fn=input) -> bool:
    print(f"\nPROPOSED ACTION: {description}")
    print("Type APPROVE to execute this ONE action, anything else rejects it.")
    return input_fn("Approval > ").strip() == "APPROVE"

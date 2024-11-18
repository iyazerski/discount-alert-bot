from pydantic import ValidationError


def extract_error_message(e: Exception) -> str:
    if isinstance(e, ValidationError):
        error_msgs = []
        for error in e.errors():
            field = ".".join(str(loc) for loc in error.get("loc", []))
            msg = error.get("msg", "")
            error_msgs.append(f"{field}: {msg}")
        error_text = "\n".join(error_msgs)
    else:
        error_text = str(e)

    return f"```\n{error_text}\n```"

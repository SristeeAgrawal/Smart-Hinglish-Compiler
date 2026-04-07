
def simple_parser(code):
    errors = []
    lines = code.split("\n")

    for i, line in enumerate(lines, start=1):

        stripped_line = line.strip()

        # Skip empty lines
        if not stripped_line:
            continue

        #  Normalize keywords (same as compiler)
        normalized = stripped_line.lower()

        #  Condition check (if / while)
        if ("agar" in normalized or "jabtak" in normalized or 
            "if" in normalized or "while" in normalized):
            
            if not stripped_line.endswith(":"):
                errors.append(f"Line {i}: Missing ':' in condition")

        #  Function check
        if "function" in normalized:
            parts = stripped_line.split()
            if len(parts) < 2:
                errors.append(f"Line {i}: Function name missing")

        #  Indentation check
        if i > 1:
            prev_line = lines[i-2].strip()

            if prev_line.endswith(":"):
                if not line.startswith("    "):
                    errors.append(f"Line {i}: Indentation missing")

    return errors


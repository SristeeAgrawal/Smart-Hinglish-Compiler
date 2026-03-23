def simple_parser(code):
    errors = []
    lines = code.split("\n")

    for i, line in enumerate(lines, start=1):

        stripped_line = line.strip()

        # 🔹 Check for missing colon
        if ("agar" in stripped_line or "jabtak" in stripped_line):
            if not stripped_line.endswith(":"):
                errors.append(f"Line {i}: Missing ':' in condition")

        # 🔹 Indentation check
        if i > 1:
            prev_line = lines[i-2].strip()   # ✅ always defined

            if prev_line.endswith(":"):
                if not line.startswith("    "):
                    errors.append(f"Line {i}: Indentation missing")

    return errors
from parser import simple_parser

def hinglish_to_code(code, language="python"):

    mapping = {
        "bolo": "print",
        "likho": "print",
        "dikhao": "print",
        "agar": "if",
        "warna": "else",
        "jabtak": "while",
        "ke_liye": "for",
        "input_lo": "input",
        "function": "function"
    }

    code = code.replace("\r\n", "\n").replace("\r", "\n")

    lines = code.split("\n")
    output_code = []

    for line in lines:
        leading_spaces = len(line) - len(line.lstrip())
        indent = " " * leading_spaces
        stripped = line.strip()

        if not stripped:
            output_code.append("")
            continue

        words = stripped.split()
        normalized = [mapping.get(word.lower(), word) for word in words]

        # FUNCTION
        if normalized[0] == "function":
            if len(normalized) < 2:
                output_code.append("# Error: function name missing")
                continue

            func_name = normalized[1]

            if language == "python":
                new_line = f"def {func_name}():"
            elif language == "c":
                new_line = f"void {func_name}() {{"
            elif language == "java":
                new_line = f"public static void {func_name}() {{"
            else:
                new_line = "Unsupported language"

            output_code.append(indent + new_line)
            continue

        # ELSE
        if normalized[0] == "else":
            if language == "python":
                new_line = "else:"
            elif language in ["c", "java"]:
                new_line = "else {"
            else:
                new_line = "Unsupported language"

            output_code.append(indent + new_line)
            continue

        
        # PRINT (FINAL SAFE FIX)
        if stripped.lower().startswith(("bolo", "likho", "dikhao")):

            # Extract value safely
            parts = stripped.split(maxsplit=1)
            value = parts[1] if len(parts) > 1 else ""

            # Case 1: bolo("Hello")
            if "(" in stripped and ")" in stripped:
                new_line = stripped.replace("bolo", "print") \
                                .replace("likho", "print") \
                                .replace("dikhao", "print")

                # extract inner value for C/Java
                value = stripped[stripped.find("(")+1 : stripped.rfind(")")]
                value = value.replace('"', '')

            # Case 2: bolo hello
            else:
                new_line = f'print("{value}")'

            if language == "python":
                output_code.append(indent + new_line)

            elif language == "c":
                output_code.append(indent + f'printf("{value}\\n");')

            elif language == "java":
                output_code.append(indent + f'System.out.println("{value}");')

            continue



        # DEFAULT
        new_line = " ".join(normalized)
        output_code.append(indent + new_line)

    return "\n".join(output_code)


# Wrapper function
def compile_code(code, language="python"):

    errors = simple_parser(code)

    if errors:
        return "\n".join(errors)

    return hinglish_to_code(code, language)


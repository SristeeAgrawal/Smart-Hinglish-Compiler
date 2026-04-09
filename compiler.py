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
        "function": "def"
    }

    code = code.replace("\r\n", "\n").replace("\r", "\n")
    lines = code.split("\n")
    output_code = []
    
    # C/Java mein Boilerplate handle karne ke liye
    if language in ["c", "java"]:
        if language == "c":
            output_code.append("#include <stdio.h>\n\nint main() {")
        else:
            output_code.append("public class Main {\n    public static void main(String[] args) {")
        indent_base = "    "
    else:
        indent_base = ""

    for line in lines:
        leading_spaces = len(line) - len(line.lstrip())
        indent = (indent_base + (" " * leading_spaces))
        stripped = line.strip()

        if not stripped:
            output_code.append("")
            continue

        # Condition logic (agar / if)
        if stripped.lower().startswith(("agar", "if")):
            condition = stripped.replace("agar", "").replace("if", "").replace(":", "").strip()
            if language == "python":
                new_line = f"if {condition}:"
            else:
                new_line = f"if ({condition}) {{"
            output_code.append(indent + new_line)
            continue

        # Else logic (warna / else)
        if stripped.lower().startswith(("warna", "else")):
            if language == "python":
                new_line = "else:"
            else:
                new_line = "} else {"
            output_code.append(indent + new_line)
            continue

        # 1. FUNCTION LOGIC (Fix: def greet():)
        if stripped.lower().startswith("function"):
            parts = stripped.split()
            if len(parts) >= 2:
                # Bracket hatakar saaf naam nikalo
                func_name = parts[1].replace("(", "").replace(")", "").replace(":", "").strip()
                
                if language == "python":
                    new_line = f"def {func_name}():" # Sahi Python Syntax
                elif language == "c":
                    new_line = f"void {func_name}() {{"
                else:
                    new_line = f"public static void {func_name}() {{"
                
                output_code.append(indent + new_line)
                continue

        # 2. PRINT LOGIC (Fix: print("hello"))
        if stripped.lower().startswith(("bolo", "likho", "dikhao")):
            # Content nikalo
            if "(" in stripped and ")" in stripped:
                content = stripped[stripped.find("(")+1 : stripped.rfind(")")]
            else:
                parts = stripped.split(maxsplit=1)
                content = parts[1] if len(parts) > 1 else ""
            
            # Agar content ke aas-paas quotes nahi hain, toh quotes add karo (string treatment)
            # Lekin agar wo koi number hai, toh quotes mat lagao
            if not (content.startswith('"') or content.startswith("'")) and not content.isdigit():
                content = f'"{content}"'

            if language == "python":
                output_code.append(indent + f"print({content})")
            elif language == "c":
                output_code.append(indent + f'printf("%s\\n", {content});')
            else:
                output_code.append(indent + f"System.out.println({content});")
            continue
        
        # Variable handling for C/Java (Basic detection)
        if "=" in stripped and not (stripped.startswith("if") or "==" in stripped):
            if language in ["c", "java"]:
                parts = stripped.split("=")
                var_name = parts[0].strip()
                val = parts[1].strip()
                # Agar value number hai toh 'int' laga do, else assume it's already declared
                prefix = "int " if val.isdigit() else ""
                output_code.append(indent + f"{prefix}{var_name} = {val};")
                continue

        # Default fallback
        words = stripped.split()
        normalized = [mapping.get(word.lower(), word) for word in words]
        output_code.append(indent + " ".join(normalized))

    # Closing braces for C/Java
    if language in ["c", "java"]:
        output_code.append("    }\n}") if language == "java" else output_code.append("    return 0;\n}")

    return "\n".join(output_code)

# Wrapper function
def compile_code(code, language="python"):
    errors = simple_parser(code)
    if errors:
        return "\n".join(errors)
    return hinglish_to_code(code, language)

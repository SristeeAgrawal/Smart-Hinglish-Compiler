from flask import Flask, render_template, request
from compiler import compile_code
import io
import sys
import traceback
from parser import simple_parser

app = Flask(__name__)   

@app.route("/", methods=["GET"])
def home():
    hinglish_code = request.args.get("code", "")
    return render_template("index.html", hinglish_code=hinglish_code)


@app.route("/result", methods=["POST"])
def result():
    language = request.form.get("language", "python")
    hinglish_code = request.form["code"]
    generated_code = compile_code(hinglish_code, language)

    output = ""

    # 🔹 Parser check
    parse_errors = simple_parser(hinglish_code)
    if parse_errors:
        output = "❌ Syntax Errors:\n\n" + "\n".join(parse_errors)
        return render_template(
            "result.html",
            generated_code=generated_code,
            language=language,
            output=output,
            hinglish_code=hinglish_code
        )

    try:
        user_input = request.form.get("user_input", "")

        # ✅ ONLY PYTHON EXECUTION
        if language == "python":
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()

            exec(generated_code, {"input": lambda _: user_input})

            output = sys.stdout.getvalue()
            sys.stdout = old_stdout

        else:
            output = f"⚠ Execution not supported for {language.upper()}"

    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)

        output = f"❌ {error_type}\n💡 {error_msg}"

    return render_template(
        "result.html",
        generated_code=generated_code,
        output=output,
        hinglish_code=hinglish_code,
        language=language
    )


if __name__ == "__main__":
    app.run(debug=True)


🚀 Smart Hinglish Compiler
Smart Hinglish Compiler ek lightweight tool hai jo Hinglish (Hindi + English) commands ko standard programming languages jaise Python, C, aur Java mein convert karta hai. Ye un logo ke liye best hai jo apni natural bhasha mein coding seekhna chahte hain.

✨ Features
Hinglish Syntax: agar, warna, jabtak, aur bolo jaise keywords ka support.

Multi-Language Support: Ek hi Hinglish code se Python, C, aur Java code generate karein.

Smart Formatting: C aur Java ke liye automatic Boilerplate (#include, main()) aur Semicolons add karta hai.

Function Support: Hinglish mein functions define karein aur unhe execute karein.

Error Handling: parser.py ki madad se syntax aur indentation errors detect karta hai.

🛠️ Tech Stack
Python 3.x

Regex (re module) for Lexical Analysis

Custom Parser for Syntax Validation

💻 Example Code
Hinglish Input:
function greet
    bolo "Hello World"

x = 10
agar x > 5:
    bolo "Bada hai"
warna:
    bolo "Chhota hai"

greet()


Generated Python Output:

def greet():
    print("Hello World")

x = 10
if x > 5:
    print("Bada hai")
else:
    print("Chhota hai")

greet()

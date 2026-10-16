
import tkinter as tk
import re

# Main window
root = tk.Tk()
root.title("Gowtham - Smart Calculator")
root.geometry("360x560")
root.resizable(False, False)
root.configure(bg="#171923")

expression = ""
just_calculated = False

# Display area
tk.Label(
    root,
    text="SMART CALCULATOR",
    font=("Arial", 16, "bold"),
    bg="#171923",
    fg="#8b9cff"
).pack(pady=(20, 12))

display_frame = tk.Frame(root, bg="#222635", padx=15, pady=15)
display_frame.pack(fill="x", padx=15, pady=5)

expression_label = tk.Label(
    display_frame,
    text="",
    font=("Arial", 15),
    bg="#222635",
    fg="#a8b0c5",
    anchor="e"
)
expression_label.pack(fill="x", pady=(0, 10))

answer_var = tk.StringVar(value="0")

tk.Label(
    display_frame,
    textvariable=answer_var,
    font=("Arial", 30, "bold"),
    bg="#222635",
    fg="white",
    anchor="e"
).pack(fill="x")


# Format the result
def format_result(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return f"{value:.10g}"


# Update calculation and answer automatically
def update_display():
    shown = expression.replace("*", " × ").replace("/", " ÷ ")
    shown = shown.replace("+", " + ").replace("-", " − ")
    expression_label.config(text=shown)

    # Evaluate the complete expression or its valid partial part
    candidate = expression

    while candidate:
        candidate = candidate.rstrip("+-*/.")

        if not candidate:
            break

        try:
            if not re.fullmatch(r"[0-9+\-*/. ()]+", candidate):
                break

            result = eval(candidate, {"__builtins__": None}, {})

            if isinstance(result, (int, float)):
                if result != result or abs(result) == float("inf"):
                    break

                answer_var.set(format_result(result))
                return

        except Exception:
            pass

        # Handle an incomplete expression
        candidate = candidate[:-1]

    answer_var.set("0")


# Button function
def press_button(value):
    global expression, just_calculated

    if value == "C":
        expression = ""
        just_calculated = False
        expression_label.config(text="")
        answer_var.set("0")
        return

    if value == "⌫":
        if just_calculated:
            expression = ""
            just_calculated = False
        else:
            expression = expression[:-1]

        update_display()
        return

    if value == "=":
        if expression:
            try:
                if not re.fullmatch(r"[0-9+\-*/. ()]+", expression):
                    raise ValueError

                result = eval(expression, {"__builtins__": None}, {})

                if not isinstance(result, (int, float)):
                    raise ValueError

                if result != result or abs(result) == float("inf"):
                    raise ValueError

                answer_var.set(format_result(result))
                just_calculated = True

            except Exception:
                answer_var.set("Error")

        return

    # Percentage
    if value == "%":
        match = re.search(r"(\d+\.?\d*|\.\d+)$", expression)

        if match:
            number = float(match.group(0))
            expression = (
                expression[:match.start()]
                + format_result(number / 100)
            )
            just_calculated = False
            update_display()
        return

    # Positive / negative
    if value == "±":
        match = re.search(r"(\d+\.?\d*|\.\d+)$", expression)

        if match:
            number = float(match.group(0))
            expression = (
                expression[:match.start()]
                + format_result(-number)
            )
            just_calculated = False
            update_display()
        return

    # Continue calculation after equals
    if just_calculated:
        if value in ["+", "-", "×", "÷"]:
            # Continue from the previous answer
            expression = answer_var.get()
        else:
            # Start a fresh calculation
            expression = ""

        just_calculated = False

    # Convert display operators
    if value == "×":
        value = "*"
    elif value == "÷":
        value = "/"

    # Avoid repeated decimal points
    if value == ".":
        current = re.split(r"[+\-*/]", expression)[-1]

        if "." in current:
            return

        if not current:
            value = "0."

    # Replace the previous operator when needed
    if value in ["+", "-", "*", "/"] and expression:
        if expression[-1] in ["+", "-", "*", "/"]:
            if value == "-" and expression[-1] in ["*", "/"]:
                expression += value
                update_display()
                return

            expression = expression[:-1]

    expression += value

    # This updates the answer without pressing equals
    update_display()


# Button layout
button_frame = tk.Frame(root, bg="#171923")
button_frame.pack(fill="both", expand=True, padx=12, pady=12)

buttons = [
    ("C", "#dc5967"), ("⌫", "#dc5967"),
    ("%", "#444c65"), ("÷", "#6b79d9"),
    ("7", "#2c3142"), ("8", "#2c3142"),
    ("9", "#2c3142"), ("×", "#6b79d9"),
    ("4", "#2c3142"), ("5", "#2c3142"),
    ("6", "#2c3142"), ("-", "#6b79d9"),
    ("1", "#2c3142"), ("2", "#2c3142"),
    ("3", "#2c3142"), ("+", "#6b79d9"),
    ("±", "#444c65"), ("0", "#2c3142"),
    (".", "#2c3142"), ("=", "#4caf91")
]

for index, (text, color) in enumerate(buttons):
    row = index // 4
    col = index % 4

    tk.Button(
        button_frame,
        text=text,
        font=("Arial", 16, "bold"),
        bg=color,
        fg="white",
        activebackground="#626b85",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda v=text: press_button(v)
    ).grid(
        row=row,
        column=col,
        padx=4,
        pady=4,
        sticky="nsew",
        ipady=10
    )

for row in range(5):
    button_frame.grid_rowconfigure(row, weight=1)

for col in range(4):
    button_frame.grid_columnconfigure(col, weight=1)


# Keyboard support
def keyboard_input(event):
    key = event.keysym
    char = event.char

    if char in "0123456789.":
        press_button(char)
    elif char in "+-":
        press_button(char)
    elif char == "*":
        press_button("×")
    elif char == "/":
        press_button("÷")
    elif key in ["Return", "KP_Enter"]:
        press_button("=")
    elif key == "BackSpace":
        press_button("⌫")
    elif key == "Escape":
        press_button("C")
    elif char == "%":
        press_button("%")

    return "break"


root.bind("<Key>", keyboard_input)

root.mainloop()





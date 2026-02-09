#tkinter is python's built-in GUI library
import tkinter as tk #as tk to keep code shorter
import random

# ---------- Window ----------
root = tk.Tk() #creates the main application window 
root.title("Higher or Lower") #sets the window title
root.geometry("420x420") #sets the window size, widtg x height
root.configure(bg="#1e1e2e") #sets the background colour

# ---------- Game State ----------
secret_number = None 
max_number = 100
max_guesses = None
guesses_taken = 0
difficulty = None

high_scores = { #dictionary layered by difficulty
    "Easy": None, #starts at none because no games have been won yet
    "Medium": None,
    "Hard": None
}

# ---------- Styles ----------
TITLE_FONT = ("Helvetica", 20, "bold") #fonts are tuples
TEXT_FONT = ("Helvetica", 12)

BG = "#1e1e2e"
FG = "#f8f8f2"
ACCENT = "#89b4fa"
SUCCESS = "#a6e3a1"
ERROR = "#f38ba8"
WARN = "#f9e2af"

# ---------- Functions ----------
def start_game(level):
    global secret_number, max_number, max_guesses, guesses_taken, difficulty #global lets the function modify variables defined outside it

    difficulty = level #level is the chosen difficulty
    guesses_taken = 0

    if level == "Easy": #small range, unlimited guesses
        max_number = 10
        max_guesses = None
    elif level == "Medium": #medium range, limited guesses
        max_number = 50
        max_guesses = 7
    else: #large range, fewer guesses
        max_number = 100
        max_guesses = 5

    secret_number = random.randint(1, max_number) #picks the secret number
    message_label.config(
        text=f"I'm thinking of a number between 1 and {max_number}",
        fg=ACCENT
    )
    result_label.config(text="") #clears previous results
    score_label.config(text=get_score_text()) #updates high-score display
    guess_entry.delete(0, tk.END) #clears input field
    guess_entry.focus() #moves keyboard focus into the entry box

def get_score_text(): 
    best = high_scores[difficulty] #looks up best score for the current difficulty
    return f"🏆 Best ({difficulty}): {best if best else '--'} guesses" #shows -- if no score yet

def check_guess(event=None):
    global guesses_taken

    if secret_number is None: #prevents guessing before a game starts
        return

    try:
        guess = int(guess_entry.get()) #converts to int
    except ValueError:
        result_label.config(text="Enter a valid number!", fg=ERROR)
        return

    if not (1 <= guess <= max_number):
        result_label.config(
            text=f"Enter a number between 1 and {max_number}",
            fg=WARN
        )
        return

    guesses_taken += 1 #increment attemps
    distance = abs(secret_number - guess) #measures closeness for hints

    if guess == secret_number: #player wins
        result_label.config(
            text=f"🎉 You got it in {guesses_taken} guesses!",
            fg=SUCCESS
        )

        best = high_scores[difficulty] #updates high score if there is no score yet or player used fewer guesses
        if best is None or guesses_taken < best:
            high_scores[difficulty] = guesses_taken
            score_label.config(text="🏆 NEW HIGH SCORE!", fg=SUCCESS)
        return

    hint = "Too low!" if guess < secret_number else "Too high!"

    if distance <= 3: #proximity feedback
        hint += " 🔥 Very close!"
    elif distance <= 10:
        hint += " 🌡️ Warm"
    else:
        hint += " ❄️ Cold"

    if max_guesses: #only runs if guesses are limited
        remaining = max_guesses - guesses_taken 
        hint += f"\nGuesses left: {remaining}"
        if remaining == 0: #ends the game if no guesses remain
            hint = f"💀 Out of guesses! The number was {secret_number}."
            result_label.config(text=hint, fg=ERROR)
            return

    result_label.config(text=hint, fg=FG) #updates UI with hint

def restart(): #resets UI without quitting the game
    message_label.config(text="Choose a difficulty to start", fg=ACCENT)
    result_label.config(text="")
    score_label.config(text="")
    guess_entry.delete(0, tk.END)
    guess_entry.focus()

# ---------- UI ----------
tk.Label(root, text="Higher or Lower", font=TITLE_FONT, bg=BG, fg=FG).pack(pady=10) #creates label, .pack() places it, pady adds vertical spacing

message_label = tk.Label(root, text="Choose a difficulty to start", 
                         font=TEXT_FONT, bg=BG, fg=ACCENT)
message_label.pack() #saved to a variable because its updated later

button_frame = tk.Frame(root, bg=BG)
button_frame.pack(pady=10) #a container to keep buttons aligned horizontally

# ---------- Custom Label Buttons ----------
def make_button(parent, text, command):
    btn = tk.Label(
        parent,
        text=text,
        width=10,
        bg="#313244",
        fg=FG,
        font=TEXT_FONT,
        padx=10,
        pady=5,
        cursor="hand2"
    )
    btn.bind("<Button-1>", lambda e: command()) #>Button-1? is left mouse click #lambda lets you call command later
    btn.bind("<Enter>", lambda e: btn.config(bg="#45475a")) 
    btn.bind("<Leave>", lambda e: btn.config(bg="#313244"))
    return btn

for level in ["Easy", "Medium", "Hard"]: 
    make_button(
        button_frame,
        level,
        lambda l=level: start_game(l) #captures the current value #prevents all buttons from using "Hard"
    ).pack(side="left", padx=5)

# ---------- Guess Entry ----------
guess_entry = tk.Entry(root, font=TEXT_FONT, justify="center")
guess_entry.pack(pady=10)
guess_entry.bind("<Return>", check_guess) #pressing enter triggers guess

# ---------- Guess Button ----------
tk.Button(
    root,
    text="Guess",
    font=TEXT_FONT,
    bg=ACCENT,
    fg=BG,
    command=check_guess
).pack(pady=5)

# ---------- Result & Score Labels ----------
result_label = tk.Label(root, text="", wraplength=350,
                        font=TEXT_FONT, bg=BG, fg=FG)
result_label.pack(pady=10)

score_label = tk.Label(root, text="", font=TEXT_FONT, bg=BG, fg=FG)
score_label.pack()

# ---------- Restart Button ----------
tk.Button(
    root,
    text="Restart",
    font=TEXT_FONT,
    bg=ACCENT,
    fg=BG,
    command=restart
).pack(pady=5) #resets game state visually

root.mainloop() #starts the event loop, keeps the window open, without this, the app would instantly close
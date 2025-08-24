import tkinter as tk
from bot.chatbot import get_response

# Create main window
window = tk.Tk()
window.title("UneeqBot 🤖")
window.geometry("500x600")
window.resizable(False, False)
window.configure(bg="#1e1e1e")

# Headline / Chatbot name
headline = tk.Label(
    window,
    text="UneeqBot 🤖",
    font=("Segoe UI Emoji", 20, "bold"),
    fg="#ffffff",
    bg="#1e1e1e"
)
headline.grid(row=0, column=0, columnspan=2, pady=10)

# Chat display with scrollbar
chat_display = tk.Text(
    window,
    bd=1,
    bg="#2c2c2c",
    fg="#ffffff",
    font=("Segoe UI Emoji", 12),
    wrap=tk.WORD
)
chat_display.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0,5))
chat_display.config(state=tk.DISABLED)

scrollbar = tk.Scrollbar(window, command=chat_display.yview)
scrollbar.grid(row=1, column=2, sticky="ns")
chat_display.config(yscrollcommand=scrollbar.set)

# Configure row/column weights so chat display expands
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

# Entry frame for input and send button
entry_frame = tk.Frame(window, bg="#1e1e1e")
entry_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
entry_frame.grid_columnconfigure(0, weight=1)

# Entry box
user_input = tk.Entry(
    entry_frame,
    bd=1,
    bg="#2c2c2c",
    fg="#ffffff",
    font=("Arial", 12),
    insertbackground="white"
)
user_input.grid(row=0, column=0, sticky="ew", padx=(0,5))

# Send button function
def send_message(event=None):
    msg = user_input.get()
    if msg.strip() != "":
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {msg}\n", "user")
        response = get_response(msg)
        chat_display.insert(tk.END, f"UneeqBot 🤖: {response}\n\n", "bot")
        chat_display.config(state=tk.DISABLED)
        chat_display.see(tk.END)
        user_input.delete(0, tk.END)

# Send button
send_btn = tk.Button(
    entry_frame,
    text="Send",
    width=8,
    bg="#16a085",
    fg="white",
    font=("Arial", 10, "bold"),
    command=send_message
)
send_btn.grid(row=0, column=1)

# Tag colors for messages
chat_display.tag_config("user", foreground="#f1c40f")
chat_display.tag_config("bot", foreground="#1abc9c", font=("Segoe UI Emoji", 12, "italic"))

# Bind Enter key to send message
window.bind('<Return>', send_message)

# Run the GUI
window.mainloop()
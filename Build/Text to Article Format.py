from openai import OpenAI
from langdetect import detect, DetectorFactory
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Ensure consistent language detection
DetectorFactory.seed = 0

# Initialize the OpenAI client
client = OpenAI(api_key="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")

def rewrite_sentence(sentence, language, style):
    """
    Use GPT to rewrite a text into a well-structured article format.
    The function ensures the output language matches the input language.
    
    Args:
        sentence (str): The input text to rewrite.
        language (str): The detected language of the input text.
        style (str): The writing style (formal or informal).
        
    Returns:
        str: The rewritten text in article format.
    """
    try:
        # Use OpenAI's ChatCompletion to rewrite the text
        messages = [{
            "role": "user",
            "content": f"Transform the following text into a well-structured article format. Use a {style} style. Ensure the output is clear, logical, and grammatically correct. Respond in the same language as the input:\n\n\"{sentence}\""
        }]
        response = client.chat.completions.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if you prefer faster responses
            messages=messages,
            n=1,  # Only generate one suggestion
            temperature=0.7
        )
        
        # Extract the best suggestion and remove quotation marks
        best_suggestion = response.choices[0].message.content.strip()
        best_suggestion = best_suggestion.replace('"', '')  # Remove quotation marks
        return best_suggestion

    except Exception as e:
        return f"Error: {e}"

def on_submit():
    """Handle the submit button click event."""
    # Get the input sentence
    sentence = input_text.get("1.0", tk.END).strip()
    
    if not sentence:
        messagebox.showwarning("Input Error", "Please enter a text to rewrite.")
        return
    
    # Detect the language of the input
    try:
        language = detect(sentence)
        language_label.config(text=f"Detected Language: {language}")
    except:
        messagebox.showerror("Language Detection Error", "Could not detect the language of the input.")
        return
    
    # Get the selected writing style
    style = style_var.get()
    
    # Generate the best rewritten version
    output_text.delete("1.0", tk.END)  # Clear previous output
    output_text.insert(tk.END, "Generating the best rewritten version...")
    window.update()  # Update the GUI to show the loading message
    
    best_suggestion = rewrite_sentence(sentence, language, style)
    output_text.delete("1.0", tk.END)  # Clear the loading message
    output_text.insert(tk.END, best_suggestion)

# Create the main window
window = tk.Tk()
window.title("Text to Article Converter")
window.geometry("600x500")  # Set the window size

# Input Section
input_label = tk.Label(window, text="Enter a text to rewrite:", font=("Arial", 12))
input_label.pack(pady=10)

input_text = tk.Text(window, height=5, width=70, font=("Arial", 12))
input_text.pack(pady=10)

# Language Detection Label
language_label = tk.Label(window, text="Detected Language: ", font=("Arial", 12))
language_label.pack(pady=10)

# Style Selection Section
style_label = tk.Label(window, text="Choose Writing Style:", font=("Arial", 12))
style_label.pack(pady=10)

style_var = tk.StringVar(value="formal")
style_formal = tk.Radiobutton(window, text="Formal", variable=style_var, value="formal")
style_informal = tk.Radiobutton(window, text="Informal", variable=style_var, value="informal")
style_formal.pack()
style_informal.pack()

# Submit Button
submit_button = tk.Button(window, text="Rewrite Text", command=on_submit, font=("Arial", 12))
submit_button.pack(pady=10)

# Output Section
output_label = tk.Label(window, text="Best Rewritten Version:", font=("Arial", 12))
output_label.pack(pady=10)

output_text = scrolledtext.ScrolledText(window, height=10, width=70, font=("Arial", 12))
output_text.pack(pady=10)

# Run the application
window.mainloop()
from tkinter import Tk, Label, Text, Button, Scrollbar, END, messagebox
from langdetect import detect_langs, DetectorFactory
import langdetect.lang_detect_exception
import pycountry

# Set seed for consistent langdetect results
DetectorFactory.seed = 0


# Helper functions
def get_language_name(language_code):
    """
    Converts a language code to its full language name.
    :param language_code: str, ISO 639-1 code (e.g., 'en', 'fr')
    :return: str, Full name of the language
    """
    try:
        language = pycountry.languages.get(alpha_2=language_code)
        return language.name if language else "Unknown Language"
    except Exception:
        return "Unknown Language"


def detect_human_language(text):
    """
    Detects the human language of a given text input along with the confidence percentage.
    :param text: str, input text
    :return: str, detected language name with percentage of chances
    """
    if len(text.strip()) < 5:
        return "Error: Input is too short to detect a human language."

    try:
        # Using detect_langs() to get probabilities for multiple languages
        detected_languages = detect_langs(text)
        if detected_languages:
            # Get the most probable language and its probability
            most_probable_lang = detected_languages[0]
            language_code = most_probable_lang.lang
            probability = most_probable_lang.prob * 100
            language_name = get_language_name(language_code)
            return (
                f"Detected Language: {language_name} with {probability:.2f}% chances."
            )
        else:
            return "Error: Unable to detect human language. The text might be too ambiguous or insufficient."
    except langdetect.lang_detect_exception.LangDetectException:
        return "Error: Unable to detect human language. The text might be too ambiguous or insufficient."
    except Exception as e:
        return f"Error: Unexpected issue in human language detection. Details: {e}"


def detect_programming_language(code):
    """
    Rule-based detection of programming languages based on syntax and keywords.
    :param code: str, input code snippet
    :return: str, detected programming language
    """
    if len(code.strip()) < 5:
        return "Error: Input is too short to detect a programming language."

    patterns = {
        "Python": ["def ", "print(", "import ", "class ", ":"],
        "JavaScript": ["function ", "console.log", "let ", "var ", "const ", "=>"],
        "Java": ["public class", "System.out.println", "void main(", "import java."],
        "C": ["#include", "int main(", "printf(", ";"],
        "C++": ["#include", "std::cout", "using namespace std;", "std::endl"],
        "HTML": ["<!DOCTYPE html>", "<html>", "<head>", "<body>", "</html>"],
    }

    try:
        for language, keywords in patterns.items():
            if any(keyword in code for keyword in keywords):
                return language
        return "Unknown programming language. No patterns matched."
    except Exception as e:
        return f"Error: Unable to detect programming language. Details: {e}"


# GUI Application
class LanguageDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Detector App")
        self.root.geometry("600x400")

        # Labels
        self.label = Label(
            root, text="Enter your text or code below:", font=("Arial", 14)
        )
        self.label.pack(pady=10)

        # Text Input
        self.text_area = Text(root, wrap="word", font=("Arial", 12), height=10)
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)

        # Scrollbar
        self.scrollbar = Scrollbar(self.text_area, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)

        # Buttons
        self.detect_human_btn = Button(
            root,
            text="Detect Human Language",
            font=("Arial", 12),
            command=self.detect_human_language,
        )
        self.detect_human_btn.pack(pady=5)

        self.detect_programming_btn = Button(
            root,
            text="Detect Programming Language",
            font=("Arial", 12),
            command=self.detect_programming_language,
        )
        self.detect_programming_btn.pack(pady=5)

        self.detect_both_btn = Button(
            root, text="Detect Both", font=("Arial", 12), command=self.detect_both
        )
        self.detect_both_btn.pack(pady=5)

    def detect_human_language(self):
        """
        Detects and displays the human language from the input.
        """
        user_input = self.text_area.get("1.0", END).strip()
        if not user_input:
            messagebox.showerror("Error", "Input field is empty! Please provide text.")
            return

        result = detect_human_language(user_input)
        messagebox.showinfo("Human Language Detection", result)

    def detect_programming_language(self):
        """
        Detects and displays the programming language from the input.
        """
        user_input = self.text_area.get("1.0", END).strip()
        if not user_input:
            messagebox.showerror("Error", "Input field is empty! Please provide code.")
            return

        result = detect_programming_language(user_input)
        messagebox.showinfo(
            "Programming Language Detection", f"Detected Language: {result}"
        )

    def detect_both(self):
        """
        Detects and displays both human and programming languages.
        """
        user_input = self.text_area.get("1.0", END).strip()
        if not user_input:
            messagebox.showerror(
                "Error", "Input field is empty! Please provide text or code."
            )
            return

        human_language = detect_human_language(user_input)
        programming_language = detect_programming_language(user_input)
        messagebox.showinfo(
            "Both Language Detection",
            f"Detected Human Language: {human_language}\n"
            f"Detected Programming Language: {programming_language}",
        )


# Run the application
if __name__ == "__main__":
    root = Tk()
    app = LanguageDetectorApp(root)
    root.mainloop()

import flashcard_gui
import sys

if __name__ == "__main__":

    file_path = ""

    if len(sys.argv) > 1:
        file_path = sys.argv[1]

    app = flashcard_gui.FlashcardApplication()
    gui = flashcard_gui.FlashcardGUI(app, file_path)
    gui.root.mainloop()

import flashcard_gui

if __name__ == "__main__":
    app = flashcard_gui.FlashcardApplication()
    gui = flashcard_gui.FlashcardGUI(app)
    gui.root.mainloop()

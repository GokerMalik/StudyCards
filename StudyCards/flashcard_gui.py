import random
import tkinter as tk
import tkinter.simpledialog
import tkinter.filedialog

import json

#define the flashcard class
class Flashcard:
    def __init__(self, front, back):
        self.front = front
        self.back = back

#define the deck class
class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, front, back):
        self.cards.append(Flashcard(front, back))

    def remove_card(self, index):
        self.cards.pop(index)

#define caregory class
class Category:
    def __init__(self, name):
        self.name = name
        self.decks = []

    def add_deck(self, name):
        self.decks.append(Deck(name))

    def remove_deck(self, index):
        self.decks.pop(index)

#define the application
class FlashcardApplication:
    def __init__(self):
        self.categories = []

    def add_category(self, name):
        self.categories.append(Category(name))

    def remove_category(self, index):
        self.categories.pop(index)

    def add_deck(self, category_index, name):
        self.categories[category_index].add_deck(name)

    def remove_deck(self, category_index, deck_index):
        self.categories[category_index].remove_deck(deck_index)

    def add_card(self, category_index, deck_index, front, back):
        self.categories[category_index].decks[deck_index].add_card(front, back)

    def remove_card(self, category_index, deck_index, card_index):
        self.categories[category_index].decks[deck_index].remove_card(card_index)

    def random_flashcard(self):
        category = random.choice(self.categories)
        deck = random.choice(category.decks)
        card = random.choice(deck.cards)
        return card.front, card.back

#Create the interface elements
class FlashcardGUI:
    def __init__(self, app):
        self.app = app
        self.root = tk.Tk()
        self.root.title("Flashcards")

        self.category_frame = tk.Frame(self.root)
        self.category_frame.pack(side=tk.LEFT)

        self.deck_frame = tk.Frame(self.root)
        self.deck_frame.pack(side=tk.LEFT)

        self.card_frame = tk.Frame(self.root)
        self.card_frame.pack(side=tk.LEFT)

        self.categories_listbox = tk.Listbox(self.category_frame, selectmode=tk.SINGLE)
        self.categories_listbox.pack(side=tk.TOP)
        self.categories_listbox.bind("<<ListboxSelect>>", self.update_decks_listbox)

        self.add_category_button = tk.Button(self.category_frame, text="Add Category", command=self.add_category)
        self.add_category_button.pack(side=tk.TOP)

        self.remove_category_button = tk.Button(self.category_frame, text="Remove Category", command=self.remove_category)
        self.remove_category_button.pack(side=tk.TOP)

        self.decks_listbox = tk.Listbox(self.deck_frame, selectmode=tk.SINGLE)
        self.decks_listbox.pack(side=tk.TOP)

        self.add_deck_button = tk.Button(self.deck_frame, text="Add Deck", command=self.add_deck)
        self.add_deck_button.pack(side=tk.TOP)

        self.remove_deck_button = tk.Button(self.deck_frame, text="Remove Deck", command=self.remove_deck)
        self.remove_deck_button.pack(side=tk.TOP)

        self.cards_listbox = tk.Listbox(self.card_frame)
        self.cards_listbox.pack(side=tk.TOP)

        self.add_card_button = tk.Button(self.card_frame, text="Add Card", command=self.add_card)
        self.add_card_button.pack(side=tk.TOP)

        self.remove_card_button = tk.Button(self.card_frame, text="Remove Card", command=self.remove_card)
        self.remove_card_button.pack(side=tk.TOP)

        self.random_card_button = tk.Button(self.card_frame, text="Random Card", command=self.show_random_card)
        self.random_card_button.pack(side=tk.TOP)

        self.front_label = tk.Label(self.card_frame, text="Front:")
        self.front_label.pack(side=tk.TOP)

        self.front_textbox = tk.Text(self.card_frame, height=5, width=50)
        self.front_textbox.pack(side=tk.TOP)

        self.back_label = tk.Label(self.card_frame, text="Back:")
        self.back_label.pack(side=tk.TOP)

        self.back_textbox = tk.Text(self.card_frame, height=5, width=50)
        self.back_textbox.pack(side=tk.TOP)

        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Open", command=self.open)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.root.config(menu=self.menu_bar)

        self.update_categories_listbox()

    def update_categories_listbox(self):
        self.categories_listbox.delete(0, tk.END)
        for category in self.app.categories:
            self.categories_listbox.insert(tk.END, category.name)

    def update_decks_listbox(self, event = None):
        selected_categories = self.categories_listbox.curselection()
        if selected_categories:
            selected_category_index = selected_categories[0]
            selected_category = self.app.categories[selected_category_index]
            self.decks_listbox.delete(0, tk.END)
            for deck in selected_category.decks:
                self.decks_listbox.insert(tk.END, deck.name)

    def update_cards_listbox(self, category_index, deck_index):
        self.cards_listbox.delete(0, tk.END)
        for card in self.app.categories[category_index].decks[deck_index].cards:
            self.cards_listbox.insert(tk.END, card.front)

    def add_category(self):
        category_name = tk.simpledialog.askstring("Add Category", "Enter a name for the new category:")
        if category_name:
            self.app.add_category(category_name)
            self.update_categories_listbox()

    def remove_category(self):
        category_index = self.categories_listbox.curselection()
        if category_index:
            self.app.remove_category(category_index[0])
            self.update_categories_listbox()

    def add_deck(self):
        category_index = self.categories_listbox.curselection()
        if category_index:
            deck_name = tk.simpledialog.askstring("Add Deck", "Enter a name for the new deck:")
            if deck_name:
                self.app.add_deck(category_index[0], deck_name)
                self.update_decks_listbox(category_index[0])

    def remove_deck(self):
        category_index = self.categories_listbox.curselection()
        deck_index = self.decks_listbox.curselection()
        if category_index and deck_index:
            self.app.remove_deck(category_index[0], deck_index[0])
            self.update_decks_listbox(category_index[0])
            self.update_cards_listbox(category_index[0], 0)

    def add_card(self):
        category_index = self.categories_listbox.curselection()
        deck_index = self.decks_listbox.curselection()
        if category_index and deck_index:
            front_text = self.front_textbox.get("1.0", tk.END).strip()
            back_text = self.back_textbox.get("1.0", tk.END).strip()
            if front_text and back_text:
                self.app.add_card(category_index[0], deck_index[0], front_text, back_text)
                self.update_cards_listbox(category_index[0], deck_index[0])
                self.front_textbox.delete("1.0", tk.END)
                self.back_textbox.delete("1.0", tk.END)

    def remove_card(self):
        category_index = self.categories_listbox.curselection()
        deck_index = self.decks_listbox.curselection()
        card_index = self.cards_listbox.curselection()
        if category_index and deck_index and card_index:
            self.app.remove_card(category_index[0], deck_index[0], card_index[0])
            self.update_cards_listbox(category_index[0], deck_index[0])

    def show_random_card(self):
        category_index = self.categories_listbox.curselection()
        deck_index = self.decks_listbox.curselection()
        if category_index and deck_index:
            deck = self.app.categories[category_index[0]].decks[deck_index[0]]
            if deck.cards:
                card = random.choice(deck.cards)
                tk.messagebox.showinfo(card.front, card.back)
            else:
                tk.messagebox.showerror("Error", "This deck has no cards.")

    def save(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".json")
        if file_path:
            with open(file_path, "w") as f:
                categories_json = []
                for category in self.app.categories:
                    decks_json = []
                    for deck in category.decks:
                        cards_json = []
                        for card in deck.cards:
                            cards_json.append({
                                "front": card.front,
                                "back": card.back
                            })
                        decks_json.append({
                            "name": deck.name,
                            "cards": cards_json
                        })
                    categories_json.append({
                        "name": category.name,
                        "decks": decks_json
                    })
                json.dump(categories_json, f)

    def open(self):
        file_path = tk.filedialog.askopenfilename(defaultextension=".json")
        if file_path:
            with open(file_path, "r") as f:
                categories_json = json.load(f)
                categories = []
                for category_json in categories_json:
                    category_name = category_json["name"]
                    cur_category = Category(category_name)
                    decks_json = category_json["decks"]
                    for deck_json in decks_json:
                        deck_name = deck_json["name"]
                        cards_json = deck_json["cards"]
                        cur_deck = Deck(deck_name)
                        cards = []
                        for card_json in cards_json:
                            front = card_json["front"]
                            back = card_json["back"]
                            cur_card = Flashcard(front, back)
                            cards.append(cur_card)
                            cur_deck.add_card(cur_card)
                        cur_category.add_deck(deck_name)
                    categories.append(cur_category)
                self.app.categories = categories
                self.update_categories_listbox()
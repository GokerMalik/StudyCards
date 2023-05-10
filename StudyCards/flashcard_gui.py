import random
import tkinter as tk
import tkinter.simpledialog
import tkinter.filedialog

import tkinter.messagebox

import json

#define the flashcard class
class Flashcard:
    def __init__(self, deck, front, back):
        self.deck = deck
        self.front = front
        self.back = back

#define the deck class
class Deck:
    def __init__(self, category, name, askFront, askBack):
        self.name = name
        self.cards = []
        self.category = category
        self.askFront = askFront
        self.askBack = askBack

    def add_card(self, front, back):
        self.cards.append(Flashcard(self, front, back))

    def remove_card(self, index):
        self.cards.pop(index)

#define category class
class Category:
    def __init__(self, name):
        self.name = name
        self.decks = []

    def add_deck(self, name, askFront, askBack):
        self.decks.append(Deck(self, name, askFront, askBack))

    def add_deck(self, deck):
        self.decks.append(deck)

    def remove_deck(self, index):
        self.decks.pop(index)

class Session:
    def __init__(self, gui):

        self.response_window = None
        self.session_end = 0

        self.gui = gui
        self.screen = gui.session_screen

        if gui.app.lastDeck:

            self.screen.config(bg = '#aee1e5')
            self.run_session()

        else:
            tk.messagebox.showinfo(title = "No Deck", message = "Please select a deck first")

    def run_session(self):

        deck = self.gui.app.lastDeck[0]

        card_list = []
        for card in deck.cards:
            card_list.append(card)

        front = deck.askFront
        back = deck.askBack

        screen_text = self.screen.create_text(100,50,fill="#e1924d",font="Times 20 bold", text="abc")

        while (len(card_list) > 0):

            cur_card = random.choice(card_list)

            sides = [cur_card.front, cur_card.back]

            question_side = 0
            if (front & back):
                question_side = random.choice([0,1])
            elif front:
                question_side = 0
            else:
                question_side = 1

            question = sides[question_side]
            answer = sides[question_side*(-1)+(1)]

            question_message = self.get_question_message(question)
            self.screen.itemconfig(screen_text, text=question_message)

            self.response_window = tk.Toplevel(self.gui.root)
            name_label = tk.Label(self.response_window, text= "Wrack it!")
            name_label.pack(side = tk.TOP)

            user_response = tk.StringVar()
            session_end = tk.IntVar()
            session_end.set(0)

            name_entry = tk.Entry(self.response_window, textvariable=user_response)
            name_entry.pack(side=tk.TOP)

            response_frame = tk.Frame(self.response_window)
            response_frame.pack(side = tk.TOP)

            check_button = tk.Button(response_frame, text = 'Check', command=self.response_window.destroy)
            check_button.pack(side=tk.LEFT)

            check_button = tk.Button(response_frame, text = 'Finish', command=self.end_session)
            check_button.pack(side=tk.LEFT)

            self.response_window.wait_window(self.response_window)

            if self.session_end == 1:
                break

            user_response = user_response.get()

            if answer == user_response:
                card_list.remove(cur_card)

        del self


    def end_session(self):
        self.response_window.destroy()
        self.session_end = 1

    def get_question_message(self, question):
        ## Create question card

        if (len(question) > 10):
            showQuest = ''
            wordList = question.split(" ")
            splitList = []
            
            for ind in range(len(wordList)):
                if (len(wordList[ind]) >10):

                    toModify = wordList[ind]
                    PieceNum = int(len(toModify)/10)+1
                    wordList.remove(toModify)

                    for count in range(PieceNum):
                        if (count != PieceNum-1):
                            toSend = toModify[count*10:(count+1)*10] + "-"
                            wordList.insert(ind + count, toSend)
                        else:
                            toSend = toModify[count*10:]
                            wordList.insert(ind + count, toSend)
            
            splitList.append(wordList[0])

            for word in wordList:
                if (word != wordList[0]):
                    if (len(splitList[-1] + " " + word)<=10):
                        splitList[-1] = splitList[-1] + " " + word
                    else:
                        splitList.append(word)

            for piece in splitList:
                showQuest = showQuest + piece + "\n"
            showQuest = showQuest[0:showQuest.rfind("\n")]

        else:
            showQuest = question

        return showQuest



#define the application
class FlashcardApplication:
    def __init__(self):
        self.categories = []
        self.lastCategory = None
        self.lastDeck = None

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

        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side = tk.LEFT)

        self.mid_frame = tk.Frame(self.root)
        self.mid_frame.pack(side = tk.LEFT)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side = tk.LEFT)

        self.category_frame = tk.Frame(self.left_frame)
        self.category_frame.pack(side=tk.TOP)

        self.deck_frame = tk.Frame(self.left_frame)
        self.deck_frame.pack(side=tk.TOP)

        self.session_frame = tk.Frame(self.mid_frame)
        self.session_frame.pack(side = tk.TOP)

        self.session_card_frame = tk.Frame(self.session_frame)
        self.session_card_frame.pack(side = tk.TOP)

        self.session_buttons_frame = tk.Frame(self.session_frame)
        self.session_buttons_frame.pack(side = tk.TOP)

        self.card_frame = tk.Frame(self.right_frame)
        self.card_frame.pack(side=tk.TOP)

        self.categories_listbox = tk.Listbox(self.category_frame, selectmode=tk.SINGLE)
        self.categories_listbox.pack(side=tk.TOP)
        self.categories_listbox.bind("<<ListboxSelect>>", self.category_select)

        self.add_category_button = tk.Button(self.category_frame, text="Add Category", command=self.add_category)
        self.add_category_button.pack(side=tk.TOP)

        self.remove_category_button = tk.Button(self.category_frame, text="Remove Category", command=self.remove_category)
        self.remove_category_button.pack(side=tk.TOP)

        self.decks_listbox = tk.Listbox(self.deck_frame, selectmode=tk.SINGLE)
        self.decks_listbox.pack(side=tk.TOP)
        self.decks_listbox.bind("<<ListboxSelect>>", self.deck_select)

        self.add_deck_button = tk.Button(self.deck_frame, text="Add Deck", command=self.add_deck)
        self.add_deck_button.pack(side=tk.TOP)

        self.remove_deck_button = tk.Button(self.deck_frame, text="Remove Deck", command=self.remove_deck)
        self.remove_deck_button.pack(side=tk.TOP)

        self.session_screen = tk.Canvas(self.session_card_frame, bg = self.root.cget("bg"))
        self.session_screen.pack(side = tk.TOP)

        self.start_session_button = tk.Button(self.session_buttons_frame, text="Start Session", command = self.start_session)
        self.start_session_button.pack(side=tk.LEFT)

        self.cards_listbox = tk.Listbox(self.card_frame)
        self.cards_listbox.pack(side=tk.TOP)

        self.add_card_button = tk.Button(self.card_frame, text="Add Card", command=self.add_card)
        self.add_card_button.pack(side=tk.TOP)

        self.remove_card_button = tk.Button(self.card_frame, text="Remove Card", command=self.remove_card)
        self.remove_card_button.pack(side=tk.TOP)

        self.front_label = tk.Label(self.card_frame, text="Front:")
        self.front_label.pack(side=tk.TOP)

        self.front_textbox = tk.Text(self.card_frame, height=5, width=20)
        self.front_textbox.pack(side=tk.TOP)

        self.back_label = tk.Label(self.card_frame, text="Back:")
        self.back_label.pack(side=tk.TOP)

        self.back_textbox = tk.Text(self.card_frame, height=5, width=20)
        self.back_textbox.pack(side=tk.TOP)

        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Open", command=self.open)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.root.config(menu=self.menu_bar)

        self.update_categories_listbox()

    def category_select(self, event = None):
        #fall here only when a selection is made. If category deleted, do not fall
        selected_categories = self.categories_listbox.curselection()

        if selected_categories:

            #get index
            selected_category_index = selected_categories[0]

            #update lisbox
            self.update_decks_listbox(selected_category_index)
            self.update_cards_listbox(selected_category_index, -1)

            #set last category
            selected_category = self.app.categories[selected_category_index]
            self.app.lastCategory = [selected_category]

    def deck_select(self, event = None):
        #fall here only when a selection is made. If deck deleted, do not fall
        selected_decks = self.decks_listbox.curselection()

        if selected_decks:
            #get index
            selected_deck_index = selected_decks[0]

            #if a deck is selected, last category has to exist. Actions which may change deck selection without a last category are responsible for other scenarios
            deck_category = self.app.lastCategory[0]
        
            #update cardbox
            self.update_cards_listbox(self.app.categories.index(deck_category), selected_deck_index)

            #set last deck
            selected_deck = deck_category.decks[selected_deck_index]
            self.app.lastDeck = [selected_deck]

    def update_categories_listbox(self):
        self.categories_listbox.delete(0, tk.END)
        for category in self.app.categories:
            self.categories_listbox.insert(tk.END, category.name)

    def update_decks_listbox(self, selected_category_index):
        self.decks_listbox.delete(0, tk.END)

        if selected_category_index >= 0:
            selected_category = self.app.categories[selected_category_index]
            for deck in selected_category.decks:
                self.decks_listbox.insert(tk.END, deck.name)

    def update_cards_listbox(self, category_index, deck_index):
        self.cards_listbox.delete(0, tk.END)
        if category_index >= 0 and deck_index >=0:
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
            self.update_decks_listbox(-1)
            self.update_cards_listbox(-1,-1)
        self.app.lastCategory = None

    def add_deck(self):
        if self.categories_listbox.curselection():
            category_index = self.categories_listbox.curselection()
        elif self.app.lastCategory:
            category_index = [self.app.categories.index(self.app.lastCategory[0])]

        dialog = tk.Toplevel(self.root)
        name_label = tk.Label(dialog, text= "Deck Name:")
        name_label.pack(side = tk.TOP)

        deck_name = tk.StringVar()

        name_entry = tk.Entry(dialog, textvariable=deck_name)
        name_entry.pack(side=tk.TOP)

        ask_front_var = tk.BooleanVar(value = True)
        ask_back_var = tk.BooleanVar(value = False)

        frontCheckBox = tk.Checkbutton(dialog, text = "Ask front side", variable = ask_front_var)
        backCheckBox = tk.Checkbutton(dialog, text = "Ask back side", variable = ask_back_var)

        frontCheckBox.pack(side = tk.TOP)
        backCheckBox.pack(side = tk.TOP)

        create_button = tk.Button(dialog, text = 'Create', command=dialog.destroy)
        create_button.pack(side=tk.TOP)

        dialog.wait_window(dialog)

        deck_name = deck_name.get()

        if deck_name:
            newDeck = Deck(self.app.categories[category_index[0]], deck_name, ask_front_var.get(), ask_back_var.get())
            self.app.add_deck(category_index[0], newDeck)
            self.update_decks_listbox(category_index[0])
            self.app.lastDeck = [newDeck]

    def remove_deck(self):
        deck_index = self.decks_listbox.curselection()
        category_index = [self.app.categories.index(self.app.lastCategory[0])]
        if category_index and deck_index:
            self.app.remove_deck(category_index[0], deck_index[0])
            self.update_decks_listbox(category_index[0])
            self.update_cards_listbox(category_index[0], -1)
        self.app.lastDeck = None

    def add_card(self):
        deck_index = self.decks_listbox.curselection()
        category_index = [self.app.categories.index(self.app.lastCategory[0])]

        if category_index and deck_index:
            front_text = self.front_textbox.get("1.0", tk.END).strip()
            back_text = self.back_textbox.get("1.0", tk.END).strip()
            if front_text and back_text:
                self.app.add_card(category_index[0], deck_index[0], front_text, back_text)
                self.update_cards_listbox(category_index[0], deck_index[0])
                self.front_textbox.delete("1.0", tk.END)
                self.back_textbox.delete("1.0", tk.END)

    def remove_card(self):
        card_index = self.cards_listbox.curselection()

        card = deck[0].cards[card_index[0]]
        deck = card.deck
        category = deck.category

        deck_index = [category.decks.index(deck)]
        category_index = [self.app.categories.index(category)]

        if category_index and deck_index and card_index:
            self.app.remove_card(category_index[0], deck_index[0], card_index[0])
            self.update_cards_listbox(category_index[0], deck_index[0])

    def start_session(self):

        session = Session(self)

        '''
        category_index = self.categories_listbox.curselection()
        deck_index = self.decks_listbox.curselection()
        if category_index and deck_index:
            deck = self.app.categories[category_index[0]].decks[deck_index[0]]
            if deck.cards:
                card = random.choice(deck.cards)
                tk.messagebox.showinfo(card.front, card.back)
            else:
                tk.messagebox.showerror("Error", "This deck has no cards.")
        '''

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
                            "askFront": deck.askFront,
                            "askBack": deck.askBack,
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
                        deck_askFront = deck_json["askFront"]
                        deck_askBack = deck_json["askBack"]
                        cards_json = deck_json["cards"]
                        cur_deck = Deck(cur_category, deck_name, deck_askFront, deck_askBack)
                        for card_json in cards_json:
                            front = card_json["front"]
                            back = card_json["back"]
                            cur_deck.add_card(front, back)
                        cur_category.add_deck(cur_deck)
                    categories.append(cur_category)
                self.app.categories = categories
                self.update_categories_listbox()
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

class AestheticTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Pink Cream Tic Tac Toe")
        self.root.config(bg="#FFF0F5")
        self.root.geometry("700x750")

        self.board_size = 6
        self.to_win = 4
        self.board = [""] * (self.board_size ** 2)
        self.buttons = []

        # Load flower image
        try:
            self.flower_img = ImageTk.PhotoImage(Image.open("flower.png").resize((50, 50)))
        except:
            self.flower_img = None

        # Load character GIF
        try:
            self.char_img = ImageTk.PhotoImage(Image.open("character_walk.gif").resize((60, 60)))
        except:
            self.char_img = None

        self.create_widgets()
        self.animate_character()

    def create_widgets(self):
        title = tk.Label(self.root, text="🌸 Pink Cream Tic Tac Toe 🌸",
                         font=("Comic Sans MS", 22, "bold"),
                         fg="#B83F368B", bg="#FFF0F5B9")
        title.pack(pady=10)

        # Decorative flowers
        if self.flower_img:
            tk.Label(self.root, image=self.flower_img, bg="#FFF0F5").place(x=10, y=10)
            tk.Label(self.root, image=self.flower_img, bg="#FFF0F5").place(x=630, y=10)

        # Character canvas (top animation)
        self.canvas = tk.Canvas(self.root, width=700, height=60, bg="#FFF0F5", highlightthickness=0)
        self.canvas.pack()
        if self.char_img:
            self.char = self.canvas.create_image(0, 0, image=self.char_img, anchor="nw")

        # Game grid
        self.frame = tk.Frame(self.root, bg="#FFF0F5")
        self.frame.pack()

        for i in range(self.board_size ** 2):
            btn = tk.Button(self.frame, text="", font=("Helvetica", 16, "bold"),
                            width=4, height=2,
                            bg="#FFC0CB", fg="#C71585",
                            activebackground="#FF69B4", activeforeground="white",
                            command=lambda i=i: self.make_move(i))
            btn.grid(row=i // self.board_size, column=i % self.board_size, padx=3, pady=3)
            self.buttons.append(btn)

        tk.Button(self.root, text="Restart Game", command=self.reset_board,
                  font=("Arial", 12), bg="#FFB6C1", fg="#C71585").pack(pady=15)

    def animate_character(self):
        if not hasattr(self, 'char'):
            return

        def move():
            current_x = self.canvas.coords(self.char)[0]
            new_x = current_x + 2
            if new_x > 700:
                new_x = -60
            self.canvas.coords(self.char, new_x, 0)
            self.root.after(50, move)

        move()

    def make_move(self, index):
        if self.board[index] == "":
            self.place_mark(index, "X")
            if "" in self.board:
                self.root.after(500, self.computer_move)

    def place_mark(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player)
        if self.check_winner(player):
            messagebox.showinfo("Game Over", f"{player} wins!")
            self.reset_board()
        elif "" not in self.board:
            messagebox.showinfo("Game Over", "It's a Draw!")
            self.reset_board()

    def check_winner(self, player):
        b = self.board
        s = self.board_size
        t = self.to_win

        for row in range(s):
            for col in range(s):
                idx = row * s + col

                # Horizontal
                if col <= s - t and all(b[idx + i] == player for i in range(t)):
                    return True

                # Vertical
                if row <= s - t and all(b[idx + s * i] == player for i in range(t)):
                    return True

                # Diagonal right-down
                if row <= s - t and col <= s - t and all(b[idx + (s + 1) * i] == player for i in range(t)):
                    return True

                # Diagonal left-down
                if row <= s - t and col >= t - 1 and all(b[idx + (s - 1) * i] == player for i in range(t)):
                    return True

        return False

    def computer_move(self):
        available = [i for i, val in enumerate(self.board) if val == ""]

        # Try to win
        for i in available:
            self.board[i] = "O"
            if self.check_winner("O"):
                self.place_mark(i, "O")
                return
            self.board[i] = ""

        # Try to block
        for i in available:
            self.board[i] = "X"
            if self.check_winner("X"):
                self.board[i] = "O"
                self.place_mark(i, "O")
                return
            self.board[i] = ""

        # Random fallback
        self.place_mark(random.choice(available), "O")

    def reset_board(self):
        self.board = [""] * (self.board_size ** 2)
        for button in self.buttons:
            button.config(text="")

# Run it
root = tk.Tk()
app = AestheticTicTacToe(root)
root.mainloop()

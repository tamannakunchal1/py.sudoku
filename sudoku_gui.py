import tkinter as tk
from tkinter import messagebox
from sudoku_logic import solve, is_valid, generate_puzzle

def create_rounded_button(parent, text, command, bg, fg="black"):
    canvas = tk.Canvas(parent, width=110, height=40, bg=parent["bg"], highlightthickness=0)

    canvas.create_arc((0, 0, 30, 30), start=90, extent=90, fill=bg, outline=bg)
    canvas.create_arc((80, 0, 110, 30), start=0, extent=90, fill=bg, outline=bg)
    canvas.create_arc((0, 10, 30, 40), start=180, extent=90, fill=bg, outline=bg)
    canvas.create_arc((80, 10, 110, 40), start=270, extent=90, fill=bg, outline=bg)
    canvas.create_rectangle(15, 0, 95, 40, fill=bg, outline=bg)
    canvas.create_rectangle(0, 15, 110, 25, fill=bg, outline=bg)

    canvas.create_text(55, 20, text=text, fill=fg, font=("Segoe UI", 10, "bold"))
    canvas.bind("<Button-1>", lambda e: command())

    return canvas


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver Game - Premium")
        self.root.geometry("500x700")
        self.root.configure(bg="#0F0C29")
        self.cells = {}

        self.create_levels()
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        frame = tk.Frame(self.root, bg="#302B63", padx=10, pady=10)
        frame.pack(pady=20)

        for r in range(9):
            for c in range(9):
                padx = (1, 1)
                pady = (1, 1)
                if c % 3 == 0 and c != 0:
                    padx = (5, 1)
                if r % 3 == 0 and r != 0:
                    pady = (5, 1)

                entry = tk.Entry(frame, width=2, font=('Segoe UI', 20, 'bold'),
                                 justify='center', borderwidth=0, relief="flat",
                                 bg="#24243E", fg="#00F2FE", insertbackground="#00F2FE")

                entry.grid(row=r, column=c, padx=padx, pady=pady, sticky="nsew")
                self.cells[(r, c)] = entry

    def create_levels(self):
        level_frame = tk.Frame(self.root, bg="#0F0C29")
        level_frame.pack(pady=10)

        tk.Label(level_frame, text="CHOOSE DIFFICULTY",
                 font=("Segoe UI", 12, "bold"),
                 bg="#0F0C29", fg="#00F2FE").pack()

        diff_frame = tk.Frame(level_frame, bg="#0F0C29")
        diff_frame.pack()

        levels = [("Easy", "#00F2FE"), ("Medium", "#FF9800"), ("Hard", "#F44336")]

        for text, color in levels:
            btn = create_rounded_button(diff_frame, text,
                                        lambda t=text: self.new_game(t), color)
            btn.pack(side=tk.LEFT, padx=5, pady=5)

    def new_game(self, difficulty):
        board = generate_puzzle(difficulty)
        self.clear_grid()
        self.set_board(board)

    def create_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#0F0C29")
        btn_frame.pack(pady=20)

        btn1 = create_rounded_button(btn_frame, "Solve", self.solve_clicked, "#9D50BB")
        btn1.grid(row=0, column=0, padx=5)

        btn2 = create_rounded_button(btn_frame, "Clear", self.clear_grid, "#6E48AA")
        btn2.grid(row=0, column=1, padx=5)

        btn3 = create_rounded_button(btn_frame, "Sample", self.load_sample, "#00F2FE")
        btn3.grid(row=0, column=2, padx=5)

        btn4 = create_rounded_button(btn_frame, "Check", self.check_board, "#ff4d4d")
        btn4.grid(row=0, column=3, padx=5)

    def get_board(self):
        board = []
        for r in range(9):
            row = []
            for c in range(9):
                val = self.cells[(r, c)].get()
                if val == "":
                    row.append(0)
                else:
                    try:
                        num = int(val)
                        if 1 <= num <= 9:
                            row.append(num)
                        else:
                            raise ValueError
                    except:
                        messagebox.showwarning("Input Error", f"Invalid input at {r+1},{c+1}")
                        return None
            board.append(row)
        return board

    def set_board(self, board):
        for r in range(9):
            for c in range(9):
                cell = self.cells[(r, c)]

                cell.config(state="normal")  
                cell.delete(0, tk.END)

                if board[r][c] != 0:
                    cell.insert(0, str(board[r][c]))
                    cell.config(fg="cyan", state="disabled")
                else:
                    cell.config(fg="white")

    def solve_clicked(self):
    
        for r in range(9):
            for c in range(9):
                self.cells[(r, c)].config(bg="#24243E")
        board = self.get_board()
        if board is None:
            return

        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    temp = board[r][c]
                    board[r][c] = 0
                    if not is_valid(board, r, c, temp):
                        self.highlight_errors(board)
                        messagebox.showwarning("Error", "Invalid Sudoku! Check red cells.")
                        return
                    board[r][c] = temp

        if solve(board):
            self.set_board(board)
            messagebox.showinfo("Success", "Solved!")
        else:
            messagebox.showerror("Failed", "No solution exists.")
    
    def clear_grid(self):
        for r in range(9):
            for c in range(9):
                cell = self.cells[(r, c)]
                cell.config(state="normal")  
                cell.delete(0, tk.END)
                cell.config(bg="#24243E")

    def load_sample(self):
        sample = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.clear_grid()
        self.set_board(sample)

    def highlight_errors(self, board):
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val != 0:
                    board[r][c] = 0
                    if not is_valid(board, r, c, val):
                        self.cells[(r, c)].config(bg="#ff4d4d")
                    else:
                        self.cells[(r, c)].config(bg="#24243E")
                    board[r][c] = val

    def check_board(self):
        board = self.get_board()
        if board:
            self.highlight_errors(board)                

if __name__ == "__main__":
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()
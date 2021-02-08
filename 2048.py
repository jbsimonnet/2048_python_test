# Créé par jb_si, le 08/02/2021 en Python 3.7

import tkinter as tk
import couleurs as c
import random

class jeu(tk.Frame):
    def __init__(self):
        # création de la fenettre principale
        tk.Frame.__init__(self)
        self.grid()
        self.master.title(2048)

        self.main_grid = tk.Frame(
            self, bg=c.GRID_COLOR, bd=3, width=600, height=600
        )
        self.main_grid.grid(pady=(100, 0))
        self.creer_GUI()
        self.demarrage_jeu()

        # assocation des touches du clavier
        self.master.bind("<Left>", self.gauche)
        self.master.bind("<Right>", self.droite)
        self.master.bind("<Up>", self.haut)
        self.master.bind("<Down>", self.bas)

        self.mainloop()


    def creer_GUI(self):
        # création de la grille
        self.cells = []
        for i in range(4):
            row = []
            for j in range (4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOR,
                    width=150,
                    height=150
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        # gestion du score
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor="center")
        tk.Label(
            score_frame,
            text="Score",
            font=c.SCORE_LABEL_FONT
        ).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)

    # creation de la matrice de calcul
    def demarrage_jeu(self):
        # initialisation de la matrice avec des 0
        self.matrix = [[0] *4 for _ in range (4)]

        # ajouter 2 cellules aleatoires avec des 2
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2"
        )
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2"
        )

        self.score = 0

    # operations dans la matrice
    def assemble(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    def retourne(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix

    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    # ajoute un 2 ou un 4 a une cellule vide
    def ajout_nouv_cell(self):
        if any(0 in row for row in self.matrix):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            while(self.matrix[row][col] != 0):
                row = random.randint(0, 3)
                col = random.randint(0, 3)
            self.matrix[row][col] = random.choice([2, 4])

    # mise a jour de l'interface pour correspondre a l'etat de la matrice
    def maj_gui(self):
        for i in range(4):
            for j in range (4):
                cell_value= self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[cell_value],
                        fg=c.CELL_NUMBER_COLORS[cell_value],
                        font=c.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value)
                    )
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    # gestion des controles
    def gauche(self, event):
        self.assemble()
        self.combine()
        self.assemble()
        self.ajout_nouv_cell()
        self.maj_gui()
        self.fin_jeu()

    def droite(self, event):
        self.retourne()
        self.assemble()
        self.combine()
        self.assemble()
        self.retourne()
        self.ajout_nouv_cell()
        self.maj_gui()
        self.fin_jeu()

    def haut(self, event):
        self.transpose()
        self.assemble()
        self.combine()
        self.assemble()
        self.transpose()
        self.ajout_nouv_cell()
        self.maj_gui()
        self.fin_jeu()

    def bas(self, event):
        self.transpose()
        self.retourne()
        self.assemble()
        self.combine()
        self.assemble()
        self.retourne()
        self.transpose()
        self.ajout_nouv_cell()
        self.maj_gui()
        self.fin_jeu()

    # verification si un tour est encore possible
    def horizontal_coup_existe(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    def vertical_coup_existe(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    # verification si fin de jeu, gagne ou perd
    def fin_jeu(self):
        if any(2048 in row for row in self.matrix):
            fin_jeu_frame = tk.Frame(self.main_grid, borderwidth=2)
            fin_jeu_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                fin_jeu_frame,
                text="Vous avez gagnez !",
                bg=c.GAGNANT_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT
            ).pack()
        elif not any(0 in row for row in self.matrix) and not self.horizontal_coup_existe() and not self.vertical_coup_existe():
            fin_jeu_frame = tk.Frame(self.main_grid, borderwidth=2)
            fin_jeu_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                fin_jeu_frame,
                text="Perdu !",
                bg=c.PERDANT_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT
            ).pack()

def main():
    jeu()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import messagebox
import random

# Constantes para o tamanho do tabuleiro, tamanho dos cartões, cores, etc.
NUM_ROWS = 4
NUM_COLS = 4
CARD_SIZE_W = 10
CARD_SIZE_H = 5
CARD_COLORS = ['red', 'blue', 'green', 'yellow',
               'purple', 'orange', 'cyan', 'magenta']
BG_COLOR = '#87CEEB'  # Nova cor de fundo
FONT_COLOR = 'white'
FONT_STYLE = ('Arial', 12, 'bold')
MAX_ATTEMPTS = 25


def create_card_grid():
    # Cria uma grade embaralhada de cores para os cartões
    colors = CARD_COLORS * 2
    random.shuffle(colors)
    grid = []
    for _ in range(NUM_ROWS):
        row = []
        for _ in range(NUM_COLS):
            color = colors.pop()
            row.append(color)
        grid.append(row)
    return grid


def card_clicked(row, col):
    # Lida com o clique em um cartão
    card = cards[row][col]
    color = card['bg']
    if color == 'black':
        card['bg'] = grid[row][col]
        revealed_cards.append(card)
        if len(revealed_cards) == 2:
            check_match()


def check_match():
    # Verifica se dois cartões revelados são iguais
    card1, card2 = revealed_cards
    if card1['bg'] == card2['bg']:
        # Se são iguais, destroem os cartões e verifica se o jogador venceu
        card1.after(1000, card1.destroy)
        card2.after(1000, card2.destroy)
        matched_cards.extend([card1, card2])
        check_win()
    else:
        # Se não são iguais, volta a cobrir os cartões após um segundo
        card1.after(1000, lambda: card1.config(bg='black'))
        card2.after(1000, lambda: card2.config(bg='black'))
    revealed_cards.clear()
    update_score()


def check_win():
    # Verifica se o jogador venceu o jogo
    if len(matched_cards) == NUM_ROWS * NUM_COLS:
        messagebox.showinfo('Parabéns!', 'Você venceu o jogo!')
        window.quit()


def update_score():
    # Atualiza as tentativas do jogador e verifica se o jogo acabou
    global attempts
    attempts += 1
    attempts_label.config(
        text='Tentativas: {}/{}'.format(attempts, MAX_ATTEMPTS))
    if attempts >= MAX_ATTEMPTS:
        messagebox.showinfo('Fim de Jogo', 'Você perdeu o jogo!')
        window.quit()


# Configuração da janela principal
window = tk.Tk()
window.title('Jogo de Memória')
window.configure(bg=BG_COLOR)

# Cria a grade de cartões e inicializa variáveis
grid = create_card_grid()
cards = []
revealed_cards = []
matched_cards = []
attempts = 0

# Criação dos botões de cartões e configuração de estilo
for row in range(NUM_ROWS):
    row_of_cards = []
    for col in range(NUM_COLS):
        card = tk.Button(window, width=CARD_SIZE_W, height=CARD_SIZE_H, bg='black',
                         relief=tk.RAISED, bd=3, command=lambda r=row, c=col: card_clicked(r, c))
        card.grid(row=row, column=col, padx=5, pady=5)
        row_of_cards.append(card)
    cards.append(row_of_cards)

# Definição do estilo dos botões
button_style = {'activebackground': '#f8f9fa',
                'font': FONT_STYLE, 'fg': FONT_COLOR}
window.option_add('*Button', button_style)

# Adição do rótulo para exibir o número de tentativas
attempts_label = tk.Label(window, text='Tentativas: {}/{}'.format(
    attempts, MAX_ATTEMPTS), fg=FONT_COLOR, bg=BG_COLOR, font=FONT_STYLE)
attempts_label.grid(row=NUM_ROWS, columnspan=NUM_COLS, padx=10, pady=10)


# Adição da informação no rodapé com uma linha entre as frases
footer_label = tk.Label(window, text='Desenvolvido por Bruno Portugal\nCom estudos no Site "Usando Python"',
                        fg=FONT_COLOR, bg=BG_COLOR, font=FONT_STYLE)
footer_label.grid(row=NUM_ROWS + 1, columnspan=NUM_COLS, padx=10, pady=10)


# Início do loop principal da interface gráfica
window.mainloop()

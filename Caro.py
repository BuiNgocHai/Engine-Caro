import numpy as np
board =[[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']]
for i in range(0,15):
    board.append(board[0])
board = np.array(board)
def show_board():
    print('\t','0   ','1  ','2  ','3  ','4  ','5  ','6  ','7  ','8  ','9  ','10 ','11 ','12 ','13 ','14  ')
    print()
    for i in range(0,15):
        print(i,'\t|',end=' ')
        for j in range(0,15):
            print(board[i][j],'|',end=' ')
        print()
        print('        -------------------------------------------------------------')
def check_line(ch,i,j):
    if board[i][j+1] == ch and board[i][j+2] == ch and board[i][j+3] == ch and board[i][j+4]==ch:
        return True
    if board[i+1][j] == ch and board[i+2][j] == ch and board[i+3][j] == ch and board[i+4][j]==ch:
        return True
    if board[i+1][j+1]==ch and board[i+2][j+2] == ch and board[i+3][j+3]==ch and board[i+4][j+4]==ch:
        return True
    if board[i+1][j-1]==ch and board[i+2][j-2] == ch and board[i+3][j-3] == ch and board[i+4][j-4]==ch:
        return True
    return False
def check_all(ch):
    for i in range(0,15):
        for j in range(0,15):
            if board[i][j] == ch:
                if check_line(board[i][j],i,j):
                    return True
    return False
def con_o_trong():
    for i in range(0,15):
        for j in range(0,15):
            if board[i][j] != 'x' and board[i][j] != 'o':
               return True
show_board()
win=0
while con_o_trong():
    row = int(input("Please enter a row: "))
    while row >= 15 or row < 0 :
        row = int(input("Please enter again(0-14): "))
    column = int(input("Please enter a column: "))
    while column >= 15 or row <0:
        column = int(input("Please enter again(0-14): "))
    if board[row][column] == 'x' or board[row][column] == 'o':
        print("Ô này đã bị chiếm")
    else :
        board[row][column] = 'x'
    show_board()
    if check_all('x'):
        win='you'
        break
if win==0:
    print('Hoa')
else:
    print(win,' win')

    
    

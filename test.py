import turtle
import random
import time
# import os
# os.chdir('E:\\Documents\\OneDrive\\UT\\CSC180\\project2\\stringmethod')

global move_history

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def is_empty(board):
    return board == [[' ']*len(board)]*len(board)

def is_in(board, y, x):
    return 0 <= y < len(board) and 0 <= x < len(board)

def is_win(board):
    
    black = score_of_col(board,'b')
    white = score_of_col(board,'w')
    
    sum_sumcol_values(black)
    sum_sumcol_values(white)
    
    if 5 in black and black[5] == 1:
        return 'Black won'
    elif 5 in white and white[5] == 1:
        return 'White won'
        
    if sum(black.values()) == black[-1] and sum(white.values()) == white[-1] or possible_moves(board)==[]:
        return 'Draw'
        
    return 'Continue playing'

##AI Engine
'''
need to adapt to global board
'''
def march(board,y,x,dy,dx,length):
    '''
    tìm vị trí xa nhất trong dy,dx trong khoảng length
    go as far as posible in direction dy, dx for length
    '''
    yf = y + length*dy 
    xf = x + length*dx
    # chừng nào yf,xf không có trong board
    while not is_in(board,yf,xf):
        yf -= dy
        xf -= dx
        
    return yf,xf
    
def score_ready(scorecol):
    '''
    Khởi tạo hệ thống điểm chuyển
    transform this form:
    {(0, 1): [0, 0, 0, 0, 0],(-1, 1): [0, 1, 1, 1, 1],(1, 0): [0, 0, -1, -1, -1],(1, 1): [0, 0, 0, 0, 0]}
    to this form
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {},-1: {}}
    '''
    print(scorecol)
    sumcol = {0: {},1: {},2: {},3: {},4: {},5: {},-1: {}}
    for key in scorecol:
        for score in scorecol[key]:
            if key in sumcol[score]:
                sumcol[score][key] += 1
            else:
                sumcol[score][key] = 1
            
    return sumcol
    
def sum_sumcol_values(sumcol):
    '''
    merge the scores of each directions.
    '''
    
    for key in sumcol:
        if key == 5:
            sumcol[5] = int(1 in sumcol[5].values())
        else:
            sumcol[key] = sum(sumcol[key].values())
            
def score_of_list(lis,col):
    '''
    take in a 5 unit list, show a number representing what it is like
    '''
    
    blank = lis.count(' ')
    filled = lis.count(col)
    
    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled

def row_to_list(board,y,x,dy,dx,yf,xf):
    '''
    trả về list của y,x từ yf,xf
    return the list expression of the y,x to yf, xf (inclusive)
    '''
    row = []
    while y != yf + dy or x !=xf + dx:
        row.append(board[y][x])
        y += dy
        x += dx
    return row
    
def score_of_row(board,cordi,dy,dx,cordf,col):
    '''
    trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối
    return a list, with each element representing the score of one 5 block units. e.g [1,2,2,3,4] means there are one 1's, two 2's, one 3 and one 4, in the direction dy,dx
    '''
    colscores = []
    y,x = cordi
    yf,xf = cordf
    row = row_to_list(board,y,x,dy,dx,yf,xf)
    for start in range(len(row)-4):
        score = score_of_list(row[start:start+5],col)
        colscores.append(score)
    
    return colscores

def score_of_col(board,col):
    '''
    pretty much like detect_rows, calculate the scores of lists for each direction for col, used for is_win only. for one step, use score_of_col_one
    '''

    f = len(board)
    scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
    for start in range(len(board)):
        scores[(0,1)].extend(score_of_row(board,(start, 0), 0, 1,(start,f-1), col))
        scores[(1,0)].extend(score_of_row(board,(0, start), 1, 0,(f-1,start), col))
        scores[(1,1)].extend(score_of_row(board,(start, 0), 1,1,(f-1,f-1-start), col))
        scores[(-1,1)].extend(score_of_row(board,(start,0), -1, 1,(0,start), col))
        
        if start + 1 < len(board):
            scores[(1,1)].extend(score_of_row(board,(0, start+1), 1, 1,(f-2-start,f-1), col)) 
            scores[(-1,1)].extend(score_of_row(board,(f -1 , start + 1), -1,1,(start+1,f-1), col))
            
    return score_ready(scores)
    
def score_of_col_one(board,col,y,x):
    '''
    return the score dictionary for col in y,x in 4 directions. key: score of the 5 unit blocks, value:number of such 5 unit blocks
    improvement: only check 5 blocks away instead of whole row
    '''
    
    scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
    
    scores[(0,1)].extend(score_of_row(board,march(board,y,x,0,-1,4), 0, 1,march(board,y,x,0,1,4), col))
    
    scores[(1,0)].extend(score_of_row(board,march(board,y,x,-1,0,4), 1, 0,march(board,y,x,1,0,4), col))
    
    scores[(1,1)].extend(score_of_row(board,march(board,y,x,-1,-1,4), 1, 1,march(board,y,x,1,1,4), col))

    scores[(-1,1)].extend(score_of_row(board,march(board,y,x,-1,1,4), 1,-1,march(board,y,x,1,-1,4), col))
    
    return score_ready(scores)
    
def possible_moves(board):
    '''
    khởi tạo danh sách tọa độ có thể có tại danh giới các nơi đã đánh phạm vi 3 đơn vị
    return a list of possible coordinates at the boundary of existing stones off-set by 3 units
    '''
    #l = len(board)
    #mảng taken lưu giá trị của người chơi và của máy trên bàn cờ
    taken = []
    # mảng directions lưu hướng đi (8 hướng)
    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(-1,1),(1,-1)]
    # cord: lưu các vị trí không đi 
    cord = {}
    
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != ' ':
                taken.append((i,j))
    ''' duyệt trong hướng đi và mảng giá trị trên bàn cờ của người chơi và máy, kiểm tra nước không thể đi(trùng với 
    nước đã có trên bàn cờ)
    '''
    for direction in directions:
        dy,dx = direction
        for coord in taken:
            y,x = coord
            for length in [1,2,3,4]:
                move = march(board,y,x,dy,dx,length)
                if move not in taken and move not in cord:
                    cord[move]=False
    return cord
    
def TF34score(score3,score4):
    '''
    return if a certain 3+4 case is winnable
    '''
    for key4 in score4:
        if score4[key4] >=1:
            for key3 in score3:
                if key3 != key4 and score3[key3] >=2:
                        return True
    return False
    
def stupid_score(board,col,anticol,y,x):
    '''
    attempt to move y,x for both col
    return the advantage of col if put on y,x + the advantage of anticol if put on y,x
    '''
    
    global colors
    M = 1000
    res,adv, dis = 0, 0, 0
    
    #offense
    board[y][x]=col
    #draw_stone(x,y,colors[col])
    sumcol = score_of_col_one(board,col,y,x)       
    a = winning_situation(sumcol)
    adv += a * M
    sum_sumcol_values(sumcol)
    #{0: 0, 1: 15, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}
    #print (sumcol)
    adv +=  sumcol[-1] + sumcol[1] + 4*sumcol[2] + 8*sumcol[3] + 16*sumcol[4]
    
    #defense
    board[y][x]=anticol
    #draw_stone(x,y,colors[anticol])
    sumanticol = score_of_col_one(board,anticol,y,x)  
    #board[y][x]=col
    #draw_stone(x,y,colors[col])
    d = winning_situation(sumanticol)
    dis += d * (M-100)
    sum_sumcol_values(sumanticol)
    dis += sumanticol[-1] + sumanticol[1] + 4*sumanticol[2] + 8*sumanticol[3] + 16*sumanticol[4]

    res = adv + dis
    
    #remove_stone(x,y)
    board[y][x]=' '
    return res
    
def winning_situation(sumcol):
    '''
    return the kind of winning situation sumcol is in
    sumcol looks like:
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    '''
    
    if 1 in sumcol[5].values():
        return 5
    elif len(sumcol[4])>=2 or (len(sumcol[4])>=1 and max(sumcol[4].values())>=2):
        return 4
    elif TF34score(sumcol[3],sumcol[4]):
        return 4
    else:
        score3 = sorted(sumcol[3].values(),reverse = True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0
    
def best_move(board,col):
    '''
    trả lại điểm số của mảng trong lợi thế của từng màu
    return the score of the board in advantage of the color col
    the more low step to fives, the better. the higher the score the better
    '''
    if col == 'w':
        anticol = 'b'
    else:
        anticol = 'w'
        
    movecol = (0,0)
    maxscorecol = ''
    # kiểm tra nếu bàn cờ rỗng thì cho vị trí random nếu không thì đưa ra giá trị trên bàn cờ nên đi 
    if is_empty(board):
        movecol = ( int((len(board))*random.random()),int((len(board[0]))*random.random()))
    else:
        moves = possible_moves(board)

        for move in moves:
            y,x = move
            if maxscorecol == '':
                scorecol=stupid_score(board,col,anticol,y,x)
                maxscorecol = scorecol
                movecol = move
            else:
                scorecol=stupid_score(board,col,anticol,y,x)
                if scorecol > maxscorecol:
                    maxscorecol = scorecol
                    movecol = move
    return movecol

##Graphics Engine

def click(x,y):
    global board,colors,win, move_history
    
    x,y = getindexposition(x,y)
    
    if x == -1 and y == -1 and len(move_history) != 0:
        x, y = move_history[-1]
        remove_stone(x, y)
        del(move_history[-1])
        board[y][x] = " "
        x, y = move_history[-1]
        remove_stone(x, y)
        del(move_history[-1])
        board[y][x] = " "
        return
    
    if not is_in(board, y, x):
        return
    
    if board[y][x] == ' ' and win == False:
        
        draw_stone(x,y,colors['b'])
        board[y][x]='b'
        
        move_history.append((x, y))
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print (game_res)
            win = True
            return
            
            #screen.bye()
            
        ay,ax = best_move(board,'w')
        draw_stone(ax,ay,colors['w'])
        board[ay][ax]='w'    
            
        move_history.append((ax, ay))
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print (game_res)
            win = True
            return
            
            #screen.bye()
        
    
def initialize(size):
    
    global win,board,screen,colors, move_history#,border
    
    move_history = []
    win = False
    board = make_empty_board(size)
    
    screen = turtle.Screen()
    screen.onclick(click)
    screen.setup(screen.screensize()[1]*2,screen.screensize()[1]*2)
    screen.setworldcoordinates(-1,size,size,-1)
    screen.bgcolor('orange')
    screen.tracer(500)
    
    colors = {'w':turtle.Turtle(),'b':turtle.Turtle(), 'g':turtle.Turtle()}
    colors['w'].color('white')
    colors['b'].color('black')
    colors['g'].color('green')
    for key in colors:
        colors[key].ht()
        colors[key].penup()
        colors[key].speed(0)
    
    border = turtle.Turtle()
    border.speed(9)
    border.penup()
    
    side = (size-1)/2
    
    i=-1
    for start in range(size):
        border.goto(start,side + side *i)     #z-shaped drawing for optimum speed
        border.pendown()
        i*=-1
        border.goto(start,side + side *i)     #(side + side *i) alternates between 0 and size-1
        border.penup()
        
    i=1
    for start in range(size):
        border.goto(side + side *i,start)
        border.pendown()
        i *= -1
        border.goto(side + side *i,start)
        border.penup()
        
    border.ht()
    
    # undo button

    draw_stone(-1,-1,colors['g'])
    
    screen.listen()
    screen.mainloop()
    
def getindexposition(x,y):
    '''
    return the index position of the board in list form
    '''
    intx,inty = int(x),int(y)
    dx,dy = x-intx,y-inty
    if dx > 0.5:
        x = intx +1
    elif dx<-0.5:
        x = intx -1
    else:
        x = intx
    if dy > 0.5:
        y = inty +1
    elif dx<-0.5:
        y = inty -1
    else:
        y = inty
    return x,y
''' 
def remove_stone(x,y):
    global screen
    
    eraser = turtle.Turtle()
    eraser.penup()
    eraser.speed(0)
    eraser.ht()
    
    eraser.color(screen.bgcolor())
    draw_stone(x,y,eraser)
    eraser.color('black')
    eraser.pendown()
    eraser.goto(x,y+0.4)
    eraser.penup()
    eraser.goto(x-0.3,y)
    eraser.pendown()
    eraser.goto(x+0.4,y)
    eraser.penup()
    '''
def draw_stone(x,y,colturtle):
    colturtle.goto(x,y-0.3)
    colturtle.pendown()
    colturtle.begin_fill()
    colturtle.circle(0.3)
    colturtle.end_fill()
    colturtle.penup()
    
if __name__ == '__main__':
    initialize(15)
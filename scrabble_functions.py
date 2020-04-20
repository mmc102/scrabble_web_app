import random
import copy 
tile_values ={'a':1,'b':4,'c':3,'d':2,'e':1,'f':5,'g':1,'h':4,'i':1,'j':8,'k':5,'l':1,'m':3,'n':1,'o':1,'p':4,'q':10,'r':1,'s':1,'t':1,'u':1,'v':5,'w':5,'x':8,'y':2,'z':10}
multipliers = {(1,14):1,(2,14):3}

#make a bag with the correct distribution of letters, returns the bag
def form_the_bag():
    multipliers = [9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1,2] #from game board
    the_bag = [] #stores final lot of all letters
    letters = 'abcdefghijklmnopqrstuvwxyz?' #? reps the blank
    all_letters = '' #temp storage of the strings
    for index, letter in enumerate(letters):
        all_letters = all_letters + letter*multipliers[index]

    for  letter in all_letters:
        the_bag.append(letter)

    return the_bag

def print_the_board(board):
    for  i in board:
        print(i)

#given a tray (any degree of filled), this returns the tile bag less the tiles that were put into the tray, and the full tray itself  
def draw_tiles(tile_bag,current_tray):
    tiles_to_draw = 7-len(current_tray)
    random.shuffle(tile_bag)
    
    while tiles_to_draw > 0:
        current_tray.append(tile_bag.pop())
        tiles_to_draw -=1
    return tile_bag, current_tray

#makes a board that is the size of the scrabble board 
def form_the_board():
    board = []
    for i in range(15):
        temp_row = []
        for j in range(15):
            square = [' ']
            temp_row.append(square)
        board.append(temp_row)
    for multiplier in multipliers:
        board[multiplier[0]][multiplier[1]] = [str(multipliers.get(multiplier))]
    return board

#collects a validated word from the user and checks against the tray, return the tray less the letters, and the word itself
def collect_validate_word(the_tray):
    valid = False
    while valid == False:
        print('input *swap to exchange letters')
        word = input('the letters you will use (in order, excluding those already on the board):').lower()
        if word == '*swap':
            valid == True
            letters_to_swap = input('what letters do you want to swap?')
            if all([True if letter in the_tray else False for letter in letters_to_swap]):
                for letter in word:
                    the_tray.remove(letter)
            #need to work this out ****************************************

        elif all([True if letter in the_tray else False for letter in word]):
            valid = True
            if len(word) == 0:
                skip_q = input('are you sure you want to skip your turn? no to enter word ')
                if skip_q.lower() == 'no':
                    valid = False
            
        else:
            print('not a valid word based on your tray, try again')
    
    
    for letter in word:
        the_tray.remove(letter)
    word = blank_handling(word)
    return the_tray, word

#validates both the position and the argument for location and orientation, then puts the letters into the board. might error if the location is >14. see line 2 final conditional
#returns original board that can be used to determine which letter were laid
def letters_onto_board(board,letters):
    original_board = copy.deepcopy(board)
    valid = False
    print(letters)
    if len(letters) == 0:
        location = [0,0] 
        h_or_v = 0
        valid = True
    while valid == False:
        try:
            location = list(map(int, input('coordinates "x y" of starting letter: ').rstrip().split()))
            while not location[0] <= 14 and not location[1] <= 14 and len(location) != 2 and board[location[0]][location[1]] != '':
                print('not an accetable cordinate, try again')
                location = list(map(int, input('coordinates "x y" of starting letter: ').rstrip().split()))
            
            h_or_v = int(input('0 for horizontal, 1 for vertical '))
            while not (h_or_v == 0 or h_or_v == 1):
                h_or_v = int(input('0 for horizontal, 1 for vertical '))
            
            if h_or_v == 0:
                if len(letters)-1 + location[1]<15: 
                    for index, letter in enumerate(letters):
                        spacer = 1
                        if board[location[0]][location[1] + index] == [' ']:
                            board[location[0]][location[1] + index] = [letter]
                        else:
                            while board[location[0]][location[1] + index + spacer ] != [' ']:
                                spacer +=1
                            board[location[0]][location[1] + index + spacer ] = [letter]
                else: 
                    raise ValueError
                
            elif h_or_v == 1:
                if len(letters)-1 + location[0]<15: 
                    for index, letter in enumerate(letters):
                        spacer = 1
                        if board[location[0]+ index][location[1]] == [' ']:
                            board[location[0]+ index][location[1]] = [letter]
                        else:
                            while board[location[0]+ index+spacer][location[1]] != [' ']:
                                spacer += 1
                            
                            board[location[0]+ index+ spacer][location[1]] = [letter]
                else:
                    raise ValueError
            valid = True
        except:
            print('your placement goes of the boundries of the board, reconsider please')
    
    return board, original_board, location , h_or_v 

#compares the previous board and returns the new letters' cordinates 'cordinates new tiles'
def added_tiles(master_board,temp_board):
    cordinates_new_tiles = []
    for i in range(15):
        for  j in range(15):
            if master_board[i][j] != temp_board[i][j]:
                cordinates_new_tiles.append([[i,j],''.join(temp_board[i][j])])

    return cordinates_new_tiles
#using the origin of the previous word, determine all the words that someone made with their play 
#this func is way to hectic...
def all_words_from_move(board,origin,horizontal_or_vertical,cordinates_new_tiles):
    #lets start with just the horizontal case first. 
    all_words = []
    if horizontal_or_vertical == 0:
        #go to the origin of the word, and trace left for white space or the end of the board:
        cur_location = [origin[0],origin[1]-1]
        value = board[cur_location[0]][cur_location[1]]
        while not(cur_location[1] == 0 or value == [' ']):
            cur_location[1] -= 1
            value = board[cur_location[0]][cur_location[1]]

        #resore current location to the cell before it found the end or blank
        cur_location[1] += 1
        full_word = ''
        letter = ''.join(board[cur_location[0]][cur_location[1]])
        word_data = []
        while not(cur_location[1] == 15 or letter == ' '):
            
            letter = ''.join(board[cur_location[0]][cur_location[1]])
            full_word = full_word + letter
            position =  cur_location.copy()
            word_data.append([letter,position])
            if cur_location in cordinates_new_tiles:
                #this is fundamentally broken. I need to develope an inate knowledge about the previous board and the board withthe new tiles 
                #or i need to pass the tiles that were played and the location that they were played on. 
                
                ortho_cur_location = cur_location.copy()
                value = board[ortho_cur_location[0]][ortho_cur_location[1]]
            
                while not(ortho_cur_location[0] == 0 or value == ' '):
                    ortho_cur_location[0] -= 1
            
                    #go upward, until a terminal, then trace back until the next terminal 

                ortho_full_word = ''
                ortho_letter = ''.join(board[ortho_cur_location[0]][ortho_cur_location[1]])
                ortho_word_data = []
                while not(ortho_cur_location[0] == 15 or ortho_letter == ' '):
                    ortho_cur_location[0] += 1
                    
                    ortho_full_word = ortho_full_word + ortho_letter
                    ortho_position = ortho_cur_location.copy()
                    ortho_word_data.append([ortho_letter,ortho_position])
                    ortho_letter = ''.join(board[ortho_cur_location[0]][ortho_cur_location[1]])
                ortho_full_word = ortho_full_word.strip(' ')
                if len(ortho_full_word) >1:
                    all_words.append(ortho_word_data)
            cur_location[1] += 1
            
        all_words.append(word_data)
    else:
        #this handles the vertical oreiented words
        #go to the origin of the word, and trace le for white space or the end of the board:
        cur_location = [origin[0]-1,origin[1]]
        value = board[cur_location[0]][cur_location[1]]
        while not(cur_location[0] == 0 or value == [' ']):
            cur_location[0] -= 1
            value = board[cur_location[0]][cur_location[1]]
        #reset current location to the cell before it found the end or blank,only if we find blank and not end of board 
        if value== [' ']:
            cur_location[0] = cur_location[0] + 1  #helpful for preventing the boundry error 
        full_word = ''
        letter = ''.join(board[cur_location[0]][cur_location[1]])
        
        word_data = []
        while not(cur_location[0] == 14 or letter == ' '):
            full_word = full_word + letter
            position =  cur_location.copy()
            word_data.append([letter,position])
            if cur_location in cordinates_new_tiles:
                ortho_cur_location = cur_location.copy()
                value = board[ortho_cur_location[0]][ortho_cur_location[1]]
                
                while not(ortho_cur_location[1] == 0 or value == ' '):
                    ortho_cur_location[1] -= 1
                    value = ''.join(board[ortho_cur_location[0]][ortho_cur_location[1]])
                    
                    #go upward, until a terminal, then trace back until the next terminal 

                ortho_full_word = ''.join(board[ortho_cur_location[0]][ortho_cur_location[1]])
                ortho_letter = ''
                ortho_word_data = []
                
                while not(ortho_cur_location[1] == 14 or ortho_letter == ' '):
                    
                    ortho_letter = ''.join(board[ortho_cur_location[0]][ortho_cur_location[1]])
                    ortho_full_word = ortho_full_word + ortho_letter
                    ortho_position = ortho_cur_location.copy()
                    ortho_word_data.append([ortho_letter,ortho_position])
                    ortho_cur_location[1] += 1
                ortho_full_word = ortho_full_word.strip(' ')
                if len(ortho_full_word) >1:
                    all_words.append(ortho_word_data)
            cur_location[0] += 1
            letter = ''.join(board[cur_location[0]][cur_location[1]])
        all_words.append(word_data)
    return all_words

def blank_handling(word):
    list_word = [letter for letter in word]
    for index,letter in enumerate(list_word):
        if letter == '?':
            chosen_letter = input('What letter what you like the blank to be?' )
            print('ok')
            list_word[index] = chosen_letter.upper()
    word = ''.join(list_word)
    return word

def mark_new_words(cordinates_new_tiles, all_words):
    cordinates_new_tiles = [i[0] for  i in cordinates_new_tiles]
    print(all_words)  #why are you empty 
    for word in all_words:
        for letters in word:
            if letters[1] in cordinates_new_tiles:  
                letters.append(1)
            else:
                letters.append(0)
    return all_words
    
def add_in_multipliers(letters_and_data,multipliers):

    for  word in letters_and_data:
        for letter in word:
            
            try:
                multiplier = multipliers[tuple(letter[1])]
            except:
                multiplier = 0
            letter.append(multiplier)
            if letter[0] == ' ':
                word.remove(letter)

    print(letters_and_data)
    return letters_and_data

def score_of_words(letters_and_data,tile_values):
    
    total_score = 0
    for word in letters_and_data:
        singe_word_score = 0
        score_multiplier = 1
        if len(word) == 7:
            singe_word_score+=50
            #for a bingo
        for letter in word:
            if letter[0].islower():
                value = tile_values[letter[0]]
            
                if letter[3] == 1:
                    value = value *2
                    print('double letter!', letter[0])
                elif letter[3] ==2:
                    value = value *3
                elif letter[3] ==3:
                    score_multiplier += 2
                    print('double word!', letter[0])
                elif letter[3] == 4:
                    score_multiplier += 3
                singe_word_score += value
        total_score += singe_word_score * score_multiplier   
    
    return total_score

def initiate_the_game():
    num_players = int(input('How many players?'))
    print('ok!')
    players = []
    tile_bag = form_the_bag()
 
    for i in range(num_players):
        tile_bag, tray = draw_tiles(tile_bag,[])
        players.append([tray,0])

    master_board = form_the_board()

    return master_board,tile_bag,players

def one_turn(whos_turn,master_board,tile_bag,players):

    print_the_board(master_board) #show the board
    current_tray = players[whos_turn][0] #show their tray
    print(current_tray)
    players[whos_turn][0], played_word = collect_validate_word(current_tray)  #collect word
    new_board,master_board, location, h_or_v = letters_onto_board(master_board,played_word) #put the word on the board, broken index
    print_the_board(new_board)
    cords_new_tiles = added_tiles(master_board,new_board)
    just_cords = [cords[0] for cords in cords_new_tiles] #add to appropriate func 
    all_words_and_data = all_words_from_move(new_board,tuple(location),h_or_v,just_cords)
    score = score_of_words(add_in_multipliers(mark_new_words(cords_new_tiles,all_words_and_data),multipliers),tile_values)
    print('you scored', score, 'points!')
    tile_bag,players[whos_turn][0] = draw_tiles(tile_bag,current_tray)
    players[whos_turn][1] += score
    master_board = new_board
    if whos_turn == 0:
        whos_turn = 1
    else:
        whos_turn = 0 
    return whos_turn


    


def game_play():
    master_board,tile_bag,players = initiate_the_game()
    whos_turn = 0 
    while len(tile_bag)>0:
        whos_turn = one_turn(whos_turn,master_board,tile_bag,players)
        for numer,player in enumerate(players):
            print('player ',numer+1,': ',player[1])
            
        
        #choose a random player to begin the game


game_play()

# need to display the bonus tiles on the board, need to make sure the words actually intersect with the other words 
#need to put some sort of values on the permimeter to make the locating easier 

#need to add trade letters and skip 
#need to make sure they start on the correct tile 
#need to add challenge feature 

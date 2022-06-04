def print_blank(length, row_num):
    print('_ ' * length + '\u140a')
    for i in range(6 - row_num):
        print('_ ' * length)

def word_state_list(length):
    
    out = []
    char_list = ['0','.','1']
    out_length = len(char_list)**length
    
    for i in range(out_length):
        out.append('')
    

    for i in range(length):
        index = 0
        for j in range(out_length//(len(char_list)**(length-i))):
            for char in char_list:
                for k in range(out_length//((out_length//(len(char_list)**(length-i)))*3)):
                    out[index] += char
                    index += 1
    return out

def freq_dict(game_words_list):
    freq_char_dict = {}
    word_score_dict = {}
    
    for i in game_words_list:
        lis_of_char = []
        for k in i:
            if k not in lis_of_char:
                lis_of_char.append(k)
        for j in lis_of_char:
            if j not in freq_char_dict:
                freq_char_dict[j] = 1
            else:
                freq_char_dict[j] += 1
    
    for i in game_words_list:
        word_score = 0
        lis_of_char = []
        for k in i:
            if k not in lis_of_char:
                lis_of_char.append(k)
        for j in lis_of_char:
            word_score += freq_char_dict[j]
        word_score_dict[i] = word_score
    
    freq_char_dict = sorted(freq_char_dict.items(), key=lambda kv: kv[1], reverse=False)
    word_score_dict = sorted(word_score_dict.items(), key=lambda kv: kv[1], reverse=False)
    
    return word_score_dict

def wordle_solver():
    
    # init
    length = int(input('Word Length: '))

    if length == 5:
        english_words_list = []
        with open('wordle_words.txt') as f:
            for line in f:
                english_words_list.append(line[:len(line)-1])
        english_words_list.sort()
    else:
        english_words_list = []
        with open('words_alpha.txt') as f:
            for line in f:
                english_words_list.append(line[:len(line)-1])
    
    played_word_list = []
    game_words_list = []
    for i in english_words_list:
        if len(i) == length:
            game_words_list.append(i)
    
    word_score_dict = freq_dict(game_words_list)
    suggest_word = list(word_score_dict)[len(word_score_dict)-1]
    print(f"Suggested Word: {suggest_word[0]} [{suggest_word[1]}]")
    
    c = 0
    yes_no = input("Continue [y/n]: ")
    while yes_no == 'n':
        c+=1
        suggest_word = list(word_score_dict)[len(word_score_dict)-1-c]
        print(f"Suggested Word: {suggest_word[0]} [{suggest_word[1]}]")
        yes_no = input("Continue [y/n]: ")
            
    # game
    
    actual_word = ['-']*length
    yellow_list = {}
    black_list = []
    
    for game_num in range(1,7):
        
        # print played word
        for played_word in played_word_list:
            print(played_word)
        
        # print blank
        print_blank(length, game_num)
        
        # input word
        word = input().lower()
        while len(word) != length:
            print("Error: Word Not Possible")
            word = input().lower()

        # input state
        word_state = input()
        while word_state not in word_state_list(length):
            print("Error: State Not Correct")
            word_state = input()
       
        # add played word to list
        played_word = ''
        for i in word:
            played_word += i + ' '
        played_word_list.append(played_word)
        
        if word_state == '1'*length:
            break
        
        # implementing word_state
        for i in range(len(word)):
            if word_state[i] == '0':
                black_list.append(word[i])
            if word_state[i] == '.':
                yellow_list[word[i]] = i
            if word_state[i] == '1':
                actual_word[i] = word[i]
        black_list_copy = black_list.copy()
        for i in black_list_copy:
            if i in actual_word:
                black_list.remove(i)
                
                
        print('--- Possible Words ---')
        
        # remove not-according-to-green
        possible_words_list_1 = game_words_list.copy()
        for possible_word in game_words_list:
            for i in range(len(actual_word)):
                if actual_word[i] != '-':
                    if actual_word[i] != possible_word[i]:
                        if possible_word in possible_words_list_1:
                            possible_words_list_1.remove(possible_word)
        
        # remove not-according-to-black
        possible_words_list_2 = possible_words_list_1.copy()
        for possible_word in possible_words_list_1:  
            for i in possible_word:
                if i in black_list and i not in actual_word and i not in yellow_list:
                    if possible_word in possible_words_list_2:
                        possible_words_list_2.remove(possible_word)
        
        # remove not-according-to-yellow
        possible_words_list_3 = possible_words_list_2.copy()
        for possible_word in possible_words_list_2:  
            for i in yellow_list:
                if i not in possible_word:
                    if possible_word in possible_words_list_3:
                        possible_words_list_3.remove(possible_word)
                elif possible_word.index(i) == yellow_list[i]:
                    if possible_word in possible_words_list_3:
                        possible_words_list_3.remove(possible_word)
                    
        
        # print all remaining words
        game_words_list = possible_words_list_3.copy()
        word_score_dict = freq_dict(game_words_list)
        for i in word_score_dict:
            print(f"{i[0]} [{i[1]}]")
        print(f'--- Round {game_num} has ended ---')
            
        print()
        
    # finish
    print('-' * (length*2-1))
    for i in played_word_list:
        print(i)
    print('-' * (length*2-1))

wordle_solver()
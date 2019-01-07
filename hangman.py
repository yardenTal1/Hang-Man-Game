import hangman_helper


def same_length(words, pattern):
    """
    A auxiliary function for 'filter_words_lis', that receive word list and pattern and check if the in same length.
    the function returns a filter list of those words
    """
    new_list = list()
    for i in words:
        if len(pattern) == len(i):
            new_list.append(i)
    return new_list


def if_in_wrong_guess(wrong_guess_lst,words):
    """
    A auxiliary function for 'filter_words_lis', that receive word list and wrong guess list and check
     if the wrong letter that already chosen not in the word. the function returns a filter list of those words
    """
    new_list = list()
    if wrong_guess_lst==[]:
        return words
    for j in range(len(words)):
        counter= 0
        for i in wrong_guess_lst:
            if i not in words[j]:
                counter += 1
                if counter==len(wrong_guess_lst):
                    new_list.append(words[j])
            else:
                break
    return new_list


def same_pattern(words,pattern):
    """
    A auxiliary function for 'filter_words_lis', that receive word list and pattern and check
    if the words in word list are in same pattern kike a current pattern.
    The function returns a filter list of those words
    """
    filter_list=list()
    for i in words:
        for j in range(len(pattern)):
            if j==len(pattern)-1:
                if pattern[j]=='_' or pattern[j]==i[j]:
                    filter_list.append(i)
            if pattern[j] == '_':
                continue
            elif pattern[j] != '_' and pattern[j] != i[j]:
                break
    return filter_list


def word_and_pattern (word,pattern):
    """
     A auxiliary function for 'filter_words_lis', that receive a word and pattern and check
     if they have the same number of each letter that appears in the pattern.
     The function returns a filter list of those words
     """
    for i in range(len(pattern)):
        if pattern[i]!= '_' and pattern.count(pattern[i]) != word.count(pattern[i]):
            return False
    return True


def lst_and_pattern (filer_lst, pattern):
    """
    A auxiliary function for 'filter_words_lis', that receive a list words and pattern and use with 'word_and_pattern'
     function to check all the words in the list.
    The function returns a filter list of those words
    """
    new_filter_lst=[]
    for word in filer_lst:
        if word_and_pattern(word,pattern):
            new_filter_lst.append(word)
    return new_filter_lst


def filter_words_list(words,pattern,wrong_guess_lst):
    """
    A function that receive a words list, pattern and wrong guess list
    and use with four auxiliary function to filter the words list, in order to give a good hint to the user.
    The function returns a filter list of those words depending on conditions in the auxiliary functions.
    """
    list_hints = same_length(words,pattern)
    list_hints = if_in_wrong_guess(wrong_guess_lst,list_hints)
    list_hints = same_pattern(list_hints,pattern)
    list_hints = lst_and_pattern(list_hints,pattern)
    return list_hints


CHAR_A = 97


def letter_to_index(letter):
    """Return the index of the given letter in an alphabet list."""
    return ord(letter.lower()) - CHAR_A


def index_to_letter(index):
    """Return the letter corresponding to the given index."""
    return chr(index + CHAR_A)


def choose_letter_in_word(word,list_letter,pattern):
    """
    A auxiliary function for 'choose_letter', that receive a word, an empty list and pattern and returns the empty
    list with with the number of each letter by its index (use with 'letter_to_index' function)
    """
    for j in range(len(str(word))):
        if word[j] not in pattern:
            index= letter_to_index(word[j])
            list_letter[index] += 1
    return list_letter


def choose_letter(words,pattern):
    """
    A  function that receive a list words and pattern and return the first letter that appears
     most often on the list.
    """
    list_all_letter=list()
    for j in range (26):
        list_all_letter.append(0)
    for i in words:
        list_all_letter= choose_letter_in_word(i,list_all_letter,pattern)
    maximum = max(list_all_letter)
    for k in range(len(list_all_letter)):
        if list_all_letter[k]==maximum:
            letter_max= index_to_letter(k)
            return letter_max


def update_word_pattern(word,pattern,letter):
    """
    A function receives as parameters the current pattern, word and letter and returns
    an updated pattern containing the same letter.
    """
    new_pattern = list()
    for i in range(len(word)):
        if word[i] == letter and pattern[i] == '_':
            new_pattern.append(letter)
        else:
            new_pattern.append(pattern[i])
    return_pattern=''.join(new_pattern)
    return return_pattern


def if_letter(letter):
    """
    A function that check if value is a lowercase letter in English.
    """
    str_abc= ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    answer= False
    for i in range(len(str_abc)):
        if letter==str_abc[i]:
            answer=True
    return answer


def run_single_game(words_list):
    """
     The main function that receives word list and enable to run single game with a random word.
     The game doesn't end as long as the pattern haven't been fully
    and several incorrect guesses less than specified in the MAXEROR value.
    """
    word = hangman_helper.get_random_word(words_list) #random word
    pattern = len(word)*'_'
    wrong_guess_lst= list()
    error_count=0
    msg= hangman_helper.DEFAULT_MSG
    ask_play=False
    while error_count < hangman_helper.MAX_ERRORS and '_' in pattern:
        hangman_helper.display_state(pattern, error_count, wrong_guess_lst, msg, ask_play)
        user_input = hangman_helper.get_input()
        does_letter = if_letter(user_input[1]) #if the input is letter or not
        if user_input[0] == hangman_helper.HINT:
            filter_list= filter_words_list(words_list,pattern,wrong_guess_lst)
            filter_1 = choose_letter(filter_list,pattern)
            msg = hangman_helper.HINT_MSG+filter_1
        else:
            if len(user_input[1])!=1 or does_letter==False:
                msg= hangman_helper.NON_VALID_MSG
            elif user_input[1] in wrong_guess_lst or user_input[1] in pattern:
                msg= hangman_helper.ALREADY_CHOSEN_MSG+user_input[1]
            elif user_input[1] in word:
                pattern = update_word_pattern(word, pattern, user_input[1])
                msg = hangman_helper.DEFAULT_MSG
            else:
                error_count+=1
                msg=hangman_helper.DEFAULT_MSG
                wrong_guess_lst.append(user_input[1])
    if '_' in pattern:
        ask_play = True
        msg = hangman_helper.LOSS_MSG + word
    else:
        ask_play = True
        msg = hangman_helper.WIN_MSG
    hangman_helper.display_state(pattern, error_count, wrong_guess_lst, msg, ask_play)


def main():
    """
    A function that runs the game once or more depending on the user's selection
    """
    words = hangman_helper.load_words(file='words.txt')
    run_single_game(words)
    type_of_input=hangman_helper.get_input()
    while type_of_input[1]:
        run_single_game(words)
        type_of_input = hangman_helper.get_input()


if __name__ == '__main__':
    hangman_helper.start_gui_and_call_main(main)
    hangman_helper.close_gui()




















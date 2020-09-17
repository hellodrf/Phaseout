def colour(card):
    if card[1]=='S' or card[1]=='C':
        return 'B'
    else:
        return 'R'

def valuefunc(card, r=False):
    if r:
        dict_card={25: 'A', 10: '0', 11: 'J', 12: 'Q', 13: 'K'}
        if str(card) in '23456789':
            return str(card)
        else:
            return dict_card[card]
    dict_card={'A': 25, '0': 10, 'J': 11, 'Q': 12, 'K': 13}
    if card[0] in '23456789':
        return int(card[0])
    else:
        return dict_card[card[0]]

def phasedout_group_type(group):
    #INNI
    card_count=len(group)
    group_no_wild=[card for card in group if card[0]!='A']
    wild=card_count-len(group_no_wild)
    count=0
    try:
        first_card=group_no_wild[0]
        first_index=group.index(first_card)
    except IndexError:
        first_card='WILD'
        first_index=0
    if card_count==3 and wild<2 and [card for card in group_no_wild if 
                                     card[0]==first_card[0]]==group_no_wild:
        return 1
    if card_count==7 and wild<6 and [card for card in group_no_wild if 
                                     card[1]==first_card[1]]==group_no_wild:
        return 2   
    if card_count==8 and wild<7:
        for card in group:
            cur_value=(count-first_index)+int(first_card[0])
            if valuefunc(card)!=cur_value and card[0]!='A' or not cur_value in range(2, 14):
                return None
            count+=1
        return 4     
    if card_count==4 and wild<3:
        if [card for card in group_no_wild if card[0]==first_card[0]]==group_no_wild:
            return 3
        if [card for card in group_no_wild if colour(card)==colour(first_card)]==group_no_wild:
            for card in group:
                cur_value=(count-first_index)+int(first_card[0])
                if valuefunc(card)!=cur_value and card[0]!='A' or not cur_value in range(2, 14):
                    return None
                count+=1
            return 5

def phasedout_phase_type(hand):
    output=list(map(phasedout_group_type, hand))
    if output==[1, 1]:
        return 1
    if output==[2]:
        return 2
    if output==[3, 3]:
        return 3
    if output==[4]:
        return 4
    if output==[5, 3]:
        return 5

#unpack(): unpacker for 2D lists.
def unpack(lst):
    output=[]
    for char in lst:
        for char_ in char:
            output.append(char_)
    return output

def type_test(group, c_type):
    card_count=len(group)
    group_no_wild=[card for card in group if card[0]!='A']
    wild=card_count-len(group_no_wild)
    count=0
    try:
        first_card=group_no_wild[0]
        first_index=group.index(first_card)
    except IndexError:
        first_card='WILD'
        first_index=0
        
    if c_type=='VALUE':
        return [card for card in group_no_wild if card[0]==first_card[0]]==group_no_wild
    if c_type=='SUIT':
        return [card for card in group_no_wild if card[1]==first_card[1]]==group_no_wild
    if c_type=='RUN':
        for card in group:
            cur_value=(count-first_index)+int(first_card[0])
            if valuefunc(card)!=cur_value and card[0]!='A' or not cur_value in range(2, 14):
                return False
            count+=1
        return True
    if c_type=='CRUN':
        for card in group:
            cur_value=(count-first_index)+int(first_card[0])
            if valuefunc(card)!=cur_value and card[0]!='A' or not cur_value in range(2, 14):
                return None
            count+=1
        return [card for card in group_no_wild if colour(card)==colour(first_card)]==group_no_wild

def clear(data):
    for item in data:
        print(item)
      
def phasedout_is_valid_play(play, player_id, table, turn_history, phase_status,
                            hand, discard):
    #INNI
    play_type=play[0]
    if turn_history[-1][0]!=player_id-1 and turn_history[-1][0]!=player_id+3\
       and turn_history[-1][0]!=player_id:
        return 'Error Code: 1'
    
    if play_type==1:
        if turn_history[-1][0]==player_id:
            if 1 in unpack(turn_history[-1][1]) or 2 in unpack(turn_history
                                                               [-1][1]):
                return 'Error Code: 2'
        return True
                
    if play_type==2:
        if turn_history[-1][0]==player_id:
            if 1 in unpack(turn_history[-1][1]) or 2 in unpack(turn_history
                                                               [-1][1]):
                return 'Error Code: 3'
        return play[1]==discard
        
    if play_type==3:
        if turn_history[-1][0]==player_id:
            for char in [3, 4, 5]:
                if char in unpack(turn_history[-1][1]):
                    return 'Error Code: 4'
        for item in unpack(play[1]):
            if item not in hand:
                return 'Error Code: 5'
            hand.remove(item)
        return phasedout_phase_type(play[1])==phase_status[player_id]+1

    if play_type==4:
        previous_plays=unpack([play[1] for play in turn_history if 
                               play[0]==player_id])
        
        if not 3 in [char[0] for char in previous_plays]:
            return 'Error Code: 6'
        
        if turn_history[-1][0]==player_id:
            if 5 in unpack(turn_history[-1][1]):
                return 'Error Code: 7'
                
        if not play[1][0] in hand:
            return 'Error Code: 8'
        target_id=play[1][1]
        target_group=table[target_id[0]][1][target_id[1]]
        target_type=phasedout_group_type(target_group)
        if target_id[2] not in range(0, len(target_group)+1):
            return 'Error Code: 9'
        
        if target_type==1 or target_type==3:
            if play[1][0]=='A':
                return True
            target_group.insert(target_id[2], play[1][0])
            return type_test(target_group, 'VALUE')
        
        if target_type==2:
            if play[1][0]=='A':
                return True
            target_group.insert(target_id[2], play[1][0])
            return type_test(target_group, 'SUIT')
            
        if target_type==4:
            target_group.insert(target_id[2], play[1][0])
            return type_test(target_group, 'RUN')
            
        if target_type==5:
            target_group.insert(target_id[2], play[1][0])
            return type_test(target_group, 'CRUN')
        
    if play_type==5:
        if turn_history[-1][0]==player_id and 5 in unpack(turn_history[-1][1]):
            return 'Error Code: 10'
        return play[1] in hand
  
def phasedout_score(hand):
    return sum(map(valuefunc, hand))

def read(desire_dict):
    print('Desire_Dict_Reader')
    for item in (33, 5, 4.5, 4, 3, 2, 1, 0):
        print(item, ':', [card for card in desire_dict if desire_dict[card]==item])
    print('End')

desire_sort_suit=lambda item:sum([desire_dict[item+suit] for suit in 'SCHD'])
desire_sort_value=lambda item:sum([desire_dict[item+suit] for value in 
                              '234567890JQK'])
desire_sort=lambda item:desire_dict[item]
        

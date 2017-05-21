from my_lib import phasedout_score, phasedout_is_valid_play
from my_lib import colour, unpack, clear, read, valuefunc
from collections import Counter
import time
###############################################################################
def phasedout_play(player_id, table, turn_history, phase_status, hand, discard):
    ###INIT###
    class obj:
        def __init__(self, validation=0):
            self.vd=validation
    draw, recover, phase, sets, discards=obj(), obj(), obj(), obj(), obj()
    ###End_of_Section###
    
    ###Extract_Info###
    highest_phase=[[player for player in range(0,4) if phase_status[player]==
                    max(phase_status)], max(phase_status)]
    current_move=[play[0] for play in turn_history[-1][1] if turn_history
                  [-1][0]==player_id]
    previous_play=unpack([play[1] for play in turn_history if play[0]==
                          player_id])
    previous_move=[move[0] for move in previous_play]
    card_count=len(hand)
    hand_no_wild=[card for card in hand if card[0]!='A']
    wild_count=card_count-len(hand_no_wild)
    wild=[card for card in hand if card[0]=='A']
    if table[player_id][0]!=None:
        current_phase=phase_status[player_id]
    else:
        current_phase=phase_status[player_id]+1
    try:
        first_card=hand_no_wild[0]
    except IndexError:
        first_card='WILD'
    ###End_of_Section###
    
     ###Move_Validation###
    if current_move==[]:
        draw.vd+=1
    if draw.vd and discard:
        recover.vd+=1
    if not draw.vd and not [item for item in current_move if item>2] and table\
        [player_id][0]==None and first_card!='WILD': 
        phase.vd+=1
    if not draw.vd and 3 in previous_move:
        sets.vd+=1
    if not draw.vd:
        discards.vd+=1
    ###End_of_Section###    
    
    ##Desire_Core###
    desire_dict={}
    for value in 'A234567890JQK':
        for suit in 'SCHD':
            desire_dict[value+suit]=0
    if "I'm just a folder mate" and phase.vd: 
        if current_phase in [1, 3]:
            break_value=Counter([item[0] for item in hand_no_wild])\
                        .most_common(5)
            adjust=0
            counter=0
            for value in break_value:
                if value[1]<0.5*current_phase+2.5:
                    if break_value.index(value)>0 and value[1]==break_value\
                           [break_value.index(value)-1][1]:
                            adjust+=1
                    for suit in 'SCHD':
                        desire_dict[value[0]+suit]=5-break_value.index(value)\
                                                   +adjust
                if value[1]==0.5*current_phase+2.5:
                    for suit in 'SCHD':
                        desire_dict[value[0]+suit]=4.5
            if wild_count<current_phase+1:
                for suit in 'SCHD':
                    desire_dict['A'+suit]=33
            else:
                for suit in 'SCHD':
                    desire_dict['A'+suit]=4.5

        if current_phase==2:
            break_suit=Counter([item[1] for item in hand_no_wild]).most_common\
                       (4)
            adjust=0
            for suit in break_suit:
                if break_suit.index(suit)>0 and suit[1]==break_suit\
                           [break_suit.index(suit)-1][1]:
                            adjust+=1
                for value in 'A234567890JQK':
                    desire_dict[value+suit[0]]=5-break_suit.index(suit)+adjust
            if wild_count<5:
                for suit in 'SCHD':
                    desire_dict['A'+suit]=33
            else:
                for suit in 'SCHD':
                    desire_dict['A'+suit]=4.5
        
        if current_phase==4:
            break_value=[]
            hand_value=list(map(valuefunc, hand_no_wild))
            for card in hand_value:
                 break_value.append([(card,item) for item in hand_value
                                     [hand_value.index(card)+1:] if card!=item])
            break_point=sorted(unpack(break_value), 
                               key=lambda x:abs(8-abs(x[0]-x[1])))           
            count=0
            for item in break_point[-5:]:
                count+=1
                range_value=set(filter(lambda x:14>x>1 and x not in hand_value, list(range(item[0],
                            item[0]+8))+list(range(item[1]-8, item[1]))))
                for value in range_value:
                    for suit in 'SCHD':
                        desire_dict[valuefunc(value, r=True)+suit]=count
            if wild_count<6:
                for suit in 'SCHD':
                    desire_dict['A'+suit]=33
            else:
                for suit in 'SCHD':
                    desire_dict['A'+suit]=4.5
                    
        if current_phase==5:
            break_value=Counter([item[0] for item in hand_no_wild]).most_common\
                        (5)
            break_point=[item for item in break_value if item[1]>1]
            #counter>1?
            if break_point:
                #if value completed:
                if break_point[0][1]+wild_count<4:
                    adjust=0
                    for item in break_point:
                        if break_point.index(item)>0 and item[1]==break_point\
                           [break_point.index(item)-1][1]:
                            adjust+=1
                        for suit in 'SCHD':
                            desire_dict[item[0]+suit]=5-break_point.index(item)\
                                                      +adjust
                    #Wild process
                    if wild_count<4:
                        for suit in 'SCHD':
                            desire_dict['A'+suit]=33
                    else:
                        for suit in 'SCHD':
                            desire_dict['A'+suit]=4.5
            #counter<1?
            else:
                for item in break_value:
                    for suit in 'SCHD':
                        desire_dict[item[0]+suit]=5
                for suit in 'SCHD':
                            desire_dict['A'+suit]=33
            
            break_value=[]
            hand_value=list(map(valuefunc, hand_no_wild))
            for card in hand_value:
                 break_value.append([(card,item) for item in hand_value
                                     [hand_value.index(card)+1:] if card!=item])
            break_point=sorted(unpack(break_value), 
                               key=lambda x:abs(8-abs(x[0]-x[1])))           
            count=0
            for item in break_point[-5:]:
                count+=1
                range_value=set(filter(lambda x:14>x>1, list(range(item[0]-4,
                            item[0]+4))+list(range(item[1]-4, item[1]+4))))
                for value in range_value:
                    for suit in 'SCHD':
                        desire_dict[valuefunc(value, r=True)+suit]=count
    ###End_of_Section###
 
    ###Desire_Dict_Controls###
    desire_dict['6S']=0
    read(desire_dict)
    desire_sort_suit=lambda item:sum([desire_dict[item+suit] for suit in 
                                      'SCHD'])
    desire_sort_value=lambda item:sum([desire_dict[value+item] for value in 
                              '234567890JQK'])
    desire_sort=lambda item:desire_dict[item]
    ###End_of_Section###

    ###Move_Core###
    if draw.vd:
        if discard:
            if desire_dict[discard]>4:
                return (2, discard)
        return (1, None)
    
    if phase.vd:
        if current_phase in (1, 3):
            suspect=Counter([item[0] for item in hand_no_wild]).most_common(5)
            capacity=int(0.5*current_phase+2.5)
            group=[item[0] for item in suspect if item[1]+wild_count>0.5*
                      current_phase+1.5 and item[1]>1]
            if len(group)>1:
                group=sorted(group, key=desire_sort_suit)
                group_a=sorted([item for item in hand_no_wild if item[0]==group[0]],
                           key=desire_sort)               
                group_b=sorted([item for item in hand_no_wild if item[0]==group[1]], 
                           key=desire_sort)
                if len(group_a)>=capacity and len(group_b)>=capacity:
                    return (3, [tuple(group_a[:capacity]), tuple(group_b[:capacity])])
                else:
                    for item in (group_a, group_b):
                        while len(item)<capacity:
                            item.append(wild[0])
                            wild.remove(wild[0])
                    return  (3, [tuple(group_a[:capacity]), tuple(group_b[:capacity])])
  
        if current_phase==2:
            suspect=Counter([item[1] for item in hand_no_wild]).most_common(5)
            capacity=7
            group=([item[0] for item in suspect if item[1]+wild_count>6 
                           and item[1]>1])
            if group:
                group=sorted(group, key=desire_sort_value)
                group_output=sorted([item for item in hand_no_wild if item[1]==group[0]], 
                                key=desire_sort, reverse=True)
                if len(group_output)>=capacity:
                    return (3, [tuple(group_output[:7])])
                else:
                    while len(group_output)<capacity:
                        group_output.append(wild[0])
                        wild.remove(wild[0])
                    return (3, [tuple(group_output[:7])])
                 
        if current_phase==4:
            count, wild_break, counter, output_group=0, 0, -1, []
            input_group=sorted(hand_no_wild, key=valuefunc)
            start_card=input_group[0]
            for card in input_group:
                cur_value=count+valuefunc(start_card[0])
                if valuefunc(card)!=cur_value or not cur_value in range(2, 14):
                    same_value_lock=0
                    counter+=1
                    try:
                        if card[0]==input_group[counter-1]:
                            if sorted([card, input_group[counter-1]], key=desire_sort_value)==[card, input_group[counter-1]]:
                                del output_group[-1]
                                output_group.append(card)
                            same_value_lock=1
                    except IndexError:
                        pass
                    if wild_count and not same_value_lock:
                        while count+valuefunc(start_card[0])!=valuefunc(card):
                            print(output_group, count+valuefunc(start_card[0]))
                            if not wild_count:
                                wild_break=1
                                break
                            wild_count-=1
                            output_group.append(wild[0])
                            wild.remove(wild[0])
                            count+=1
                        if not wild_break:
                            output_group.append(card)
                            count+=1
                    elif not same_value_lock:
                        start_card=card
                        count=0
                        output_group=[card]
                elif valuefunc(card)==cur_value and cur_value in range(2, 14):
                    output_group.append(card)
                    count+=1
            if len(output_group)+wild_count>=8 and len(output_group)<8:
                if int(output_group[0][0])>7:
                    while len(output_group)<8:
                        output_group.insert(0, wild[0])
                        wild.remove(wild[0])
                        wild_count-=1
                elif int(output_group[0][0])==7:
                    while len(output_group)<7:
                        output_group.append(wild[0])
                        wild.remove(wild[0])
                        wild_count-=1
                    output_group.insert(0, wild[0])
                if len(output_group)>7 and len([card for card in output_group if card[0]!='A'])>1:
                    return (3, [output_group])

        if current_phase==5:
            colour_r=sorted([card for card in hand_no_wild if colour(card)=='R']
                                         , key=valuefunc)
            colour_b=sorted([card for card in hand_no_wild if colour(card)=='B']
                                          , key=valuefunc)
            for group in [colour_r, colour_b]:
                counter=0
                output_group, suspect_group=[], []
                for card in group:
                    if counter+1<len(group):
                        if group[counter+1]-card=1:
                            try:
                                if group[counter+2]-group[counter+1]=1:
                                    output_group.append((card, group[counter+1]), group[counter+2])
                                else:
                                    suspect_group.append((card, group[counter+1]))
                            except IndexError:
                                pass
                        
                        if 0<group[counter+1]-card<3
                        counter+=1
                
        
     
    if sets.vd:
        #blablabla
         pass
         
    if discards.vd:
        discards_card=sorted(hand, key=desire_sort)[0]
        return (5, discards_card)
    ###End_of_Section###
    
     
#EOF   

    
    
 ##############################################################################
if __name__ == '__main__':
    start=time.clock()
    ######
    player_id=1
    table=[(None, []), (None, []), (None, []), (None, [])]
    turn_history=[(0, [(2, 'JS'), (5, 'JS')]), (1, [(2, 'JS')])]
    phase_status=[0, 4, 0, 0]
    hand=['7H', '8H', '9S', '9D', '5D']
    discard='2S'
    play=phasedout_play(player_id, table, turn_history, phase_status, hand, discard)
    is_valid=phasedout_is_valid_play(play, player_id, table, turn_history, phase_status, hand, discard)
    ######
    end=time.clock()
    print('Result:', play)
    print('Is_Valid?:', is_valid)
    print('Program executed in', end-start, 'Seconds')
    






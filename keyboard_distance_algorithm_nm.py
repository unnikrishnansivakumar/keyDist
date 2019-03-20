#Owner: Rajesh MP
#Function: To get the distance between two strings in terms of 
#Keyboard layout smaller case#Developers: Unnikrishnan S, Sini GM,Anoop Pallipatuillom
#Last Updated on 2/7/2018
#Last Update By Unnikrishnan S

from scipy.spatial.distance import euclidean
import numpy as np
from alignment import Needleman, Hirschberg

#Keyboard layout smaller case
qwertyKeyboardArray = [
    ['`','1','2','3','4','5','6','7','8','9','0','-','='],
    ['q','w','e','r','t','y','u','i','o','p','[',']','\\'],
    ['a','s','d','f','g','h','j','k','l',';','\'','*','*'],
    ['z','x','c','v','b','n','m',',','.','/','*','*',' '],
    ]

#Keyboard layout upper case
qwertyShiftedKeyboardArray = [
    ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+','`'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"','`','*'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?','','',''],
    ]


def get_coordinates(char_val):
    '''get coordinate of the key in th keyboard uses the keyboard layout  qwertyKeyboardArray,qwertyShiftedKeyboardArray
        input: char_val
        output: coordinate values'''
    lower_case = np.array(qwertyKeyboardArray)
    upper_case = np.array(qwertyShiftedKeyboardArray)
    if (np.where(lower_case==char_val)[0].size!=0 and np.where(lower_case==char_val)[1].size!=0) or char_val!='*':
        x,y = np.where(lower_case==char_val)
    else:
        x,y = np.where(upper_case==char_val)
    return x[0],y[0]



def calc_euc_dist(a,b):
    '''get euclidean distance between a and b  given the keys
        input: a,b
        output: euclidean distance '''
    print("vals =",a,b)
    val1 = get_coordinates(a)
    val2 = get_coordinates(b)
    return euclidean(val1,val2)



def get_pos_values(stra):
    ''' get the position values of the needleman wunsch string'''
    pos_counter = {}
    counter = 0
    for i in range(len(stra)):
        if stra[i]!='|':
            counter+=1
            pos_counter[i]=counter-1
        else:
            pos_counter[i]=counter-1
    return pos_counter



def keyboard_typosim_algo(s1,s2):
    '''get euclidean distance based proximity score between a and b  given the keys for char substitution
        input: a,b
        output: proximity score ranging from zero to one '''
    s1 = s1.lower()
    s2 = s2.lower()
    change_log = identify_type_ops(s1,s2)
    print(change_log)
    euc_dist = 0
    if len(change_log) == (len(s1)+len(s2)-1):
        euc_dist = 3*max(len(s1),len(s2))
    elif s1==s2:
        euc_dist = 0
    else:
        for typ_err,pos in change_log:
            if typ_err =='sub':
                euc_dist+=calc_euc_dist(s1[pos],s2[pos])
            elif typ_err =='ins':
                if pos !=len(s1)-1 and pos!=0:
                    euc_dist+=(calc_euc_dist(s1[pos],s2[pos-1])+calc_euc_dist(s1[pos],s2[pos]))/2
                elif pos==0:
                    euc_dist += calc_euc_dist(s1[pos],s2[pos])
                else:
                    euc_dist += calc_euc_dist(s1[pos],s2[pos-1])
            else:
                euc_dist+=1.0
    # print('dist is ',euc_dist)
    prob_typo = 1-(euc_dist/(3*max(len(s1),len(s2))))
    return prob_typo



def keyboard_typosim_dist(s1,s2):
    '''get euclidean distance based proximity score between a and b  given the keys for char substitution
        input: a,b
        output: proximity score ranging from zero to one '''
    s1 = s1.lower()
    s2 = s2.lower()
    change_log = identify_type_ops(s1,s2)
    euc_dist = 0
    if len(change_log) == (len(s1)+len(s2)-1):
        euc_dist = 3*max(len(s1),len(s2))
    elif s1==s2:
        euc_dist = 0
    else:
        for typ_err,pos in change_log:
            if typ_err =='sub':
                euc_dist+=calc_euc_dist(s1[pos],s2[pos])
            elif typ_err =='ins':
                if pos !=len(s1)-1 and pos!=0:
                    euc_dist+=(calc_euc_dist(s1[pos],s2[pos-1])+calc_euc_dist(s1[pos],s2[pos]))/2
                elif pos==0:
                    euc_dist += calc_euc_dist(s1[pos],s2[pos])
                else:
                    euc_dist += calc_euc_dist(s1[pos],s2[pos-1])
            else:
                euc_dist+=1.0
    return euc_dist   



def identify_type_ops(str1,str2):
    ''' Based on needleman wunsch algorithm we identify the type of operations performed
        Input: String1,String2
        Output: changelog
    '''
    str1 = str1.strip()
    str2 = str2.strip()
    seqa = list(str1)
    seqb = list(str2)
    # Align using Needleman-Wunsch algorithm.
    n = Needleman()
    a,b = n.align(seqa, seqb)
    try:
        val_list = np.array(a)!=np.array(b)
    except:
        val_list = []
    positions = np.where(val_list == True)[0]
    consa = np.array([a,b])
    pos_a_corr = get_pos_values(a)
    pos_b_corr = get_pos_values(b)
    print(consa)
    posb = np.where(np.array(b)=='|')
    posa = np.where(np.array(a)=='|')
    change_log = []
    # print(pos_b_corr)
    print(posa)
    print(posb)
    for i in np.ravel(posb):
        print(i,len(a),len(b))
        if i==len(a)-1:
            if a[i-1]=='|' and b[i]=='|':
                change_log.append(('sub',pos_b_corr[i]))
            else:
                change_log.append(('ins',pos_a_corr[i]))
        elif a[i+1]=='|':
            change_log.append(('sub',pos_b_corr[i]+1))
        else:
            change_log.append(('ins',pos_a_corr[i]))     
    for i in np.ravel(posa):
        try:
            if i!=len(a)-2:
                if a[i]=='|':
                    if b[i-1]!='|':
                        change_log.append(('del',pos_a_corr[i]))                
        except IndexError:
            print("Empty String!")
    return change_log



if __name__ == '__main__':
    print('Similarity is ',keyboard_typosim_algo('Benjasini Luthef','Benjamin Luthes'))

    


#Function: To get the distance between two strings in terms of 
#Keyboard layout smaller case

from scipy.spatial.distance import euclidean
import numpy as np
import Levenshtein

#Keyboard layout smaller case
qwertyKeyboardArray = [
    ['`','1','2','3','4','5','6','7','8','9','0','-','='],
    ['q','w','e','r','t','y','u','i','o','p','[',']','\\'],
    ['a','s','d','f','g','h','j','k','l',';','\'','*','*'],
    ['z','x','c','v','b','n','m',',','.','/','*','*',' '],
    ]

#Keyboard layout upper case
qwertyShiftedKeyboardArray = [
    ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_','+'],
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
    if (np.where(lower_case==char_val)[0].size!=0 and np.where(lower_case==char_val)[1].size!=0) or char_val=='*':
        x,y = np.where(lower_case==char_val)
    else:
        x,y = np.where(upper_case==char_val)
    return x[0],y[0]



def calc_euc_dist(a,b):
    '''get euclidean distance between a and b  given the keys
        input: a,b
        output: euclidean distance '''
    # print("vals =",a,b)
    val1 = get_coordinates(a)
    val2 = get_coordinates(b)
    return euclidean(val1,val2)



def keyboard_weighted_levenshtein(a,b):
    '''get the distance between strings using a weighted levenshtein method'''
    a=a.lower().strip()
    b=b.lower().strip()
    ss = Levenshtein.editops(a,b) 
    cost=0
    for i,j,k in ss:
        if i=="delete":
            cost+=1
        elif i=="replace":
            cost+=calc_euc_dist(a[j],b[k])
        elif i=="insert":
            ins_cost=calc_euc_dist(a[j-1],b[k])
            if j<len(a):
                ins_cost+=calc_euc_dist(a[j],b[k])
                cost+=ins_cost/2
            else:
                cost=ins_cost
    return cost


if __name__ == '__main__':
    print(keyboard_weighted_levenshtein('test','testing'))

    


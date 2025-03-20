from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))

import numpy



THE_DTYPE = numpy.float32#可以改，但是一般不用改
STEP_LENGTH = 0.1#可以改

#下面两个加起来不超过1.
SELF_REACT_STRENGTH_MAX = 0.5#可以改
CROSS_REACT_STRENGTH_MAX = 0.5#可以改
if SELF_REACT_STRENGTH_MAX + CROSS_REACT_STRENGTH_MAX > 1.:
    raise Exception("emmm.")

ingre_names = ["a","b","c",]#"d",]#可以改
ingre_len = ingre_names.__len__()
iota_ingre_len = numpy.linspace(0,ingre_len-1,num=ingre_len, dtype=numpy.int64)

#global tool
def ingre_index_lookup(name:str)->int:
    for i, name_from_table in enumerate(ingre_names):
        if name_from_table == name:
            return i
        pass        
    return -1



outside_self_react_strength_n_n:numpy.ndarray = numpy.zeros([ingre_len,ingre_len],dtype=THE_DTYPE)
outside_self_react_consuption_n:numpy.ndarray = numpy.zeros([ingre_len],dtype=THE_DTYPE)
def set_self_react(ingre:int, prod:int, strength:float):
    if strength<0:
        raise Exception("strength must >= 0.")
    if (ingre == prod) and strength!=0.:
        raise Exception("diagonal is designed to be 0.")
    outside_self_react_strength_n_n[ingre, prod] = strength
    outside_self_react_consuption_n[ingre] = outside_self_react_strength_n_n[ingre,:].sum()
    pass

def set_self_react_with_name(ingre:str, prod:str, strength:float):
    ingre_ind = ingre_index_lookup(ingre)
    prod_ind = ingre_index_lookup(prod)
    set_self_react(ingre_ind, prod_ind, strength)
    pass

def get_self_react_strength(ingre:int, prod:int)->float:
    return outside_self_react_strength_n_n[ingre, prod]
def get_self_react_consuption(ingre:int)->float:
    return outside_self_react_consuption_n[ingre]
def calc_self_react_consuption(outside_self_react_table)->numpy.ndarray:
    result_n:numpy.ndarray = outside_self_react_table.sum(axis=1)
    return result_n
#outside_self_react_consuption_n = calc_self_react_consuption(outside_self_react_table_n_n)
if False:    
    set_self_react(0,1,0.1)
    set_self_react(0,1,0.1)
    set_self_react(0,2,0.1)
    pass
if "print out" and False:
    print(outside_self_react_strength_n_n)
    print(outside_self_react_consuption_n)
    pass
def ____check_self_react_table():
    #condition 1, all >= 0
    temp1 = outside_self_react_strength_n_n.__ge__(0.)
    if not(temp1.all()):
        raise Exception("all elements must be >= 0")
    temp1 = outside_self_react_consuption_n.__ge__(0.)
    if not(temp1.all()):
        raise Exception("Some bug exists in this code. Report to the author.")
    #condition 2, diagonal == 0
    temp2 = outside_self_react_strength_n_n[iota_ingre_len,iota_ingre_len]
    zeros_n = numpy.zeros([ingre_len])
    temp_flag = temp2.__eq__(zeros_n)
    if not(temp_flag.all()):
        raise Exception("diagonal elements are designed as zeros.")
    #condition 3, sum < the max constant. This check is actually a repeating to part of set_strength function.
    #raise Exception("untested")
    temp3_n:numpy.ndarray = outside_self_react_strength_n_n.sum(axis=1)
    temp4_n = temp3_n.__lt__(SELF_REACT_STRENGTH_MAX)
    if not(temp4_n.all()):
        raise Exception("emmm react too quickly.")
    pass
____check_self_react_table()

outside_cross_react_strength_n_n_n:list[numpy.ndarray] = []
for i in range(1,ingre_len):
    temp_table = numpy.zeros([ingre_len-i,ingre_len],dtype=THE_DTYPE)
    outside_cross_react_strength_n_n_n.append(temp_table)
    pass
outside_cross_react_consuption_original_n_n_n:numpy.ndarray = numpy.zeros([ingre_len,ingre_len,ingre_len],dtype=THE_DTYPE)
outside_cross_react_consuption_n_n:numpy.ndarray = numpy.zeros([ingre_len,ingre_len],dtype=THE_DTYPE)
def print_outside_cross_react_strength():
    print("outside_cross_react_strength_n_n_n:")
    for sub_ndarray in outside_cross_react_strength_n_n_n:
        print(sub_ndarray)
        pass
    pass
def set_cross_react(ingre1:int, ingre2:int, prod:int, strength1:float, strength2:float):
    if strength1<0 or strength2<0:
        raise Exception("strength must >= 0.")
    total_strength = strength1 + strength2
    if ingre1 == ingre2:
        raise Exception("ingre1 must != ingre2.")
    ingre1_ = ingre1
    ingre2_ = ingre2
    strength1_ = strength1
    strength2_ = strength2
    if ingre1>ingre2:#swap them.
        ingre1_ = ingre2
        ingre2_ = ingre1
        strength1_ = strength2
        strength2_ = strength1
        pass
    outside_cross_react_strength_n_n_n[ingre1_][ingre2_-ingre1_-1, prod] = total_strength
    outside_cross_react_consuption_original_n_n_n[ingre1_,ingre2_,prod] = strength1_
    outside_cross_react_consuption_original_n_n_n[ingre2_,ingre1_,prod] = strength2_
    outside_cross_react_consuption_n_n[ingre1_,ingre2_] = outside_cross_react_consuption_original_n_n_n[ingre1_,ingre2_].sum()
    outside_cross_react_consuption_n_n[ingre2_,ingre1_] = outside_cross_react_consuption_original_n_n_n[ingre2_,ingre1_].sum()
    pass

def set_cross_react_with_name(ingre1:str, ingre2:str, prod:str, strength1:float, strength2:float):
    ingre1_ind = ingre_index_lookup(ingre1)
    ingre2_ind = ingre_index_lookup(ingre2)
    prod_ind = ingre_index_lookup(prod)
    set_cross_react(ingre1_ind, ingre2_ind, prod_ind, strength1, strength2)
    pass

if "test" and False:
    set_cross_react(0,1,3,0.1,0.11)
    set_cross_react(1,0,3,0.1,0.11)
    set_cross_react(0,2,3,0.2,0.22)
    #set_cross_react(0,1,2,0.1,0.2)
    
    #print_outside_cross_react_strength()
    print(outside_cross_react_consuption_original_n_n_n)
    print(outside_cross_react_consuption_n_n)
    pass
def get_cross_react_strength(ingre1:int, ingre2:int, prod:int)->float:
    if ingre1 == ingre2:
        raise Exception("ingre1 must != ingre2.")
    ingre1_ = ingre1
    ingre2_ = ingre2
    if ingre1>ingre2:#swap them.
        ingre1_ = ingre2
        ingre2_ = ingre1
        pass
    strength = outside_cross_react_strength_n_n_n[ingre1_][ingre2_-ingre1_-1, prod]
    return strength        
if "test" and False:
    fds=get_cross_react_strength(0,1,3)
    set_cross_react(0,1,3,0.1,0.11)
    fds=get_cross_react_strength(0,1,3)
    set_cross_react(1,0,3,0.2,0.22)
    fds=get_cross_react_strength(0,1,3)
    pass
def get_cross_react_consuption(ingre1:int, ingre2:int, prod:int)->tuple[numpy.float32,numpy.float32]:
    if ingre1 == ingre2:
        raise Exception("ingre1 must != ingre2.")
    ingre1_ = ingre1
    ingre2_ = ingre2
    if ingre1>ingre2:#swap them.
        ingre1_ = ingre2
        ingre2_ = ingre1
        pass
    strength1_ = outside_cross_react_consuption_original_n_n_n[ingre1_][ingre2_, prod]
    strength2_ = outside_cross_react_consuption_original_n_n_n[ingre2_][ingre1_, prod]
    print(type(strength1_))
    if ingre1<ingre2:#swap them.
        return(strength1_,strength2_)
    else:
        return(strength2_,strength1_)
if "test" and False:
    fds=get_cross_react_consuption(0,1,3)
    set_cross_react(0,1,3,0.1,0.11)
    fds=get_cross_react_consuption(0,1,3)
    fds=get_cross_react_consuption(1,0,3)
    set_cross_react(1,0,3,0.2,0.22)
    fds=get_cross_react_consuption(0,1,3)
    fds=get_cross_react_consuption(1,0,3)
    pass
# def get_cross_react_prod_with_only_ingre(ingre1:int, ingre2:int)->numpy.ndarray:
#     if ingre1 == ingre2:
#         raise Exception("ingre1 must != ingre2.")
#     if ingre1>ingre2:#swap them.
#         temp = ingre1
#         ingre1 = ingre2
#         ingre2 = temp
#         pass
#     继续。
#     return outside_cross_react_strength_n_n_n[ingre1][ingre2-ingre1-1, :]

def get_cross_react_consuption_for_1_ingre(ingre:int)->numpy.float32:
    temp1:numpy.ndarray = outside_cross_react_consuption_n_n[ingre]
    temp2 = temp1.sum()
    #print(type(temp2))
    return temp2
if "test" and False:
    fds=get_cross_react_consuption_for_1_ingre(0)
    set_cross_react(0,1,3,0.1,0.11)
    fds=get_cross_react_consuption_for_1_ingre(0)
    set_cross_react(0,1,3,0.2,0.22)
    fds=get_cross_react_consuption_for_1_ingre(0)
    set_cross_react(0,2,3,0.1,0.11)
    fds=get_cross_react_consuption_for_1_ingre(0)
    set_cross_react(1,2,3,0.1,0.11)
    fds=get_cross_react_consuption_for_1_ingre(0)
    pass
def get_cross_react_consuption_for_all()->numpy.ndarray:
    temp1:numpy.ndarray = outside_cross_react_consuption_n_n.sum(axis=1)
    #print(type(temp2))
    return temp1
if "test" and False:
    fds=get_cross_react_consuption_for_all()
    set_cross_react(0,1,3,0.1,0.11)
    fds=get_cross_react_consuption_for_all()
    set_cross_react(0,1,3,0.2,0.22)
    fds=get_cross_react_consuption_for_all()
    set_cross_react(0,2,3,0.1,0.11)
    fds=get_cross_react_consuption_for_all()
    set_cross_react(1,2,3,0.1,0.11)
    fds1=get_cross_react_consuption_for_all()
    pass

if False:
    set_cross_react(0,1,3,0.01,0.02)
    set_cross_react(0,2,3,0.01,0.02)
    pass
def ____check_react_table():
    #condition 1, all >= 0
    for numpy_ndarryr in outside_cross_react_strength_n_n_n:
        temp1 = numpy_ndarryr.__ge__(0.)
        if not(temp1.all()):
            raise Exception("all elements must be >= 0")
        pass
    temp1 = outside_cross_react_consuption_original_n_n_n.__ge__(0.)
    if not(temp1.all()):
        raise Exception("all elements must be >= 0")
    temp1 = outside_cross_react_consuption_n_n.__ge__(0.)
    if not(temp1.all()):
        raise Exception("all elements must be >= 0")
    #condition 2, diagonal are 0s.
    temp2 = outside_cross_react_consuption_original_n_n_n[iota_ingre_len,iota_ingre_len,:]
    temp3 = temp2.__eq__(0.)
    if not(temp1.all()):
        raise Exception("diagonal are designed to be all 0s.")
    temp2 = outside_cross_react_consuption_n_n[iota_ingre_len,iota_ingre_len]
    temp3 = temp2.__eq__(0.)
    if not(temp1.all()):
        raise Exception("diagonal are designed to be all 0s.")
    
    #condition 3, sum < the max constant.
    # logically:
    # 1111  2...  .3..  ..4.  ...5
    #  ...   222   3..   .4.   ..5
    #   ..    ..    33    4.    .5
    #    .     .     .     4     5
    # programmingly:
    # 1111  2...  .3..  ..4.  ...5
    # ...   222   3..   .4.   ..5
    # ..    ..    33    4.    .5
    # .     .     .     4     5  
    # but I decide to use a simpler but slower method.
    temp_consuption:numpy.ndarray = get_cross_react_consuption_for_all()
    temp1 = temp_consuption.__lt__(CROSS_REACT_STRENGTH_MAX)
    if not(temp1.all()):
        raise Exception("emmm react too quickly.")
    pass
____check_react_table()


#请将从db生成器.py得到的代码复制到这里。



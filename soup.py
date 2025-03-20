import numpy
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))

#改这个名字
#from example_db import THE_DTYPE, STEP_LENGTH, ingre_len, ingre_names, ingre_index_lookup, print_outside_cross_react_strength, outside_self_react_strength_n_n, outside_self_react_consuption_n, set_self_react, outside_cross_react_strength_n_n_n, outside_cross_react_consuption_n_n, set_cross_react, print_outside_cross_react_strength
from test_db import THE_DTYPE, STEP_LENGTH, ingre_len, ingre_names, ingre_index_lookup, print_outside_cross_react_strength, outside_self_react_strength_n_n, outside_self_react_consuption_n, set_self_react, outside_cross_react_strength_n_n_n, outside_cross_react_consuption_n_n, set_cross_react, print_outside_cross_react_strength




class Soup:
    def __init__(self, step_len:float = STEP_LENGTH):
        assert step_len>0
        self.cont_n:numpy.ndarray = numpy.zeros([ingre_len,],dtype=THE_DTYPE)
        self.step_len:float = step_len
        pass
    def __str__(self):
        temp = ""
        for i in range(ingre_len):
            amount = self.cont_n[i]
            if amount > 0:
                temp += f"{ingre_names[i]}:{amount:.3f}, "
                pass
            pass
        if temp.__len__() == 0:
            return "Soup is empty."
        else:
            return "Content of this soup:  "+temp
        #end of function
        
    def add(self, ingre_name:str, amount:float):
        ingre_index = ingre_index_lookup(ingre_name)
        if ingre_index<0:
            raise Exception(f"{ingre_name} is not a correct name.")
        if amount<0.:
            raise Exception("amount must be >= 0.")
            
        self.cont_n[ingre_index]+=amount
        pass
    
    def react(self, duration, max_step = 10000)->None:
        steps = int(duration/self.step_len)
        assert steps<=max_step, "duration too long. If you mean to do this, set max_step to a bigger value."
        assert steps>=1, "duration too short, or negative."
        
        total_amount:float = self.cont_n.sum()
        if 0. == total_amount:
            raise Exception("It's empty???")
        norm_ed_cont_n:numpy.ndarray = self.cont_n/total_amount
        
        for i in range(steps):
            total_offset_n:numpy.ndarray = numpy.zeros_like(norm_ed_cont_n)
            
            #self react prod
            self_react_strength_n_n = outside_self_react_strength_n_n*self.step_len
            
            reshaped_norm_ed_cont_1_n = norm_ed_cont_n.reshape((1,ingre_len))
            offset_from_self_react_prod_1_n = reshaped_norm_ed_cont_1_n.__matmul__(self_react_strength_n_n)
            offset_from_self_react_prod_n = offset_from_self_react_prod_1_n.reshape((ingre_len))
            #self react consuption
            self_react_consuption_n = outside_self_react_consuption_n*self.step_len
            offset_from_self_react_consuption_n = norm_ed_cont_n.__mul__(self_react_consuption_n)
            
            #cross react prod
            cross_react_strength_n_n_n:list[numpy.ndarray] = []
            for sub_outside_cross_react_table_n_n in outside_cross_react_strength_n_n_n:
                cross_react_strength_n_n_n.append(sub_outside_cross_react_table_n_n*self.step_len)
                pass
            cross_react_prod_n = numpy.zeros([ingre_len],dtype=THE_DTYPE)
            for i in range(ingre_len-1):
                norm_ed_cont_of_i = norm_ed_cont_n[i]
                if norm_ed_cont_of_i>0:
                    sliced_norm_ed_cont__:numpy.ndarray = norm_ed_cont_n[i+1:]
                    scaled_sliced_norm_ed_cont__ = sliced_norm_ed_cont__*norm_ed_cont_of_i
                    reshaped_scaled_sliced_norm_ed_cont_1__:numpy.ndarray = scaled_sliced_norm_ed_cont__.reshape([1,ingre_len-i-1])
                    
                    cross_react_strength_for_this_iter___n = cross_react_strength_n_n_n[i]
                    cross_react_1_n = reshaped_scaled_sliced_norm_ed_cont_1__.__matmul__(cross_react_strength_for_this_iter___n)
                    reshaped_cross_react_n = cross_react_1_n.reshape([ingre_len])
                    cross_react_prod_n += reshaped_cross_react_n
                    pass
                pass
            
            #cross react consuption
            cross_react_consuption_n_n = outside_cross_react_consuption_n_n*self.step_len
            
            self_cross_square_of_norm_ed_cont_n_n = norm_ed_cont_n.reshape([ingre_len,1])*norm_ed_cont_n.reshape([1,ingre_len])
            cross_react_consuption_before_sum_n_n = self_cross_square_of_norm_ed_cont_n_n.__mul__(cross_react_consuption_n_n)
            cross_react_consuption_n = cross_react_consuption_before_sum_n_n.sum(axis=1)
            
            #sum them up.
            total_offset_n += offset_from_self_react_prod_n
            total_offset_n -= offset_from_self_react_consuption_n
            total_offset_n += cross_react_prod_n
            total_offset_n -= cross_react_consuption_n
            norm_ed_cont_n += total_offset_n
            
            # always some ieee754 error. Some correction(normalization)   
            div_this = norm_ed_cont_n.sum()
            norm_ed_cont_n /= div_this
            pass#for i in range(steps):
        self.cont_n = norm_ed_cont_n*total_amount
        
        pass#end of function
    
    pass

if "self react test" and True:
    print(outside_self_react_strength_n_n)
    print(outside_self_react_consuption_n)
    set_self_react(0,1,0.1)
    print("----------------set---------------")
    print(outside_self_react_strength_n_n)
    print(outside_self_react_consuption_n)
    
    s = Soup()
    s.add("a", 1.)
    print(s)
    s.react(0.1)
    print("---------------after reacting-------------")
    print(s)
    pass
if "cross react test" and True:
    print_outside_cross_react_strength()
    print(outside_cross_react_consuption_n_n)
    set_cross_react(0,1,2,0.1,0.2)
    print("----------------set---------------")
    print_outside_cross_react_strength()
    print(outside_cross_react_consuption_n_n)
    
    s = Soup()
    s.add("a", 1.)
    s.add("b", 1.)
    print(s)
    s.react(0.1)
    print("---------------after reacting-------------")
    print(s)
    pass
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 17:14:37 2018

@author: nathanielreisenburg
"""
from itertools import islice
from pandas import read_excel
from operator import itemgetter

import os.path




BASE = os.path.dirname(os.path.abspath(__file__))


#PROTOTYPES
############################################################

#calcs to be added
'''
<<<dataframe splitting>>>
  def convert_match_df_index(self):
        if self.var.get() == "Was there a defect in the product upon delivery?":
            return "Defects in goods"
        elif self.var.get() == "Was the item an imitation/knockoff?":
            return "Imitation, pirated"
        elif self.var.get() == "Were the wrong goods delivered?":
            return "Delivered wrong goods"
        elif self.var.get() == "Were the wrong number of goods delivered?":
            return "Delivered wrong number"
        elif self.var.get() == "Was the seller at fault for some misc reason?":
            return "Fault on Seller's part in general"
        else:
            return "Defect is Buyer's Fault"

 <<<results>>>       
    def make_label_solution(self):
        if self.label_solution[self.label_counter] == 1:
            text = "Full Refund/Exchange & Delivery Cost Borne by Seller"
        elif self.label_solution[self.label_counter] == 2:
            text = "Exchange or Refund Offered + Delivery Cost Born by Buyer"
        elif self.label_solution[self.label_counter] == 3:
            text = "Refund Only & Delivery Cost Born by Buyer"
        elif self.label_solution[self.label_counter] == 4:
            text = "80% Refund + Delivery Cost Borne by Buyer" 
        elif self.label_solution[self.label_counter] == 5:
            text = "50% Refund + Delivery Cost Borne by Buyer"
        elif self.label_solution[self.label_counter] == 6:
            text = "40% Refund + Delivery Cost Borne by Buyer"
        elif self.label_solution[self.label_counter] == 7:
            text = "Cancelation of Order + Refund"
        else:
            text = "No Refund or Exchange Offered"
        x = Label(self.master, text=text)
        x.place(x=self.xx,y=self.yy)
'''    
#creates unique dictionaries for each group
class CalcDic():  

    def __init__(self,test_number, unsorted_dic):
        dic_use = {}

        self.test_number = test_number
        self.unsorted_dic = unsorted_dic
        self.dic_use = dic_use

     #for simplicity simply included key generator in init  
        for key,value in self.unsorted_dic.items():
            if value[2] == self.test_number:
                dic_use[key] = value

    #this generates individual values, it's never called indp. 
    def indiv_value(self):
        weight_add = 0
        for key,value in self.dic_use.items():
            weight_add = weight_add + value[0]
        return weight_add   
    
        
#FUNCTIONS USED FOR EITHER THE PROGRAM OR FOR TESTING
############################################################
     
#CORE ALGORITHM (!!!CRITICAL!!!)    
#Note that the initilizing code is found near the bottom of this document
def core_calcs(html_form_inputs):
    
    #calc_results is made global in order to avoid re-running the entire function every time the results are called  
    global calc_results
    
    #DATA LOADING AND PROCESSING 
    data = read_excel(os.path.join(BASE, "Rules_v10.xlsx"))
    data.fillna(0, inplace=True)
    data.iloc[:,1:] = data.iloc[:,1:].astype(int)
    
    #Variables used throughout this function
    b = {}
    core = []
    unsatisfied_conditions = {}
    satisfied_conditions = {}
    lst_unique_success = []
    ratio = []

    
    #the dataframe is filtered based on the appropriate "cause of action" i.e. the type of seller/buyer fault so that only relevant rules appear
    #a dictionary is then created with the label = ID; value = list containing the necessary conditions
    
    ######
    #replaced convert_match_df_index with html_form_inputs list indexed to 0. 
    ######
    for i in data[data[html_form_inputs[0]]==1].itertuples():
        b[i.ID] = [x for x in [i[2], list(i[14:20]), i[21]]]
    #print("b list: {}".format(b))    
    
    #tests the keys that are drawn from the dataframe (saved as dictionary b; see above loop) vs those from the user's inputs
    #note that with dictionaries if you re-add value with same label, it does not duplicate. 
    for key, element in b.items():
        for x,y in zip(element, islice(element, 1, 2)):
            for i in range(6):
                if y[i] & html_form_inputs[1][i] == 1:
                    unsatisfied_conditions[key] = element    
                 
    #with the new unsatisfied conditions present, applies a boolean to create a satisfied conditions list. 
    for key,value in b.items():
        if value not in unsatisfied_conditions.values():
            satisfied_conditions[key] = value
    
    #turns over all unsastisfied conditions to the 8th and final option (no refund)
    for key, element in unsatisfied_conditions.items():
        element[2] = 8
        '''
        need to consider how to handle possible duplicate revenue entries being counted under 8. 
        Is it intended? How do we want to handle this?
        '''
    
    #print("\ngroups that have not been kicked out: {}".format(satisfied_conditions))
    #combine the dictionaries. 
    combined_results = {**satisfied_conditions, **unsatisfied_conditions}
    #print("\ncombined results: {}\n".format(combined_results))
    
    #determines how many unique results (out of 8) there are
    [lst_unique_success.append(i[2]) for i in combined_results.values() if i[2] not in lst_unique_success]
    #print("\nlist unique success: {}\n".format(lst_unique_success))
        
    #this creates a group list
    [core.append("group"+ str(i + 1)) for i in range(len(lst_unique_success))]
    #print("\ncore: {}\n".format(core))
    
    #   used to create tupples for each unique group including: group#; group's value; result.      
    counterx=0
    for i in core:
        globals()[i] = CalcDic(lst_unique_success[counterx],combined_results) 
        counterx = counterx +1
    #print("\ngroup1 example(could be up to 8 cores): {}\n".format(group1.indiv_value()))
    
    #helps to identify the total value
    total = 0
    for i in core:
        total = total + globals()[i].indiv_value()
    #print("\ntotal value: {}\n".format(total))
    
    ###creates list of tupples with each tupple including: group#; ratio of the group's value/total value of all options; result.
    for i in core:
        ratio.append(globals()[i].indiv_value() / total)
        
    x = list(zip(core, ratio,lst_unique_success))
    return sorted(x,key=itemgetter(1),reverse=True)


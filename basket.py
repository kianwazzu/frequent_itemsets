#KIAN ANKERSON
#basket class, support table class, freq items classes for apriori algorithm
#For CPTS 315 HW 2


import pandas as pd
from pandas import DataFrame


class basket:
    def __init__(self):
        self.items = []
        self.num_of_items = 0
        self.has_freq_item = False
        self.has_freq_pair = False
        #self.has_freq_triple = False

    def add_item(self, item_id):
        self.items.append(item_id)
        self.num_of_items += 1
    def __str__(self):
        string = f"# Items: {self.num_of_items}. Items: {str(self.items)}"
       # string = f"Items: {self.items}"
        return  string

class support_table:
    def __init__(self):
      #  self.df = DataFrame({'item_id':[None],'support':[None]})
        self.df = DataFrame(columns=['item_id','support'])
    def add_or_update(self, item_id):
        if item_id in self.df.item_id.values:
            old_val = self.df.query('item_id==@item_id')['support']
            old_val = old_val.values[0]

            row_num = self.df[self.df['item_id']==item_id].index[0]
            #this is only updating one value, because theres row numbers
          #  test = self.df.at[row_num, 'support']
            self.df.at[row_num,'support'] = old_val + 1
        else:
            self.df = self.df.append(DataFrame({'item_id':[item_id],'support':[1]}) ,ignore_index=True)

class freq_pairs:
    def __init__(self):
        self.df = DataFrame(columns=['item_id1','item_id2', 'support'])
    def add_or_update(self, first_item,second_item):
        #check if item in the list
        row = self.df.loc[((self.df.item_id1 == first_item) & (self.df.item_id2 == second_item))]
        if row.empty:
            self.df = self.df.append(DataFrame({'item_id1': [first_item], 'item_id2': [second_item], 'support': [1]}), ignore_index=True)
        else:
            #get position
            row_num = row.index[0]
           # row_num = self.df[(self.df['item_id1'] == first_item) & (self.df['item_id2'] == second_item) ].index[0]
            old_val = row['support'].values[0]
          #  test = self.df.at[row_num, 'support'][]
          #  self.df.at
            self.df.at[row_num,'support'] = old_val + 1

class freq_triples:
    def __init__(self):
        self.df = DataFrame(columns=['item_id1','item_id2','item_id3','support'])
    def add_or_update(self, first_item, second_item, third_item):
        row = self.df.loc[((self.df.item_id1 == first_item) & (self.df.item_id2 == second_item) & (self.df.item_id3 == third_item))]
        if row.empty:
            self.df = self.df.append(DataFrame({'item_id1': [first_item], 'item_id2': [second_item], 'item_id3': [third_item], 'support': [1]}), ignore_index=True)
        else:
            #get position
            row_num = row.index[0]
           # row_num = self.df[(self.df['item_id1'] == first_item) & (self.df['item_id2'] == second_item) ].index[0]
            old_val = row['support'].values[0]
          #  test = self.df.at[row_num, 'support'][]
          #  self.df.at
            self.df.at[row_num,'support'] = old_val + 1



def test_sup_table():
    hey = support_table()
    hey.add_or_update(1)
    hey.add_or_update(2)
    hey.add_or_update(3)
    hey.add_or_update(1)
    hey.add_or_update(1)
    hey.add_or_update(2)
    hey.add_or_update(3)
    hey.add_or_update(2)
    hey.add_or_update(1)
    hey.add_or_update(6)
    hey.add_or_update(3)
    yo = 0

if __name__ == "__main__":
    test_sup_table()

import time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

from file_read import read_file
import basket as bk
import numpy as np
from pandas import DataFrame

#in sampledata, support level is 8

def apriori(baskets,support_table, support_level = 100):
    print("Running Apriori Algo...")
    start_time = time.time()
    pass_2_time = time.time()
    #pass 2
    #make a dataframe
    freq_pairs = bk.freq_pairs()
    test = 0
    def keep_frequent(basket, support_table=support_table, support_level=support_level, test = test):
        freq_items = []
        for item in basket.items:
            item_sl = support_table.df.query('item_id==@item')['support'].values[0]
            # item_sl = item_sl.values[0]
            if item_sl >= support_level:
                # add it to temp_items
                freq_items.append(item)
            freq_items.sort()
        basket.items = freq_items
        basket.num_of_items = len(freq_items)
        if basket.num_of_items > 1:
            basket.has_freq_pair = True
            basket.has_freq_item = True
        elif basket.num_of_items > 0:
            basket.has_freq_item = True
        return basket

    def count_pairs(basket,freq_pairs=freq_pairs):
       # def add_pairs(items):
        i = 0
        if basket.num_of_items < 2:
            return
        for item in basket.items:
            i +=1
            #make pairs for all remaining items
            for j in range(i, basket.num_of_items):
                #add the pair to a table
                second_id = basket.items[j]
                first_id = item
                #add or update dataframe
                freq_pairs.add_or_update(first_item=first_id,second_item=second_id)
        return freq_pairs

    freq_triples = bk.freq_triples()
    def count_trips(basket, freq_triples=freq_triples):
        i = 0
        if basket.num_of_items > 2:
            for item in basket.items:
                i += 1
                # make a pair with all other items in baskets
                for j in range(i, basket.num_of_items):
                    for k in range((j + 1), basket.num_of_items):
                        # there's a frequent triple
                        list_to_add = [item, basket.items[j], basket.items[k]]
                        freq_triples.add_or_update(first_item=list_to_add[0], second_item=list_to_add[1],
                                                   third_item=list_to_add[2])
        return  freq_triples

    baskets = list(map(keep_frequent, baskets))

    freq_pairs = list(map(count_pairs, baskets))[0]

    pass_2_time_end = time.time()
    print(f"Pass 2 time {pass_2_time_end - pass_2_time}")
    freq_triples = list(map(count_trips, baskets))[0]
    #pass 3
    #freq_triples = bk.freq_triples()
    #for basket in baskets:
    #    i = 0
    #    #check for a triple
    #    if basket.num_of_items >= 3:
    #        for item in basket.items:
    #            i += 1
    #            #make a pair with all other items in baskets
    #            for j in range(i, basket.num_of_items):
    #                for k in range((j+1),basket.num_of_items):
    #                    #there's a frequent triple
    #                    list_to_add = [item,basket.items[j],basket.items[k]]
    #                    freq_triples.add_or_update(first_item=list_to_add[0],second_item=list_to_add[1],third_item=list_to_add[2])
    # sorting not needed
   # freq_triples.df = freq_triples.df.sort_values(by=['support'], ascending=False)
   # freq_pairs.df = freq_pairs.df.sort_values(by=['support'], ascending=False)
    #only keep ones with support of support_level

    freq_pairs.df = freq_pairs.df[freq_pairs.df['support'] >= support_level]
    freq_triples.df = freq_triples.df[freq_triples.df['support'] >= support_level]

    pass_3_end_time = time.time()
    print(f"Pass 3 time: {round(pass_3_end_time-pass_2_time_end, 3)} seconds")
    print('Done w/ Apriori')
    print(f"Total Apriori Time: {round(pass_3_end_time-start_time ,3)}")
    return [freq_pairs,freq_triples]

def compute_confidence(item_dict, freq_pairs, freq_triples, support_table):
    print("Inside Compute Confidence...")
    #confidence scores for pairs, every row in the inputted data should be filtered to support level
    #add columns for confidence scores
    freq_pairs.df['has_item_1'] = 0
    freq_pairs.df['has_item_2'] = 0

    freq_pairs.df.apply()

    for i in freq_pairs.df.index:
        #set items as variables, makes it easier to read code
        item_1 = freq_pairs.df['item_id1'][i]
        item_2 = freq_pairs.df['item_id2'][i]

        #WE CAN JUST USE SUPPORT TABLE
        freq_pairs.df.loc[i,'has_item_1'] = support_table.df.query('item_id==@item_1')['support'].values[0]
        freq_pairs.df.loc[i,'has_item_2'] = support_table.df.query('item_id==@item_2')['support'].values[0]
    #calc the scores
    freq_pairs.df['given_item_1_has_item_2'] = freq_pairs.df['support'] / freq_pairs.df['has_item_1']
    freq_pairs.df['given_item_2_has_item_1'] = freq_pairs.df['support'] / freq_pairs.df['has_item_2']
    #do confidence scores for trips

    freq_triples.df['has_1_2'] = 0
    freq_triples.df['has_1_3'] = 0
    freq_triples.df['has_2_3'] = 0

    for i in freq_triples.df.index:
        # set items as variables, makes it easier to read code
        item_1 = freq_triples.df['item_id1'][i]
        item_2 = freq_triples.df['item_id2'][i]
        item_3 = freq_triples.df['item_id3'][i]

        #cant Use support table, but can use pair count, because we know that the subset of a frequent itemset is also frequent
        #items ids should be sorted small to big left to right
        freq_triples.df.loc[i, 'has_1_2'] = freq_pairs.df.query('item_id1==@item_1 and item_id2==@item_2')['support'].values[0]
        freq_triples.df.loc[i, 'has_1_3'] = freq_pairs.df.query('item_id1==@item_1 and item_id2==@item_3')['support'].values[0]
        freq_triples.df.loc[i, 'has_2_3'] = freq_pairs.df.query('item_id1==@item_2 and item_id2==@item_3')['support'].values[0]



    # calc the scores
    freq_triples.df['has_1_given_2_3'] = freq_triples.df['support'] / freq_triples.df['has_2_3']
    freq_triples.df['has_2_given_1_3'] = freq_triples.df['support'] / freq_triples.df['has_1_3']
    freq_triples.df['has_3_given_1_2'] = freq_triples.df['support'] / freq_triples.df['has_1_2']


    #need to find top 5 scores for pairs
    #convert to numeric
    freq_pairs.df['given_item_1_has_item_2']  = pd.to_numeric(freq_pairs.df['given_item_1_has_item_2'])
    freq_pairs.df['given_item_2_has_item_1']  = pd.to_numeric(freq_pairs.df['given_item_2_has_item_1'])

    p1_top_5_pairs = freq_pairs.df.nlargest(5, 'given_item_1_has_item_2', keep="all")
    p2_top_5_pairs = freq_pairs.df.nlargest(5, 'given_item_2_has_item_1', keep="all")
    p1_top_5_pairs = p1_top_5_pairs.drop(['has_item_2','given_item_2_has_item_1','has_item_1'], 1)
    p2_top_5_pairs = p2_top_5_pairs.drop(['has_item_1','given_item_1_has_item_2','has_item_2'], 1)
    #rename column
    p1_top_5_pairs.rename(columns={"item_id1":"given_item","item_id2":"has_item","given_item_1_has_item_2":"confidence"}, inplace=True)
    p2_top_5_pairs.rename(columns={"item_id1":"has_item","item_id2":"given_item","given_item_2_has_item_1":"confidence"}, inplace=True)
    #combine into 1 df
    top_5_pairs = pd.concat([p1_top_5_pairs, p2_top_5_pairs])
    del p1_top_5_pairs
    del p2_top_5_pairs

    #grab 5 largest
    top_5_pairs = top_5_pairs.nlargest(5, 'confidence', keep = "all")
    top_5_pairs.reset_index(drop=True,inplace=True)
    #now, make new df with the actual string names
    top_5_pairs_names = DataFrame(columns=['given_item','has_item','confidence'])
    for i in top_5_pairs.index:
        #get item id
        item_1 = top_5_pairs['given_item'][i]
        item_2 = top_5_pairs['has_item'][i]
        #get item name
        item1_name = list(item_dict.keys())[list(item_dict.values()).index(item_1)]
        item2_name = list(item_dict.keys())[list(item_dict.values()).index(item_2)]
        #add to new df
        top_5_pairs_names = top_5_pairs_names.append(DataFrame({'given_item': [item1_name], 'has_item': [item2_name], 'confidence': [top_5_pairs['confidence'][i]]}),ignore_index=True)

    #top 5 scores for triples
    #convert to numeric
    freq_triples.df['has_1_given_2_3'] = pd.to_numeric(freq_triples.df['has_1_given_2_3'])
    freq_triples.df['has_2_given_1_3'] = pd.to_numeric(freq_triples.df['has_2_given_1_3'])
    freq_triples.df['has_3_given_1_2'] = pd.to_numeric(freq_triples.df['has_3_given_1_2'])

    t1 = freq_triples.df.nlargest(5, 'has_1_given_2_3', keep="all")
    t2 = freq_triples.df.nlargest(5, 'has_2_given_1_3', keep="all")
    t3 = freq_triples.df.nlargest(5, 'has_3_given_1_2', keep="all")
    t1 = t1.drop(columns=['has_2_3','has_2_given_1_3','has_1_3','has_3_given_1_2','has_1_2'])
    t2 = t2.drop(columns=['has_1_2','has_1_given_2_3','has_2_3','has_3_given_1_2','has_1_3'])
    t3 = t3.drop(columns=['has_1_2','has_1_given_2_3','has_1_3','has_2_given_1_3','has_2_3'])
    #rename columns
    t1.rename(columns={'item_id1':'has_item','item_id2':'given_1','item_id3':'given_2','has_1_given_2_3':'confidence'}, inplace=True)
    t2.rename(columns={'item_id1':'given_1','item_id2':'has_item','item_id3':'given_2','has_2_given_1_3':'confidence'}, inplace=True)
    t3.rename(columns={'item_id1':'given_1','item_id2':'given_2','item_id3':'has_item','has_3_given_1_2':'confidence'}, inplace=True)
    # combine into 1 df
    top_5_trips = pd.concat([t1,t2,t3])

    del t1
    del t2
    del t3
    #grab 5 largest
    top_5_trips = top_5_trips.nlargest(5,'confidence', keep='all')
    # now, make new df with the actual string names
    top_5_trips_names = DataFrame(columns=['given_item1', 'given_item2', 'has_item', 'confidence'])
    top_5_trips.reset_index(drop=True, inplace= True)
    for i in top_5_trips.index:
        # get item id
        item_1 = top_5_trips['given_1'][i]
        item_2 = top_5_trips['given_2'][i]
        item_3 = top_5_trips['has_item'][i]

      #  item_1 = item_1.values[0]
      #  item_2 = item_2.values[0]
      #  item_3 = item_3.values[0]
        # get item name
        item1_name = list(item_dict.keys())[list(item_dict.values()).index(item_1)]
        item2_name = list(item_dict.keys())[list(item_dict.values()).index(item_2)]
        item3_name = list(item_dict.keys())[list(item_dict.values()).index(item_3)]
        #sort items
        if item1_name > item2_name:
            #swap
            temp = item2_name
            item2_name = item1_name
            item1_name = temp
        # add to new df
        top_5_trips_names =  top_5_trips_names.append(DataFrame(
            {'given_item1': [item1_name], 'given_item2':[item2_name], 'has_item': [item3_name], 'confidence': [top_5_trips['confidence'][i]]}),ignore_index=True)

    del top_5_pairs
    del top_5_trips
    del item_1
    del item_2
    del item_3
    # deal with ties for pairs
    top_5_pairs_names['confidence'] = pd.to_numeric(top_5_pairs_names['confidence'])
    top_5_pairs_names.sort_values(by=['confidence', 'given_item', 'has_item'], ascending=[False, True, True], inplace=True)
    top_5_pairs_names.reset_index(drop=True,inplace=True)
   # top_5_pairs_names = top_5_pairs_names.nlargest(5,columns=['confidence','given_item'], keep="all")


    # deal with ties for trips
    top_5_trips_names['confidence'] = pd.to_numeric(top_5_trips_names['confidence'])
    top_5_trips_names.sort_values(by=['confidence', 'given_item1','given_item2', 'has_item'],ascending= [False, True, True, True], inplace= True)
  #  top_5_trips_names = top_5_trips_names.nlargest(5,columns=['confidence','given_item1','given_item2'], keep='all')

    yo = 0
    print("Done with computing Confidence")
    #now i have both tables, not necessarily 5 entries, but sorted so the first 5 i grab are the ones i want
    return [top_5_pairs_names, top_5_trips_names]

def write_file(outfile, pairs, trips):
    print("writing output file")
    try:
        out = open(outfile, mode= 'w')
    except:
        OSError("Error opening output file")
        return
    #output a
    out.write("OUTPUT A\n")
    for i in range(0,5):
        #write line data frame
        item1 = pairs['given_item'][i]
        item2 = pairs['has_item'][i]
        conf = pairs['confidence'][i]
        out.write(f"{item1} {item2} {conf}\n")
    out.write("OUTPUT B\n")
    for i in range(0,5):
        item1 = trips['given_item1'][i]
        item2 = trips['given_item2'][i]
        item3 = trips['has_item'][i]
        conf = trips['confidence'][i]
        out.write(f"{item1} {item2} {item3} {conf}\n")
    out.close()
    print("Done writing output file")

def test_apriori():
    item_dict = dict()
    support_table = bk.support_table()
    infile = 'test_data/biggersample.txt'
 #   infile = 'test_data/biggersample.txt'

    outfile = 'output.txt'
    baskets = read_file(infile, item_dict, support_table)
    results = apriori(baskets=baskets,support_table= support_table, support_level=8)
    #done with baskets.. delete
    del baskets
    results = compute_confidence(item_dict,results[0],results[1], support_table=support_table)
    write_file(outfile,results[0], results[1])
    time.sleep(10)

if __name__ == "__main__":
    test_apriori()
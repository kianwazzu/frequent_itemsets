#KIAN ANKERSON
#read file function for hw 2 assignment, does updates support table, puts items in basket objects


from basket import basket
import basket as bk
import time

#return list of baskets
def read_file(infile, item_dict, support_table):
    print("Reading Files...")
    start_time = time.time()
    distinct_item_count = 0
    try:
        infile = open(infile, mode='r')
    except OSError:
        print(f"Error opening file: {infile}")
    if infile.readable():
        lines = infile.readlines()
        num_baskets_to_allocate = len(lines)
        baskets = []
        infile.close()

        for line in lines:
            temp_basket = basket()
            items = line.split()
            #give items a unique id if not already in dict()
            for item in items:
                if item not in item_dict:
                    #add item
                    distinct_item_count +=1
                    item_dict[item] = distinct_item_count

                #add it to basket
                temp_basket.add_item(item_dict.get(item))
                #add to support table
                support_table.add_or_update(item_dict.get(item))
            baskets.append(temp_basket)


    else:
        print("Error. File could not be read.")
        raise OSError

    end_time = time.time()
    print(f"Done Reading Files.\nBaskets: {len(baskets)}. Time: {round(end_time-start_time, 3)} seconds")
    return baskets

def test_read_file():
    item_dict = dict()
    infile = 'test_data/browsingdata_50baskets.txt'
    support_table = bk.support_table()
    baskets = read_file(infile,item_dict, support_table)
    print('yo')

if __name__ == '__main__':
    test_read_file()
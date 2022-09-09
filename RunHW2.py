#RUN the apriori and generate output file

import basket as bk
from file_read import read_file
from Apriori import apriori, compute_confidence, write_file

def main():
    item_dict = dict()
    support_table = bk.support_table()
    infile = 'browsing-data.txt'
    outfile = 'output.txt'
    baskets = read_file(infile, item_dict, support_table)
    results = apriori(baskets=baskets, support_table=support_table, support_level=8)
    # done with baskets.. delete
    del baskets
    results = compute_confidence(item_dict, results[0], results[1], support_table=support_table)
    write_file(outfile, results[0], results[1])


if __name__ ==  "__main__":
    main()
filenames = ['./data/berlin_stockholm_london.csv', './data/keiv_lviv_toronto.csv', './data/ny_seattle.csv']
i = 0
with open('./data/dataset.csv', 'w+') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
                i += 1
                print("{} lines written".format(i))
print('Finished')

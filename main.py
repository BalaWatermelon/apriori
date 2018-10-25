# ID: cl656
# Section & Course: apriori, cs634
# File name: cs634_CheYuLin_apriori.py
# Due date: 11:59pm on Monday Oct. 29
# This program is use to find frequent item set using apriori with a specific minimum support.
# It takes three parameter for clean data
#
#  python3 main.py clean.txt support output.txt
#
# and four for unclean data, which adds a mapping file [map.txt]
#
#  python3 main.py dirty.txt map.txt support output.txt
#
#
import sys
import logging

# Basic logging setup
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


def clean(inputFile, mappingFile):
    '''
    Clean up inputFile with mappingFile
    '''
    logger.info('Cleaning file {} with mapping data {}...'.format(
        inputFile, mappingFile))

    # Generate mapping and reversMapping dictionary
    logger.debug('Generating mapping dictionary')
    mapping = {}
    reversMapping = {}
    with open(mappingFile, 'r') as inputF:
        # Loop through lines and store index:name & name:index mapping
        for line in inputF:
            index, name = line.split()
            mapping[index] = name
            reversMapping[name] = index
    logger.debug('mapping: {}'.format(mapping))
    logger.debug('reversMapping: {}'.format(reversMapping))
    logger.debug('Mapping created')

    # Start to clean up transaction with mapping & reverseMapping dict.
    logger.debug('Start to clean file')
    # Store the temprary cleaned file in 'tempCleaned.txt'
    cleanedFile = 'tempCleaned.txt'
    with open(cleanedFile, 'w+') as output:  # Open temporary cleaned file
        with open(inputFile, 'r') as inputF:
            # Loop through lines in input file.
            for line in inputF:
                keep = []   # Used to store valid items in transaction
                line = line.replace(';', ' ')
                elements = line.split()  # Seperate element with space
                logger.debug('Original elements: len({}) data:{}'.format(
                    len(elements), elements))
                # Loop through ever element in one line(one transaction)
                for element in elements:
                    # Store element if it's in valid PXX format inside mappingFile given
                    if element in mapping:
                        keep.append(element)
                    # Store element if it's listed as String in mappingFile then reverse it to PXX format
                    elif element in reversMapping:
                        keep.append(reversMapping[element])

                logger.debug(
                    'Cleaned elements: len({}) data:{}'.format(len(keep), keep))
                # Save cleaned transaction in to cleanedfile
                output.write(' '.join(keep)+'\n')
    # File cleaned
    logger.info('File cleaned, storing cleaned file at {}.'.format(cleanedFile))
    return cleanedFile


class candidate:
    def __init__(self, value, count=0):
        self.value = value
        self.count = 0

    def __str__(self):
        return 'candidate<{}, count:{}>'.format(self.value, self.count)

    def __repr__(self):
        return 'candidate<{}, count:{}>'.format(self.value, self.count)


def apriori(inputFile, outputFile, minimumSupport=3):
    '''
    Find out frequent item set with apriori,
    default minimumSupport set to 3
    '''
    logger.info('Applying apriori with minimum support {} on {}'.format(
        minimumSupport, inputFile))
    l = []
    candidates = []
    l.append(find_frequent_1_itemsets(inputFile, minimumSupport))
    logger.debug('First generation {}'.format(l[0]))
    k = 1
    while len(l[k-1]) > 0:
        logger.debug('Running iteration {}'.format(k))
        candidates = apriori_gen(l[k-1])
        logger.debug('Current candidates {}'.format(candidates))
        with open(inputFile, 'r') as f:
            for line in f:
                transaction = line.strip().split()
                # Skip transaction that has less item than candidate, speeds up program
                if not len(transaction) < k+1:
                    transaction = set(transaction)
                    for c in candidates:
                        if set(c.value) < transaction:  # if candidate is a subset of t
                            c.count += 1
        temp = [c.value for c in candidates if c.count >= minimumSupport]
        l.append(temp)
        k += 1
    logger.debug('Result: {}'.format(l))
    with open(outputFile, 'w+') as f:
        for iteration in l:
            for element in iteration:
                f.write('[{}], '.format(' '.join(element)))
            f.write('\n')
    logger.info('Saving result to {}'.format(outputFile))
    pass


def apriori_gen(itemSets):
    r = []
    for itemSetA in itemSets:
        for itemSetB in itemSets:
            if itemSetA != itemSetB:
                c = list(set(itemSetA) | set(itemSetB))  # Join setA setB
                if not has_infrequent_subset(c, itemSets):
                    if c not in r:
                        r.append(c)
    r = [candidate(c) for c in r]
    return r


def has_infrequent_subset(candidate, itemSets):
    '''
    Find if candidate contains infrequent subset from itemSet it gen from
    '''
    for s in subset(candidate):
        if s not in itemSets:
            return True
    return False


def subset(itemSet):
    '''
    Return subsetOfLength(length of item in itemSet - 1) of itemSet
    '''
    r = []
    for i in itemSet:
        q = list(itemSet)
        q.remove(i)
        r.append(q)
    return r


def find_frequent_1_itemsets(inputFile, minimumSupport):
    l = dict()  # Store each item appearence
    with open(inputFile, 'r') as f:
        for line in f:
            line = list(set(line.split()))
            for element in line:
                if element in l:
                    l[element] += 1
                else:
                    l[element] = 0
    r = [[key] for key in l if l[key] >= minimumSupport]
    logger.debug('First statistic {}'.format(l))
    return r


if __name__ == '__main__':
    # Clean Data: python3 main.py clean.txt support output.txt
    if len(sys.argv) == 4:
        inputFile = sys.argv[1]
        try:
            minimumSupport = int(sys.argv[2])
        except ValueError:
            logger.warning('Please enter valid minimum support number')
            sys.exit('Program terminated')
        outputFile = sys.argv[3]
        logger.info('Processing with clean file {}'.format(inputFile))
        apriori(inputFile, outputFile, minimumSupport)

    # Dirty Data: python3 main.py dirty.txt map.txt support output.txt
    elif len(sys.argv) == 5:
        dirtyFile = sys.argv[1]
        mappingFile = sys.argv[2]
        try:
            minimumSupport = int(sys.argv[3])
        except ValueError:
            logger.warning("Please enter valid minimum support number")
            sys.exit("Program terminated")
        outpuFile = sys.argv[4]
        logger.info('Processing with dirty file {}'.format(dirtyFile))
        cleanedFile = clean(dirtyFile, mappingFile)
        logger.debug('Using cleaned file {}'.format(cleanedFile))
        apriori(cleanedFile, outpuFile, minimumSupport)

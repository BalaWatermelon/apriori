import sys
import logging

# Basic logging setup
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


def clean(inputFile, mappingFile):
    logger.info('Cleaning file {} with mapping data {}...'.format(
        inputFile, mappingFile))

    # Generate mapping and reversMapping dictionary
    logger.debug('Generating mapping dictionary')
    mapping={}
    reversMapping={}
    with open(mappingFile,'r') as inputF:
        for line in inputF:
            index, name = line.split()
            mapping[index] = name
            reversMapping[name] = index
    logger.debug('mapping: {}'.format(mapping))
    logger.debug('reversMapping: {}'.format(reversMapping))
    logger.debug('Mapping created')

    # Start to clean up transaction with mapping & reverseMapping dict.
    logger.debug('Start to clean file')
    cleanedFile = 'tempCleaned.txt' # Store the temprary cleaned file in 'tempCleaned.txt'
    with open(cleanedFile,'w+') as output:  # Open temporary cleaned file
        line = ''
        with open(inputFile,'r') as inputF: # Open uncleaned input file
            for line in inputF:
                keep = []
                line = line.replace(';',' ')    # Replace every semicolumn with space
                elements = line.split()         # Seperate element with space
                logger.debug('Original elements: len({}) data:{}'.format(len(elements),elements))
                for element in elements:        # Loop through ever element in one line(one transaction)
                    if element in mapping:      # If element is a valid PXX format inside mappingFile given
                        keep.append(element)
                    elif element in reversMapping: # If element is listed as String in mappingFile then reverse it to PXX format
                        keep.append(reversMapping[element])
                logger.debug('Cleaned elements: len({}) data:{}'.format(len(keep),keep))
                output.write(' '.join(keep)+'\n') # Save cleaned transaction in to cleanedfile
    # Filed cleaned
    logger.info('File cleaned, storing cleaned file at {}.'.format(cleanedFile))
    return cleanedFile


def apriori(inputFile, outputFile, minimumSupport):
    logger.info('Applying apriori with minimum support {} on {}'.format(
        minimumSupport, inputFile))
    logger.info('Saving result to {}'.format(outputFile))
    pass


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

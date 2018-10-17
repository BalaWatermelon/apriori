import sys
import logging

# Basic logging setup
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


def clean(inputFile, mappingFile):
    logger.info('Cleaning file {} with mapping data {}...'.format(
        inputFile, mappingFile))
    pass


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
        apriori(cleanedFile, outpuFile, minimumSupport)

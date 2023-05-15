import os
import logging

from better_profanity import profanity
from better_profanity.utils import read_wordlist

logging.basicConfig(level=logging.INFO)
logging.info('Config profanity filter')
profanity.load_censor_words(
    custom_words=read_wordlist(os.path.dirname(os.path.realpath(__file__)) + "/resources/profanity_wordlist.txt"))

profanity_filter = profanity
logging.info('Config profanity filter complete')

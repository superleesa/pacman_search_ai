"""
Logger for single search agent.

Logs timestamps, functions called, state of agent, locayion of agent, path length, expansion, #capsules eaten,
#fruits eaten, #ghosts run into, #wins, #losses, avg. score, scores, win rate

@author: emelypi
@date: 22.07.2023
"""

import logging as log


def search_logger(filename: str = None):

    logger = log.getLogger('root')

    if filename is None:
        logger.disabled = True
        return

    f_handler = log.FileHandler('logs/'+filename+'.log')
    f_handler.setLevel(log.INFO)
    f_format = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    logger.setLevel(log.INFO)




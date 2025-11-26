'''
Module Name: Player.py
Purpose: store and manage player class
Input(s): None
Output(s): None
Author(s):  Jacob Kice
Outside Source(s):  None
Creation Date: 10/22/2025
Updated Date: 10/22/2025
'''

class Player():
    '''
        Args:
            color: string indicating which player the object is for; valid values: 'white', 'black'
        Purpose: 
            serves as a player manager for power chess
            stores pieces list and turn information
    '''
    def __init__(self, color):
        self.color = color
        self.turn = False
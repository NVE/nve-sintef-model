
def get_uketime_tsnitt_map(antall_tsnitt):
    """
    returnerer et dict med uketime -> tsnitt for antall_tsnitt = 1, 5, 28, 56 eller 168

    uketime = 1,2,3,..,168, og representerer hver time i uken (mandag til sondag)

    antall_tsnitt = 1, 28, 56 og 168 forklarer seg selv

    antall_tsnitt = 5 er definert paa folgende maate:

    4,   4,   4,   4,   4,   4,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   3,   3,   3,   3,   3,   3,   4,   4,Mon
    4,   4,   4,   4,   4,   4,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   3,   3,   3,   3,   3,   3,   4,   4,Tue
    4,   4,   4,   4,   4,   4,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   3,   3,   3,   3,   3,   3,   4,   4,Wed
    4,   4,   4,   4,   4,   4,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   3,   3,   3,   3,   3,   3,   4,   4,Thu
    4,   4,   4,   4,   4,   4,   1,   1,   1,   1,   2,   2,   2,   2,   2,   2,   3,   3,   3,   3,   3,   3,   4,   4,Fri
    4,   4,   4,   4,   4,   4,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   4,   4,Sat
    4,   4,   4,   4,   4,   4,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   5,   4,   4,Sun

    """

    assert isinstance(antall_tsnitt, int), "antall_tsnitt maa vaere et heltall"
    assert antall_tsnitt in [1, 5, 28, 56, 168] 
    
    if antall_tsnitt == 1:
        return {i : 1 for i in range(1,169)}
    
    elif antall_tsnitt == 168:
        return {i : i for i in range(1,169)}
        
    elif antall_tsnitt == 56:
        ts = sorted([i for i in range(1,57)]*3)
        return {i : ts[i-1] for i in range(1, 169)}

    elif antall_tsnitt == 28:
        ts = sorted([i for i in range(1,29)]*6)
        return {i : ts[i-1] for i in range(1, 169)}
    
    elif antall_tsnitt == 5:
        return {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 1, 8: 1, 9: 1, 10: 1, 11: 2, 12: 2, 13: 2, 14: 2, 
                15: 2, 16: 2, 17: 3, 18: 3, 19: 3, 20: 3, 21: 3, 22: 3, 23: 4, 24: 4, 25: 4, 26: 4, 27: 4, 
                28: 4, 29: 4, 30: 4, 31: 1, 32: 1, 33: 1, 34: 1, 35: 2, 36: 2, 37: 2, 38: 2, 39: 2, 40: 2, 
                41: 3, 42: 3, 43: 3, 44: 3, 45: 3, 46: 3, 47: 4, 48: 4, 49: 4, 50: 4, 51: 4, 52: 4, 53: 4, 
                54: 4, 55: 1, 56: 1, 57: 1, 58: 1, 59: 2, 60: 2, 61: 2, 62: 2, 63: 2, 64: 2, 65: 3, 66: 3, 
                67: 3, 68: 3, 69: 3, 70: 3, 71: 4, 72: 4, 73: 4, 74: 4, 75: 4, 76: 4, 77: 4, 78: 4, 79: 1, 
                80: 1, 81: 1, 82: 1, 83: 2, 84: 2, 85: 2, 86: 2, 87: 2, 88: 2, 89: 3, 90: 3, 91: 3, 92: 3, 
                93: 3, 94: 3, 95: 4, 96: 4, 97: 4, 98: 4, 99: 4, 100: 4, 101: 4, 102: 4, 103: 1, 104: 1, 
                105: 1, 106: 1, 107: 2, 108: 2, 109: 2, 110: 2, 111: 2, 112: 2, 113: 3, 114: 3, 115: 3, 
                116: 3, 117: 3, 118: 3, 119: 4, 120: 4, 121: 4, 122: 4, 123: 4, 124: 4, 125: 4, 126: 4, 
                127: 5, 128: 5, 129: 5, 130: 5, 131: 5, 132: 5, 133: 5, 134: 5, 135: 5, 136: 5, 137: 5, 
                138: 5, 139: 5, 140: 5, 141: 5, 142: 5, 143: 4, 144: 4, 145: 4, 146: 4, 147: 4, 148: 4, 
                149: 4, 150: 4, 151: 5, 152: 5, 153: 5, 154: 5, 155: 5, 156: 5, 157: 5, 158: 5, 159: 5, 
                160: 5, 161: 5, 162: 5, 163: 5, 164: 5, 165: 5, 166: 5, 167: 4, 168: 4}

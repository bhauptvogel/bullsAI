import numpy as np

def dart_throw_sim(target: np.array, std_dev: float) -> np.array:
    return np.random.normal(target, std_dev, size=2)

def get_points_of_coordinates(dart_coordinates: np.array) -> int:
    distance_to_origin = np.linalg.norm(dart_coordinates)
    if(distance_to_origin < 0.635):
        return 50 # bullseye
    elif(distance_to_origin < 1.6):
        return 25 # single bull
    
    sector_index = int((np.arctan2(dart_coordinates[0], dart_coordinates[1]) / np.pi + 1/20 + 1) * 10) - 1
    index_to_field = [19,7,16,8,11,14,9,12,5,20,1,18,4,13,6,10,15,2,17,3]
    field = index_to_field[sector_index]
    
    if(distance_to_origin < 9.9):
        return field # single
    elif(distance_to_origin < 10.7):
        return field * 3 # triple
    elif(distance_to_origin < 16.2):
        return field # single
    elif(distance_to_origin < 17.0):
        return field * 2 # double
    else:
        return 0
    
def get_field_of_coordinates(dart_coordinates: np.array) -> str:
    distance_to_origin = np.linalg.norm(dart_coordinates)
    if(distance_to_origin < 0.635):
        return 'D25' # bullseye
    elif(distance_to_origin < 1.6):
        return '25' # single bull
    
    sector_index = int((np.arctan2(dart_coordinates[0], dart_coordinates[1]) / np.pi + 1/20 + 1) * 10) - 1
    index_to_field = [19,7,16,8,11,14,9,12,5,20,1,18,4,13,6,10,15,2,17,3]
    field = index_to_field[sector_index]
    
    if(distance_to_origin < 9.9):
        return str(field) # single
    elif(distance_to_origin < 10.7):
        return 'T' + str(field) # triple
    elif(distance_to_origin < 16.2):
        return str(field) # single
    elif(distance_to_origin < 17.0):
        return 'D' + str(field) # double
    else:
        return str(0)
    
def was_double_hit(dart_coordinates: np.array) -> bool:
    distance_to_origin = np.linalg.norm(dart_coordinates)
    return (distance_to_origin < 0.635) or (distance_to_origin > 16.2 and distance_to_origin < 17.0)


def get_target_coordinates(field: str) -> np.array:
    # TODO: Maybe do a different goal for the 25
    if field == 'B' or field == '50' or field == 'D25' or field == 'S25' or field == '25' or field == 'SB':
        return [0,0] # double or single bull

    target_distance_to_origin = 13.45

    if field.startswith('T'):
        target_distance_to_origin = 10.3
    elif field.startswith('D'):
        target_distance_to_origin = 16.6

    field = int("".join([ele for ele in field if ele.isdigit()]))
    field_to_index = [20,1,18,4,13,6,10,15,2,17,3,19,7,16,8,11,14,9,12,5]
    angle = field_to_index.index(field)/20 * 2 * np.pi

    return np.array([target_distance_to_origin * np.sin(angle), target_distance_to_origin * np.cos(angle)])


def get_next_target_field(remaining_points: int, remaining_darts: int):
    # TODO: Do the occasional T19 (only if average under 120)
    if remaining_points >= 136:
        return 'T20'
    
    # special case if only 2 darts left: if the first does not hit, player can still target D25
    if remaining_darts == 2 and remaining_points >= 62 and remaining_points <= 70:
        checkout_table_2_darts = {
            61: 'T11',
            62: 'T12',
            63: 'T13',
            64: 'T14',
            65: 'T15',
            66: 'T16',
            67: 'T17',
            68: 'T18',
            69: 'T19',
            70: 'T20',
        }
        return checkout_table_2_darts[remaining_points]
    
    checkout_table = {
        135: 'S25',
        134: 'T20',
        133: 'T20',
        132: 'T20',
        131: 'T20',
        130: 'T20',
        129: 'T19',
        128: 'T18',
        127: 'T20',
        126: 'T19',
        125: 'T20',
        124: 'T20',
        123: 'T19',
        122: 'T18',
        121: 'T20',
        120: 'T20',
        119: 'T19',
        118: 'T20',
        117: 'T20',
        116: 'T20',
        115: 'T20',
        114: 'T20',
        113: 'T19',
        112: 'T20',
        111: 'T20',
        110: 'T20',
        109: 'T20',
        108: 'T20',
        107: 'T19',
        106: 'T20',
        105: 'T20',
        104: 'T18',
        103: 'T19',
        102: 'T20',
        101: 'T20',
        100: 'T20',
        99: 'T19',
        98: 'T20',
        97: 'T19',
        96: 'T20',
        95: 'T19',
        94: 'T18',
        93: 'T19',
        92: 'T20',
        91: 'T17',
        90: 'T20',
        89: 'T19',
        88: 'T20',
        87: 'T17',
        86: 'T18',
        85: 'T15',
        84: 'T20',
        83: 'T17',
        82: 'D25',
        81: 'T19',
        80: 'T20',
        79: 'T19',
        78: 'T18',
        77: 'T19',
        76: 'T20',
        75: 'T17',
        74: 'T14',
        73: 'T19',
        72: 'T16',
        71: 'T13',
        70: 'T18',
        69: 'T15',
        68: 'T20',
        67: 'T17',
        66: 'T10',
        65: 'T11',
        64: 'T16',
        63: 'T13',
        62: 'T10',
        61: 'T15',
        60: 'S20',
        59: 'S19',
        58: 'S18',
        57: 'S17',
        56: 'S16',
        55: 'S15',
        54: 'S14',
        53: 'S13',
        52: 'S12',
        51: 'S19',
        50: 'S18',
        49: 'S9',
        48: 'S16',
        47: 'S15',
        46: 'S14',
        45: 'S13',
        44: 'S12',
        43: 'S11',
        42: 'S10',
        41: 'S9',
        40: 'D20',
        39: 'S7', 
        38: 'D19', 
        37: 'S5',
        36: 'D18',
        35: 'S3',
        34: 'D17',
        33: 'S1', # ! für sehr schlechte Spieler S17 (bei S3 auch Finish)
        32: 'D16',
        31: 'S15', # ! für sehr schlechte Spieler S19 (bei S3/S7 auch Finish)
        30: 'D15',
        29: 'S13',
        28: 'D14',
        27: 'S11', # ! für schlechte Spieler S19
        26: 'D13',
        25: 'S9',
        24: 'D12',
        23: 'S7',
        22: 'D11',
        21: 'S5', # ! für sehr schlechte Spieler S13
        20: 'D10',
        19: 'S3', # ! für sehr schlechte Spieler S11
        18: 'D9',
        17: 'S1', # ! für sehr schlechte Spieler S9
        16: 'D8', 
        15: 'S7',
        14: 'D7',
        13: 'S5',
        12: 'D6',
        11: 'S3',
        10: 'D5',
        9: 'S1',
        8: 'D4',
        7: 'S3',
        6: 'D3',
        5: 'S1',
        4: 'D2',
        3: 'S1',
        2: 'D1'
    }

    return checkout_table[remaining_points]

# hit = dart_throw(get_target('T19'), 3)
# print(get_points(hit))

# print(get_next_target(65, 2))
import numpy as np
import checkouts

def dart_throw_sim(target: np.array, std_dev: float) -> np.array:
    return np.random.normal(target, std_dev, size=2)
    
def get_field_of_coordinates(dart_coordinates: np.array) -> str:
    distance_to_origin = np.linalg.norm(dart_coordinates)
    if(distance_to_origin < 0.635):
        return 'D25' # bullseye
    elif(distance_to_origin < 1.6):
        return '25' # single bull
    
    # TODO: refactor this math - make it more clear and match with reverse (get_target_coordinates)
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
    
def get_points_of_coordinates(dart_coordinates: np.array) -> int:
    field = get_field_of_coordinates(dart_coordinates)
    if field.startswith('T'):
        return int(field[1:]) * 3
    elif field.startswith('D'):
        return int(field[1:]) * 2
    elif field.startswith('S') or field.isdigit():
        return int(field.replace('S', ''))
    else:
        raise ValueError(f'Invalid field: {field}')
    
def was_double_hit(dart_coordinates: np.array) -> bool:
    distance_to_origin = np.linalg.norm(dart_coordinates)
    return (distance_to_origin < 0.635) or (distance_to_origin > 16.2 and distance_to_origin < 17.0)


def get_target_coordinates(field: str) -> np.array:
    # TODO: Maybe do a different goal for the 25, especially if player has strong std (TESTING)
    if field in ['B', 'Bull', 'D25', 'S25', '25', 'SB']:
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
    # TODO: Test if this really gives an advantage (at different stds)
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

    return checkouts.checkouts[str(remaining_points)][0]

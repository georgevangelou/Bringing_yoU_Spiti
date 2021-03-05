############################  USED LIBRARIES  ############################

from constants import MAP_STATUS_TO_DISCOUNT, NORMAL_MONTHLY_VALUE, PERSON_STATIC_COORDINATES



############################  FUNCTIONS  ############################

def get_Card_Value(cardholder_type, monthly_duration):
    '''
    discount, card_value = f{cardholder_type, monthly_duration}\n
    Calculates the discount and final value of card given
    '''

    discount = 0
    try:
        discount = MAP_STATUS_TO_DISCOUNT[cardholder_type]
    except Exception as e:
        print(e)
        print("Discount type set to 0")
    return discount, int(NORMAL_MONTHLY_VALUE * monthly_duration * (100-discount)/100.0) 


def get_My_Coordinates():
    '''
    person_coordinates = PERSON_STATIC_COORDINATES\n
    Returns the current position of the person using this app
    '''


    return PERSON_STATIC_COORDINATES
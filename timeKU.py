from datetime import datetime, time

# from time import sleep

def adjust_temp(_up_votes,_down_votes):
    _up_votes = int(_up_votes)
    _down_votes = int(_down_votes)
    if _up_votes > _down_votes:
        print('send up')
    else:
        print('send down')

def set_off(_time_end):
    # Split the input string and convert to integers
    hours, minutes = map(int, _time_end.split(':'))
    # Create a time object with the given hours and minutes
    target_time = time(hours, minutes)
    current_time = datetime.now().time()
    
    while current_time < target_time:
        current_time = datetime.now().time()
    
    # Execute the desired function here
    print('stopnow')
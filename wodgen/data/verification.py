from type import WorkoutType

def verify_workout_type(input_string):
    input_string = input_string.upper()
    print(input_string)
    for workout_type in WorkoutType:
        if workout_type.value in input_string:
            return workout_type
    return WorkoutType.FT

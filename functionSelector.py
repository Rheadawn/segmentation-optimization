from execute_stars import by_length, static_segment_length_ticks, static_segment_length_meters, dynamic_segment_length_meters_speed, dynamic_segment_length_meters_speed_acceleration_1

def getBounds(segmentationType):
    match segmentationType:
        case "BY_LENGTH":
            return {'x': (100, 200)}
        case "STATIC_SEGMENT_LENGTH_TICKS":
            return {'windowSize': (50, 200), 'stepSize': (0.1, 0.75)}
        case "STATIC_SEGMENT_LENGTH_METERS":
            return {'windowSize': (30, 150), 'stepSize': (0.1, 0.75)}
        case "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED":
            return {'lookAhead': (10, 100), 'scalar': (200, 400), 'stepSize': (1, 50)}
        case "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1":
            return {'lookAhead': (10, 100), 'stepSize': (1, 50)}
        
def getMethod(segmentationType):
    match segmentationType:
        case "BY_LENGTH":
            return by_length
        case "STATIC_SEGMENT_LENGTH_TICKS":
            return static_segment_length_ticks
        case "STATIC_SEGMENT_LENGTH_METERS":
            return static_segment_length_meters
        case "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED":
            return dynamic_segment_length_meters_speed
        case "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1":
            return dynamic_segment_length_meters_speed_acceleration_1
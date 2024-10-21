from execute_stars import by_length, static_segment_length_seconds, static_segment_length_meters, dynamic_segment_length_meters_speed, dynamic_segment_length_meters_speed_acceleration_1, sliding_window_multistart_meters, sliding_window_multistart_seconds

def getBounds(segmentationType):
    match segmentationType:
        case "BY_LENGTH":
            return {'x': (100, 200)} #segmentSize
        case "STATIC_SEGMENT_LENGTH_SECONDS":
            return {'x': (25, 100), 'y': (0.1, 0.75)} #windowSize, overlapPercentage
        case "STATIC_SEGMENT_LENGTH_METERS":
            return {'x': (30, 150), 'y': (0.1, 0.75)} #windowSize, overlapPercentage
        case "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1":
            return {'x': (10, 100), 'y': (1, 50)} #lookAhead, stepSize
        case "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED":
            return {'x': (10, 100), 'y': (200, 400), 'z': (1, 50)} #lookAhead, scalar, stepSize
        case "SLIDING_WINDOW_MULTISTART_METERS":
            return {'x': (30, 150), 'y': (30, 150), 'z': (30, 150)} #windowSize1, windowSize2, windowSize3
        case "SLIDING_WINDOW_MULTISTART_SECONDS":
            return {'x': (25, 100), 'y': (25, 100), 'z': (25, 100)} #windowSize1, windowSize2, windowSize3
        
        
def getMethod(segmentationType):
    match segmentationType:
        case "BY_LENGTH":
            return by_length
        case "STATIC_SEGMENT_LENGTH_SECONDS":
            return static_segment_length_seconds
        case "STATIC_SEGMENT_LENGTH_METERS":
            return static_segment_length_meters
        case "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED":
            return dynamic_segment_length_meters_speed
        case "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1":
            return dynamic_segment_length_meters_speed_acceleration_1
        case "SLIDING_WINDOW_MULTISTART_METERS":
            return sliding_window_multistart_meters
        case "SLIDING_WINDOW_MULTISTART_SECONDS":
            return sliding_window_multistart_seconds
        

def getNumberOfDimensions(segmentationType):
    match segmentationType:
        case "BY_LENGTH":
            return 1
        case "STATIC_SEGMENT_LENGTH_SECONDS":
            return 2
        case "STATIC_SEGMENT_LENGTH_METERS":
            return 2
        case "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED":
            return 3
        case "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1":
            return 2
        case "SLIDING_WINDOW_MULTISTART_METERS":
            return 3
        case "SLIDING_WINDOW_MULTISTART_SECONDS":
            return 3
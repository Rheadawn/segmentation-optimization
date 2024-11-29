from execute_stars import by_length, static_segment_length_seconds, static_segment_length_meters, dynamic_segment_length_meters_speed, dynamic_segment_length_meters_speed_acceleration_1, sliding_window_multistart_meters, sliding_window_multistart_seconds

def getBounds(segmentationType):
    if segmentationType == "BY_LENGTH":
        return [(100, 200)]  # segmentSize
    elif segmentationType == "STATIC_SEGMENT_LENGTH_SECONDS":
        return [(5, 150), (10.0, 10.0)]  # windowSize, stepSize
    elif segmentationType == "STATIC_SEGMENT_LENGTH_METERS":
        return [(5, 300), (20.0, 20.0)]  # windowSize, stepSize
    elif segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1":
        return [(5, 100), (5, 5)]  # lookAhead, stepSize
    elif segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED":
        return [(2, 40), (0.2, 4.0), (5, 5)]  # lookAhead, scalar, stepSize
    elif segmentationType == "SLIDING_WINDOW_MULTISTART_METERS":
        return [(30, 150), (30, 150), (30, 150)]  # windowSize1, windowSize2, windowSize3
    elif segmentationType == "SLIDING_WINDOW_MULTISTART_SECONDS":
        return [(25, 100), (25, 100), (25, 100)]  # windowSize1, windowSize2, windowSize3

def getMethod(segmentationType):
    if segmentationType == "BY_LENGTH":
        return by_length
    elif segmentationType == "STATIC_SEGMENT_LENGTH_SECONDS":
        return static_segment_length_seconds
    elif segmentationType == "STATIC_SEGMENT_LENGTH_METERS":
        return static_segment_length_meters
    elif segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED":
        return dynamic_segment_length_meters_speed
    elif segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1":
        return dynamic_segment_length_meters_speed_acceleration_1
    elif segmentationType == "SLIDING_WINDOW_MULTISTART_METERS":
        return sliding_window_multistart_meters
    elif segmentationType == "SLIDING_WINDOW_MULTISTART_SECONDS":
        return sliding_window_multistart_seconds

def getNumberOfDimensions(segmentationType):
    if segmentationType == "BY_LENGTH":
        return 1
    elif segmentationType == "STATIC_SEGMENT_LENGTH_SECONDS":
        return 2
    elif segmentationType == "STATIC_SEGMENT_LENGTH_METERS":
        return 2
    elif segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED":
        return 3
    elif segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1":
        return 2
    elif segmentationType == "SLIDING_WINDOW_MULTISTART_METERS":
        return 3
    elif segmentationType == "SLIDING_WINDOW_MULTISTART_SECONDS":
        return 3
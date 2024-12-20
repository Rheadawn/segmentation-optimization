from execute_stars import by_length, static_segment_length_seconds, static_segment_length_meters, dynamic_segment_length_meters_speed, dynamic_segment_length_meters_speed_acceleration_1, sliding_window_multistart_meters, sliding_window_multistart_seconds

def getBounds(segmentationType):
    if segmentationType == "BY_LENGTH":
        return [(100.0, 200.0)]  # segmentSize
    elif segmentationType == "STATIC_SEGMENT_LENGTH_SECONDS":
        return [(0.5, 120.0)]  # windowSize
    elif segmentationType == "STATIC_SEGMENT_LENGTH_METERS":
        return [(0.5, 300.0)]  # windowSize
    elif segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1":
        return [(0.5, 150.0)]  # lookAhead
    elif segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED":
        return [(2.0, 40.0), (0.2, 4.0), (5.0, 5.0)]  # lookAhead, scalar, stepSize
    elif segmentationType == "SLIDING_WINDOW_MULTISTART_METERS":
        return [(30.0, 150.0), (30.0, 150.0), (30.0, 150.0)]  # windowSize1, windowSize2, windowSize3
    elif segmentationType == "SLIDING_WINDOW_MULTISTART_SECONDS":
        return [(25.0, 100.0), (25.0, 100.0), (25.0, 100.0)]  # windowSize1, windowSize2, windowSize3

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
        return 1
    elif segmentationType == "STATIC_SEGMENT_LENGTH_METERS":
        return 1
    elif segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED":
        return 3
    elif segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1":
        return 1
    elif segmentationType == "SLIDING_WINDOW_MULTISTART_METERS":
        return 3
    elif segmentationType == "SLIDING_WINDOW_MULTISTART_SECONDS":
        return 3
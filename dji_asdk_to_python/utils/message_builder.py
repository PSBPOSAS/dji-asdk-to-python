class MessageBuilder:
    # DJI Methods names
    START_TAKEOFF = "startTakeoff"
    START_LANDING = "startLanding"
    CONFIRM_LANDING = "confirmLanding"
    GET_VIRTUAL_STICK_MODE_ENABLED = "getVirtualStickModeEnabled"
    IS_CONNECTED = "isConnected"
    GET_STATE = "getState"
    GET_BATTERY_STATE = "getBatteryState"
    SEND_VIRTUAL_STICK_FLIGHT_CONTROL_DATA = (
        "sendVirtualStickFlightControlData"
    )
    SET_VIRTUAL_STICK_CONTROL_MODE_ENABLED = "setVirtualStickModeEnabled"
    GET_VERTICAL_CONTROL_MODE = "getVerticalControlMode"
    SET_VERTICAL_CONTROL_MODE = "setVerticalControlMode"
    LOAD_MISSION = "loadMission"
    GET_LOADED_MISSION = "getLoadedMission"
    UPLOAD_MISSION = "uploadMission"
    RETRY_UPLOAD_MISSION = "retryUploadMission"
    GET_WAYPOINT_MISSION_OPERATOR = "getWaypointMissionOperator"
    GET_CURRENT_STATE = "getCurrentState"
    START_MISSION = "startMission"
    SET_AUTO_FLIGHT_SPEED = "setAutoFlightSpeed"
    WAYPOINT_COUNT = "waypointCount"
    MAX_FLIGHT_SPEED = "maxFlightSpeed"
    AUTO_FLIGHT_SPEED = "autoFlightSpeed"
    WAYPOINT_LIST = "waypointList"
    SET_MISSION_ID = "setMissionID"
    REPEAT_TIMES = "repeatTimes"
    SET_GIMBAL_PITCH_ROTATION_ENABLED = "setGimbalPitchRotationEnabled"
    SET_EXIT_MISSION_ON_RC_SIGNAL_LOST_ENABLED = (
        "setExitMissionOnRCSignalLostEnabled"
    )
    GO_TO_FIRST_WAYPOINT_MODE = "gotoFirstWaypointMode"
    FLIGHT_PATH_MODE = "flightPathMode"
    HEADING_MODE = "headingMode"
    START_GO_HOME = "startGoHome"
    CANCEL_GO_HOME = "cancelGoHome"
    GET_HOME_LOCATION = "getHomeLocation"
    SET_HOME_LOCATION = "setHomeLocation"
    ADD_LISTENER = "addListener"
    REMOVE_LISTENER = "removeListener"
    ADD_STATE_CALLBACK = (
        "setStateCallback"  # TODO change name in app to addStateCallback
    )
    REMOVE_STATE_CALLBACK = "removeStateCallback"
    IS_STREAMING = "isStreaming"
    SET_LIVE_URL = "setLiveUrl"
    START_STREAM = "startStream"
    STOP_STREAM = "stopStream"
    ROTATE = "rotate"
    GET_CHARGE_REMAINING_IN_PERCENT = "getChargeRemainingInPercent"

    # CAMERA
    GET_EXPOSURE_MODE = "getExposureMode"
    SET_EXPOSURE_MODE = "setExposureMode"
    GET_ISO = "getISO"
    SET_ISO = "setISO"
    GET_SHUTTER_SPEED = "getShutterSpeed"
    SET_SHUTTER_SPEED = "setShutterSpeed"
    SET_DISPLAY_MODE = "setDisplayMode"

    GO_TO_ACTION = "goToAction"
    AIRCRAFT_YAW_ACTION = "aircraftYawAction"
    SET_COLLISION_AVOIDANCE_ENABLED = "setCollisionAvoidanceEnabled"

    # DJI Classes
    FLIGHT_CONTROLLER = "FlightController"
    MISSION_CONTROL = "MissionControl"
    WAYPOINT_MISSION_OPERATOR = "WaypointMissionOperator"
    BUILDER = "Builder"
    LIVE_STREAM_MANAGER = "LiveStreamManager"
    GIMBAL = "Gimbal"
    BATTETY = "Battery"
    CAMERA = "Camera"
    MISSION_ACTION = "MissionAction"

    # Custom flags
    SUCCESS = "success"
    ERROR_TYPE = "errorType"
    DATA = "data"
    BOOL = "bool"
    INT = "int"
    TRUE = "true"
    FALSE = "false"
    VERTICAL_CONTROL_MODE = "vertical_control_mode"

    # Error types
    DJI_ERROR = "DJI_ERROR"
    JSON_ERROR = "JSON_ERROR"
    MODULE_NOT_AVAILABLE = "MODULE_NOT_AVAILABLE_ERROR"
    IOERROR = "IOERROR"

    # Custom methods
    RTP_STREAMING = "RTPStreaming"
    START_RTP_STREAMING = "startStreaming"
    STOP_RTP_STREAMING = "stopStreaming"

    @staticmethod
    def build_message(message_method, message_class, message_data):
        return str(
            {
                "method": message_method,
                "class": message_class,
                "data": message_data
            }
        )

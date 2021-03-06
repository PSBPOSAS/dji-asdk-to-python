from dji_asdk_to_python.flight_controller.flight_controller import (
    FlightController
)

from dji_asdk_to_python.video_record_manager import VideoRecordManager
from dji_asdk_to_python.gimbal.gimbal import Gimbal
from dji_asdk_to_python.battery.battery import Battery
from dji_asdk_to_python.camera.camera import Camera
from dji_asdk_to_python.mission_action.mission_action import MissionAction
from dji_asdk_to_python.sdk_manager.live_stream_manager import (
    LiveStreamManager
)


class Aircraft:
    def __init__(self, app_ip):
        self.app_ip = app_ip

    def getGimbal(self):
        return Gimbal(self.app_ip)

    def getFlightController(self):
        return FlightController(self.app_ip)

    def getVideoRecordManager(self):
        return VideoRecordManager(self)

    def getLiveStreamManager(self):
        return LiveStreamManager(self.app_ip)

    def getBattery(self):
        return Battery(self.app_ip)

    def getCamera(self):
        return Camera(self.app_ip)

    def getMissionAction(self):
        return MissionAction(self.app_ip)

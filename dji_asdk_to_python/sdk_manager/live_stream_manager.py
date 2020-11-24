import string
import random
import threading
import cv2
from dji_asdk_to_python.utils.streaming_utils import CV2_Listener, WebRTC_Listener
from dji_asdk_to_python.utils.socket_utils import SocketUtils
from dji_asdk_to_python.utils.message_builder import MessageBuilder
from dji_asdk_to_python.utils.FPS import FPS

import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst  # noqa: E402


class RTPManager:
    def __init__(self, app_ip):
        self.app_ip = app_ip
        letters = [c for c in string.ascii_lowercase]
        self.stream_id = "".join(random.choice(letters) for i in range(10))
        self.streaming_listener = None

    def remote_start(self):
        assert self.streaming_listener is not None
        assert self.streaming_listener.port is not None
        ip = SocketUtils.getIp()
        message = MessageBuilder.build_message(
            message_method=MessageBuilder.START_RTP_STREAMING,
            message_class=MessageBuilder.RTP_STREAMING,
            message_data={"port": self.streaming_listener.port, "ip": ip, "stream_id": self.stream_id},
        )

        def callback(result):
            if isinstance(result, bool) and result:
                return True
            else:
                return result

        return_type = bool
        timeout = 10
        result = SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=True,
        )
        return result

    def set_stream_id(self, stream_id):
        assert isinstance(stream_id, str)
        self.stream_id = stream_id

    def remote_stop(self):
        message = MessageBuilder.build_message(
            message_method=MessageBuilder.STOP_RTP_STREAMING,
            message_class=MessageBuilder.RTP_STREAMING,
            message_data={"stream_id": self.stream_id},
        )

        def callback(result):
            if isinstance(result, bool) and result:
                self.streaming_listener.stop()
                return True
            else:
                return result

        return_type = bool
        timeout = 10

        result = SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            callback=callback,
            timeout=timeout,
            return_type=return_type,
            blocking=True,
        )
        return result


class CV2_Manager(RTPManager):

    def __init__(self, app_ip):
        super().__init__(app_ip)
        self.streaming_listener = CV2_Listener()

    def setWidth(self, width):
        """
        Set frames width
        """
        assert isinstance(width, int)
        if self.isStreaming():
            raise Exception("Already streaming, can not set width")
        self.streaming_listener.width = width

    def setHeigth(self, height):
        """
        Set frames heigth
        """
        assert isinstance(height, int)
        if self.isStreaming():
            raise Exception("Already streaming, can not set height")
        self.streaming_listener.height = height

    def getWidth(self):
        """
        Returns:
            [int]: Width of frames
        """
        return self.streaming_listener.width

    def getHeight(self):
        """
        Returns:
            [int]: Height of frames
        """
        return self.streaming_listener.height

    def isStreaming(self):
        """
        Returns:
            [boolean]: True if is streaming
        """
        return self.streaming_listener.streaming

    def getFrame(self):
        """
        Returns:
            [numpy.array]: An rgb image
        """
        return self.streaming_listener.getFrame()

    def startStream(self):
        """
            Start CV2 streaming
        """
        res = self.remote_start()
        self.streaming_listener.start()
        return res

    def stopStream(self):
        """
            Stop CV2 streaming
        """
        return self.remote_stop()


class WebRTC_Manager(RTPManager):
    def __init__(self, app_ip):
        super().__init__(app_ip)
        self.streaming_listener = WebRTC_Listener()

    def start(self, signalig_server, secret_key):
        self.remote_start()
        self.streaming_listener.start(signalig_server, secret_key)


class CV2_With_WebRTC_Manager(RTPManager):
    def __init__(self, app_ip):
        super().__init__(app_ip)
        self.streaming_listener = CV2_Listener()
        self.webrtc_listener = WebRTC_Listener()
        self.streaming = False
        self.w = 1280
        self.h = 720
        self.fps = 15
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        self.frame_counter = 0

    def start(self, signalig_server, secret_key):
        self.thread_process_cv2_frames = threading.Thread(target=self._process_cv2_frames, args=[])
        self.thread_process_cv2_frames.start()
        self.webrtc_listener.start(signalig_server, secret_key)

    def stop(self):
        self.streaming = False
        self.thread_process_cv2_frames.join()
        self.thread_process_cv2_frames = None

    def _process_cv2_frames(self):
        assert self.remote_start()
        self.streaming_listener.start()
        self.streaming = True

        launch_string = 'appsrc name=source is-live=true format=GST_FORMAT_TIME ' \
                        ' caps=video/x-raw,format=BGR,width=%s,height=%s,framerate=%s/1 ' \
                        '! videoconvert ! video/x-raw,format=I420 ' \
                        '! x264enc speed-preset=ultrafast tune=zerolatency byte-stream=true ' \
                        '! h264parse ! rtph264pay config-interval=-1 pt=96 ! udpsink host=127.0.0.1 port=%s sync=false' % (
                            self.w, self.h, self.fps, self.webrtc_listener.port)

        pipeline = Gst.parse_launch(launch_string)
        appsrc = pipeline.get_child_by_name('source')
        pipeline.set_state(Gst.State.PLAYING)

        fps = FPS()

        print(self.streaming_listener.port)
        print(self.webrtc_listener.port)

        while self.streaming:
            frame = self.streaming_listener.getFrame()

            if frame is None:
                continue

            # print("FPS %s" % fps())

            # frame = cv2.resize(frame, (self.w, self.h), interpolation=cv2.INTER_AREA)
            data = frame.tostring()
            buf = Gst.Buffer.new_allocate(None, len(data), None)
            buf.fill(0, data)
            buf.duration = self.duration

            self.frame_counter += 1
            retval = appsrc.emit('push-buffer', buf)
            if retval != Gst.FlowReturn.OK:
                print(retval)

        pipeline.set_state(Gst.State.NULL)


class RTMPManager:
    def __init__(self, app_ip):
        self.app_ip = app_ip

    def isStreaming(self, timeout=10):
        """
        Determines if the live streaming starts or not. After starting this flag will not be affected by the RTMP server status.

        Returns:
            [bool]: True if the live stream manager is streaming.
        """

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.IS_STREAMING,
            message_class=MessageBuilder.LIVE_STREAM_MANAGER,
            message_data=None,
        )

        return_type = bool

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            timeout=timeout,
            callback=None,
            return_type=return_type,
            blocking=True,
        )

    def setLiveUrl(self, live_url, timeout=10):
        """
        Determines if the live streaming starts or not. After starting this flag will not be affected by the RTMP server status.

        Args:
            - live_url (str): The URL address string of the RTMP Server.

        Returns:
            [bool]: True if live url was setted
        """

        assert isinstance(live_url, str)

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.SET_LIVE_URL,
            message_class=MessageBuilder.LIVE_STREAM_MANAGER,
            message_data={"live_url": live_url},
        )

        return_type = bool

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            timeout=timeout,
            return_type=return_type,
            callback=None,
            blocking=True,
        )

    def startStream(self, timeout=10):
        """
        Starts the live streaming. If the manager starts successfully, isStreaming will return true. The encoder will start to encoding the video frame if it is needed. The video will be streamed to the RTMP server if the server is available. The audio can be streamed along with the video if the audio setting is enabled.

        Returns:
            [int]: An int value of the error code.
        """

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.START_STREAM,
            message_class=MessageBuilder.LIVE_STREAM_MANAGER,
            message_data=None,
        )

        return_type = int

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            timeout=timeout,
            callback=None,
            return_type=return_type,
            blocking=True,
        )

    def stopStream(self, timeout=10):
        """
        Stop the live streaming. The operation is asynchronous and isStreaming will return false when the operation is complete.

        Returns:
            [bool]: True if stopStream was called
        """

        message = MessageBuilder.build_message(
            message_method=MessageBuilder.STOP_STREAM,
            message_class=MessageBuilder.LIVE_STREAM_MANAGER,
            message_data=None,
        )

        return_type = bool

        return SocketUtils.send(
            message=message,
            app_ip=self.app_ip,
            timeout=timeout,
            return_type=return_type,
            callback=None,
            blocking=True,
        )


class LiveStreamManager:
    """
        The manager is used to live streaming using RTMP and RTP protocols over different listeners.
    """

    def __init__(self, app_ip):
        self.app_ip = app_ip

    def getCV2Manager(self):
        """
        Returns:
            [CV2_Manager]: An CV2_Manager instance
        """
        return CV2_Manager(self.app_ip)

    def getWebRTC_Manager(self):
        """
        Returns:
            [WebRTC_Manager]: An WebRTC_Manager instance
        """
        return WebRTC_Manager(self.app_ip)

    def getCV2_With_WebRTC_Manager(self):
        """
        Returns:
            [CV2_With_WebRTC_Manager]: An CV2_With_WebRTC_Manager instance
        """
        return CV2_With_WebRTC_Manager(self.app_ip)

    def getRTMPManager(self):
        """
        Returns:
            [RTMPManager]: An RTMPManager instance
        """
        return RTMPManager(self.app_ip)

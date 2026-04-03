import requests
import time


class PTZController:
    def pan_move(self, speed, times):
        data = {
            "Velocity": {
                "PanTilt": {
                    "x": speed,
                    "y": 0
                },
                "Zoom": {
                    "x": 0
                }

            },
            "Timeout": times
        }
        response = requests.post("http://127.0.0.1:8889/ptz/move/ContinuousMove", json=data)

    def tilt_move(self, speed, times):
        data = {
            "Velocity": {
                "PanTilt": {
                    "x": 0,
                    "y": speed
                },
                "Zoom": {
                    "x": 0
                }

            },
            "Timeout": times
        }
        response = requests.post("http://127.0.0.1:8889/ptz/move/ContinuousMove", json=data)

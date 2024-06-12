#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use ALTabletService to Control Video Playback"""

import qi
import argparse
import sys
import time

def main(session):
    """
    This script demonstrates how to use the ALTabletService to play, pause, and stop video playback.
    It plays a video, pauses after a few seconds, resumes, and finally stops the video.
    """
    try:
        # Get the ALTabletService
        tabletService = session.service("ALTabletService")

        # Enable tablet wifi, required for accessing internet videos
        tabletService.enableWifi()

        # URL of the video to play
        video_url = "https://youtu.be/dQw4w9WgXcQ?si=RtMR6vXY0RJAhsaK"

        # Start playing video
        if tabletService.playVideo(video_url):
            print("Video started successfully.")
        else:
            print("Failed to start video.")
            return

        # Let the video play for 10 seconds
        time.sleep(120)

        # Pause the video
        if tabletService.pauseVideo():
            print("Video paused.")
        else:
            print("Failed to pause video.")

        # Wait for 5 seconds while video is paused
        time.sleep(5)

        # Resume video playback
        if tabletService.resumeVideo():
            print("Video resumed.")
        else:
            print("Failed to resume video.")

        # Let the video play for another 10 seconds
        time.sleep(10)

        # Stop the video and close the player
        if tabletService.stopVideo():
            print("Video stopped and player closed.")
        else:
            print("Failed to stop video.")

    except Exception as e:
        print("Error was:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.140",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n"
              "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)

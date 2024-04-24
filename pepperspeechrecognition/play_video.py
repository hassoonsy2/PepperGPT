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
        video_url = "https://rr3---sn-5hne6nsk.googlevideo.com/videoplayback?expire=1713971372&ei=TMwoZtz2HrnB6dsPseyC-As&ip=193.32.8.36&id=o-AB0sF8xhVOtpDmicgrRa3T0Z4J1WVfBGrc7E2ohAQEX1&itag=22&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&mh=y4&mm=31%2C29&mn=sn-5hne6nsk%2Csn-5hnednsz&ms=au%2Crdu&mv=m&mvi=3&pl=24&gcr=nl&initcwndbps=296250&spc=UWF9f8zd0L9XgyMBJIvgUMGqZa6-Czkr_7Wk&vprv=1&svpuc=1&mime=video%2Fmp4&cnr=14&ratebypass=yes&dur=167.648&lmt=1706010379068705&mt=1713949491&fvip=4&c=ANDROID&txp=4532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cgcr%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=AJfQdSswRgIhAKjqp_s69uTM8FOcGEA-e9M6LNvOkemt9um1g7wZzBeuAiEA3QhvQfT3aQ21iaDefFqaSe_IU_X27M9kgWphpnpoVe8%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AHWaYeowRgIhAPblzxuWfCgT_qKSL2ChdBqYaKp_ZEz39okv4Q5Cnfm3AiEA8ETySiBBV9yAyHBxwFPqz-rJ-qNBnLSYUWIrnGFhwas%3D&title=Iggy%20Azalea%20-%20Kream%20ft.%20Tyga"

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
    parser.add_argument("--ip", type=str, default="127.0.0.1",
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

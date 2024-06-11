@echo off
start cmd /k python3 startDialogueServer.py --server openai
timeout /t 10
start cmd /k python module_speechrecognition.py --pip 192.168.1.140
timeout /t 10
start cmd /k python module_dialogue.py --pip 192.168.1.140 --server openai

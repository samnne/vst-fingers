# VST Fingers — Camera-to-Max9 Controller

A short project for a music class that uses a camera and finger detection to trigger VST instruments inside Max9. The Python app detects fingers via webcam, sends OSC messages to Max9, and Max maps those messages to VST parameters/notes.

## Highlights
- Live finger detection from a webcam.
- OSC messages sent to Max9 to trigger VSTs.

## Requirements
- Python 3.11
- Max9 (Demo or Full)
- Webcam (internal or USB)
- Recommended Python packages: opencv-python, python-osc, pyautogui
- 3 VST's of your choosing


## Install & Run
1. Open a terminal:
cd python_code
pip install opencv-python python-osc pyautogui
python main.py 

2. In Max9, open the patch that listens for OSC on the same port (see [python_code/max-port.txt](python_code/max-port.txt) for the port used in this project).
3. Focus the camera on your hand and use fingers to control synth parameters or trigger notes.

## How it works (quick)
- The Python app in [python_code/main.py](python_code/main.py) captures frames from the webcam and runs the hand detector implemented in [python_code/track_hand.py](python_code/track_hand.py).
- The main loop is implemented by `main.handle_connection` which reads frames, computes which fingers are up, and sends OSC.
  - See symbol: [`main.handle_connection`](python_code/main.py)
- OSC messages are sent with:
  - See symbol: [`main.client.send_message`](python_code/main.py)
  - Path used: `/filter` with a list of five integers representing each finger state.
- The hand detector class is `track_hand.handDetector`, instantiated in `main`:
  - See symbol: [`track_hand.handDetector`](python_code/track_hand.py)

## Max Integration
- Max receives `/filter` (an array of five 0/1 values) and maps finger patterns to VST actions (note on/off, parameter changes).
- Edit the Max patch to change mappings or port; keep the port consistent with the `--port` value passed to `main.py`.
- In the max patch load up 3 plugins and set the presets you desire and then run the python script `main.py`. 

## Files of interest
- Python controller: [python_code/main.py](python_code/main.py)
- Hand detection: [python_code/track_hand.py](python_code/track_hand.py)
- Project README and docs: [python_code/README.md](python_code/README.md)
- Max port config: [python_code/max-port.txt](python_code/max-port.txt)

## Notes & tips
- To use an ESP32-CAM or other IP camera, replace the VideoCapture source in [python_code/main.py](python_code/main.py). (Very finnicky: works loosly)
- For reliability, run Max and the Python app on the same machine or same LAN and ensure firewall allows UDP on the chosen port.

Credits: project built using OpenCV-based hand detection and OSC control for Max9.
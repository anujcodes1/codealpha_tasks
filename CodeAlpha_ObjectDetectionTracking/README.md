# 🎯 Object Detection and Tracking

**CodeAlpha Artificial Intelligence Internship - Task 4**

Real-time object detection and multi-object tracking on a webcam stream or video file.
Every object gets a bounding box, a class label, a confidence score and a **unique tracking ID** that stays
with it from frame to frame.

## Features
- Real-time video input from a **webcam or video file** (OpenCV)
- **YOLOv8** pre-trained detector (80 COCO classes: person, car, dog, bottle...)
- **ByteTrack** tracking (SORT-family: Kalman filter + IoU association); BoT-SORT also available
- Bounding boxes, labels, confidence and **tracking IDs** drawn on every frame
- Movement **trails** for each tracked object
- Live counters: objects in frame and total unique objects tracked
- Filter by class (`--classes person car`), adjust confidence, save annotated output video

## Tech stack
Python · OpenCV · Ultralytics YOLOv8 · ByteTrack · NumPy

## Setup & run
```bash
git clone https://github.com/anujcodes1/CodeAlpha_ObjectDetectionTracking.git
cd CodeAlpha_ObjectDetectionTracking
pip install -r requirements.txt

python detect_track.py                                   # webcam
python detect_track.py --source sample.mp4               # video file
python detect_track.py --source sample.mp4 --save output.mp4
python detect_track.py --classes person car --conf 0.5   # track only people and cars
python detect_track.py --tracker botsort.yaml            # use BoT-SORT instead
```
Press **q** or **ESC** to quit. The YOLO weights (`yolov8n.pt`, ~6 MB) download automatically on the first run.

## Options
| Option | Default | Description |
|--------|---------|-------------|
| `--source` | `0` | Webcam index or video file path |
| `--model` | `yolov8n.pt` | YOLO weights; use `yolov8s.pt`/`m.pt` for more accuracy |
| `--tracker` | `bytetrack.yaml` | `bytetrack.yaml` or `botsort.yaml` |
| `--conf` | `0.35` | Confidence threshold |
| `--classes` | all | Class names to keep |
| `--save` | none | Save annotated video |
| `--no-show` | off | Run without a display window |
| `--no-trails` | off | Hide movement trails |

## How it works
1. OpenCV/Ultralytics reads frames from the webcam or video file.
2. YOLOv8 detects objects in each frame.
3. The tracker matches detections to existing tracks using motion prediction (Kalman filter) and IoU,
   assigning each object a persistent ID.
4. The frame is annotated with boxes, labels, IDs and trails, then displayed in real time.

## Author
Anuj Mishra - [GitHub](https://github.com/anujcodes1)

#CodeAlpha

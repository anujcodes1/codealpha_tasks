"""Real-time object detection and tracking.

Detection : YOLOv8 (pre-trained on COCO, 80 classes) via `ultralytics`
Tracking  : ByteTrack (a SORT-family tracker built on Kalman filter + IoU association)
Video     : OpenCV - webcam or video file

Examples
    python detect_track.py                          # webcam
    python detect_track.py --source video.mp4       # video file
    python detect_track.py --source video.mp4 --save output.mp4 --classes person car
Press  q  or  ESC  in the video window to quit.
"""
import argparse
import os
import sys
from collections import defaultdict, deque

import cv2
import numpy as np
from ultralytics import YOLO


def parse_args():
    p = argparse.ArgumentParser(description="Object detection and tracking (YOLOv8 + ByteTrack)")
    p.add_argument("--source", default="0", help="webcam index (0, 1...) or path to a video file")
    p.add_argument("--model", default="yolov8n.pt", help="YOLO weights (yolov8n/s/m/l/x.pt)")
    p.add_argument("--tracker", default="bytetrack.yaml", choices=["bytetrack.yaml", "botsort.yaml"])
    p.add_argument("--conf", type=float, default=0.35, help="confidence threshold")
    p.add_argument("--classes", nargs="*", default=None,
                   help="only track these class names, e.g. --classes person car")
    p.add_argument("--save", default=None, help="save the annotated video to this path (e.g. out.mp4)")
    p.add_argument("--no-show", action="store_true", help="do not open a display window")
    p.add_argument("--no-trails", action="store_true", help="do not draw movement trails")
    return p.parse_args()


def color_for_id(track_id):
    """Stable, distinct colour per track ID."""
    rng = np.random.RandomState(track_id * 7919 % (2**31))
    return tuple(int(c) for c in rng.randint(60, 255, 3))


def main():
    args = parse_args()
    source = int(args.source) if args.source.isdigit() else args.source
    if isinstance(source, str) and not os.path.exists(source):
        sys.exit(f"Error: video file not found: {source}")

    model = YOLO(args.model)
    names = model.names  # {class_id: class_name}

    class_ids = None
    if args.classes:
        lookup = {v.lower(): k for k, v in names.items()}
        missing = [c for c in args.classes if c.lower() not in lookup]
        if missing:
            sys.exit(f"Unknown class name(s): {missing}. Available: {sorted(lookup)}")
        class_ids = [lookup[c.lower()] for c in args.classes]

    trails = defaultdict(lambda: deque(maxlen=30))
    seen_ids = set()
    writer = None
    frame_no = 0

    results = model.track(source=source, stream=True, persist=True, tracker=args.tracker,
                          conf=args.conf, classes=class_ids, verbose=False)
    try:
        for result in results:
            frame = result.orig_img.copy()
            boxes = result.boxes
            if boxes is not None and boxes.id is not None:
                xyxy = boxes.xyxy.cpu().numpy().astype(int)
                ids = boxes.id.cpu().numpy().astype(int)
                cls = boxes.cls.cpu().numpy().astype(int)
                confs = boxes.conf.cpu().numpy()
                for (x1, y1, x2, y2), tid, c, conf in zip(xyxy, ids, cls, confs):
                    seen_ids.add(int(tid))
                    color = color_for_id(int(tid))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    label = f"ID {tid} {names[c]} {conf:.2f}"
                    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
                    cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 6, y1), color, -1)
                    cv2.putText(frame, label, (x1 + 3, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.55, (255, 255, 255), 1, cv2.LINE_AA)
                    trails[int(tid)].append(((x1 + x2) // 2, (y1 + y2) // 2))
                    if not args.no_trails:
                        pts = np.array(trails[int(tid)], dtype=np.int32).reshape(-1, 1, 2)
                        cv2.polylines(frame, [pts], False, color, 2)
                current = len(ids)
            else:
                current = 0

            hud = f"Objects in frame: {current} | Unique tracked: {len(seen_ids)}"
            cv2.putText(frame, hud, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4, cv2.LINE_AA)
            cv2.putText(frame, hud, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

            if args.save:
                if writer is None:
                    h, w = frame.shape[:2]
                    writer = cv2.VideoWriter(args.save, cv2.VideoWriter_fourcc(*"mp4v"), 25, (w, h))
                writer.write(frame)

            if not args.no_show:
                cv2.imshow("Object Detection & Tracking (press q to quit)", frame)
                if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                    break
            frame_no += 1
    except KeyboardInterrupt:
        pass
    finally:
        if writer is not None:
            writer.release()
            print(f"Saved annotated video to {args.save}")
        cv2.destroyAllWindows()
    print(f"Processed {frame_no} frames. Unique objects tracked: {len(seen_ids)}")


if __name__ == "__main__":
    main()

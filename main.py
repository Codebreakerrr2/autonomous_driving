import cv2
import time

from perception.lane_detector import LaneDetector
from perception.yolo_detector import ObjectDetector
from perception.depth_estimator import  DepthEstimator
from graph.scene_graph import SceneGraph
"from decision.decision_module import DecisionModule"


# ============================================
#                 MAIN LOOP
# ============================================
def main():
    cap = cv2.VideoCapture(0)   # Kamera oder Video

    lane_detector = LaneDetector()
    object_detector = ObjectDetector()
    depth_estimator = DepthEstimator()

    decision_module = DecisionModule()

    frame_count = 0
    depth_map = None

    graph = SceneGraph()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 1) --- LANE DETECTION ---
        lanes = lane_detector.detect(frame)


        # 2) --- OBJECT DETECTION ---
        objects = object_detector.detect(frame)


        # 3) --- DEPTH ESTIMATION ( EVERY N FRAMES) ---
        if frame_count % 5 == 0:          # run every 5 frames for speed
            depth_map = depth_estimator.estimate(frame)

        # 4) --- BUILD SCENE GRAPH ---
        graph.clear()
        graph.add_lanes(lanes)

        if depth_map is not None:
            graph.add_objects(objects, depth_map)
        else:
            graph.add_objects(objects)

        # 5) --- DECISION MAKING ---
        car_state = graph.extract_car_state()  # position, angle, distances
        surrounding = graph.extract_surrounding()

        command = decision_module.decide(car_state, surrounding)
        # command ∈ {"go_straight", "slow_down", "stop", "steer_left", ...}

        # 6) --- OUTPUT COMMAND ---
        print("Decision:", command)

        # Optional visualization
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

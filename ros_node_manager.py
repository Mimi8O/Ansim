import threading
import rclpy
from utils.ros_publisher import RoutePublisher

class ROS2NodeWrapper:
    def __init__(self):
        self.node = None

ros2_node_holder = ROS2NodeWrapper()

def start_ros2_node():
    print("🌱 [ROS2 Init] rclpy.init() 시작")
    try:
        rclpy.init()
        print("🌳 [ROS2 Init] RoutePublisher 초기화 시작")
        ros2_node_holder.node = RoutePublisher()
        print("✅ [ROS2 Init] ROS2 노드 생성 완료, spin 시작")
        rclpy.spin(ros2_node_holder.node)
    except Exception as e:
        print(f"❌ [ROS2 Init] 오류 발생: {e}")

def run_ros2_background():
    print("🧵 ROS2 백그라운드 스레드 시작")
    thread = threading.Thread(target=start_ros2_node, daemon=True)
    thread.start()


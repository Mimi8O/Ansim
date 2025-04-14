# utils/ros_publisher.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

class RoutePublisher(Node):
    def __init__(self):
        super().__init__('route_publisher')
        self.publisher_ = self.create_publisher(String, 'tmap_route', 10)

    def publish_route(self, route_data):
        msg = String()
        msg.data = json.dumps(route_data)
        self.publisher_.publish(msg)


# app.py
from flask import Flask
from routes.call_robot import call_robot_bp
from routes.verify_user import verify_user_bp
from routes.set_destination import set_destination_bp

from ros_node_manager import run_ros2_background, ros2_node_holder
import time

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 블루프린트 등록
app.register_blueprint(call_robot_bp, url_prefix='/call_robot')
app.register_blueprint(verify_user_bp, url_prefix='/verify_user')
app.register_blueprint(set_destination_bp, url_prefix='/set_destination')

# ROS2 백그라운드 실행
run_ros2_background()

# ✅ ros2_node가 준비될 때까지 대기 (최대 5초)
timeout = 5
while ros2_node_holder is None and timeout > 0:
    print("⏳ Waiting for ROS2 node to spin up...")
    time.sleep(0.5)
    timeout -= 0.5

if ros2_node_holder:
    print("✅ ROS2 Node is ready.")
else:
    print("❌ ROS2 Node failed to start.")

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask
from routes.call_robot import call_robot_bp
from routes.verify_user import verify_user_bp
from routes.set_destination import set_destination_bp

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 블루프린트 등록
app.register_blueprint(call_robot_bp, url_prefix='/call_robot')
app.register_blueprint(verify_user_bp, url_prefix='/verify_user')
app.register_blueprint(set_destination_bp, url_prefix='/set_destination')

if __name__ == '__main__':
    app.run(debug=True)


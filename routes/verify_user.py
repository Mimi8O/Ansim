from flask import Blueprint, request, jsonify

verify_user_bp = Blueprint('verify_user', __name__)

@verify_user_bp.route('/', methods=['POST'])
def verify_user():
    # 사용자 인증용 더미 처리
    data = request.get_json()
    user_id = data.get("user_id")
    code = data.get("code")
    print("인증 시도:", user_id, code)
    return jsonify({"message": "사용자 인증 완료(가정)"})


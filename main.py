from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 이벤트 상세 정보
event = {
    "name": "테크 혁신가 모임",
    "date": "2024-09-30",
    "time": "18:00",
    "location": "테크허브, 혁신 거리 123, 실리콘 밸리",
    "description": "최첨단 기술 강연과 업계 리더들과의 네트워킹을 위한 저녁 모임에 참여하세요!"
}

# 등록 정보를 위한 인메모리 저장소
registrations = {}

@app.route("/")
def index():
    return render_template("index.html", event=event)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    full_name = data.get("fullName")

    if email and full_name:
        # 인메모리 저장
        registrations[email] = full_name
        return jsonify({"success": True, "message": "등록이 성공적으로 완료되었습니다!"}), 200
    else:
        return jsonify({"success": False, "message": "유효하지 않은 데이터가 제공되었습니다."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

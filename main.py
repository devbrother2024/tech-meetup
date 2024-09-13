from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Event details
event = {
    "name": "Tech Innovators Meetup",
    "date": "2023-07-15",
    "time": "18:00",
    "location": "TechHub, 123 Innovation Street, Silicon Valley",
    "description": "Join us for an evening of cutting-edge tech talks and networking with industry leaders!"
}

# In-memory storage for registrations
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
        # Store in-memory
        registrations[email] = full_name
        return jsonify({"success": True, "message": "Registration successful!"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid data provided."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

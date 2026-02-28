from flask import Flask, render_template, request
import pandas as pd
import qrcode
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_image = None

    if request.method == "POST":
        file = request.files["file"]
        user_id = request.form["id"]

        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            data = pd.read_excel(filepath)

            row = data[data["ID"] == int(user_id)]

            if not row.empty:
                row_data = row.iloc[0]
                qr_text = ""
                for col in data.columns:
                    qr_text += f"{col}: {row_data[col]}\n"

                qr = qrcode.make(qr_text)
                qr_path = f"static/QR_{user_id}.png"
                qr.save(qr_path)

                qr_image = qr_path

    return render_template("index.html", qr_image=qr_image)

if __name__ == "__main__":
    app.run(debug=True)
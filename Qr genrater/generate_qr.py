import uuid
import qrcode
import os

# Students list (Roll/Name/ID etc.)
students = [
    {"name": "Akash", "roll_no": "123"},
    {"name": "Priya", "roll_no": "124"},
    {"name": "Rahul", "roll_no": "125"},
    {"name": "muskan", "roll_no": "126"},
    {"name": "prince", "roll_no": "128"}
]

output_folder = "qr_gallery"
os.makedirs(output_folder, exist_ok=True)

for student in students:
    # Generate a random UUID token for each student
    qr_token = str(uuid.uuid4())
    student["qr_token"] = qr_token  # Store token with student

    # Create QR code image
    qr_img = qrcode.make(qr_token)

    # Save image (filename: rollnumber.png)
    file_path = os.path.join(output_folder, f"{student['roll_no']}.png")
    qr_img.save(file_path)

    print(f"QR for {student['name']} saved at {file_path}")

# Optional: Save all tokens to DB or JSON for future verification

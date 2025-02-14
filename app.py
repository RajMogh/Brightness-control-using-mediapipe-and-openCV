from flask import Flask, render_template_string
import threading

app = Flask(__name__)

# Global list to store patient details
patients = []

# Define the HTML content as a string
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Patient Management</title>
    <style>
        /* Your existing CSS styles */
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<body>

<header class="header">
    <img src="Vit.png" alt="VIT Logo" class="logo-left">
    <img src="vi.png" alt="Vitality Ventures Logo" class="logo-right">
    <h1>VIT Vellore Institute Of Technology<br>Bhopal</h1>
</header>

<div class="content">
    <div class="form-container">
        <h2>Add Patient</h2>

        <!-- Photo upload section with edit button overlay -->
        <div class="photo-upload-container">
            <button class="edit-button" onclick="document.getElementById('photo').click()">
                <i class="fas fa-edit"></i>
            </button>
            <input type="file" id="photo" accept="image/png, image/jpeg, image/jpg" onchange="previewPhoto(event)">
            <img id="previewImg" src="default.png" alt="Preview" class="patient-photo">
        </div>

        <label for="name">Name:</label>
        <input type="text" id="name" placeholder="Enter patient name" required>

        <label for="age">Age:</label>
        <input type="number" id="age" placeholder="Enter patient age" required>

        <label for="contact">Contact Number:</label>
        <input type="tel" id="contact" placeholder="Enter contact number" required>

        <label for="history">Medical History:</label>
        <input type="text" id="history" placeholder="Enter medical history" required>

        <button onclick="addPatient()">Add Patient</button>
    </div>

    <div class="patient-list" id="patientList">
        <h2>Patient List</h2>
        <div class="search-container">
            <input type="text" id="search" placeholder="Search by name" oninput="searchPatient()">
            <button id="searchButton" onclick="searchPatient()">🔍</button>
        </div>
        <div id="patientCards">
            <p>No patients added yet.</p>
        </div>
    </div>
</div>

<footer>
    <p>&copy; 2024 Vitality Ventures. All rights reserved.</p>
</footer>
<style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
        }

        .header {
            position: relative;
            background-color: #fff;
            padding: 20px 0;
            text-align: center;
        }

        .header h1 {
            margin: 0;
            font-size: 2em;
            color: #333;
            line-height: 1.5;
        }

        .logo-left,
        .logo-right {
            position: absolute;
            top: 10px;
            max-width: 150px;
            height: auto;
        }

        .logo-left {
            left: 30px;
        }

        .logo-right {
            right: 30px;
        }

        .content {
            display: flex;
            padding: 20px;
            justify-content: space-between;
        }

        .form-container {
            width: 25%;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .patient-list {
            width: 70%;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            margin-left: 20px;
        }

        .form-container label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }

        .form-container input,
        .form-container button {
            width: calc(100% - 24px);
            padding: 12px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 14px;
            box-sizing: border-box;
        }

        .form-container button {
            background-color: #007bff;
            color: #fff;
            border: none;
            cursor: pointer;
        }

        .form-container button:hover {
            background-color: #0056b3;
        }

        .patient-card {
            padding: 15px;
            border-bottom: 1px solid #ddd;
        }

        .patient-card:last-child {
            border-bottom: none;
        }

        .patient-card h3 {
            margin: 0;
            color: #333;
        }

        .patient-card p {
            margin: 5px 0;
            color: #555;
        }

        .search-container {
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }

        .search-container input {
            padding: 8px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 5px;
            width: 150px;
            margin-right: 5px;
        }

        .search-container button {
            padding: 8px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #007bff;
            color: #fff;
            cursor: pointer;
        }

        .search-container button:hover {
            background-color: #0056b3;
        }

        footer {
            background-color: #333;
            color: #fff;
            padding: 10px;
            text-align: center;
        }

        footer p {
            margin: 0;
        }

        .monitoring-box {
            display: flex;
            align-items: center;
            margin-top: 10px;
        }

        .blinking-light {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: red;
            animation: blink 1s infinite;
            margin-right: 10px;
        }

        @keyframes blink {
            0%, 50% {
                opacity: 1;
            }
            50.01%, 100% {
                opacity: 0;
            }
        }

        .monitoring-text {
            font-size: 14px;
            color: #333;
        }
        
        .icon-container {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 10px;
            position: relative; /* Ensure that edit button appears over the image */
        }

        .icon-container button {
            background: none;
            border: none;
            cursor: pointer;
        }

        .icon-container i {
            font-size: 18px;
        }

        .icon-container button:hover {
            opacity: 0.2;
        }

        /* New styles for the image */
        .patient-photo {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
            margin-right: 15px;
        }

        .photo-upload-container {
            margin-bottom: 15px;
            text-align: center;
            position: relative; /* Make sure the icon is positioned on top */
        }

        .photo-upload-container input {
            display: none;
        }

        .upload-button {
            cursor: pointer;
            background-color: #007bff;
            color: white;
            padding: 8px 15px;
            border: none;
            border-radius: 90px;
            margin-top: 10px;
        }

        .upload-button:hover {
            background-color: #0056b3;
        }

        /* Style for edit button overlay */
        /* Style for edit button overlay */
        .edit-button {
            position: absolute;
            top: 5px;
            right: 5px;
            background-color: transparent; /* Transparent background */
            border: 2px solid rgba(0, 123, 255, 0.5); /* Light blue border */
            color: rgba(0, 123, 255, 0.5); /* Blue icon color */
            padding: 8px;
            border-radius: 50%; /* Make the button circular */
            cursor: pointer;
            opacity: 0; /* Make the button invisible by default */
            transition: opacity 0.3s ease, background-color 0.3s ease, border-color 0.3s ease;
            width: 40px; /* Define a fixed width */
            height: 40px; /* Define a fixed height */
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Make edit button visible when hovering over the image container */
        .photo-upload-container:hover .edit-button {
            opacity: 1; /* Make button visible on hover */
            background-color: rgba(0, 123, 255, 0.1); /* Light blue background when hovered */
            border-color: rgba(0, 123, 255, 0.7); /* Darker blue border when hovered */
            color: rgba(0, 123, 255, 0.7); /* Darker blue icon color when hovered */
        }

        .edit-button i {
            font-size: 18px; /* Icon size */
        }


    </style>

<script>
    const patients = []; // Array to store patient details

    // Function to preview the uploaded photo
    function previewPhoto(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const previewImg = document.getElementById("previewImg");
                previewImg.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    }

    // Function to add a patient
    function addPatient() {
        const name = document.getElementById("name").value;
        const age = document.getElementById("age").value;
        const contact = document.getElementById("contact").value;
        const history = document.getElementById("history").value;
        const photo = document.getElementById("previewImg").src || 'default.png'; // Use default PNG image if no photo is uploaded

        if (name && age && contact && history) {
            // Add patient with default alert status (0 for green, 1 for red)
            patients.push({ name, age, contact, history, photo, alertStatus: 0, alertMessage: "Patient is stable." });
            document.getElementById("name").value = '';
            document.getElementById("age").value = '';
            document.getElementById("contact").value = '';
            document.getElementById("history").value = '';
            document.getElementById("previewImg").src = 'default.png'; // Reset photo preview
            displayPatients(); // Refresh the patient list
        } else {
            alert("Please fill out all fields.");
        }
    }

    // Function to display patients
    function displayPatients(filteredPatients = patients) {
        const patientCardsContainer = document.getElementById("patientCards");
        patientCardsContainer.innerHTML = ""; // Clear previous cards

        if (filteredPatients.length === 0) {
            patientCardsContainer.innerHTML = "<p>No patients found.</p>";
        } else {
            filteredPatients.forEach((patient, index) => {
                const patientCard = document.createElement("div");
                patientCard.className = "patient-card";
                patientCard.innerHTML = 
                    `<div style="display: flex; align-items: center;">
                        <img src="${patient.photo}" class="patient-photo" alt="Patient Photo">
                        <div>
                            <h3>${patient.name}</h3>
                            <p><strong>Age:</strong> ${patient.age}</p>
                            <p><strong>Contact:</strong> ${patient.contact}</p>
                            <p><strong>Medical History:</strong> ${patient.history}</p>
                        </div>
                    </div>
                    <div class="monitoring-box">
                        <div class="blinking-light" style="background-color: ${patient.alertStatus === 0 ? 'green' : 'red'};"></div>
                        <span class="monitoring-text">${patient.alertMessage}</span>
                    </div>
                    <div class="icon-container">
                        <button onclick="editPatient(${index})"><i class="fas fa-edit"></i></button>
                        <button onclick="deletePatient(${index})"><i class="fas fa-trash-alt"></i></button>
                    </div>`;
                patientCardsContainer.appendChild(patientCard);
            });
        }
    }

    // Function to edit a patient
    function editPatient(index) {
        const patient = patients[index];
        document.getElementById("name").value = patient.name;
        document.getElementById("age").value = patient.age;
        document.getElementById("contact").value = patient.contact;
        document.getElementById("history").value = patient.history;

        // Remove the patient from the list and re-render
        patients.splice(index, 1);
        displayPatients();
    }

    // Function to delete a patient
    function deletePatient(index) {
        if (confirm("Are you sure you want to delete this patient?")) {
            patients.splice(index, 1); // Remove patient from array
            displayPatients(); // Refresh the patient list
        }
    }

    // Function to search for a patient by name
    function searchPatient() {
        const searchTerm = document.getElementById("search").value.toLowerCase();
        const filteredPatients = patients.filter(patient =>
            patient.name.toLowerCase().includes(searchTerm)
        );
        displayPatients(filteredPatients); // Update the patient cards based on the search
    }
</script>

</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_content)

# Function to handle terminal input
def terminal_input():
    while True:
        try:
            # Get patient index and alert status from terminal input
            patient_index = int(input("Enter patient index (0-based): "))
            alert_status = int(input("Enter alert status (0 for green, 1 for red): "))

            # Validate input
            if patient_index < 0 or patient_index >= len(patients):
                print("Invalid patient index.")
                continue
            if alert_status not in [0, 1]:
                print("Invalid alert status. Enter 0 or 1.")
                continue

            # Update patient alert status
            patients[patient_index]["alertStatus"] = alert_status
            patients[patient_index]["alertMessage"] = "Patient is stable." if alert_status == 0 else "Patient needs attention!"
            print(f"Patient {patient_index} alert status updated to {'green' if alert_status == 0 else 'red'}.")
        except ValueError:
            print("Invalid input. Please enter integers.")

# Run the terminal input function in a separate thread
threading.Thread(target=terminal_input, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)
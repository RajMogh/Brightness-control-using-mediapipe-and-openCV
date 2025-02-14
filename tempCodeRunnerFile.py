from flask import Flask, render_template_string, jsonify
import threading
import time

app = Flask(__name__)

# Global list to store patient details
patients = [
    {"name": "John Doe", "age": 30, "contact": "1234567890", "history": "None", "photo": "default.png", "alertStatus": 0, "alertMessage": "Patient is stable."}
]

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

<script>
    let patients = []; // Array to store patient details

    // Function to fetch patient data from the server
    function fetchPatients() {
        fetch('/get_patients')
            .then(response => response.json())
            .then(data => {
                patients = data;
                displayPatients();
            });
    }

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

    // Fetch patient data every 2 seconds
    setInterval(fetchPatients, 2000);
</script>

</body>
</html>
'''

# Route to fetch patient data
@app.route('/get_patients')
def get_patients():
    return jsonify(patients)

# Function to monitor the text file and update patient alert status
def monitor_file():
    while True:
        try:
            with open("data.txt", "r") as file:
                lines = file.readlines()
                if lines:
                    # Get the last line in the file
                    last_line = lines[-1].strip()
                    # Extract the numeric value (e.g., "29" from "2025-01-26 15:04:37 : 29")
                    value = int(last_line.split(":")[-1].strip())
                    # Update patient alert status based on the value
                    if value < 60 or value > 100:
                        patients[0]["alertStatus"] = 1  # Red
                        patients[0]["alertMessage"] = "Patient needs attention!"
                    else:
                        patients[0]["alertStatus"] = 0  # Green
                        patients[0]["alertMessage"] = "Patient is stable."
        except Exception as e:
            print(f"Error reading file: {e}")
        time.sleep(2)  # Check the file every 2 seconds

# Run the file monitoring function in a separate thread
threading.Thread(target=monitor_file, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)
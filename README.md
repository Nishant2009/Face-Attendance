# Face-Attendance System for Classroom

This project is a face recognition-based attendance system designed for classrooms. It is built using Python, OpenCV, and the `face_recognition` library to streamline attendance tracking efficiently.

---

## **Features**
- **Student Dataset Creation**:
  - Capture and store images of students with their Roll Numbers.
  - Save student data in JSON format for easy management.
- **Face Recognition**:
  - Real-time face recognition using the `face_recognition` library.
- **Gesture-Based Validation**:
  - Prevents false attendance using gesture recognition.
  - Simple gestures like stone, paper, and scissors are used in random order to confirm attendance.
- **Attendance Logging**:
  - Attendance is marked and stored in `Class_Name/attendance.csv`.

---

## **Requirements**
- Python 3.10
- OpenCV
- Libraries mentioned in `requirements.txt`

---

## **Setup Instructions**

### 1. Clone the Repository
```bash
git clone https://github.com/Nishant2009/Face-Attendance
cd Face-Attendance
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare the Dataset
- **Images**: 
  - Store images of students in the `Class_Name/New_Faces` folder.
  - Ensure each image file is named with the Roll Number of the respective student.
- **Attendance File**: 
  - Populate the `Class_Name/attendance.csv` file with the following format:
    ```csv
    Registration No.,Name
    1, Name1
    2, Name2
    ```

---

## **Usage Instructions**

### Running the Program
1. Execute the main script:
   ```bash
   python main.py
   ```
2. Follow the on-screen instructions:
   - Show faces to the camera to mark attendance.
   - Perform the prompted gestures to confirm attendance.
3. Press `q` to exit the program.

### Notes
- Ensure the camera is functional and accessible.
- The program has been tested on **Windows 11** with **Python 3.10**. Compatibility with other platforms may vary.

---

## **Key Functionalities**

### Dataset Creation
- Automatically encodes faces from the images stored in the dataset folder (`Class_Name/New_Faces`).
- Saves face encodings and Roll Numbers in a JSON file for quick lookup.

### Real-Time Recognition
- Uses the camera feed to detect and recognize faces.
- Matches detected faces with the stored dataset to identify students.

### Gesture-Based Validation
- Implements a rock-paper-scissors gesture game to prevent misuse (e.g., showing photos for attendance).
- Randomly prompts gestures and validates the input before marking attendance.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

### **Contact**
For any issues or suggestions, please raise an issue in the [GitHub repository](https://github.com/Nishant2009/Face-Attendance).

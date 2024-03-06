# Face-Attendance

This is a simple face recognition based attendance system. The program takes images of the students and stores them in a folder. It then uses these images to recognize the students and mark their attendance. The attendance is then stored in a CSV file.

## Installation

Clone the repository and install the required packages using the following command:

```bash
git clone https://github.com/Nishant2009/Face-Attendance.git
cd Face-Attendance
pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
pip install -r requirements.txt
```

## Usage

1. Store the images of the students in the `BTech\known_faces` folder.
2. Run the `Face_encoder.py` file to encode the images.
3. Run the `Attendance_taker.py` file to mark the attendance.
4. The attendance will be stored in the `BTech\attendance_temp.csv` file.

## Features

- Easy to use
- Fast and efficient
- Just need single image of the student to mark attendance


## License
[MIT](https://choosealicense.com/licenses/mit/)

## Support

For any questions or issues, please open an issue on GitHub.

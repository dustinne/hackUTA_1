from flask import Flask, jsonify
import cv2
from deepface import DeepFace
from collections import Counter
import pymongo

# Initialize the Flask app
app = Flask(__name__)

# Configure MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/your_database_name"


# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_emotion():
    # Start capturing video
    cap = cv2.VideoCapture(0)

    frame_count = 0
    detected = []
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convert grayscale frame to RGB format
        rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Extract the face ROI (Region of Interest)
            face_roi = rgb_frame[y:y + h, x:x + w]

            
            # Perform emotion analysis on the face ROI
            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

            # Determine the dominant emotion
            emotion = result[0]['dominant_emotion']
            detected.append(emotion)
            
            print(emotion)

        # Display the resulting frame
        cv2.imshow('Real-time Emotion Detection', frame)
        
        frame_count += 1

        if frame_count >= 50:
            break
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    emotion_counter = Counter(detected)
    mce = emotion_counter.most_common(1)[0][0]
    print("the most common: ", mce)

    if mce == "happy":
        em = 10
    elif mce == "sad":
        em = 0
    elif mce == "fear":
        em = 2
    elif mce == "angry":
        em = 2
    elif mce == "disgust":
        em = 2
    elif mce == "neutral":
        em = 5
    elif mce == "surprise":
        em = 7


    # Release the capture and close all windows
    cap.release()
    cv2.destroyAllWindows()
    return em


@app.route('/get-emotion', methods=['GET'])
def get_emotion():
    # Call the function to detect the dominant emotion
    emotion = detect_emotion()
    # Store emotion in MongoDB
    # mongo.db.emotions.insert_one({
    #     "user_id": user_id,
    #     "emotion": emotion,
    #     "timestamp": timestamp
    # })
    # Return the result as a JSON response
    return jsonify({"dominant_emotion": emotion})

    


if __name__ == '__main__':
    app.run(debug=True)

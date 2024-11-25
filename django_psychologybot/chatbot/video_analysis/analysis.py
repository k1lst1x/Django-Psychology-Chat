import dlib
from PIL import Image
import cv2
import json
from os import listdir, remove
from os.path import join
import random
import requests


API_TOKEN = '0d8068e8c7ae4e2d855e8f9da83665bf'


def extract_faces(video_path, output_dir):
    detector = dlib.get_frontal_face_detector()

    print('Video path: ', video_path)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray_frame)

        for i, face in enumerate(faces):
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            face_img = frame[y:y+h, x:x+w]
            Image.fromarray(face_img).save(f"{output_dir}/face_{frame_count}_{i}.jpg")

        frame_count += 1

    cap.release()

    chosen_images = choose_images(output_dir)

    return process_images(chosen_images)


def choose_images(output_dir):
    all_images = [jpg_file for jpg_file in listdir(output_dir) if jpg_file.endswith('.jpg')]
    selected_images = random.sample(all_images, 3)

    for image_name in all_images:
        if image_name not in selected_images:
            remove(join(output_dir, image_name))

    chosen_images = []
    for selected_image_name in selected_images:
        selected_image_path = join(output_dir, selected_image_name)
        # selected_image = Image.open(selected_image_path)

        chosen_images.append(selected_image_path)

    return chosen_images


def process_images(images):
    emotion_responses = []

    for image_file in images:
        files = {
            "photo": open(image_file, "rb"),
        }
        # Endpoint URL
        url = "https://api.luxand.cloud/photo/emotions"

        # Request headers
        headers = {
            "token": API_TOKEN,
        }
        # Making the POST request
        response = requests.request("POST", url, headers=headers, files=files)

        print('Text: ', response.text)

        emotion_responses.append(response.text.encode('utf8'))

    return emotion_responses
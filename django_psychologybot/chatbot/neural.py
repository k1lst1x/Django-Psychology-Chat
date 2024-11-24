import os

# Set cache directories for XDG and Hugging Face Hub
os.environ['XDG_CACHE_HOME'] = '/home/msds2023/jlegara/.cache'
os.environ['HUGGINGFACE_HUB_CACHE'] = '/home/msds2023/jlegara/.cache'

import torch

# Set device to GPU if available, otherwise use CPU
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
from tqdm.notebook import tqdm

from moviepy.editor import VideoFileClip, ImageSequenceClip

import torch
from facenet_pytorch import (MTCNN)

from transformers import (AutoFeatureExtractor,
                          AutoModelForImageClassification,
                          AutoConfig)
                             
from PIL import Image, ImageDraw



# Initialize MTCNN model for single face cropping
mtcnn = MTCNN(
    image_size=160,
    margin=0,
    min_face_size=200,
    thresholds=[0.6, 0.7, 0.7],
    factor=0.709,
    post_process=True,
    keep_all=False,
    device=device
)
    
# Load the pre-trained model and feature extractor
extractor = AutoFeatureExtractor.from_pretrained(
    "trpakov/vit-face-expression"
)
model = AutoModelForImageClassification.from_pretrained(
    "trpakov/vit-face-expression"
)  


def load_video():
    scene = 'White Chicks - short.mp4'
    clip = VideoFileClip(scene)

    # Save video frames per second
    vid_fps = clip.fps

    # Get the video (as frames)
    video = clip.without_audio()

    return np.array(list(video.iter_frames()))


def detect_emotions(image):
    """
    Detect emotions from a given image.
    Returns a tuple of the cropped face image and a
    dictionary of class probabilities.
    """
    temporary = image.copy()

    # Detect faces in the image using the MTCNN group model
    sample = mtcnn.detect(temporary)
    if sample[0] is not None:
        box = sample[0][0]

        # Crop the face
        face = temporary.crop(box)

        # Pre-process the face
        inputs = extractor(images=face, return_tensors="pt")

        # Run the image through the model
        outputs = model(**inputs)

        # Apply softmax to the logits to get probabilities
        probabilities = torch.nn.functional.softmax(outputs.logits,
                                                    dim=-1)

        # Retrieve the id2label attribute from the configuration
        config = AutoConfig.from_pretrained(
            "trpakov/vit-face-expression"
        )
        id2label = config.id2label

        # Convert probabilities tensor to a Python list
        probabilities = probabilities.detach().numpy().tolist()[0]

        # Map class labels to their probabilities
        class_probabilities = {
            id2label[i]: prob for i, prob in enumerate(probabilities)
        }

        return face, class_probabilities
    return None, None


video_data = load_video()
frame = video_data[10]  # choosing the 10th frame

# Convert the frame to a PIL image and display it
image = Image.fromarray(frame)
detect_emotions(image)

# Choose a frame
frame = video_data[40]  # choosing the 40th frame

# Convert the frame to a PIL image and display it
image = Image.fromarray(frame)
detect_emotions(image)
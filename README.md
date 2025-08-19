# Reflex
### AI Game Event Detector

[![Python Version][python-shield]][python-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

An AI that watches your game to auto-detect kills and wins, saving your best moments as video clips.

<br/>
<p align="center">
  <img src="https://i.imgur.com/your_project_demo.gif" alt="Project Demo">
</p>
<br/>

## About The Project

Every gamer knows the frustration of making an incredible play, only to realize they weren't recording. **Reflex** is a smart, AI-powered tool designed to solve that problem by acting as your personal, automated cameraman. You focus on playing the game; Reflex focuses on capturing your best moments.

Leveraging the power of computer vision, Reflex monitors your screen in real-time without interfering with your gameplay. It uses a custom-trained Convolutional Neural Network (CNN) to instantly recognize specific in-game events. When the AI detects a key moment with high confidence, it automatically triggers an action, such as saving the last 30 seconds of gameplay footage to your hard drive.

This project is built to be game-agnostic—by simply learning to recognize pixels on the screen, it can be trained to work with virtually any video game.

### Key Features:

* **Real-time Event Detection:** Uses a lightweight CNN to analyze the screen live with minimal performance impact.
* **Automatic Clipping:** Can be configured to automatically save video clips of highlights the moment they happen.
* **Game Agnostic:** Works with any game by training the model on new visual cues from the screen.
* **Fully Customizable:** Train it to recognize any event you want: kills, deaths, level-ups, rare item drops, round wins, and more.
* **Open Source & Extendable:** Built with Python, making it easy for others to contribute or adapt.

### Technology Stack

* **Language:** `Python`
* **Machine Learning:** `TensorFlow (Keras)` / `PyTorch`
* **Computer Vision:** `OpenCV`
* **Screen Capture:** `MSS`, `Pillow`
* **Numerical Processing:** `NumPy`
* **Video Handling:** `MoviePy` (for clipping)

## Getting Started

To run this project, you will need the following software installed on your machine.

### Prerequisites

* Python 3.8 or higher
* pip package manager
* All required Python packages can be installed from `requirements.txt` via:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

The project operates in three main stages: data collection, model training, and real-time detection.

### 1. Data Collection

First, you need to collect image samples for the events you want to detect (the "positive" class) and for normal gameplay (the "negative" class).

Run the data collection script, specifying a label and the number of images to capture. You will be prompted to position a capture window over the relevant part of your screen.

```sh
# Collect 200 samples of a 'kill' event
python collect_data.py --label kill --count 200

# Collect 500 samples of 'no_event' for the negative class
python collect_data.py --label no_event --count 500

## Badges
[python-shield]: https://img.shields.io/badge/Python-3.8+-blue.svg
[python-url]: https://www.python.org/
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/keerthan-kodi-48209931b/


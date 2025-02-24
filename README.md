# Music Motivator

A desktop application that motivates you by playing music as a reward for completing lessons, guided exercises, and unit labs. The app calculates a “minutes bank” based on your progress and uses it to control music playback. As you work through your lessons, exercises, and labs, you earn minutes which are then consumed while you listen to your favorite tracks.

## Features

- **Progress Tracking:**  
  - Earn minutes by completing additional lessons (5 minutes each), guided exercises (10 minutes each), and unit labs (20 minutes each).  
  - The progress (including total lessons, exercises, labs, and minutes bank) is automatically saved to a JSON file (`progress.json`).

- **Music Playback:**  
  - Load a playlist of `.mp3` files from a folder.  
  - Supports three playback modes: **Normal**, **Shuffle**, and **Repeat**.  
  - Control playback with options to play, pause, resume, and stop.

- **Automatic Timer:**  
  - While a song is playing, the application automatically decreases the minutes bank in real time.  
  - If the minutes run out, the music playback stops.

## Dependencies

- **Python 3.x**  
- **Tkinter:** Comes bundled with most Python installations.  
- **Pygame:** Used for audio playback.

## **If you want to skip all the steps and are on Linux, just do ./songs (on linux) after downloading and unzipping the release**
## **This method does not require python or any dependencies**
## **On windows, use the .exe file (click on it). Both are zipped files recognizable by their names. You must unzip them to use**
## **All methods shown are known to work on Linux Debian 12**
## **If you are on linux debian and you want a destop install, run sudo dpkg -i fileName.deb**

## Installation

1. **Clone or download the repository.**

2. **Install the required Python packages:**  
   Open a terminal or command prompt and run:
   ```bash
   pip install pygame
   ```

3. **Ensure you have a working installation of Python 3 and Tkinter.**  
   (Tkinter is typically included with standard Python distributions.)

## Usage

1. **Run the application:**  
   In the terminal, navigate to the project directory and run:
   ```bash
   python <filename>.py
   ```
   Replace `<filename>.py` with the name of the Python file containing the code (for example, `music_motivator.py`).

2. **Add Progress:**  
   - Enter the number of additional lessons, guided exercises, and unit labs completed into their respective fields.  
   - Click the **Add Minutes** button to update your minutes bank.

3. **Load a Playlist:**  
   - Click **Load Playlist from Folder** to select a folder containing your `.mp3` files.  
   - A message will confirm the number of songs loaded.

4. **Control Playback:**  
   - Click **Play Song** to start playing a track if you have sufficient minutes.  
   - Use **Pause**, **Resume**, and **Stop Song** to control playback.  
   - Select a playback mode (Normal, Shuffle, Repeat) from the dropdown to change how the playlist is played.

5. **Progress Persistence:**  
   - Your progress is automatically saved to `progress.json` in the same directory as the script and is loaded the next time you run the application.

## File Structure

```
├── progress.json        # File for saving user progress (automatically generated)
├── <filename>.py        # Main Python script for the Music Motivator application
└── README.md            # This file
```

## Customization

- **Adjusting Minute Calculations:**  
  The function `calculate_minutes(lessons, exercises, labs)` determines how many minutes you earn for each completed activity. Modify the multipliers if you’d like to adjust the rewards.

- **Extending Playback Features:**  
  The code uses Pygame’s mixer module for audio playback. You can extend this functionality (e.g., adding volume control or additional playback options) by referring to the [Pygame documentation](https://www.pygame.org/docs/).

## License

This project is provided "as is" without warranty of any kind. Feel free to modify and use the code for personal or educational purposes.

## Acknowledgements

- **Tkinter:** For building the GUI.  
- **Pygame:** For handling the music playback functionality.

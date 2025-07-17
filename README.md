# turn_table

This Python script creates a customizable **turntable setup** inside Autodesk Maya. It's designed for artists and technical directors who want to showcase their 3D assets using a rotating camera with optional lights and background.

---

## 🎯 Features

- Custom Start and End Time for animation
- Optional creation of:
  - Three-point lighting (Key, Fill, Back)
  - Background Floor
- Choose Camera Rotation Direction (Clockwise / Counter-Clockwise)
- Adjustable Turntable Radius using slider
- Automatic camera rig setup with motion path and aim constraint

---

## 🛠 Requirements

- Autodesk Maya (2018 or newer)
- Python 3 (default in Maya 2022+)
- Maya must be launched with GUI (not standalone mode)

---

## 🚀 How to Use

1. Open Maya.
2. Open the Script Editor (Python tab).
3. Copy and paste the contents of `turntable.py` into a new Python tab.
4. Run the script.

A GUI window named **"Turn Table"** will appear with the following options:

- **Start Time / End Time**: Animation frame range
- **Create Lighting**: Adds three-point light setup
- **Create Floor**: Adds a floor plane under the object
- **Camera Rotation Direction**: Choose Clockwise or Counter-Clockwise
- **Radius of Pivot**: Distance from the object to the camera

Click **"Create Turntable"** to build the setup.

---

## 📁 File Structure

```plaintext
turntable.py        # Main Python script to create the GUI and setup
README.md           # Documentation file

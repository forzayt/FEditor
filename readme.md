# 🎬 FFmpeg Clip Tool (Python GUI)

A lightweight, high-performance video clipping tool built with **Python + PyQt5 + FFmpeg**.
Designed for creators who need **fast, lossless video extraction** without using heavy editing software.

---

## 🚀 Features

### ⚡ Lossless Video Cutting

* Uses FFmpeg `-c copy` (no re-encoding)
* **Zero quality loss**
* Processes large files (e.g., 7GB) in seconds

### 🎯 Precise Clip Extraction

* Define start and end timestamps
* Extract only the required segment

### 🔊 Multi-Audio Support

* Detects all available audio streams
* Lets you manually select the correct track (e.g., English 5.1)

### 🖼️ Video Preview

* Automatically generates a **random frame preview**
* Helps verify correct file selection visually

### 💾 Save As Dialog

* Choose output location and filename before processing

### 🖥️ Fullscreen UI

* Opens in maximized mode for better usability

---

## 🧱 Tech Stack

* **Python 3**
* **PyQt5** (GUI framework)
* **FFmpeg** (video processing engine)

---

## 📦 Installation

### 1. Install Python dependencies

```bash
pip install PyQt5
```

---

### 2. Install FFmpeg

Download from:
👉 https://www.gyan.dev/ffmpeg/builds/

Steps:

1. Extract the archive
2. Add the `bin` folder to your system **PATH**
3. Verify installation:

```bash
ffmpeg -version
```

---

## ▶️ Usage

Run the application:

```bash
python main.py
```

---

## 🛠️ How It Works

1. **Select Video File**

   * Loads metadata and detects audio streams
   * Generates a preview thumbnail

2. **Enter Timestamps**

   * Format: `HH:MM:SS`
   * Example:

     ```
     Start: 00:27:00
     End:   00:31:00
     ```

3. **Choose Audio Track**

   * Select the correct stream (e.g., English)

4. **Click "Cut Clip"**

   * Choose output location
   * Clip is generated instantly

---

## ⚙️ Core FFmpeg Command

```bash
ffmpeg -ss START -to END -i input.mkv -map 0:v -map 0:a -c copy output.mp4
```

### Explanation:

* `-ss` → Start time
* `-to` → End time
* `-map` → Select streams (video + chosen audio)
* `-c copy` → No re-encoding (lossless)

---

## 📌 Key Advantages

* ⚡ **Extremely fast** (no rendering)
* 🎥 **No quality degradation**
* 🧩 Simple and focused (not a bloated editor)
* 📂 Ideal for **YouTube clip workflows**

---

## ⚠️ Known Limitations

* Cuts are aligned to **keyframes**

  * May be off by a few seconds
* No timeline scrubbing (yet)
* Audio selection is manual (auto-detect coming soon)

---

## 🔮 Future Improvements

* ✅ Auto-select best English audio (ignore descriptive tracks)
* 🎚️ Timeline slider with preview scrubbing
* 📊 Batch processing (multiple clips)
* 🧠 Smart naming system
* 🎞️ Frame-accurate cutting (optional re-encode mode)

---

## 🧠 Design Philosophy

This tool is **not a video editor**.

It is a:

> ⚙️ Precision clip extraction utility built on top of FFmpeg

Focused on:

* Speed
* Simplicity
* Scalability

---

## 🤝 Contributing

Feel free to:

* Suggest features
* Improve UI/UX
* Optimize FFmpeg handling

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Built for high-efficiency video clipping workflows.

---

## ⭐ If you find this useful

Give it a star ⭐ and improve your video workflow.

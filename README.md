# 🤖 Video Clip Agent

Automatically analyze videos, detect interesting moments, cut clips, and save them - all for FREE!

## ✨ Features

✅ **Analyze Motion** - Detects high-motion scenes (interesting moments)  
✅ **Cut Clips** - Splits video into 30-second clips (customizable)  
✅ **Save Files** - Exports ready-to-upload MP4 files  
✅ **100% Free** - No subscriptions or API costs  
✅ **Windows/Mac/Linux** - Works everywhere  

---

## 🚀 Quick Start (5 minutes)

### Step 1: Install FFmpeg (Windows)

FFmpeg is a free tool needed to cut videos. Choose ONE method:

**Method A: Using Chocolatey (if you have it)**
```bash
choco install ffmpeg
```

**Method B: Manual Download**
1. Go to: https://ffmpeg.org/download.html
2. Download Windows build
3. Extract to a folder
4. Add to PATH (Google "add ffmpeg to PATH Windows")

**Method C: Test if you already have it**
```bash
ffmpeg -version
```
If it shows version → You're good! Skip to Step 2.

---

### Step 2: Install Python Dependencies

Open Command Prompt (Windows) and run:

```bash
# Navigate to your project folder
cd path\to\Dheeraj

# Install required packages
pip install -r requirements.txt
```

Example:
```bash
cd C:\Users\YourName\Documents\Dheeraj
pip install -r requirements.txt
```

---

### Step 3: Run the Agent

```bash
python main.py
```

**It will ask:**
```
📹 Enter path to your video file: C:\Videos\myvideo.mp4
⏱️  Enter clip duration in seconds (default 30): 30
```

Then it will:
1. 🔍 Analyze the video for interesting moments
2. ✂️ Cut it into 30-second clips
3. 💾 Save all clips to a `clips/` folder
4. ⭐ Show you the top interesting moments

---

## 📋 Example

```bash
C:\Dheeraj> python main.py

📹 Enter path to your video file: C:\Downloads\video.mp4
⏱️  Enter clip duration in seconds (default 30): 30

==================================================
🤖 VIDEO CLIP AGENT STARTED
==================================================

📹 Video Info:
   Duration: 120.50 seconds
   FPS: 30
   Resolution: 1920x1080
   Total Frames: 3615

🔍 Analyzing motion in video...
✅ Found 8 interesting scenes

✂️  Cutting video into 30-second clips...
✅ Created 4 clips

💾 Saving clips...
   ✅ Saved: clip_001.mp4 (30.00s)
   ✅ Saved: clip_002.mp4 (30.00s)
   ✅ Saved: clip_003.mp4 (30.00s)
   ✅ Saved: clip_004.mp4 (30.10s)

⭐ INTERESTING CLIPS (High Motion):
   - 10.25s to 15.80s
   - 32.10s to 38.50s
   - 65.20s to 72.30s

✅ All clips saved to: C:\Dheeraj\clips\

==================================================
```

---

## 📁 Output

All clips are saved in the `clips/` folder:
```
clips/
├── clip_001.mp4
├── clip_002.mp4
├── clip_003.mp4
└── clip_004.mp4
```

Ready to upload to YouTube or Instagram! 🎥

---

## ⚙️ Troubleshooting

### **Problem: "ffmpeg not found"**
- Solution: Install FFmpeg (see Step 1)
- The script will automatically fall back to slower method, but it will still work

### **Problem: "ModuleNotFoundError: No module named 'cv2'"**
- Solution: Run `pip install -r requirements.txt` again
- Make sure you're in the correct folder

### **Problem: Video file not found**
- Solution: Use full path, example: `C:\Users\YourName\Downloads\video.mp4`
- Or copy video to `clips/` folder and just type: `video.mp4`

### **Problem: Slow processing**
- This is normal for large videos (1GB+)
- Let it run, it will complete
- Tip: Use shorter test videos first (30 seconds)

---

## 🎯 Next Steps

Once you have clips, you can:
1. **Upload to YouTube** - Use YouTube Studio (free)
2. **Upload to Instagram** - Use Reels (free)
3. **Edit more** - Use free tool like CapCut
4. **Automate upload** - I can help with that next!

---

## 📚 What's Happening Inside?

1. **Motion Detection** - Compares frames to find action
2. **Scene Segmentation** - Groups similar moments together
3. **Video Cutting** - Uses FFmpeg to split into clips
4. **File Export** - Saves MP4 files ready to upload

---

## 💡 Pro Tips

- **Test with small video first** (30 seconds)
- **Adjust motion threshold** in code if clips are boring (change `threshold=25` to lower number like `15`)
- **Change clip duration** - Enter different seconds at runtime
- **Run multiple times** on same video with different settings

---

## 🆘 Need Help?

If something breaks:
1. Copy the error message
2. Check Troubleshooting section
3. Make sure Python and FFmpeg are installed
4. Run from Command Prompt (not from folder)

---

**Happy clipping! 🎬**

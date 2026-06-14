import cv2
import numpy as np
import os
from pathlib import Path
import subprocess

class VideoClipAgent:
    def __init__(self, video_path, output_folder="clips", clip_duration=30):
        """
        Initialize the Video Clip Agent
        
        Args:
            video_path: Path to input video file
            output_folder: Folder to save clips
            clip_duration: Duration of each clip in seconds
        """
        self.video_path = video_path
        self.output_folder = output_folder
        self.clip_duration = clip_duration
        
        # Create output folder if it doesn't exist
        Path(self.output_folder).mkdir(exist_ok=True)
        
        # Open video
        self.cap = cv2.VideoCapture(video_path)
        
        if not self.cap.isOpened():
            print(f"❌ Error: Cannot open video file: {video_path}")
            exit(1)
        
        # Get video properties
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.duration = self.frame_count / self.fps
        
        print(f"\n📹 Video Info:")
        print(f"   Duration: {self.duration:.2f} seconds")
        print(f"   FPS: {self.fps}")
        print(f"   Resolution: {self.width}x{self.height}")
        print(f"   Total Frames: {self.frame_count}")
    
    def detect_motion(self, threshold=30):
        """
        Detect scenes with high motion (interesting moments)
        Returns list of (start_frame, end_frame) tuples
        """
        print(f"\n🔍 Analyzing motion in video...")
        
        interesting_scenes = []
        prev_frame = None
        motion_frames = []
        
        frame_idx = 0
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Resize for faster processing
            frame_small = cv2.resize(frame, (320, 240))
            gray = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                # Calculate difference between frames
                diff = cv2.absdiff(prev_frame, gray)
                motion = np.sum(diff) / (320 * 240)
                
                if motion > threshold:
                    motion_frames.append(frame_idx)
            
            prev_frame = gray
            frame_idx += 1
        
        # Group consecutive motion frames into scenes
        if motion_frames:
            scene_start = motion_frames[0]
            prev_frame_idx = motion_frames[0]
            
            for frame_idx in motion_frames[1:]:
                # If gap > 1 second, it's a new scene
                if frame_idx - prev_frame_idx > self.fps:
                    interesting_scenes.append((scene_start, prev_frame_idx))
                    scene_start = frame_idx
                prev_frame_idx = frame_idx
            
            # Add last scene
            interesting_scenes.append((scene_start, prev_frame_idx))
        
        print(f"✅ Found {len(interesting_scenes)} interesting scenes")
        
        # Reset video to beginning
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        return interesting_scenes
    
    def cut_video_into_clips(self):
        """
        Cut video into fixed duration clips
        """
        print(f"\n✂️  Cutting video into {self.clip_duration}-second clips...")
        
        clips = []
        clip_frame_duration = int(self.clip_duration * self.fps)
        
        for i in range(0, self.frame_count, clip_frame_duration):
            start_frame = i
            end_frame = min(i + clip_frame_duration, self.frame_count)
            clips.append((start_frame, end_frame))
        
        print(f"✅ Created {len(clips)} clips")
        return clips
    
    def save_clips(self, clips, clip_names):
        """
        Save clips to files using ffmpeg
        
        Args:
            clips: List of (start_frame, end_frame) tuples
            clip_names: List of output file names
        """
        print(f"\n💾 Saving clips...")
        
        for idx, (start_frame, end_frame) in enumerate(clips):
            output_path = os.path.join(self.output_folder, clip_names[idx])
            
            # Calculate time in seconds
            start_time = start_frame / self.fps
            duration = (end_frame - start_frame) / self.fps
            
            # Use ffmpeg to extract clip (faster than opencv)
            try:
                cmd = [
                    'ffmpeg',
                    '-i', self.video_path,
                    '-ss', str(start_time),
                    '-t', str(duration),
                    '-c:v', 'libx264',
                    '-c:a', 'aac',
                    '-y',
                    output_path
                ]
                
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"   ✅ Saved: {clip_names[idx]} ({duration:.2f}s)")
            
            except FileNotFoundError:
                print(f"   ⚠️  ffmpeg not found. Using opencv instead...")
                self.save_clip_opencv(start_frame, end_frame, output_path)
    
    def save_clip_opencv(self, start_frame, end_frame, output_path):
        """
        Fallback method to save clip using OpenCV
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        for _ in range(end_frame - start_frame):
            ret, frame = self.cap.read()
            if ret:
                out.write(frame)
        
        out.release()
    
    def run(self):
        """
        Run the complete pipeline:
        1. Cut video into clips
        2. Detect interesting moments
        3. Save all clips
        """
        print("\n" + "="*50)
        print("🤖 VIDEO CLIP AGENT STARTED")
        print("="*50)
        
        # Step 1: Cut video into clips
        clips = self.cut_video_into_clips()
        
        # Step 2: Detect interesting moments
        interesting_scenes = self.detect_motion(threshold=25)
        
        # Step 3: Create clip names
        clip_names = [f"clip_{i+1:03d}.mp4" for i in range(len(clips))]
        
        # Step 4: Save clips
        self.save_clips(clips, clip_names)
        
        # Step 5: Highlight interesting clips
        print(f"\n⭐ INTERESTING CLIPS (High Motion):")
        if interesting_scenes:
            for start_frame, end_frame in interesting_scenes[:5]:  # Show top 5
                start_sec = start_frame / self.fps
                end_sec = end_frame / self.fps
                print(f"   - {start_sec:.2f}s to {end_sec:.2f}s")
        else:
            print(f"   No high-motion scenes detected. Try lowering threshold in code.")
        
        print(f"\n✅ All clips saved to: {os.path.abspath(self.output_folder)}/")
        print("="*50)
        
        self.cap.release()


if __name__ == "__main__":
    # USER INPUT SECTION
    # ==================
    
    video_file = input("\n📹 Enter path to your video file: ").strip()
    
    if not os.path.exists(video_file):
        print(f"❌ File not found: {video_file}")
        exit(1)
    
    # Optional: Custom clip duration
    try:
        duration = int(input("⏱️  Enter clip duration in seconds (default 30): ").strip() or "30")
    except:
        duration = 30
    
    # Create agent and run
    agent = VideoClipAgent(
        video_path=video_file,
        output_folder="clips",
        clip_duration=duration
    )
    
    agent.run()

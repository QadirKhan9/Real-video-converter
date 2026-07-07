import os
import subprocess
import sys
import re
import imageio_ffmpeg

def parse_time(time_str):
    """Parses HH:MM:SS.ms string to seconds (float)"""
    try:
        parts = time_str.split(':')
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    except Exception:
        return 0.0

def convert_mkv_to_mp4(input_file, output_file=None):
    """Converts an MKV file to MP4 using H.264/AAC for TV compatibility."""
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.mp4'
    
    # We will pass -y to ffmpeg so it automatically overwrites the file instead
    # of skipping it, so you can restart the conversion securely!
    
    print(f"\nStarting conversion: '{input_file}' -> '{output_file}'")
    
    # Get the FFmpeg executable from imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    # Translate video to H.264 (AVC) and audio to AAC, which are supported by almost all TVs.
    # -preset fast makes it go a bit faster.
    # Use -y to overwrite if the user accidentally has a leftover file.
    command = [
        ffmpeg_exe, '-y', '-i', input_file, 
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '23', 
        '-c:a', 'aac', '-b:a', '192k', 
        output_file
    ]
    
    print("Preparing conversion (parsing video duration)...")
    
    total_duration = 0.0
    duration_regex = re.compile(r"Duration: (\d{2}:\d{2}:\d{2}\.\d{2})")
    time_regex = re.compile(r"time=(\d{2}:\d{2}:\d{2}\.\d{2})")

    try:
        # Use Popen to read stderr line by line since ffmpeg logs there
        process = subprocess.Popen(
            command,
            stderr=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            universal_newlines=True,
            encoding='utf-8', 
            errors='replace'
        )
        
        for line in process.stderr:
            # 1. Look for duration if we haven't found it yet
            if total_duration == 0.0:
                match_duration = duration_regex.search(line)
                if match_duration:
                    total_duration = parse_time(match_duration.group(1))
                    print(f"Total video duration: {match_duration.group(1)}")
            
            # 2. Look for current time update
            match_time = time_regex.search(line)
            if match_time and total_duration > 0.0:
                current_time = parse_time(match_time.group(1))
                percent = (current_time / total_duration) * 100
                
                # Draw a simple progress bar
                bar_len = 30
                filled_len = int(round(bar_len * percent / 100))
                # Prevent overflow if percent goes slightly above 100%
                filled_len = min(filled_len, bar_len)
                percent = min(percent, 100.0)
                
                bar = '#' * filled_len + '-' * (bar_len - filled_len)
                
                # Write to stdout with \r to overwrite line
                sys.stdout.write(f"\rProgress: [{bar}] {percent:.1f}%")
                sys.stdout.flush()

        process.wait()
        
        # Print a newline and completion message when done
        if process.returncode == 0:
            print(f"\n\nSuccessfully created '{output_file}'!")
        else:
            print(f"\n\nError converting '{input_file}'. Return code: {process.returncode}")

    except Exception as e:
        print(f"\nFailed to run FFmpeg: {e}")

def main():
    # If files are passed as arguments via terminal
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.lower().endswith('.mkv'):
                convert_mkv_to_mp4(arg)
            else:
                print(f"Skipping '{arg}': not an MKV file.")
    else:
        # Scan current directory for MKV files
        mkv_files = [f for f in os.listdir('.') if f.lower().endswith('.mkv')]
        
        if not mkv_files:
            print("No .mkv files found in the current directory.")
            return
            
        print(f"Found {len(mkv_files)} MKV file(s). Starting...")
        for mkv in mkv_files:
            convert_mkv_to_mp4(mkv)

if __name__ == "__main__":
    main()

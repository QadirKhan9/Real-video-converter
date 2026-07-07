import os
import re
import subprocess
import sys
import imageio_ffmpeg


def get_next_output_name():
    existing_numbers = set()

    for file in os.listdir():
        if file.lower().endswith(".mkv"):
            name = os.path.splitext(file)[0]
            if name.isdigit():
                existing_numbers.add(int(name))

    number = 1
    while number in existing_numbers:
        number += 1

    return f"{number}.mkv"


def parse_time(time_str):
    try:
        parts = time_str.split(':')
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    except Exception:
        return 0.0


def convert_mp4_to_mkv(input_file, output_file=None):
    if output_file is None:
        output_file = get_next_output_name()
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    print(f"Converting: {input_file} -> {output_file}")

    command = [
        ffmpeg_exe,
        "-y",
        "-i", input_file,
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "medium",
        "-c:a", "aac",
        "-b:a", "192k",
        output_file,
    ]

    try:
        process = subprocess.Popen(
            command,
            stderr=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            universal_newlines=True,
            encoding='utf-8',
            errors='replace'
        )

        total_duration = 0.0
        duration_regex = re.compile(r"Duration:\s+(\d{2}:\d{2}:\d{2}\.\d{2})")
        time_regex = re.compile(r"time=(\d{2}:\d{2}:\d{2}\.\d{2})")

        for line in process.stderr:
            if total_duration == 0.0:
                match_duration = duration_regex.search(line)
                if match_duration:
                    total_duration = parse_time(match_duration.group(1))
                    print(f"Total duration: {match_duration.group(1)}")

            match_time = time_regex.search(line)
            if match_time and total_duration > 0.0:
                current_time = parse_time(match_time.group(1))
                percent = min(100.0, (current_time / total_duration) * 100 if total_duration else 0.0)
                bar_len = 30
                filled_len = int(bar_len * percent / 100)
                bar = "#" * filled_len + "-" * (bar_len - filled_len)
                sys.stdout.write(f"\rProgress: [{bar}] {percent:5.1f}%")
                sys.stdout.flush()

        process.wait()
        sys.stdout.write("\n")

        if process.returncode == 0:
            print(f"Converted: {input_file} -> {output_file}")
        else:
            print(f"Failed to convert '{input_file}'. Exit code: {process.returncode}")
    except Exception as e:
        print(f"Failed to convert '{input_file}': {e}")


def main():
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.lower().endswith(".mp4"):
                convert_mp4_to_mkv(arg)
            else:
                print(f"Skipping '{arg}': not an MP4 file.")
    else:
        mp4_files = [f for f in os.listdir() if f.lower().endswith(".mp4")]

        if not mp4_files:
            print("No .mp4 files found in the current directory.")
            return

        for mp4_file in mp4_files:
            convert_mp4_to_mkv(mp4_file)

    print("Done!")


if __name__ == "__main__":
    main()

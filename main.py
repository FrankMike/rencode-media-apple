import ffmpeg
from pathlib import Path
from PIL import Image


def reencode_media(source_dir, dest_dir):
        """
        Reads images and videos from source_dir, reencodes them, and saves them to dest_dir.
        """
        source_path = Path(source_dir)
        dest_path = Path(dest_dir)

        dest_path.mkdir(parents=True, exist_ok=True)

        print(f"Starting to process media from: {source_path}")
        print(f"Saving reencoded media to: {dest_path}")

        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv']
        processed_count = 0
        error_count = 0

        for item in source_path.rglob('*'):
            if not item.is_file():
                continue

            file_suffix = item.suffix.lower()
            relative_path = item.relative_to(source_path)
            new_file_path = dest_path / relative_path
            new_file_path.parent.mkdir(parents=True, exist_ok=True)

            if file_suffix in image_extensions:
                try:
                    with Image.open(item) as img:
                        img.save(new_file_path)
                        print(f"Successfully reencoded image: {new_file_path}")
                        processed_count += 1
                except Exception as e:
                    print(f"Could not process image file {item}: {e}")
                    error_count += 1
            elif file_suffix in video_extensions:
                try:
                    ffmpeg.input(item).output(str(new_file_path), vcodec='copy', acodec='copy').run(overwrite_output=True, quiet=True)
                    print(f"Successfully reencoded video: {new_file_path}")
                    processed_count += 1
                except ffmpeg.Error as e:
                    print(f"Could not process video file {item}: {e.stderr}")
                    error_count += 1

        print("\n--- Processing Complete ---")
        print(f"Successfully processed media files: {processed_count}")
        print(f"Failed to process files: {error_count}")
        print("--------------------------")


def main():
    source_directory = input("Insert the source directory: ")
    destination_directory = input("Insert the destination directory: ")

    reencode_media(source_directory, destination_directory)


if __name__ == "__main__":
    main()

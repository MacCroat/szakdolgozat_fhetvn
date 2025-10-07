import os
from PIL import Image
from typing import List

class FrameExporter:
    def __init__(self, frames_dir: str = 'graph_frames', out_dir: str = 'animated_graphs'):
        self.frames_dir = frames_dir
        self.out_dir = out_dir
        os.makedirs(self.frames_dir, exist_ok=True)
        os.makedirs(self.out_dir, exist_ok=True)
        self.frames: List[str] = []

    def add_frame(self, path: str) -> None:
        self.frames.append(path)

    def save_gif(self, filename: str) -> str:
        if not self.frames:
            raise RuntimeError("No frames to export")

        images = [Image.open(f) for f in self.frames]
        gif_path = os.path.join(self.out_dir, filename)

        images[0].save(
            gif_path,
            save_all=True,
            append_images=images[1:],
            duration=1000,
            loop=0
        )
        return gif_path

    def cleanup(self) -> None:
        try:
            for file in os.listdir(self.frames_dir):
                fp = os.path.join(self.frames_dir, file)
                if os.path.isfile(fp):
                    os.unlink(fp)
            os.rmdir(self.frames_dir)
        except Exception:
            pass
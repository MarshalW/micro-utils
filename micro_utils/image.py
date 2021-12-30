
from micro_utils.random import create_random_str
import subprocess
import shlex
import mimetypes
from pymediainfo import MediaInfo


def resize(image_path, output_path=None, resize='1920x1080^', gravity='center', extent='1920x1080'):
    if output_path is None:
        output_path = f'/tmp/{create_random_str(6)}.jpg'

    cmd = f'convert {image_path} -resize {resize} -gravity {gravity} -extent {extent} {output_path}'
    subprocess.run(shlex.split(cmd, comments=True))

    return output_path


def guess_media_type(file_path):
    return mimetypes.MimeTypes().guess_type(file_path)[
        0].split('/')[0]

def get_video_duration_ms(file_path):
    # 得到源视频时长
    media_info = MediaInfo.parse(file_path)
    return media_info.tracks[0].duration

import ffmpeg

class Clip:
    def __init__(self, path):
        self.path = path
        self.input = ffmpeg.input(path)
        self.video = self.input.video
        self.audio = self.input.audio
        self.duration = float(ffmpeg.probe(path)["format"]["duration"])
        self.dimensions = int(ffmpeg.probe(path)["streams"][0]["width"]), int(ffmpeg.probe(path)["streams"][0]["height"])

    def resize(self, width, height):
        self.dimensions = width, height
        self.video = self.video.filter("scale", width=width, height=height, force_original_aspect_ratio=1).filter("pad", width=width, height=height, x="(ow-iw)/2", y="(oh-ih)/2")

    def invert_colors(self):
        self.video = self.video.filter("negate")

    def speedx(self, factor):
        self.video = self.video.setpts(f"PTS/{factor}")
        self.audio = self.audio.filter("atempo", factor)

    def reverse(self):
        self.video = self.video.filter("reverse")
        self.audio = self.audio.filter("areverse")

    def vibrato(self, freq):
        self.audio = self.audio.filter("vibrato", f=freq)

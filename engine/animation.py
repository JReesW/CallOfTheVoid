from engine.spritesheet import SpriteSheet


class Animation:
    """
    An animation, defined by the given list of frames (spritesheet sprite names) and a frame duration, can optionally loop
    """
    
    def __init__(self, frames: list[str], frame_durations: list[float], loop=True):
        self.frames = frames
        self.frame_durations = frame_durations
        self.loop = loop

        self.current_frame = 0
        self.timer = 0
        self.finished = False

    def update(self, dt):
        """
        Update this animation
        """
        if self.finished:
            return

        self.timer += dt

        while self.timer >= self.frame_durations[self.current_frame]:
            self.timer -= self.frame_durations[self.current_frame]
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
                    break

    def get_frame(self):
        """
        Get the current frame of animation
        """
        return self.frames[self.current_frame]

    def reset(self):
        """
        Reset this animation
        """
        self.current_frame = 0
        self.timer = 0
        self.finished = False


class AnimationHandler:
    """
    Manages multiple animations in a given spritesheet
    """
    
    def __init__(self, spritesheet: SpriteSheet):
        self.spritesheet = spritesheet
        self.animations = {}
        self.current = None

        self.load()
    
    def load(self):
        """
        Load all the animations in the handler's spritesheet
        """
        for name, animation in self.spritesheet.sheet_info['animations'].items():
            self.animations[name] = Animation(animation['frames'], animation['frameDurations'], animation['loops'])
            if self.spritesheet.sheet_info['flipAll']:
                self.animations[name + 'F'] = Animation([frame + 'F' for frame in animation['frames']], animation['frameDurations'], animation['loops'])

    def play(self, name, flip=False):
        """
        Play an animation given by name
        """
        if flip:
            name += 'F'
        if self.current != name:
            self.current = name
            self.animations[name].reset()

    def update(self, dt):
        """
        Update the currenty playing animation
        """
        if self.current:
            self.animations[self.current].update(dt)

    def get_frame(self):
        """
        Get the current frame of animation
        """
        if self.current:
            return self.spritesheet.get_sprite(self.animations[self.current].get_frame())

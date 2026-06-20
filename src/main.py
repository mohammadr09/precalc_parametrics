from manim import * # type: ignore

from scene.hook import hook_scene_display
from scene.parametric_scenes import circle_demo_display

class Main(Scene):
    def construct(self):
        hook_scene_display(self)
        self.clear()

        # circle_demo_display(self)

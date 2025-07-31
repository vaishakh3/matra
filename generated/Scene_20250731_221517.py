from manim import *

class Scene_20250731_221517(Scene):
    def construct(self):
        eq1 = Text("E = mc", font_size=72)
        self.play(Write(eq1))
        self.wait(2)
        self.play(FadeOut(eq1))
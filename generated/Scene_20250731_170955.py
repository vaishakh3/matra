from manim import *

class Scene_20250731_170955(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-2*PI, 2*PI],
            y_range=[-1.5, 1.5],
            x_axis_config={"include_tip": False},
            y_axis_config={"include_tip": False},
        )
        graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        label = Text("Sine Wave").next_to(axes, UP)
        self.play(Create(axes), Create(label))
        self.play(Create(graph))
        self.wait()
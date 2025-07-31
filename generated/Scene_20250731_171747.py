from manim import *

class Scene_20250731_171747(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-4 * PI, 4 * PI, PI],
            y_range=[-1.5, 1.5, 1],
            x_length=8,
            y_length=4,
            color=WHITE,
            axis_config={"include_tip": False}
        )
        self.add(axes)
        graph = axes.plot(lambda x: np.cos(x), x_range=[-4 * PI, 4 * PI], color=BLUE)
        self.play(Create(graph), run_time=2)
        label = axes.get_axis_labels(Text("x"), Text("cos(x)"))
        self.play(Create(label), run_time=1)
        self.wait(2)
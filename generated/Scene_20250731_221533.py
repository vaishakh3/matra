from manim import *

class Scene_20250731_221533(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-1, 7, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=8,
            y_length=3,
            axis_tip_length=0.2
        )
        labels = ax.get_axis_labels(x_label=Text("x"), y_label=Text("y"))

        sine_graph = ax.plot(lambda x: np.sin(x), x_range=[0, 3 * PI], color=BLUE)
        cos_graph = ax.plot(lambda x: np.cos(x), x_range=[0, 3 * PI], color=GREEN)

        sine_label = Text("sin(x)").scale(0.6).next_to(sine_graph, UP)
        cos_label = Text("cos(x)").scale(0.6).next_to(cos_graph, DOWN)

        moving_line = Line(start=ax.c2p(0, -1.5), end=ax.c2p(0, 1.5), color=RED)

        def update_line(line, alpha):
            x_val = alpha * 3 * PI
            line.move_to(ax.c2p(x_val, 0))
            return line

        self.play(Create(ax), Write(labels))
        self.play(Create(sine_graph), Create(cos_graph))
        self.play(Write(sine_label), Write(cos_label))
        self.play(Create(moving_line))
        self.play(UpdateFromAlphaFunc(moving_line, update_line), run_time=5)
        self.wait(2)
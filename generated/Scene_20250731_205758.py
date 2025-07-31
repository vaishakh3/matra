from manim import *

class Scene_20250731_205758(Scene):
    def construct(self):
        title = Text("Electromagnetic Wave")
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        axes = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1])
        self.play(Create(axes))

        wave1 = ParametricFunction(lambda t: np.array([t, np.sin(t), 0]), t_range=[-4, 4])
        wave2 = ParametricFunction(lambda t: np.array([t, 0, np.cos(t)]), t_range=[-4, 4])
        self.play(Create(wave1), Create(wave2))

        electric_field = Arrow3D(start=np.array([-3, 0, 0]), end=np.array([-3, np.sin(-3), 0]), color=RED)
        magnetic_field = Arrow3D(start=np.array([-3, 0, 0]), end=np.array([-3, 0, np.cos(-3)]), color=BLUE)
        self.play(Create(electric_field), Create(magnetic_field))

        self.wait(1)

        self.play(
            wave1.animate.set_color(YELLOW),
            wave2.animate.set_color(GREEN),
            electric_field.animate.become(Arrow3D(start=np.array([3, 0, 0]), end=np.array([3, np.sin(3), 0]), color=RED)),
            magnetic_field.animate.become(Arrow3D(start=np.array([3, 0, 0]), end=np.array([3, 0, np.cos(3)]), color=BLUE)),
            rate_func=linear,
            run_time=3
        )

        self.wait(2)
        self.play(FadeOut(axes), FadeOut(wave1), FadeOut(wave2), FadeOut(electric_field), FadeOut(magnetic_field))
        self.wait(1)

class Arrow3D(Line):
    def __init__(self, start, end, color=WHITE, **kwargs):
        super().__init__(start, end, color=color, **kwargs)
        self.add_tip(tip_length=0.2, at_start=False)
        self.add_tip(tip_length=0.2, at_start=True)
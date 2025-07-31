from manim import *

class Scene_20250731_221950(Scene):
    def construct(self):
        ax = Axes(x_range=[0, 10, 1], y_range=[-1.5, 1.5, 0.5])
        self.play(Create(ax))

        sine_wave = ax.plot(lambda x: np.sin(x), color=BLUE)
        self.play(Create(sine_wave))

        dot = Dot(ax.coords_to_point(0, np.sin(0)), color=RED)
        self.play(Create(dot))

        def update_dot(mob, alpha):
            x = alpha * 10  # x goes from 0 to 10
            y = np.sin(x)
            mob.move_to(ax.coords_to_point(x, y))

        self.play(UpdateFromAlphaFunc(dot, update_dot), run_time=5)

        moving_sine_wave = ax.plot(lambda x: np.sin(x + 0.5 * self.time), color=GREEN)

        self.add(moving_sine_wave)

        self.wait(2)
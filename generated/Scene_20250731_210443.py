from manim import *

class Scene_20250731_210443(Scene):
    def construct(self):
        energy = Text("E")
        mass = Text("m")
        speed_of_light = Text("c")
        equals = Text("=")
        squared = Text("")

        equation = VGroup(energy, equals, mass, speed_of_light, squared)
        equation.arrange(RIGHT)

        self.play(Write(equation))
        self.wait(2)

        energy_and_equals = VGroup(energy, equals)
        mc_squared = VGroup(mass, speed_of_light, squared)

        self.play(
            energy_and_equals.animate.shift(LEFT * 2),
            mc_squared.animate.shift(RIGHT * 2)
        )
        self.wait(1)

        einstein_text = Text("E=mc - Einstein")
        self.play(FadeIn(einstein_text))
        self.wait(2)
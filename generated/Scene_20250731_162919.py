from manim import *

class Scene_20250731_162919(Scene):
    def construct(self):
        triangle = Polygon([-3, 0, 0], [0, 4, 0], [0, 0, 0], color=WHITE)
        self.play(Create(triangle))
        a = Line([0, 0, 0], [-3, 0, 0], color=WHITE)
        b = Line([0, 0, 0], [0, 4, 0], color=WHITE)
        c = Line([-3, 0, 0], [0, 4, 0], color=WHITE)
        a_label = Text("a", font_size=24).next_to(a, DOWN)
        b_label = Text("b", font_size=24).next_to(b, LEFT)
        c_label = Text("c", font_size=24).next_to(c, UP + RIGHT)
        self.play(Create(a_label), Create(b_label), Create(c_label))
        square_a = Square(side_length=3, color=BLUE).shift(LEFT * 1.5 + DOWN * 1.5)
        square_b = Square(side_length=4, color=RED).shift(UP * 2 + RIGHT * 2)
        square_c = Square(side_length=5, color=GREEN).shift(LEFT * 2.5 + UP * 2)
        self.play(Create(square_a), Create(square_b), Create(square_c))
        a_squared = Text("a^2", font_size=24).move_to(square_a.get_center())
        b_squared = Text("b^2", font_size=24).move_to(square_b.get_center())
        c_squared = Text("c^2", font_size=24).move_to(square_c.get_center())
        self.play(Create(a_squared), Create(b_squared), Create(c_squared))
        equation = Text("a^2 + b^2 = c^2", font_size=48).shift(DOWN * 3)
        self.play(Create(equation))
        self.wait()
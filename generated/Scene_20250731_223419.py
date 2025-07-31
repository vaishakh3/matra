from manim import *

class Scene_20250731_223419(Scene):
    def construct(self):
        a = 3
        b = 4
        c = 5
        triangle = Polygon(ORIGIN, RIGHT*a, UP*b, color=BLUE)
        self.play(Create(triangle))
        self.wait()
        square_a = Square(side_length=a).next_to(triangle, DOWN)
        square_a_text = Text(str(a**2)).move_to(square_a.get_center())
        self.play(Create(square_a), Write(square_a_text))
        self.wait()
        square_b = Square(side_length=b).next_to(square_a, RIGHT)
        square_b_text = Text(str(b**2)).move_to(square_b.get_center())
        self.play(Create(square_b), Write(square_b_text))
        self.wait()
        square_c = Square(side_length=c).next_to(triangle, UP)
        square_c_text = Text(str(c**2)).move_to(square_c.get_center())
        self.play(Create(square_c), Write(square_c_text))
        self.wait()
        equation = Text(f"{a}^2 + {b}^2 = {c}^2").to_edge(DOWN)
        self.play(Write(equation))
        self.wait()
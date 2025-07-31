from manim import *

class Scene_20250731_222016(Scene):
    def construct(self):
        # Define the sides of the right triangle
        a = 3
        b = 4
        c = 5

        # Create the right triangle
        triangle = Polygon(
            ORIGIN,
            [a, 0, 0],
            [a, b, 0],
            color=BLUE,
            fill_opacity=0.5
        )

        # Label the sides
        a_label = Text("a", font_size=24).move_to([a/2, -0.3, 0])
        b_label = Text("b", font_size=24).move_to([a + 0.3, b/2, 0])
        c_label = Text("c", font_size=24).move_to([a/2, b/2, 0]).shift(RIGHT * 1.5)

        # Create the squares
        a_square = Square(side_length=a, color=RED, fill_opacity=0.5).move_to([a/2, -a/2, 0]).shift(DOWN * 1.5)
        b_square = Square(side_length=b, color=GREEN, fill_opacity=0.5).move_to([a + b/2, b/2, 0]).shift(RIGHT * 1.5)
        c_square = Square(side_length=c, color=YELLOW, fill_opacity=0.5).move_to([a/2, b/2, 0]).shift(RIGHT * 5.5)
        c_square.rotate(-np.arctan(b/a), about_point=c_square.get_center())

        a_square_label = Text("a", font_size=24).move_to(a_square.get_center())
        b_square_label = Text("b", font_size=24).move_to(b_square.get_center())
        c_square_label = Text("c", font_size=24).move_to(c_square.get_center())

        # Create the equation
        equation = MathTex("a^2 + b^2 = c^2", font_size=48).move_to([0, -3, 0])

        # Add the objects to the scene
        self.play(Create(triangle))
        self.play(Write(a_label), Write(b_label), Write(c_label))
        self.wait(0.5)
        self.play(Create(a_square), Create(b_square), Create(c_square))
        self.play(Write(a_square_label), Write(b_square_label), Write(c_square_label))
        self.wait(0.5)
        self.play(Write(equation))
        self.wait(2)

        self.play(
            FadeOut(triangle),
            FadeOut(a_label),
            FadeOut(b_label),
            FadeOut(c_label),
            FadeOut(a_square),
            FadeOut(b_square),
            FadeOut(c_square),
            FadeOut(a_square_label),
            FadeOut(b_square_label),
            FadeOut(c_square_label),
            FadeOut(equation)
        )
        self.wait(0.5)
```python
from manim import *

class Scene_20250731_221310(Scene):
    def construct(self):
        e = Text("E", font_size=72)
        equals = Text("=", font_size=72)
        m = Text("m", font_size=72)
        c = Text("c", font_size=72)
        squared = Text("2", font_size=36)

        c_squared = VGroup(c, squared)
        squared.next_to(c, UP, buff=0.05)

        equation = VGroup(e, equals, m, c_squared)
        equation.arrange(RIGHT, buff=0.2)

        self.play(Write(e))
        self.play(Write(equals))
        self.play(Write(m))
        self.play(Write(c))
        self.play(Write(squared))

        self.wait(2)
```
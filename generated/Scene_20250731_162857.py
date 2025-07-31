from manim import *

class Scene_20250731_162857(Scene):
    def construct(self):
        cat_body = Dot().move_to(ORIGIN)
        cat_head = Dot().move_to(UP*0.7)
        cat_left_ear = Dot().move_to(UP*1.2 + LEFT*0.3)
        cat_right_ear = Dot().move_to(UP*1.2 + RIGHT*0.3)
        cat_left_eye = Dot().move_to(UP*0.8 + LEFT*0.2)
        cat_right_eye = Dot().move_to(UP*0.8 + RIGHT*0.2)
        cat_nose = Dot().move_to(UP*0.6)
        cat_left_whisker1 = Dot().move_to(UP*0.5 + LEFT*0.4)
        cat_left_whisker2 = Dot().move_to(UP*0.4 + LEFT*0.5)
        cat_right_whisker1 = Dot().move_to(UP*0.5 + RIGHT*0.4)
        cat_right_whisker2 = Dot().move_to(UP*0.4 + RIGHT*0.5)
        cat_tail = Dot().move_to(DOWN*0.5 + RIGHT*0.3)

        self.add(
            cat_body,
            cat_head,
            cat_left_ear,
            cat_right_ear,
            cat_left_eye,
            cat_right_eye,
            cat_nose,
            cat_left_whisker1,
            cat_left_whisker2,
            cat_right_whisker1,
            cat_right_whisker2,
            cat_tail
        )

        body_line_dots = [Dot().move_to(ORIGIN + (UP*0.7 - ORIGIN)*i/10) for i in range(11)]
        head_line_dots = [Dot().move_to(UP*0.7 + (UP*0.5 - UP*0.7)*i/10) for i in range(11)]
        left_ear_line_dots = [Dot().move_to(UP*0.7 + LEFT*0.3 + (UP*1.2 + LEFT*0.3 - (UP*0.7 + LEFT*0.3))*i/10) for i in range(11)]
        right_ear_line_dots = [Dot().move_to(UP*0.7 + RIGHT*0.3 + (UP*1.2 + RIGHT*0.3 - (UP*0.7 + RIGHT*0.3))*i/10) for i in range(11)]
        left_eye_line_dots = [Dot().move_to(UP*0.7 + LEFT*0.2 + (UP*0.8 + LEFT*0.2 - (UP*0.7 + LEFT*0.2))*i/10) for i in range(11)]
        right_eye_line_dots = [Dot().move_to(UP*0.7 + RIGHT*0.2 + (UP*0.8 + RIGHT*0.2 - (UP*0.7 + RIGHT*0.2))*i/10) for i in range(11)]
        nose_line_dots = [Dot().move_to(UP*0.7 + (UP*0.6 - UP*0.7)*i/10) for i in range(11)]
        left_whisker1_line_dots = [Dot().move_to(UP*0.6 + LEFT*0.2 + (UP*0.5 + LEFT*0.4 - (UP*0.6 + LEFT*0.2))*i/10) for i in range(11)]
        left_whisker2_line_dots = [Dot().move_to(UP*0.5 + LEFT*0.3 + (UP*0.4 + LEFT*0.5 - (UP*0.5 + LEFT*0.3))*i/10) for i in range(11)]
        right_whisker1_line_dots = [Dot().move_to(UP*0.6 + RIGHT*0.2 + (UP*0.5 + RIGHT*0.4 - (UP*0.6 + RIGHT*0.2))*i/10) for i in range(11)]
        right_whisker2_line_dots = [Dot().move_to(UP*0.5 + RIGHT*0.3 + (UP*0.4 + RIGHT*0.5 - (UP*0.5 + RIGHT*0.3))*i/10) for i in range(11)]
        tail_line_dots = [Dot().move_to(ORIGIN + (DOWN*0.5 + RIGHT*0.3 - ORIGIN)*i/10) for i in range(11)]

        self.remove(
            cat_body,
            cat_head,
            cat_left_ear,
            cat_right_ear,
            cat_left_eye,
            cat
from manim import * # type: ignore

def circle_demo_display(scene):
    circle = Circle(color=BLUE)

    scene.play(Create(circle))
    
    circle_eq = MathTex(
        "x^{2}",
        "+",
        "y^{2}",
        "=",
        "1"
    ).next_to(circle, DOWN, buff=0.5)
    scene.play(Write(circle_eq))
    
    scene.play(
        circle_eq[2].animate.set_color(YELLOW),
        Indicate(circle_eq[2], color=YELLOW)
    )

    scene.play(
        circle_eq[0].animate.set_color(ORANGE),
        Indicate(circle_eq[0], color=ORANGE)
    )

    scene.remove(circle_eq)

    xt = MathTex(r"x_t = ")
    yt = MathTex(r"y_t = ")

    equations = VGroup(xt, yt).arrange(RIGHT, buff=1.5)
    equations.move_to(circle.get_center() + DOWN * 2)

    scene.play(Write(equations))

class CircleDemo(Scene):
    def construct(self):
        circle_demo_display(self)

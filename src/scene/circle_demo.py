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

    xt = MathTex("x_t")
    plus = MathTex("+")
    yt = MathTex("y_t")
    eq = MathTex("=")
    one = MathTex("1")

    param_form = VGroup(xt, plus, yt, eq, one).arrange(RIGHT, buff=0.3)
    param_form.next_to(circle, DOWN, buff=0.5)

    scene.play(
        TransformMatchingTex(circle_eq, param_form)
    )

    xt = MathTex(r"x_t = ...")
    yt = MathTex(r"y_t = ...")

    param_eq = VGroup(xt, yt).arrange(DOWN, buff=0.3)
    param_eq.next_to(param_form, DOWN, buff=0.5)

    scene.play(Write(param_eq))

class CircleDemo(Scene):
    def construct(self):
        circle_demo_display(self)

from manim import * # type: ignore

def circle_demo_display(scene):
    circle = Circle(color=BLUE, radius=2).to_edge(LEFT, buff=1)
    scene.play(Create(circle))

    circle_eq = MathTex(
        "x^{2}",
        "+",
        "y^{2}",
        "=",
        "1"
    ).next_to(circle, RIGHT, buff=1)
    scene.play(Write(circle_eq))

    scene.wait(0.5)
    scene.play(Indicate(circle_eq[2], color=YELLOW))

    scene.wait(0.5)
    scene.play(Indicate(circle_eq[0], color=PURPLE))

    circle_parametrics = MathTex(
        r"x(t) = ",
        r"y(t) = ",
        r"t \in 2\pi"
    )

    scene.play(ReplacementTransform(circle_eq, circle_parametrics))


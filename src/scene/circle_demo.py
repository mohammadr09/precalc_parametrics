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

    circle_parametrics_x = MathTex(r"x(t) = ...").shift(UP)
    circle_parametrics_y = MathTex(r"y(t) = ...").next_to(circle_parametrics_x, DOWN, buff=0.5)
    domain = MathTex(r"t \in [0, 2\pi]").next_to(circle_parametrics_y, DOWN, buff=0.5)

    circle_parametrics = VGroup(circle_parametrics_x, circle_parametrics_y)
    scene.play(ReplacementTransform(circle_eq, circle_parametrics))
    scene.play(Write(domain))

    scene.play(FadeOut(circle_parametrics), FadeOut(domain))

    # Deriving the Circle
    radius_dot = Dot(circle.get_center(), color=WHITE)
    radius_line = Line(radius_dot, circle.point_at_angle(0))

    scene.play(Create(radius_dot))
    scene.wait(0.5)

    scene.play(Create(radius_line))
    scene.play(
        Rotate(
            radius_line, 
            angle=PI/4, 
            about_point=radius_dot.get_center()
        ),
        run_time=2
    )

    plane = NumberPlane(
        x_range=[-1.5, 1.5, 1],
        y_range=[-1.5, 1.5, 1],
        x_length=6,
        y_length=6,
        axis_config = { "color": TEAL },
        background_line_style = { "stroke_color": TEAL, "stroke_opacity": 0.4 }
    ).move_to(circle.get_center())

    scene.play(FadeIn(plane))

    radius_line_endpoint = radius_line.get_end()
    center = circle.get_center()
    vertical_target = np.array([radius_line_endpoint[0], center[1], 0])
    vertical_line = Line(radius_line_endpoint, vertical_target, color=YELLOW)
    horizontal_line = Line(center, vertical_target, color=RED)

    scene.play(Create(vertical_line), Create(horizontal_line))

    arc = Arc(radius=0.4, start_angle=0, angle=PI/4, color=TEAL, arc_center=circle.get_center())
    scene.play(Create(arc))

    cosine = MathTex(r"x = \cos\theta")
    sine = MathTex(r"y = \sin\theta")
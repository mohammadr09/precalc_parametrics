from manim import * # type: ignore
import numpy as np

def circle_demo_display(scene):
    circle = Circle(color=BLUE, radius=2).to_edge(LEFT, buff=1)

    circle_eq = MathTex(
        "x^{2}",
        "+",
        "y^{2}",
        "=",
        "1"
    ).next_to(circle, RIGHT, buff=1)
    scene.play(Write(circle_eq))
    scene.play(Create(circle))

    scene.wait(0.5)
    scene.play(Indicate(circle_eq[2], color=YELLOW))

    scene.wait(0.5)
    scene.play(Indicate(circle_eq[0], color=RED))

    circle_parametrics_x = MathTex(r"x(t) = ...").shift(UP)
    circle_parametrics_y = MathTex(r"y(t) = ...").next_to(circle_parametrics_x, DOWN, buff=0.5)
    domain = MathTex(r"t \in [0, 2\pi]").next_to(circle_parametrics_y, DOWN, buff=0.5)

    circle_parametrics = VGroup(circle_parametrics_x, circle_parametrics_y)
    scene.play(ReplacementTransform(circle_eq, circle_parametrics))
    scene.play(Write(domain))

    scene.wait(1.3)

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

    x = MathTex(r"x", color=RED).next_to(horizontal_line, DOWN).scale(0.65)
    y = MathTex(r"y", color=YELLOW).next_to(vertical_line, RIGHT).scale(0.65)

    scene.play(Create(vertical_line), Create(horizontal_line), Write(x), Write(y))

    arc = Arc(radius=0.4, start_angle=0, angle=PI/4, color=TEAL, arc_center=circle.get_center())
    theta = MathTex(r"\theta").scale(0.5)
    theta.next_to(arc, RIGHT, buff=0.1)
    scene.play(Create(arc), Write(theta))

    cosine = MathTex(r"x", r"= \cos\theta", color=RED).next_to(circle, RIGHT * 2, buff=1).shift(UP)
    sine = MathTex(r"y", r"= \sin\theta", color=YELLOW).next_to(cosine, RIGHT, buff=0.5)

    scene.play(Write(cosine), Write(sine))

    """PERHAPS SHOW THE POINT ON THE CIRCLE GOING AROUND ..."""

    x_func = MathTex(r"x(\theta)", r"= \cos\theta", color=RED)
    y_func = MathTex(r"y(\theta)", r"= \sin\theta", color=YELLOW)
    x_func.move_to(cosine)
    y_func.move_to(sine).shift(RIGHT * 0.5)

    x_func[0].set_color(RED)
    y_func[0].set_color(YELLOW)

    scene.play(
        ReplacementTransform(cosine, x_func),
        ReplacementTransform(sine, y_func)
    )

    coords = MathTex("(", r"x(\theta)", ", ", r"y(\theta)", ")").shift(RIGHT * 2)
    coords[1].set_color(RED)
    coords[3].set_color(YELLOW)

    theta_tracker = ValueTracker(PI / 4)

    dot_on_circle = Dot(color=WHITE)
    dot_on_circle.add_updater(
        lambda t : t.move_to(circle.point_at_angle(theta_tracker.get_value()))
    )

    circle_coords = MathTex("(", r"x(\theta)", ", ", r"y(\theta)", ")").scale(0.6)
    circle_coords[1].set_color(RED)
    circle_coords[3].set_color(YELLOW)

    circle_coords.add_updater(
        lambda c: c.next_to(dot_on_circle, UP, buff=0.2)
    )

    vertical_line.add_updater(
        lambda v: v.put_start_and_end_on(
            dot_on_circle.get_center(),
            np.array([dot_on_circle.get_center()[0], circle.get_center()[1], 0])
        )
    )

    horizontal_line.add_updater(
        lambda h: h.put_start_and_end_on(
            circle.get_center(),
            np.array([dot_on_circle.get_center()[0], circle.get_center()[1], 0])
        )
    )

    radius_line.add_updater(
        lambda r: r.put_start_and_end_on(
            circle.get_center(),
            dot_on_circle.get_center()
        )
    )

    scene.play(
        Write(VGroup(coords[0], coords[2], coords[4])), # type: ignore
        Create(dot_on_circle),
        TransformFromCopy(x_func[0], coords[1]),
        TransformFromCopy(y_func[0], coords[3])
    )

    scene.remove(x, y, arc, theta)

    scene.play(
        ReplacementTransform(coords, circle_coords)
    )

    scene.wait(0.5)

    scene.play(
        theta_tracker.animate.increment_value(2 * PI),
        run_time=4,
        rate_func=linear 
    )
    scene.wait()

    dot_on_circle.clear_updaters()
    circle_coords.clear_updaters()
    vertical_line.clear_updaters()
    horizontal_line.clear_updaters()
    radius_line.clear_updaters()

    """
        PLAN:
            bring forth the coords of the circle to the center of the screen
            then, instead of theta, define the angle as t
            define the domain
    """
from manim import * # type: ignore
import numpy as np

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

    scene.wait(0.5)

    scene.play(
        circle_eq[0].animate.set_color(ORANGE),
        Indicate(circle_eq[0], color=ORANGE)
    )

    scene.wait(0.5)

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
    scene.wait(1.4)

    scene.remove(param_form, param_eq)
    scene.wait(0.5)

    # Circle Parametric Equation Derivation
    plane = NumberPlane(
        x_range=[-1.5, 1.5, 1],
        y_range=[-1.5, 1.5, 1],
        background_line_style={"stroke_opacity": 0.35}
    )

    scene.play(FadeIn(plane, run_time=0.8))
    scene.add(circle, plane)
    plane.set_z_index(0)
    circle.set_z_index(1)

    scene.play(
        VGroup(circle, plane).animate.scale(1.5).move_to(LEFT * 4),
        run_time=1.2,
        rate_func=smooth
    )

    radius_line = Line(circle.get_center(), circle.point_at_angle(PI/4))
    radius_dot = Dot(radius_line.get_start(), color=YELLOW)

    theta_arc = Angle(
        Line(circle.get_center(), circle.point_at_angle(0)),
        radius_line,
        radius=0.3,
        color=YELLOW
    )
    theta_label = MathTex(r"\theta").next_to(theta_arc, RIGHT, buff=0.1)
    theta_label.scale(0.5)

    scene.play(FadeIn(radius_dot))
    scene.play(
        MoveAlongPath(radius_dot, radius_line),
        Create(radius_line),
        Create(theta_arc),
        Write(theta_label)
    )

    perpendicular_line = Line(
        circle.point_at_angle(PI/4),
        np.array([circle.point_at_angle(PI/4)[0], 0, 0]),
        color=PURPLE
    )

    horizontal_line = Line(
        circle.get_center(),
        np.array([
            circle.point_at_angle(PI/4)[0],
            circle.get_center()[1],
            0
        ]),
        color=RED
    )

    scene.play(Create(perpendicular_line))

    cosine_eq = MathTex(r"x = \cos\theta", color=RED).shift(UP * 1.5)

    scene.play(
        Write(cosine_eq),
        Indicate(horizontal_line, color=RED)
    )

    sine_eq = MathTex(r"y = \sin\theta", color=PURPLE).next_to(cosine_eq, DOWN, buff=0.5)

    scene.play(
        Write(sine_eq),
        Indicate(perpendicular_line, color=RED)
    )

    scene.remove(radius_line)
    scene.remove(horizontal_line)
    scene.remove(perpendicular_line)
    scene.remove(radius_dot)

    theta = ValueTracker(PI / 4)

    def angle_vector(angle, length):
        return np.array([
            length * np.cos(angle),
            length * np.sin(angle),
            0
        ])

    moving_dot = always_redraw(
        lambda: Dot(
            circle.point_at_angle(theta.get_value()),
            color=YELLOW
        )
    )

    radius_line = always_redraw(
        lambda: Line(
            circle.get_center(),
            circle.point_at_angle(theta.get_value()),
            color=YELLOW
        )
    )

    horizontal_line = always_redraw(
        lambda: Line(
            circle.get_center(),
            np.array([
                circle.point_at_angle(theta.get_value())[0],
                circle.get_center()[1],
                0
            ]),
            color=RED
        )
    )

    vertical_line = always_redraw(
        lambda: Line(
            circle.point_at_angle(theta.get_value()),
            np.array([
                circle.point_at_angle(theta.get_value())[0],
                circle.get_center()[1],
                0
            ]),
            color=PURPLE
        )
    )

    moving_theta_arc = always_redraw(
        lambda: Arc(
            radius=0.45,
            start_angle=0,
            angle=theta.get_value(),
            arc_center=circle.get_center(),
            color=YELLOW,
            stroke_width=7
        )
    )

    moving_theta_label = always_redraw(
        lambda: MathTex(r"\theta")
            .scale(0.55)
            .move_to(circle.get_center() + angle_vector(theta.get_value() / 2, 0.7))
    )

    scene.play(
        ReplacementTransform(theta_arc, moving_theta_arc),
        ReplacementTransform(theta_label, moving_theta_label),
        FadeIn(moving_dot),
        Create(radius_line), # type: ignore
        Create(horizontal_line), # type: ignore
        Create(vertical_line), # type: ignore
        run_time=0.8
    )

    scene.play(
        theta.animate.set_value(PI/4 + TAU),
        run_time=4,
        rate_func=linear
    )

    moving_dot.clear_updaters()
    radius_line.clear_updaters()
    horizontal_line.clear_updaters()
    vertical_line.clear_updaters()
    moving_theta_arc.clear_updaters()
    moving_theta_label.clear_updaters()

    t_label = MathTex(r"t").scale(0.55).move_to(moving_theta_label)

    scene.play(Transform(moving_theta_label, t_label), run_time=0.6)

    x_param = MathTex(
        r"x",
        r"(t)",
        r"=",
        r"\cos",
        r"t",
        color=RED
    )

    y_param = MathTex(
        r"y",
        r"(t)",
        r"=",
        r"\sin",
        r"t",
        color=PURPLE
    )

    x_param.move_to(cosine_eq)
    y_param.move_to(sine_eq)

    scene.play(
        TransformMatchingTex(cosine_eq, x_param),
        TransformMatchingTex(sine_eq, y_param)
    )


class CircleDemo(Scene):
    def construct(self):
        circle_demo_display(self)

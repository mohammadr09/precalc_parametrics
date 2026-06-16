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

    scene.wait(1.3)
    scene.play(Indicate(circle_eq[0], color=RED))

    scene.wait(0.5)
    scene.play(Indicate(circle_eq[2], color=YELLOW))

    scene.wait(3)

    circle_parametrics_x = MathTex(r"x(t) = ...").shift(UP)
    circle_parametrics_y = MathTex(r"y(t) = ...").next_to(circle_parametrics_x, DOWN, buff=0.5)
    domain = MathTex(r"t \in [0, 2\pi]").next_to(circle_parametrics_y, DOWN, buff=0.5)

    circle_parametrics = VGroup(circle_parametrics_x, circle_parametrics_y)
    scene.play(ReplacementTransform(circle_eq, circle_parametrics))
    scene.play(Write(domain))

    scene.wait(3)

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

    x = MathTex(r"x", color=RED).next_to(horizontal_line, DOWN * 0.889).scale(0.65)
    y = MathTex(r"y", color=YELLOW).next_to(vertical_line, RIGHT * 0.75).scale(0.65)

    scene.play(Create(vertical_line), Create(horizontal_line), Write(x), Write(y))

    arc = Arc(radius=0.4, start_angle=0, angle=PI/4, color=TEAL, arc_center=circle.get_center())
    theta = MathTex(r"\theta").scale(0.5)
    theta.next_to(arc, RIGHT, buff=0.1)
    scene.play(Create(arc), Write(theta))

    cosine = MathTex(r"x", r"= \cos\theta", color=RED).next_to(circle, RIGHT * 2, buff=1).shift(UP)
    sine = MathTex(r"y", r"= \sin\theta", color=YELLOW).next_to(cosine, RIGHT, buff=0.5)

    scene.play(Write(cosine), Write(sine))
    scene.wait(2.5)

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

    scene.play(
        circle_coords.animate.move_to(ORIGIN + (RIGHT * 2)).scale(2.0)
    )

    scene.wait(2.4)

    x_parametric = MathTex(r"x(t)", r"= \cos t")
    x_parametric[0].set_color(RED)
    y_parametric = MathTex(r"y(t)", r"= \sin t")
    y_parametric[0].set_color(YELLOW)
    x_parametric.move_to(x_func)
    y_parametric.move_to(y_func)

    parametric_t = MathTex("(", r"x(t)", ", ", r"y(t)", ")").scale(1.2).move_to(circle_coords)
    parametric_t[1].set_color(RED)
    parametric_t[3].set_color(YELLOW)

    scene.play(
        ReplacementTransform(circle_coords, parametric_t),
        ReplacementTransform(x_func, x_parametric),
        ReplacementTransform(y_func, y_parametric)
    )
    scene.wait(0.5)

    domain_t = MathTex(r"t \in [0, 2\pi]").next_to(parametric_t, DOWN, buff=0.5)
    
    scene.play(Write(domain_t))
    scene.wait(2)

def ellipse_demo_display(scene):
    # ── Ellipse: circle but stretched ────────────────────────────────────────
    # The key insight: x=cos t, y=sin t, but scale each axis independently.
    # We show a unit circle → stretch it → equations fall out naturally.

    a, b = 2.2, 1.2

    circle_ghost = Circle(radius=1.0, color=TEAL, stroke_opacity=0.4).to_edge(LEFT, buff=1.2)
    ellipse = ParametricFunction(
        lambda t: np.array([a * np.cos(t), b * np.sin(t), 0]),
        t_range=(0, TAU),
        color=BLUE,
    ).move_to(circle_ghost.get_center())

    center = circle_ghost.get_center()

    # a and b labels on the axes
    a_line = Line(center, center + RIGHT * a, color=RED, stroke_width=2)
    b_line = Line(center, center + UP * b, color=YELLOW, stroke_width=2)
    a_label = MathTex("a", color=RED).scale(0.7).next_to(a_line, DOWN, buff=0.15)
    b_label = MathTex("b", color=YELLOW).scale(0.7).next_to(b_line, LEFT, buff=0.15)


    # Equations: start with circle, morph to ellipse
    circle_eqs = VGroup(
        MathTex(r"x(t)", r"= \cos t").set_color_by_tex("x(t)", RED),
        MathTex(r"y(t)", r"= \sin t").set_color_by_tex("y(t)", YELLOW),
    ).arrange(DOWN, buff=0.4).next_to(circle_ghost, RIGHT * 4, buff=1.0)

    ellipse_eqs = VGroup(
        MathTex(r"x(t)", r"= a \cos t").set_color_by_tex("x(t)", RED),
        MathTex(r"y(t)", r"= b \sin t").set_color_by_tex("y(t)", YELLOW),
    ).arrange(DOWN, buff=0.4).move_to(circle_eqs)

    domain = MathTex(r"t \in [0, 2\pi]").scale(0.8)\
        .next_to(ellipse_eqs, DOWN, buff=0.4)

    # 1. Ghost circle + circle equations
    scene.play(Create(circle_ghost), Write(circle_eqs), run_time=1.2)
    scene.wait(3)

    # 2. Reveal semi-axes
    scene.play(Create(a_line), Create(b_line), Write(a_label), Write(b_label))
    scene.wait(1.25)

    # 3. Stretch circle → ellipse, equations gain a and b
    scene.play(
        ReplacementTransform(circle_ghost, ellipse),
        ReplacementTransform(circle_eqs, ellipse_eqs),
        run_time=1.4,
    )
    scene.play(Write(domain))
    scene.wait(0.8)

    # 4. Trace dot
    tracker = ValueTracker(0)
    dot = Dot(color=WHITE)
    dot.add_updater(
        lambda d: d.move_to(
            center + np.array([a * np.cos(tracker.get_value()),
                               b * np.sin(tracker.get_value()), 0])
        )
    )

    scene.add(dot)
    scene.play(
        tracker.animate.set_value(TAU),
        run_time=3.5,
        rate_func=linear,
    )
    dot.clear_updaters()
    scene.wait(1.5)


def cycloid_demo_display(scene):
    # ── Cycloid: the rolling circle makes the derivation self-evident ─────────
    # No need to write out steps — just let the audience watch the point trace
    # and show the equations. The geometry IS the derivation.

    r = 0.75
    ground_y = -2.2

    ground = Line(LEFT * 7.5, RIGHT * 7.5, color=TEAL, stroke_width=2)\
        .set_y(ground_y)

    # Equations at top — shown early so viewers can watch and read simultaneously
    param_eqs = VGroup(
        MathTex(r"x(t)", r"= r(t - \sin t)").set_color_by_tex("x(t)", RED),
        MathTex(r"y(t)", r"= r(1 - \cos t)").set_color_by_tex("y(t)", YELLOW),
    ).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.6)

    domain = MathTex(r"t \in [0, 2\pi]").scale(0.8)\
        .next_to(param_eqs, DOWN, buff=0.3)

    scene.play(Create(ground))
    scene.play(Write(param_eqs), Write(domain))
    scene.wait(0.5)

    # Rolling group: circle + spoke (shows rotation clearly)
    tracker = ValueTracker(0)

    circle = Circle(radius=r, color=BLUE, stroke_width=2)
    spoke = Line(ORIGIN, RIGHT * r, color=WHITE, stroke_width=1.5)
    center_dot = Dot(ORIGIN, color=WHITE, radius=0.05)
    rolling = VGroup(circle, spoke, center_dot)

    def get_rolling_center(t):
        return np.array([r * t, ground_y + r, 0])

    def update_rolling(g):
        t = tracker.get_value()
        g.move_to(get_rolling_center(t))
        g.rotate(t - update_rolling.last_t, about_point=get_rolling_center(t)) # type: ignore
        update_rolling.last_t = t # type: ignore
    update_rolling.last_t = 0 # type: ignore

    rolling.move_to(get_rolling_center(0))
    rolling.add_updater(update_rolling)

    # Tracing dot
    trace_dot = Dot(color=YELLOW, radius=0.08)
    trace_dot.add_updater(
        lambda d: d.move_to(np.array([
            r * (tracker.get_value() - np.sin(tracker.get_value())),
            ground_y + r * (1 - np.cos(tracker.get_value())),
            0,
        ]))
    )

    path = TracedPath(trace_dot.get_center, stroke_color=YELLOW, stroke_width=3)

    # Quick geometric cue: vertical arm from circle center to trace dot (the sin t part)
    v_arm = always_redraw(
        lambda: Line(
            get_rolling_center(tracker.get_value()),
            trace_dot.get_center(),
            color=YELLOW, stroke_width=1.5, stroke_opacity=0.7,
        )
    )

    scene.add(path, rolling, trace_dot, v_arm)
    scene.wait(0.3)

    # Roll through two full arches so the repeating pattern is clear
    scene.play(
        tracker.animate.set_value(2 * TAU),
        run_time=7,
        rate_func=linear,
    )

    rolling.clear_updaters()
    trace_dot.clear_updaters()
    scene.wait(2)

class ParametricPresentation(Scene):
    def construct(self):
        # circle_demo_display(self)

        # self.play(FadeOut(*self.mobjects))

        # ellipse_demo_display(self)

        # self.play(FadeOut(*self.mobjects))

        cycloid_demo_display(self)
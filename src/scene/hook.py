from manim import * # type: ignore
import numpy as np

def hook_scene_display(scene):
    # displaying the individual shapes
        circle = Circle(color=BLUE)
        ellipse = Ellipse(width=4, height=2)

        scene.play(Create(circle))
        scene.wait(0.3)

        scene.play(ReplacementTransform(circle, ellipse))
        scene.wait(0.3)

        plane = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=5,
        )

        labels = plane.get_axis_labels("x", "y")

        right_branch = ParametricFunction(
            lambda t: plane.c2p(2 * np.cosh(t), np.sinh(t)),
            t_range=(-2, 2)
        )

        left_branch = ParametricFunction(
            lambda t: plane.c2p(-2 * np.cosh(t), np.sinh(t)),
            t_range=(-2, 2)
        )

        hyperbola = VGroup(right_branch, left_branch)

        scene.play(FadeIn(plane), FadeIn(labels))
        scene.play(ReplacementTransform(ellipse, hyperbola))
        scene.wait(0.3)

        # cycloid
        cycloid_radius = 1

        def cycloid_point(t):
            return plane.c2p(
                cycloid_radius * (t - np.sin(t)),
                cycloid_radius * (1 - np.cos(t))
            )

        cycloid_curve = ParametricFunction(
            cycloid_point,
            t_range=(0, TAU),
            color=GOLD,
            stroke_width=5
        )

        scene.play(
            ReplacementTransform(hyperbola, cycloid_curve),
            run_time=1
        )

        scene.wait(0.5)

        initial_cycloid_group = VGroup(
            plane,
            labels,
            cycloid_curve
        )

        scene.play(FadeOut(initial_cycloid_group), run_time=0.8)

        # comparison
        circle_target = LEFT * 5.4
        ellipse_target = LEFT * 2

        circle = Circle(color=BLUE).scale(0.4).move_to(circle_target)
        ellipse = Ellipse(width=4, height=2).scale(0.4).move_to(ellipse_target)

        hyperbola_plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=2.5,
            y_length=1.5,
            background_line_style={"stroke_opacity": 0.35}
        )
        comparison_right_branch = ParametricFunction(
            lambda t: hyperbola_plane.c2p(2 * np.cosh(t), np.sinh(t)),
            t_range=(-1.4, 1.4)
        )
        comparison_left_branch = ParametricFunction(
            lambda t: hyperbola_plane.c2p(-2 * np.cosh(t), np.sinh(t)),
            t_range=(-1.4, 1.4)
        )
        comparison_hyperbola = VGroup(
            hyperbola_plane,
            comparison_right_branch,
            comparison_left_branch
        ).move_to(RIGHT * 1.5)

        cycloid_plane = NumberPlane(
            x_range=[0, TAU + 1, 1],
            y_range=[0, 2.2, 1],
            x_length=2.9,
            y_length=2.9 * 2.2 / (TAU + 1),
            background_line_style={"stroke_opacity": 0.35}
        )

        def comparison_cycloid_point(t):
            return cycloid_plane.c2p(
                cycloid_radius * (t - np.sin(t)),
                cycloid_radius * (1 - np.cos(t))
            )

        def comparison_circle_center(t):
            return cycloid_plane.c2p(cycloid_radius * t, cycloid_radius)

        comparison_cycloid_curve = ParametricFunction(
            comparison_cycloid_point,
            t_range=(0, TAU),
            color=GOLD,
            stroke_width=4
        )
        cycloid_theta = ValueTracker(0)
        comparison_rolling_circle = always_redraw(
            lambda: Circle(
                radius=cycloid_plane.x_axis.unit_size * cycloid_radius,
                color=LIGHT_PINK
            ).move_to(comparison_circle_center(cycloid_theta.get_value()))
        )
        comparison_radius_line = always_redraw(
            lambda: Line(
                comparison_circle_center(cycloid_theta.get_value()),
                comparison_cycloid_point(cycloid_theta.get_value()),
                color=YELLOW
            )
        )
        comparison_cycloid_dot = always_redraw(
            lambda: Dot(
                comparison_cycloid_point(cycloid_theta.get_value()),
                color=GOLD
            )
        )
        comparison_cycloid = VGroup(
            cycloid_plane,
            comparison_cycloid_curve,
            comparison_rolling_circle, # type: ignore
            comparison_radius_line, # type: ignore
            comparison_cycloid_dot # type: ignore
        ).move_to(RIGHT * 5.1)

        scene.play(
            Create(circle),
            Create(ellipse),
            FadeIn(comparison_hyperbola),
            FadeIn(comparison_cycloid)
        )

        circle_dot = Dot(circle.point_from_proportion(0))
        ellipse_dot = Dot(ellipse.point_from_proportion(0))
        left_hyperbola_dot = Dot(comparison_left_branch.point_from_proportion(0))
        right_hyperbola_dot = Dot(comparison_right_branch.point_from_proportion(0))

        # traces
        circle_trace = TracedPath(circle_dot.get_center)
        ellipse_trace = TracedPath(ellipse_dot.get_center)
        left_trace = TracedPath(left_hyperbola_dot.get_center)
        right_trace = TracedPath(right_hyperbola_dot.get_center)
        comparison_cycloid_trace = TracedPath(
            comparison_cycloid_dot.get_center,
            stroke_color=GOLD,
            stroke_width=4
        )

        scene.add(
            circle_trace,
            ellipse_trace,
            left_trace,
            right_trace,
            comparison_cycloid_trace
        )

        scene.play(
            FadeIn(circle_dot),
            FadeIn(ellipse_dot),
            FadeIn(left_hyperbola_dot),
            FadeIn(right_hyperbola_dot),
        )

        scene.play(
            MoveAlongPath(circle_dot, circle),
            MoveAlongPath(ellipse_dot, ellipse),
            MoveAlongPath(left_hyperbola_dot, comparison_left_branch),
            MoveAlongPath(right_hyperbola_dot, comparison_right_branch),
            cycloid_theta.animate.set_value(TAU),
            run_time=2,
            rate_func=linear
        )

        scene.wait()

class HookScene(Scene):
    def construct(self):
        hook_scene_display(self)

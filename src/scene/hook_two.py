from manim import * # type: ignore
import numpy as np

class HookSceneTwo(Scene):
    def construct(self):
        # displaying the individual shapes
        circle = Circle(color=BLUE)
        ellipse = Ellipse(width=4, height=2)

        self.play(Create(circle))
        self.wait(0.3)

        self.play(ReplacementTransform(circle, ellipse))
        self.wait(0.3)

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

        self.play(FadeIn(plane), FadeIn(labels))
        self.play(ReplacementTransform(ellipse, hyperbola))
        self.wait(0.3)

        graph_group = VGroup(plane, labels, hyperbola)

        self.play(
            graph_group.animate.scale(0.4).shift(RIGHT * 4)
        )

        self.wait()

        # comparison
        circle_target = LEFT * 4

        circle = Circle(color=BLUE).scale(0.4).move_to(circle_target)
        ellipse = Ellipse(width=4, height=2).scale(0.4).move_to(ORIGIN)

        self.play(
            Create(circle),
            Create(ellipse)
        )

        circle_dot = Dot(circle.point_from_proportion(0))
        ellipse_dot = Dot(ellipse.point_from_proportion(0))
        left_hyperbola_dot = Dot(left_branch.point_from_proportion(0))
        right_hyperbola_dot = Dot(right_branch.point_from_proportion(0))

        # traces
        circle_trace = TracedPath(circle_dot.get_center)
        ellipse_trace = TracedPath(ellipse_dot.get_center)
        left_trace = TracedPath(left_hyperbola_dot.get_center)
        right_trace = TracedPath(right_hyperbola_dot.get_center)

        self.add(
            circle_trace,
            ellipse_trace,
            left_trace,
            right_trace
        )

        self.play(
            FadeIn(circle_dot),
            FadeIn(ellipse_dot),
            FadeIn(left_hyperbola_dot),
            FadeIn(right_hyperbola_dot),
        )

        self.play(
            MoveAlongPath(circle_dot, circle),
            MoveAlongPath(ellipse_dot, ellipse),
            MoveAlongPath(left_hyperbola_dot, left_branch),
            MoveAlongPath(right_hyperbola_dot, right_branch),
            run_time=2,
            rate_func=linear
        )

        self.wait()
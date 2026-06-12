from manim import * # type: ignore

class HookScene(Scene):
    def construct(self):
        circle = Circle()
        ellipse = Ellipse(width = 4, height = 2)
        dot = Dot(circle.point_from_proportion(0))

        self.play(Create(circle))
        self.play(Create(dot))
        self.play(MoveAlongPath(dot, circle))
        

        self.play(
            ReplacementTransform(circle, ellipse),
            dot.animate.move_to(ellipse.point_from_proportion(0))
        )

        self.play(MoveAlongPath(dot, ellipse))

        hyperbola = ParametricFunction(
            lambda t: np.array([
                2*np.cosh(t),
                np.sinh(t),
                0
            ]),
            t_range=(-1.5, 1.5)
        )

        self.play(
            ReplacementTransform(ellipse, hyperbola),
            dot.animate.move_to(hyperbola.point_from_proportion(0))
        )
        self.play(MoveAlongPath(dot, hyperbola))
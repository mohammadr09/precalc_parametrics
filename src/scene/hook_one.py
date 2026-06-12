from manim import *

class HookScene(Scene):
    def construct(self):
        circle = Circle()
        ellipse = Ellipse(width=4, height=2)

        dot = Dot(circle.point_from_proportion(0))

        self.play(Create(circle))
        self.play(FadeIn(dot))
        self.play(MoveAlongPath(dot, circle))

        self.play(FadeOut(dot))
        self.wait(0.3)
        
        self.play(ReplacementTransform(circle, ellipse))

        dot.move_to(ellipse.point_from_proportion(0))

        self.play(FadeIn(dot))
        self.play(MoveAlongPath(dot, ellipse))

        self.play(FadeOut(dot))
        self.wait(0.3)

        plane = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=5,
        )

        labels = plane.get_axis_labels("x", "y")

        hyperbola = ParametricFunction(
            lambda t: plane.c2p([
                2*np.cosh(t),
                np.sinh(t)
            ]),
            t_range=(-2, 2)
        )

        self.add(plane, labels)
        self.play(ReplacementTransform(ellipse, hyperbola))

        dot.move_to(hyperbola.point_from_proportion(0))

        self.play(FadeIn(dot))
        self.play(MoveAlongPath(dot, hyperbola))
from manim import * # type: ignore

class Test(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=3,
            y_length=3,
        ).to_edge(LEFT)

        labels = plane.get_axis_labels(
            x_label="x",
            y_label="y"
        )
        
        self.play(Create(plane))
        self.wait()

        self.play(Write(labels));
        self.wait()

        eq = MathTex(r"x^2 + y^2 = 1").to_edge(RIGHT)
        self.play(Write(eq))
        self.wait()
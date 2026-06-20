from manim import * # type: ignore
import numpy as np

def hook_scene_display(scene):
    # 1. Displaying individual shapes sequentially
    circle = Circle(color=BLUE)
    ellipse = Ellipse(width=4, height=2)
    
    scene.play(Create(circle))
    scene.wait(0.3)
    scene.play(ReplacementTransform(circle, ellipse))
    scene.wait(0.3)
    
    # 2. Setup the coordinate plane for the standalone cycloid
    plane = NumberPlane(
        x_range=[-8, 8, 1],
        y_range=[-5, 5, 1],
        x_length=8,
        y_length=5,
    )
    labels = plane.get_axis_labels("x", "y")
    
    # Define the cycloid curve math properties
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
    
    # Smooth transition from ellipse to standalone cycloid curve
    scene.play(
        ReplacementTransform(ellipse, cycloid_curve),
        FadeIn(plane),
        FadeIn(labels)
    )
    scene.wait(0.5)
    
    # Fade everything out to clear the canvas for the grid comparison
    initial_cycloid_group = VGroup(plane, labels, cycloid_curve)
    scene.play(FadeOut(initial_cycloid_group), run_time=0.8)
    
    # 3. Side-by-Side Comparison Setup (Balanced 3-column layout)
    # Positions are shifted laterally to account for the removed hyperbola
    circle_target = LEFT * 4.5
    ellipse_target = ORIGIN
    cycloid_target = RIGHT * 4.5
    
    # Scale down standard tracking assets
    circle = Circle(color=BLUE).scale(0.5).move_to(circle_target)
    ellipse = Ellipse(width=4, height=2).scale(0.5).move_to(ellipse_target)
    
    # Build mini coordinate system for the rolling cycloid demo
    cycloid_plane = NumberPlane(
        x_range=[0, TAU + 1, 1],
        y_range=[0, 2.2, 1],
        x_length=3.5,
        y_length=3.5 * 2.2 / (TAU + 1),
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
    
    # Dynamic tracking mechanics using ValueTracker
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
    
    # Group assets and align to right target sector
    comparison_cycloid = VGroup(
        cycloid_plane,
        comparison_cycloid_curve,
        comparison_rolling_circle, # type: ignore
        comparison_radius_line, # type: ignore
        comparison_cycloid_dot # type: ignore
    ).move_to(cycloid_target)
    
    # Introduce clean static comparison frames
    scene.play(
        Create(circle),
        Create(ellipse),
        FadeIn(comparison_cycloid)
    )
    
    # 4. Tracing and Path Traversal Animations
    circle_dot = Dot(circle.point_from_proportion(0))
    ellipse_dot = Dot(ellipse.point_from_proportion(0))
    
    circle_trace = TracedPath(circle_dot.get_center)
    ellipse_trace = TracedPath(ellipse_dot.get_center)
    comparison_cycloid_trace = TracedPath(
        comparison_cycloid_dot.get_center,
        stroke_color=GOLD,
        stroke_width=4
    )
    
    scene.add(circle_trace, ellipse_trace, comparison_cycloid_trace)
    
    scene.play(
        FadeIn(circle_dot),
        FadeIn(ellipse_dot),
    )
    
    # Execute simultaneous linear runtime animations across shapes
    scene.play(
        MoveAlongPath(circle_dot, circle),
        MoveAlongPath(ellipse_dot, ellipse),
        cycloid_theta.animate.set_value(TAU),
        run_time=2,
        rate_func=linear
    )
    scene.wait()

class HookScene(Scene):
    def construct(self):
        hook_scene_display(self)

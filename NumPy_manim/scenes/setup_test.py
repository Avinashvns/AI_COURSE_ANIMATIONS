from manim import *


class SetupTest(Scene):
    def construct(self):
        title = Text(
            "NumPy_manim",
            font_size=72
        )

        subtitle = Text(
            "Manim Setup Test",
            font_size=36
        )

        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))

        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(subtitle)
        )

        self.wait(1)
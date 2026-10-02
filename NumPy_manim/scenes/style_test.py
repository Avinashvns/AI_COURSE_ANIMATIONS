from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30


class StyleTest(Scene):

    # =========================================================
    # CHANGE ONLY THIS
    # =========================================================

    # LAYOUT = "vertical"
    LAYOUT = "horizontal"
    # "vertical"   → Input ke niche Output
    # "horizontal" → Input ke right Output


    # =========================================================
    # COLORS
    # =========================================================

    BG = "#0B0F16"
    CELL = "#171E2B"
    CELL_STROKE = "#39465A"

    TEXT = "#F4F7FB"
    MUTED = "#8D99AA"

    BLUE = "#4DA3FF"
    YELLOW = "#FFD166"
    GREEN = "#4ADE80"


    # =========================================================
    # CELL
    # =========================================================

    def make_cell(self, value="", size=0.95):

        box = RoundedRectangle(
            corner_radius=0.10,
            width=size,
            height=size,
            stroke_color=self.CELL_STROKE,
            stroke_width=2,
            fill_color=self.CELL,
            fill_opacity=1,
        )

        number = Text(
            str(value) if value != "" else "",
            font_size=29,
            color=self.TEXT,
            weight=BOLD,
        )

        number.move_to(box)

        return VGroup(box, number)


    # =========================================================
    # ARRAY
    # =========================================================

    def make_array(self, values):

        array = VGroup(
            *[
                self.make_cell(value)
                for value in values
            ]
        )

        array.arrange(
            RIGHT,
            buff=0.08
        )

        return array


    # =========================================================
    # INDEX
    # =========================================================

    def make_indices(self, array):

        indices = VGroup()

        for i, cell in enumerate(array):

            index = Text(
                str(i),
                font_size=21,
                color=self.MUTED,
            )

            index.next_to(
                cell,
                DOWN,
                buff=0.12
            )

            indices.add(index)

        return indices


    # =========================================================
    # LABEL
    # =========================================================

    def make_label(
        self,
        text,
        color=None,
        size=25
    ):

        if color is None:
            color = self.MUTED

        return Text(
            text,
            font_size=size,
            color=color,
            weight=BOLD,
        )


    # =========================================================
    # HIGHLIGHT
    # =========================================================

    def make_highlight(self, cell):

        return SurroundingRectangle(
            cell,
            corner_radius=0.10,
            buff=0.07,
            stroke_color=self.YELLOW,
            stroke_width=4,
        )


    # =========================================================
    # SHOW RESULT
    # =========================================================

    def show_result(self, cell, value):

        number = Text(
            str(value),
            font_size=29,
            color=self.GREEN,
            weight=BOLD,
        )

        number.move_to(cell)

        self.play(
            FadeIn(
                number,
                scale=0.5
            ),
            Indicate(
                cell,
                color=self.GREEN,
                scale_factor=1.08,
            ),
            run_time=0.55,
        )


    # =========================================================
    # CODE CARD
    # =========================================================

    def make_code_card(self):

        card = RoundedRectangle(
            corner_radius=0.12,
            width=3.4,
            height=0.72,
            stroke_color="#344054",
            stroke_width=1.5,
            fill_color="#111722",
            fill_opacity=1,
        )

        code = Text(
            "arr * 2",
            font_size=28,
            color=self.TEXT,
            font="Consolas",
        )

        code.move_to(card)

        return VGroup(card, code)


    # =========================================================
    # CONSTRUCT
    # =========================================================

    def construct(self):

        self.camera.background_color = self.BG

        # -----------------------------------------------------
        # DATA
        # -----------------------------------------------------

        input_values = [5, 10, 15, 20]

        output_values = [
            value * 2
            for value in input_values
        ]


        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        title = Text(
            "NumPy Element-wise Operation",
            font_size=46,
            weight=BOLD,
            color=self.TEXT,
        )

        subtitle = Text(
            "Multiplication",
            font_size=23,
            color=self.BLUE,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.12
        )

        header = VGroup(
            title,
            subtitle
        )

        header.to_edge(
            UP,
            buff=0.40
        )

        self.play(
            FadeIn(
                title,
                shift=UP * 0.15
            ),
            FadeIn(
                subtitle,
                shift=UP * 0.10
            ),
            run_time=0.8,
        )


        # =====================================================
        # INPUT
        # =====================================================

        input_array = self.make_array(
            input_values
        )

        input_indices = self.make_indices(
            input_array
        )

        input_label = self.make_label(
            "Input",
            self.BLUE,
            25
        )

        input_label.next_to(
            input_array,
            UP,
            buff=0.22
        )

        input_indices.next_to(
            input_array,
            DOWN,
            buff=0.12
        )

        input_group = VGroup(
            input_label,
            input_array,
            input_indices
        )


        # =====================================================
        # OUTPUT
        # =====================================================

        output_array = VGroup(
            *[
                self.make_cell("")
                for _ in input_values
            ]
        )

        output_array.arrange(
            RIGHT,
            buff=0.08
        )

        output_indices = self.make_indices(
            output_array
        )

        output_label = self.make_label(
            "Output",
            self.GREEN,
            25
        )

        output_label.next_to(
            output_array,
            UP,
            buff=0.22
        )

        output_indices.next_to(
            output_array,
            DOWN,
            buff=0.12
        )

        output_group = VGroup(
            output_label,
            output_array,
            output_indices
        )


        # =====================================================
        # WIDTH SAFETY
        # =====================================================

        max_width = 9.5

        if input_group.width > max_width:

            input_group.scale_to_fit_width(
                max_width
            )

        if output_group.width > max_width:

            output_group.scale_to_fit_width(
                max_width
            )


        # =====================================================
        # LAYOUT SWITCH
        # =====================================================

        if self.LAYOUT == "vertical":

            # ---------------------------------------------
            # VERTICAL
            #
            #        INPUT
            #      [5][10][15][20]
            #        ↓ ×2
            #      OUTPUT
            #      [ ][ ][ ][ ]
            # ---------------------------------------------

            input_group.move_to(
                UP * 1.15
            )

            output_group.move_to(
                DOWN * 1.55
            )

            arrow_start = (
                input_array.get_bottom()
                + DOWN * 0.35
            )

            arrow_end = (
                output_array.get_top()
                + UP * 0.35
            )

            arrow = Arrow(
                start=arrow_start,
                end=arrow_end,
                buff=0,
                stroke_width=3,
                color=self.YELLOW,
                max_tip_length_to_length_ratio=0.12,
            )

            operation = Text(
                "× 2",
                font_size=38,
                weight=BOLD,
                color=self.YELLOW,
            )

            operation.move_to(
                (arrow_start + arrow_end) / 2
            )

            operation.shift(
                RIGHT * 0.55
            )


        elif self.LAYOUT == "horizontal":

            # ---------------------------------------------
            # HORIZONTAL
            #
            # INPUT  → ×2 →  OUTPUT
            # ---------------------------------------------

            input_group.move_to(
                LEFT * 3.0
            )

            output_group.move_to(
                RIGHT * 3.0
            )

            arrow_start = (
                input_array.get_right()
                + RIGHT * 0.35
            )

            arrow_end = (
                output_array.get_left()
                + LEFT * 0.35
            )

            arrow = Arrow(
                start=arrow_start,
                end=arrow_end,
                buff=0,
                stroke_width=3,
                color=self.YELLOW,
                max_tip_length_to_length_ratio=0.12,
            )

            operation = Text(
                "× 2",
                font_size=38,
                weight=BOLD,
                color=self.YELLOW,
            )

            operation.move_to(
                (arrow_start + arrow_end) / 2
            )

            operation.shift(
                UP * 0.65
            )


        else:

            raise ValueError(
                "LAYOUT must be "
                "'vertical' or 'horizontal'"
            )


        # =====================================================
        # SHOW INPUT
        # =====================================================

        self.play(

            FadeIn(
                input_label,
                shift=UP * 0.15
            ),

            LaggedStart(
                *[
                    FadeIn(
                        cell,
                        shift=UP * 0.15
                    )
                    for cell in input_array
                ],
                lag_ratio=0.10,
            ),

            FadeIn(
                input_indices,
                shift=UP * 0.08
            ),

            run_time=1.0,
        )

        self.wait(0.4)


        # =====================================================
        # SHOW OUTPUT
        # =====================================================

        self.play(

            FadeIn(
                output_label,
                shift=UP * 0.15
            ),

            FadeIn(
                output_array,
                shift=UP * 0.10
            ),

            FadeIn(
                output_indices,
                shift=UP * 0.08
            ),

            run_time=0.6,
        )

        self.wait(0.3)


        # =====================================================
        # SHOW OPERATION
        # =====================================================

        self.play(

            GrowArrow(
                arrow
            ),

            FadeIn(
                operation,
                scale=0.75
            ),

            run_time=0.8,
        )

        self.wait(0.4)


        # =====================================================
        # ELEMENT-BY-ELEMENT TRANSFORMATION
        # =====================================================

        for i, value in enumerate(
            input_values
        ):

            highlight = self.make_highlight(
                input_array[i]
            )


            # Highlight current element

            self.play(

                Create(
                    highlight
                ),

                input_array[i][1].animate.set_color(
                    self.YELLOW
                ),

                input_indices[i].animate.set_color(
                    self.YELLOW
                ),

                run_time=0.35,
            )


            # Emphasize operation

            self.play(

                operation.animate.scale(
                    1.10
                ),

                run_time=0.2,
            )


            self.play(

                Indicate(
                    input_array[i][1],
                    color=self.YELLOW,
                    scale_factor=1.15,
                ),

                run_time=0.4,
            )


            # Show calculated result

            self.show_result(
                output_array[i],
                output_values[i],
            )


            # Reset

            self.play(

                FadeOut(
                    highlight
                ),

                input_array[i][1].animate.set_color(
                    self.TEXT
                ),

                input_indices[i].animate.set_color(
                    self.MUTED
                ),

                operation.animate.scale(
                    1 / 1.10
                ),

                run_time=0.25,
            )

            self.wait(0.15)


        # =====================================================
        # FINAL OUTPUT HIGHLIGHT
        # =====================================================

        self.wait(0.4)

        self.play(

            *[
                Indicate(
                    cell,
                    color=self.GREEN,
                    scale_factor=1.06,
                )
                for cell in output_array
            ],

            run_time=0.8,
        )


        # =====================================================
        # CODE
        # =====================================================

        self.wait(0.5)

        code_card = self.make_code_card()

        code_card.to_edge(
            DOWN,
            buff=0.30
        )

        self.play(

            FadeIn(
                code_card,
                shift=UP * 0.15
            ),

            run_time=0.6,
        )

        self.wait(2)
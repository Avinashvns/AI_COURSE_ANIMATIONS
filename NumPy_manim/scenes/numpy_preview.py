
from manim import *
import json
from pathlib import Path


# =========================================================
# RENDER CONFIG
# =========================================================

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30


class StyleTest(Scene):

    # =====================================================
    # CONFIG LOADER
    # =====================================================

    def load_config(self):
        config_path = (
            Path(__file__).resolve().parent.parent
            / "config"
            / "numpy_operation.json"
        )

        with open(
            config_path,
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    # =====================================================
    # VALUE FORMATTER
    # =====================================================

    def format_value(self, value):
        """
        Display numeric values cleanly.

        Examples:
            5       -> "5"
            5.0     -> "5"
            5.25    -> "5.25"
            -10.0   -> "-10"
            True    -> "True"
        """

        if isinstance(value, bool):
            return str(value)

        if isinstance(value, float) and value.is_integer():
            return str(int(value))

        return str(value)

    # =====================================================
    # COLORS
    # =====================================================

    BG = "#0B0F16"
    CELL = "#171E2B"
    CELL_STROKE = "#39465A"

    TEXT = "#F4F7FB"
    MUTED = "#8D99AA"

    BLUE = "#4DA3FF"
    YELLOW = "#FFD166"
    GREEN = "#4ADE80"

    # =====================================================
    # CELL
    # =====================================================

    def make_cell(self, value=""):

        box = RoundedRectangle(
            corner_radius=0.10,
            width=self.cell_size,
            height=self.cell_size,
            stroke_color=self.CELL_STROKE,
            stroke_width=2,
            fill_color=self.CELL,
            fill_opacity=1,
        )

        number = Text(
            self.format_value(value) if value != "" else "",
            font_size=self.number_font_size,
            color=self.TEXT,
            weight=BOLD,
        )

        number.move_to(box)

        return VGroup(box, number)

    # =====================================================
    # ARRAY
    # =====================================================

    def make_array(self, values):

        array = VGroup(
            *[
                self.make_cell(value)
                for value in values
            ]
        )

        array.arrange(
            RIGHT,
            buff=self.cell_spacing,
        )

        return array

    # =====================================================
    # INDEX
    # =====================================================

    def make_indices(self, array):

        indices = VGroup()

        for i, cell in enumerate(array):

            index = Text(
                str(i),
                font_size=self.index_font_size,
                color=self.MUTED,
            )

            index.next_to(
                cell,
                DOWN,
                buff=0.12,
            )

            indices.add(index)

        return indices

    # =====================================================
    # LABEL
    # =====================================================

    def make_label(
        self,
        text,
        color=None,
        size=25,
    ):

        if color is None:
            color = self.MUTED

        return Text(
            text,
            font_size=size,
            color=color,
            weight=BOLD,
        )

    # =====================================================
    # HIGHLIGHT
    # =====================================================

    def make_highlight(self, cell):

        return SurroundingRectangle(
            cell,
            corner_radius=0.10,
            buff=0.07,
            stroke_color=self.YELLOW,
            stroke_width=4,
        )

    # =====================================================
    # SHOW RESULT
    # =====================================================

    def show_result(self, cell, value):

        number = Text(
            self.format_value(value),
            font_size=self.number_font_size,
            color=self.GREEN,
            weight=BOLD,
        )

        number.move_to(cell)

        self.play(
            FadeIn(
                number,
                scale=0.5,
            ),
            Indicate(
                cell,
                color=self.GREEN,
                scale_factor=1.08,
            ),
            run_time=0.55 * self.animation_speed,
        )

    # =====================================================
    # CODE CARD
    # =====================================================

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
            self.code_text,
            font_size=28,
            color=self.TEXT,
            font="Consolas",
        )

        code.move_to(card)

        return VGroup(
            card,
            code,
        )

    # =====================================================
    # OPERATION SYMBOL
    # =====================================================

    def get_operation_symbol(self):

        symbols = {
            "Addition": "+",
            "Subtraction": "−",
            "Multiplication": "×",
            "Division": "÷",
            "Power": "^",
            "Modulus": "%",
            "Comparison": ">",
        }

        return symbols.get(
            self.operation,
            "?",
        )

    # =====================================================
    # CODE TEXT
    # =====================================================

    def get_code_text(self):

        code_map = {
            "Addition": f"arr + {self.operand:g}",
            "Subtraction": f"arr - {self.operand:g}",
            "Multiplication": f"arr * {self.operand:g}",
            "Division": f"arr / {self.operand:g}",
            "Power": f"arr ** {self.operand:g}",
            "Modulus": f"arr % {self.operand:g}",
            "Comparison": f"arr > {self.operand:g}",
        }

        return code_map.get(
            self.operation,
            "NumPy operation",
        )

    # =====================================================
    # CONSTRUCT
    # =====================================================

    def construct(self):

        # -------------------------------------------------
        # LOAD CONFIG
        # -------------------------------------------------

        config_data = self.load_config()

        self.camera.background_color = self.BG

        # -------------------------------------------------
        # CONFIG VALUES
        # -------------------------------------------------

        self.operation = config_data["operation"]

        self.input_values = config_data["input_values"]

        self.operand = config_data["operand"]

        self.LAYOUT = config_data["layout"]

        self.cell_size = config_data["cell_size"]

        self.cell_spacing = config_data["cell_spacing"]

        self.number_font_size = (
            config_data["number_font_size"]
        )

        self.index_font_size = (
            config_data["index_font_size"]
        )

        self.show_indices = config_data.get(
            "show_indices",
            True,
        )

        self.show_code = config_data.get(
            "show_code",
            True,
        )

        self.animation_speed = config_data.get(
            "animation_speed",
            1.0,
        )

        self.element_delay = config_data.get(
            "element_delay",
            0.15,
        )

        # -------------------------------------------------
        # CALCULATE OUTPUT
        # -------------------------------------------------

        if self.operation == "Addition":

            output_values = [
                value + self.operand
                for value in self.input_values
            ]

        elif self.operation == "Subtraction":

            output_values = [
                value - self.operand
                for value in self.input_values
            ]

        elif self.operation == "Multiplication":

            output_values = [
                value * self.operand
                for value in self.input_values
            ]

        elif self.operation == "Division":

            if self.operand == 0:

                raise ValueError(
                    "Division by zero is not allowed."
                )

            output_values = [
                value / self.operand
                for value in self.input_values
            ]

        elif self.operation == "Power":

            output_values = [
                value ** self.operand
                for value in self.input_values
            ]

        elif self.operation == "Modulus":

            if self.operand == 0:

                raise ValueError(
                    "Modulus by zero is not allowed."
                )

            output_values = [
                value % self.operand
                for value in self.input_values
            ]

        elif self.operation == "Comparison":

            output_values = [
                value > self.operand
                for value in self.input_values
            ]

        else:

            raise ValueError(
                f"Operation '{self.operation}' "
                "is not supported yet."
            )

        self.code_text = self.get_code_text()

        # =================================================
        # TITLE
        # =================================================

        title = Text(
            "NumPy Operation",
            font_size=46,
            weight=BOLD,
            color=self.TEXT,
        )

        subtitle = Text(
            self.operation,
            font_size=23,
            color=self.BLUE,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.12,
        )

        header = VGroup(
            title,
            subtitle,
        )

        header.to_edge(
            UP,
            buff=0.40,
        )

        self.play(
            FadeIn(
                title,
                shift=UP * 0.15,
            ),
            FadeIn(
                subtitle,
                shift=UP * 0.10,
            ),
            run_time=0.8 * self.animation_speed,
        )

        # =================================================
        # INPUT
        # =================================================

        input_array = self.make_array(
            self.input_values
        )

        input_label = self.make_label(
            "Input",
            self.BLUE,
            25,
        )

        input_label.next_to(
            input_array,
            UP,
            buff=0.22,
        )

        input_indices = self.make_indices(
            input_array
        )

        input_indices.next_to(
            input_array,
            DOWN,
            buff=0.12,
        )

        input_group_objects = [
            input_label,
            input_array,
        ]

        if self.show_indices:

            input_group_objects.append(
                input_indices
            )

        input_group = VGroup(
            *input_group_objects
        )

        # =================================================
        # OUTPUT
        # =================================================

        output_array = VGroup(
            *[
                self.make_cell("")
                for _ in self.input_values
            ]
        )

        output_array.arrange(
            RIGHT,
            buff=self.cell_spacing,
        )

        output_indices = self.make_indices(
            output_array
        )

        output_label = self.make_label(
            "Output",
            self.GREEN,
            25,
        )

        output_label.next_to(
            output_array,
            UP,
            buff=0.22,
        )

        output_indices.next_to(
            output_array,
            DOWN,
            buff=0.12,
        )

        output_group_objects = [
            output_label,
            output_array,
        ]

        if self.show_indices:

            output_group_objects.append(
                output_indices
            )

        output_group = VGroup(
            *output_group_objects
        )

        # =================================================
        # WIDTH SAFETY
        # =================================================

        max_width = 9.5

        if input_group.width > max_width:

            input_group.scale_to_fit_width(
                max_width
            )

        if output_group.width > max_width:

            output_group.scale_to_fit_width(
                max_width
            )

        # =================================================
        # LAYOUT
        # =================================================

        if self.LAYOUT == "vertical":

            input_group.move_to(
                UP * 1.15
            )

            output_group.move_to(
                DOWN * 1.55
            )

            # ARROW — CLEAR CENTER LANE
            # =================================================

            arrow_start = (
                input_array.get_bottom()
                + DOWN * 0.55
            )

            arrow_end = (
                output_label.get_top()
                + UP * 0.12
            )

            arrow = Arrow(
                start=arrow_start,
                end=arrow_end,
                buff=0,
                stroke_width=4,
                color=self.YELLOW,
                max_tip_length_to_length_ratio=0.28,
            )

            operation = Text(
                f"{self.get_operation_symbol()} "
                f"{self.operand:g}",
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
                f"{self.get_operation_symbol()} "
                f"{self.operand:g}",
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
                "layout must be "
                "'vertical' or 'horizontal'"
            )

        # =================================================
        # SHOW INPUT
        # =================================================

        input_animations = [
            FadeIn(
                cell,
                shift=UP * 0.15,
            )
            for cell in input_array
        ]

        animations = [
            FadeIn(
                input_label,
                shift=UP * 0.15,
            ),
            LaggedStart(
                *input_animations,
                lag_ratio=0.10,
            ),
        ]

        if self.show_indices:

            animations.append(
                FadeIn(
                    input_indices,
                    shift=UP * 0.08,
                )
            )

        self.play(
            *animations,
            run_time=1.0 * self.animation_speed,
        )

        self.wait(
            0.4 * self.animation_speed
        )

        # =================================================
        # SHOW OUTPUT
        # =================================================

        output_animations = [
            FadeIn(
                output_label,
                shift=UP * 0.15,
            ),
            FadeIn(
                output_array,
                shift=UP * 0.10,
            ),
        ]

        if self.show_indices:

            output_animations.append(
                FadeIn(
                    output_indices,
                    shift=UP * 0.08,
                )
            )

        self.play(
            *output_animations,
            run_time=0.6 * self.animation_speed,
        )

        self.wait(
            0.3 * self.animation_speed
        )

        # =================================================
        # SHOW OPERATION
        # =================================================

        self.play(
            GrowArrow(arrow),
            FadeIn(
                operation,
                scale=0.75,
            ),
            run_time=0.8 * self.animation_speed,
        )

        self.wait(
            0.4 * self.animation_speed
        )

        # =================================================
        # ELEMENT-BY-ELEMENT TRANSFORMATION
        # =================================================

        for i, value in enumerate(
            self.input_values
        ):

            highlight = self.make_highlight(
                input_array[i]
            )

            # ---------------------------------------------
            # Highlight current element
            # ---------------------------------------------

            highlight_animations = [
                Create(highlight),
                input_array[i][1].animate.set_color(
                    self.YELLOW
                ),
            ]

            if self.show_indices:

                highlight_animations.append(
                    input_indices[i].animate.set_color(
                        self.YELLOW
                    )
                )

            self.play(
                *highlight_animations,
                run_time=0.35 * self.animation_speed,
            )

            # ---------------------------------------------
            # Emphasize operation
            # ---------------------------------------------

            self.play(
                operation.animate.scale(1.10),
                run_time=0.2 * self.animation_speed,
            )

            self.play(
                Indicate(
                    input_array[i][1],
                    color=self.YELLOW,
                    scale_factor=1.15,
                ),
                run_time=0.4 * self.animation_speed,
            )

            # ---------------------------------------------
            # Show calculated result
            # ---------------------------------------------

            self.show_result(
                output_array[i],
                output_values[i],
            )

            # ---------------------------------------------
            # Reset
            # ---------------------------------------------

            reset_animations = [
                FadeOut(highlight),
                input_array[i][1].animate.set_color(
                    self.TEXT
                ),
                operation.animate.scale(
                    1 / 1.10
                ),
            ]

            if self.show_indices:

                reset_animations.append(
                    input_indices[i].animate.set_color(
                        self.MUTED
                    )
                )

            self.play(
                *reset_animations,
                run_time=0.25 * self.animation_speed,
            )

            self.wait(
                self.element_delay
                * self.animation_speed
            )

        # =================================================
        # FINAL OUTPUT HIGHLIGHT
        # =================================================

        self.wait(
            0.4 * self.animation_speed
        )

        self.play(
            *[
                Indicate(
                    cell,
                    color=self.GREEN,
                    scale_factor=1.06,
                )
                for cell in output_array
            ],
            run_time=0.8 * self.animation_speed,
        )

        # =================================================
        # CODE
        # =================================================

        if self.show_code:

            self.wait(
                0.5 * self.animation_speed
            )

            code_card = self.make_code_card()

            code_card.to_edge(
                DOWN,
                buff=0.30,
            )

            self.play(
                FadeIn(
                    code_card,
                    shift=UP * 0.15,
                ),
                run_time=0.6 * self.animation_speed,
            )

        self.wait(
            2 * self.animation_speed
        )


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    scene = StyleTest

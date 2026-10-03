from manim import *
import json
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_PATH = PROJECT_ROOT / "config" / "question_diagram.json"
BACKGROUND_PATH = PROJECT_ROOT / "assets" / "background_2.png"


# ============================================================
# SCENE
# ============================================================

class QuestionDiagram(Scene):

    # ========================================================
    # COLORS
    # ========================================================

    WHITE = "#FFFFFF"
    YELLOW = "#FFD84D"
    CYAN = "#55D9FF"

    CARD_FILL = "#101C2D"
    QUESTION_FILL = "#0B1728"


    # ========================================================
    # CONSTRUCT
    # ========================================================

    def construct(self):

        # ----------------------------------------------------
        # Load Configuration
        # ----------------------------------------------------

        data = self.load_config()

        animation_speed = float(
            data.get(
                "animation_speed",
                1.0
            )
        )

        question_delay = float(
            data.get(
                "question_delay",
                0.65
            )
        )

        flow_delay = float(
            data.get(
                "flow_delay",
                1.5
            )
        )

        array_values = data.get(
            "array",
            [
                [1, 2, 3],
                [4, 5, 6]
            ]
        )

        flow_steps = data.get(
            "flow_steps",
            [
                "Array",
                "Dimension",
                "Axis",
                "Shape",
                "ndim",
                "size"
            ]
        )

        questions = data.get(
            "questions",
            [
                "Agar main aapko ye array doon:",
                "Kya aap bata sakte ho iska shape kya hai?",
                "ndim kya hoga?",
                "Total elements kitne hain?",
                "Axis 0 aur Axis 1 kya represent karta hai?"
            ]
        )


        # ====================================================
        # BACKGROUND
        # ====================================================

        self.add(
            self.create_background()
        )


        # ====================================================
        # TITLE
        # ====================================================

        title = Text(
            "ARRAY FUNDAMENTALS",
            font="Arial",
            font_size=30,
            weight=BOLD,
            color=self.CYAN,
        )

        title.to_edge(
            UP,
            buff=0.25
        )


        self.play(
            FadeIn(
                title,
                shift=DOWN * 0.15
            ),
            run_time=0.6 * animation_speed
        )


        # ====================================================
        # NUMPY ARRAY
        # ====================================================

        array_card = self.create_array(
            array_values
        )

        array_card.move_to(
            LEFT * 3.25
            + UP * 1.65
        )


        self.play(
            FadeIn(
                array_card,
                shift=LEFT * 0.15
            ),
            run_time=0.8 * animation_speed
        )


        self.wait(
            0.5 * animation_speed
        )


        # ====================================================
        # QUESTIONS
        # ====================================================

        question_boxes = []

        question_area_top = -0.05
        question_area_bottom = -3.35

        available_height = (
            question_area_top
            - question_area_bottom
        )

        number_of_questions = len(
            questions
        )

        question_gap = 0.08

        base_question_height = 0.62


        # ----------------------------------------------------
        # Calculate Required Height
        # ----------------------------------------------------

        total_needed_height = (
            number_of_questions
            * base_question_height
            + max(
                0,
                number_of_questions - 1
            )
            * question_gap
        )


        question_scale = 1.0


        if total_needed_height > available_height:

            question_scale = (
                available_height
                / total_needed_height
            )


        question_height = (
            base_question_height
            * question_scale
        )

        question_font_size = (
            21
            * question_scale
        )

        question_label_size = (
            12
            * question_scale
        )

        question_width = 5.6


        # ----------------------------------------------------
        # Minimum Sizes
        # ----------------------------------------------------

        question_height = max(
            question_height,
            0.48
        )

        question_font_size = max(
            question_font_size,
            15
        )

        question_label_size = max(
            question_label_size,
            9
        )


        # ====================================================
        # QUESTION ANIMATION LOOP
        # ====================================================

        for index, question_text in enumerate(
            questions
        ):

            question_box = self.create_question_box(

                question_text,

                width=question_width,

                height=question_height,

                font_size=question_font_size,

                label_size=question_label_size,
            )


            # ------------------------------------------------
            # Position First Question
            # ------------------------------------------------

            if index == 0:

                question_box.move_to(
                    LEFT * 3.25
                    + UP * (
                        question_area_top
                        - question_height / 2
                    )
                )


            # ------------------------------------------------
            # Position Following Questions
            # ------------------------------------------------

            else:

                question_box.next_to(
                    question_boxes[-1],
                    DOWN,
                    buff=question_gap
                )


            question_boxes.append(
                question_box
            )


            # ------------------------------------------------
            # Question Appears
            # ------------------------------------------------

            self.play(

                FadeIn(
                    question_box,
                    shift=DOWN * 0.08
                ),

                run_time=0.45 * animation_speed
            )


            # ------------------------------------------------
            # Delay Before Next Question
            # ------------------------------------------------

            self.wait(
                question_delay
            )


        # ====================================================
        # DELAY BEFORE FLOW
        # ====================================================

        self.wait(
            flow_delay
        )


        # ====================================================
        # ARRAY DIMENSION TITLE
        # ====================================================

        flow_title = Text(

            "ARRAY DIMENSION",

            font="Arial",

            font_size=23,

            weight=BOLD,

            color=self.CYAN,
        )


        flow_title.move_to(
            RIGHT * 3.25
            + UP * 2.25
        )


        # ====================================================
        # FLOW DIAGRAM
        # ====================================================

        flow_diagram = self.create_flow_diagram(
            flow_steps
        )


        flow_diagram.move_to(
            RIGHT * 3.25
            + DOWN * 0.20
        )


        # ====================================================
        # FLOW TITLE ANIMATION
        # ====================================================

        self.play(

            FadeIn(
                flow_title,
                shift=DOWN * 0.15
            ),

            run_time=0.5 * animation_speed
        )


        # ====================================================
        # FLOW ANIMATION
        # ====================================================

        self.play(

            LaggedStart(

                *[
                    FadeIn(
                        item,
                        shift=UP * 0.10
                    )

                    for item in flow_diagram
                ],

                lag_ratio=0.10
            ),

            run_time=1.5 * animation_speed
        )


        # ====================================================
        # FINAL HOLD
        # ====================================================

        self.wait(
            1.8 * animation_speed
        )


    # ========================================================
    # LOAD CONFIG
    # ========================================================

    def load_config(self):

        default_config = {

            "array": [
                [1, 2, 3],
                [4, 5, 6]
            ],

            "flow_steps": [
                "Array",
                "Dimension",
                "Axis",
                "Shape",
                "ndim",
                "size"
            ],

            "questions": [
                "Agar main aapko ye array doon:",
                "Kya aap bata sakte ho iska shape kya hai?",
                "ndim kya hoga?",
                "Total elements kitne hain?",
                "Axis 0 aur Axis 1 kya represent karta hai?"
            ],

            "animation_speed": 1.0,

            "question_delay": 0.65,

            "flow_delay": 1.5
        }


        try:

            with open(
                CONFIG_PATH,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)


        except Exception:

            return default_config


    # ========================================================
    # BACKGROUND
    # ========================================================

    def create_background(self):

        background = ImageMobject(
            str(BACKGROUND_PATH)
        )

        background.set_width(
            config.frame_width
        )

        background.set_height(
            config.frame_height
        )

        background.move_to(
            ORIGIN
        )


        overlay = Rectangle(

            width=config.frame_width,

            height=config.frame_height,

            stroke_width=0,

            fill_color=BLACK,

            fill_opacity=0.32
        )

        overlay.move_to(
            ORIGIN
        )


        return Group(
            background,
            overlay
        )


    # ========================================================
    # ARRAY CARD
    # ========================================================

    def create_array(self, values):

        rows = []


        # ----------------------------------------------------
        # Convert Array To Text
        # ----------------------------------------------------

        for row in values:

            row_text = ", ".join(
                str(value)
                for value in row
            )

            rows.append(
                f"[{row_text}]"
            )


        array_text = (
            "[\n"
            + " "
            + ",\n ".join(rows)
            + "\n]"
        )


        # ----------------------------------------------------
        # Array Text
        # ----------------------------------------------------

        array = Text(

            array_text,

            font="Consolas",

            font_size=34,

            weight=BOLD,

            color=self.WHITE,

            line_spacing=0.72,
        )


        # ----------------------------------------------------
        # Card
        # ----------------------------------------------------

        card = RoundedRectangle(

            width=5.6,

            height=2.55,

            corner_radius=0.20,

            stroke_color=self.YELLOW,

            stroke_width=2.2,

            stroke_opacity=0.80,

            fill_color=self.CARD_FILL,

            fill_opacity=0.92,
        )


        # ----------------------------------------------------
        # Label
        # ----------------------------------------------------

        label = Text(

            "NumPy Array",

            font="Arial",

            font_size=21,

            weight=BOLD,

            color=self.CYAN,
        )


        label.next_to(
            card,
            UP,
            buff=0.14
        )


        # ----------------------------------------------------
        # Array Position
        # ----------------------------------------------------

        array.move_to(
            card.get_center()
            + DOWN * 0.05
        )


        # ----------------------------------------------------
        # Safe Area
        # ----------------------------------------------------

        max_array_width = 4.6
        max_array_height = 1.65


        if array.width > max_array_width:

            array.scale_to_fit_width(
                max_array_width
            )


        if array.height > max_array_height:

            array.scale_to_fit_height(
                max_array_height
            )


        array.move_to(
            card.get_center()
            + DOWN * 0.05
        )


        return VGroup(
            card,
            label,
            array
        )


    # ========================================================
    # QUESTION BOX
    # ========================================================

    def create_question_box(
        self,
        text,
        width=5.6,
        height=0.62,
        font_size=21,
        label_size=12,
    ):

        # ----------------------------------------------------
        # Box
        # ----------------------------------------------------

        box = RoundedRectangle(

            width=width,

            height=height,

            corner_radius=0.13,

            stroke_color=self.CYAN,

            stroke_width=1.8,

            stroke_opacity=0.90,

            fill_color=self.QUESTION_FILL,

            fill_opacity=0.96,
        )


        # ----------------------------------------------------
        # Question Text
        # ----------------------------------------------------

        question = Text(

            text,

            font="Arial",

            font_size=font_size,

            weight=BOLD,

            color=self.WHITE,
        )


        max_width = (
            width
            - 0.35
        )

        max_height = (
            height
            - 0.18
        )


        if question.width > max_width:

            question.scale_to_fit_width(
                max_width
            )


        if question.height > max_height:

            question.scale_to_fit_height(
                max_height
            )


        question.move_to(
            box.get_center()
        )


        # ----------------------------------------------------
        # Question Marker
        # ----------------------------------------------------

        marker = Text(

            "?",

            font="Arial",

            font_size=label_size,

            weight=BOLD,

            color=self.YELLOW,
        )


        marker.move_to(
            box.get_left()
            + RIGHT * 0.18
        )


        return VGroup(
            box,
            marker,
            question
        )


    # ========================================================
    # FLOW DIAGRAM
    # ========================================================

    def create_flow_diagram(
        self,
        steps
    ):

        group = VGroup()

        boxes = []


        # ====================================================
        # CREATE BOXES
        # ====================================================

        for step in steps:

            box = RoundedRectangle(

                width=3.35,

                height=0.48,

                corner_radius=0.11,

                stroke_color=self.YELLOW,

                stroke_width=1.8,

                stroke_opacity=0.75,

                fill_color=self.CARD_FILL,

                fill_opacity=0.90,
            )


            text = Text(

                step,

                font="Arial",

                font_size=20,

                weight=BOLD,

                color=self.WHITE,
            )


            text.move_to(
                box.get_center()
            )


            boxes.append(
                VGroup(
                    box,
                    text
                )
            )


        # ====================================================
        # POSITION BOXES
        # ====================================================

        for index, box_group in enumerate(
            boxes
        ):

            if index == 0:

                box_group.move_to(
                    ORIGIN
                )

            else:

                box_group.next_to(

                    boxes[index - 1],

                    DOWN,

                    buff=0.13
                )


        # ====================================================
        # ADD BOXES + ARROWS
        # ====================================================

        for index, box_group in enumerate(
            boxes
        ):

            group.add(
                box_group
            )


            if index < len(boxes) - 1:

                arrow = Arrow(

                    start=box_group.get_bottom(),

                    end=boxes[index + 1].get_top(),

                    color=self.YELLOW,

                    stroke_width=4.0,

                    max_tip_length_to_length_ratio=0.45,

                    buff=0.04,
                )


                group.add(
                    arrow
                )


        return group
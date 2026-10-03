from manim import *
from manim import config as manim_config

import json
from pathlib import Path


class BasicCode(Scene):

    # ==================================================
    # COLORS
    # ==================================================

    BG = "#07111F"
    CARD = "#101C2D"
    CELL = "#13243A"

    BORDER = "#4CC9F0"
    INDEX_COLOR = "#FFD166"
    ACCENT = "#00D4FF"

    TEXT = "#FFFFFF"
    MUTED = "#A9C4D8"

    # ==================================================
    # LOAD CONFIG
    # ==================================================

    def load_config(self):

        project_root = (
            Path(__file__)
            .resolve()
            .parents[1]
        )

        config_path = (
            project_root
            / "config"
            / "basic_code.json"
        )

        if not config_path.exists():

            raise FileNotFoundError(
                f"Config file not found:\n{config_path}"
            )

        with open(
            config_path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    # ==================================================
    # MAIN
    # ==================================================

    def construct(self):

        # --------------------------------------------------
        # LOAD JSON
        # --------------------------------------------------

        config = self.load_config()

        # --------------------------------------------------
        # CONFIG VALUES
        # --------------------------------------------------

        values = config.get(
            "array",
            [10, 20, 30, 40],
        )

        array_label_text = config.get(
            "array_label",
            "ARRAY",
        )

        index_label_text = config.get(
            "index_label",
            "INDEX",
        )

        element_label_text = config.get(
            "element_label",
            "Each value is an element",
        )

        animation_speed = float(
            config.get(
                "animation_speed",
                1.0,
            )
        )

        # Safety
        if animation_speed <= 0:

            animation_speed = 1.0

        # ==================================================
        # PROJECT ROOT
        # ==================================================

        project_root = (
            Path(__file__)
            .resolve()
            .parents[1]
        )

        # ==================================================
        # BACKGROUND
        # ==================================================

        background_path = (
            project_root
            / "assets"
            / "background_2.png"
        )

        if not background_path.exists():

            raise FileNotFoundError(
                f"Background image not found:\n{background_path}"
            )

        background = ImageMobject(
            str(background_path)
        )

        # Cover complete Manim frame
        frame_width = manim_config["frame_width"]
        frame_height = manim_config["frame_height"]

        scale_factor = max(
            frame_width / background.width,
            frame_height / background.height,
        )

        background.scale(
            scale_factor
        )

        background.move_to(
            ORIGIN
        )

        # Keep background behind everything
        background.set_z_index(
            -100
        )

        self.add(
            background
        )

        # ==================================================
        # TITLE
        # ==================================================

        title = Text(
            "NUMPY ARRAY KYA HAI?",
            font="Arial",
            font_size=38,
            weight=BOLD,
            color=self.TEXT,
        )

        title.to_edge(
            UP,
            buff=0.45,
        )

        self.play(
            FadeIn(
                title,
                shift=DOWN * 0.15,
            ),
            run_time=0.6 * animation_speed,
        )

        # ==================================================
        # CODE
        # ==================================================

        formatted_values = ", ".join(
            str(value)
            for value in values
        )

        code_text = (
            f"arr = np.array([{formatted_values}])"
        )

        # Make code font smaller for long arrays

        code_font_size = 25

        if len(code_text) > 38:
            code_font_size = 22

        if len(code_text) > 50:
            code_font_size = 19

        if len(code_text) > 65:
            code_font_size = 17

        code_box = RoundedRectangle(
            width=9.2,
            height=0.72,
            corner_radius=0.12,
            stroke_color=self.ACCENT,
            stroke_width=2,
            stroke_opacity=0.55,
            fill_color=self.CARD,
            fill_opacity=0.95,
        )

        code = Text(
            code_text,
            font="Consolas",
            font_size=code_font_size,
            color=self.TEXT,
        )

        code.move_to(
            code_box.get_center()
        )

        code_group = VGroup(
            code_box,
            code,
        )

        code_group.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        self.play(
            FadeIn(
                code_group,
                shift=DOWN * 0.12,
            ),
            run_time=0.6 * animation_speed,
        )

        self.wait(
            0.4 * animation_speed
        )

        # ==================================================
        # ARRAY CELLS
        # ==================================================

        cells = VGroup()

        for value in values:

            # ----------------------------------------------
            # CELL
            # ----------------------------------------------

            cell = RoundedRectangle(
                width=1.35,
                height=0.82,
                corner_radius=0.08,
                stroke_color=self.BORDER,
                stroke_width=2,
                fill_color=self.CELL,
                fill_opacity=0.95,
            )

            # ----------------------------------------------
            # VALUE
            # ----------------------------------------------

            value_text = str(value)

            value_font_size = 28

            if len(value_text) > 5:
                value_font_size = 23

            if len(value_text) > 8:
                value_font_size = 19

            number = Text(
                value_text,
                font="Arial",
                font_size=value_font_size,
                weight=BOLD,
                color=self.TEXT,
            )

            number.move_to(
                cell.get_center()
            )

            # ----------------------------------------------
            # CELL GROUP
            # ----------------------------------------------

            cell_group = VGroup(
                cell,
                number,
            )

            cells.add(
                cell_group
            )

        # ==================================================
        # ARRAY LAYOUT
        # ==================================================

        cells.arrange(
            RIGHT,
            buff=0.08,
        )

        # Prevent large arrays from going
        # outside the screen

        max_width = 11.5

        if cells.width > max_width:

            cells.scale_to_fit_width(
                max_width
            )

        cells.move_to(
            DOWN * 0.35
        )

        # ==================================================
        # ARRAY LABEL
        # ==================================================

        array_label = Text(
            array_label_text,
            font="Arial",
            font_size=24,
            weight=BOLD,
            color=self.MUTED,
        )

        array_label.next_to(
            cells,
            UP,
            buff=1.25,
        )

        # ==================================================
        # ARRAY ARROW
        # ==================================================

        array_arrow = Arrow(
            start=array_label.get_bottom(),

            # Keep ARRAY arrow above index numbers
            end=cells.get_top() + UP * 0.85,

            color=self.MUTED,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.25,
            buff=0.08,
        )

        # ==================================================
        # ARRAY APPEAR
        # ==================================================

        self.play(
            FadeIn(
                array_label,
                shift=DOWN * 0.10,
            ),

            LaggedStart(
                *[
                    FadeIn(
                        cell,
                        shift=UP * 0.15,
                    )
                    for cell in cells
                ],
                lag_ratio=0.12,
            ),

            run_time=0.9 * animation_speed,
        )

        self.play(
            GrowArrow(
                array_arrow
            ),
            run_time=0.4 * animation_speed,
        )

        self.wait(
            0.5 * animation_speed
        )

        # ==================================================
        # INDEX LABEL
        # ==================================================

        index_label = Text(
            index_label_text,
            font="Arial",
            font_size=22,
            weight=BOLD,
            color=self.INDEX_COLOR,
        )

        index_label.next_to(
            cells,
            UP,
            buff=0.55,
        )

        index_label.shift(
            LEFT * 3.0
        )

        # ==================================================
        # SHOW INDEX LABEL FIRST
        # ==================================================

        self.play(
            FadeIn(
                index_label,
                shift=RIGHT * 0.10,
            ),
            run_time=0.4 * animation_speed,
        )

        self.wait(
            0.4 * animation_speed
        )

        # ==================================================
        # INDEX → ELEMENT ANIMATION
        # ==================================================

        for i in range(
            len(cells)
        ):

            cell = cells[i]

            # --------------------------------------------------
            # CURRENT INDEX NUMBER
            # --------------------------------------------------

            index = Text(
                str(i),
                font="Arial",
                font_size=25,
                weight=BOLD,
                color=self.INDEX_COLOR,
            )

            index.next_to(
                cell,
                UP,
                buff=0.18,
            )

            # --------------------------------------------------
            # YELLOW HIGHLIGHT
            # --------------------------------------------------

            # Follows actual cell size even after scaling

            highlight = SurroundingRectangle(
                cell,
                color=self.INDEX_COLOR,
                buff=0.06,
                stroke_width=4,
            )

            # --------------------------------------------------
            # INDEX → ELEMENT ARROW
            # --------------------------------------------------

            connection = Arrow(
                start=index.get_bottom(),

                end=cell.get_top() + UP * 0.04,

                color=self.INDEX_COLOR,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.25,
                buff=0.04,
            )

            # --------------------------------------------------
            # SHOW INDEX + HIGHLIGHT
            # --------------------------------------------------

            self.play(
                FadeIn(
                    index,
                    shift=DOWN * 0.10,
                ),

                Create(
                    highlight
                ),

                GrowArrow(
                    connection
                ),

                run_time=0.4 * animation_speed,
            )

            self.wait(
                0.45 * animation_speed
            )

            # --------------------------------------------------
            # REMOVE ONLY HIGHLIGHT + ARROW
            #
            # INDEX NUMBER REMAINS VISIBLE
            # --------------------------------------------------

            self.play(
                FadeOut(
                    highlight
                ),

                FadeOut(
                    connection
                ),

                run_time=0.25 * animation_speed,
            )

            self.wait(
                0.15 * animation_speed
            )

        # ==================================================
        # FINAL ARRAY STATE
        # ==================================================

        self.wait(
            0.5 * animation_speed
        )

        # ==================================================
        # ELEMENT LABEL
        # ==================================================

        element_label = Text(
            element_label_text,
            font="Arial",
            font_size=25,
            weight=BOLD,
            color=self.TEXT,
        )

        element_label.next_to(
            cells,
            DOWN,
            buff=0.55,
        )

        self.play(
            FadeIn(
                element_label,
                shift=UP * 0.12,
            ),
            run_time=0.5 * animation_speed,
        )

        self.wait(
            0.7 * animation_speed
        )

        # ==================================================
        # FINAL ELEMENT HIGHLIGHT
        # ==================================================

        for cell in cells:

            highlight = SurroundingRectangle(
                cell,
                color=self.ACCENT,
                buff=0.06,
                stroke_width=3,
            )

            self.play(
                Create(
                    highlight
                ),
                run_time=0.25 * animation_speed,
            )

            self.wait(
                0.18 * animation_speed
            )

            self.play(
                FadeOut(
                    highlight
                ),
                run_time=0.18 * animation_speed,
            )

        # ==================================================
        # FINAL HOLD
        # ==================================================

        self.wait(
            1.5 * animation_speed
        )
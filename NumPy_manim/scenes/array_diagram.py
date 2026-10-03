from manim import *
import json
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_PATH = PROJECT_ROOT / "config" / "array_diagram.json"
BACKGROUND_PATH = PROJECT_ROOT / "assets" / "background_2.png"


# ============================================================
# SCENE
# ============================================================

class ArrayDiagram(Scene):

    # --------------------------------------------------------
    # COLORS
    # --------------------------------------------------------

    WHITE = "#FFFFFF"
    YELLOW = "#FFD84D"

    CARD_FILL = "#101C2D"
    CARD_INNER = "#0E1928"

    # --------------------------------------------------------
    # CONSTRUCTOR
    # --------------------------------------------------------

    def construct(self):

        # ----------------------------------------------------
        # Load configuration
        # ----------------------------------------------------

        data = self.load_config()

        steps = data.get("steps", [])

        if not steps:
            steps = [
                "Array kitni dimensions ka hai?",
                "Kitne axes hain?",
                "Har axis ki length kya hai?",
                "Shape kya hai?",
                "Total elements kitne hain?",
            ]

        # ----------------------------------------------------
        # Configuration
        # ----------------------------------------------------

        base_width = float(
            data.get("card_width", 5.0)
        )

        base_height = float(
            data.get("card_height", 0.75)
        )

        base_font = float(
            data.get("font_size", 30)
        )

        base_gap = float(
            data.get("vertical_gap", 0.40)
        )

        animation_speed = float(
            data.get("animation_speed", 1.0)
        )

        show_arrows = bool(
            data.get("show_arrows", True)
        )

        animate_step_by_step = bool(
            data.get("animate_step_by_step", True)
        )

        # ----------------------------------------------------
        # Background
        # ----------------------------------------------------

        background_group = self.create_background()

        self.add(background_group)

        # ----------------------------------------------------
        # Dynamic layout calculation
        # ----------------------------------------------------

        (
            card_width,
            card_height,
            font_size,
            vertical_gap,
        ) = self.calculate_layout(
            number_of_cards=len(steps),
            base_width=base_width,
            base_height=base_height,
            base_font=base_font,
            base_gap=base_gap,
        )

        # ----------------------------------------------------
        # Create all cards
        # ----------------------------------------------------

        cards = []

        for index, step in enumerate(steps):

            card = self.create_card(
                text=str(step),
                index=index,
                card_width=card_width,
                card_height=card_height,
                font_size=font_size,
            )

            cards.append(card)

        # ----------------------------------------------------
        # Center the complete layout
        # ----------------------------------------------------

        self.position_cards(
            cards=cards,
            card_height=card_height,
            vertical_gap=vertical_gap,
        )

        # ----------------------------------------------------
        # Create arrows
        # ----------------------------------------------------

        arrows = []

        if show_arrows:

            for i in range(len(cards) - 1):

                arrow = self.create_arrow(
                    upper_card=cards[i],
                    lower_card=cards[i + 1],
                )

                arrows.append(arrow)

        # ----------------------------------------------------
        # Animation
        # ----------------------------------------------------

        if animate_step_by_step:

            self.animate_step_by_step(
                cards=cards,
                arrows=arrows,
                animation_speed=animation_speed,
                show_arrows=show_arrows,
            )

        else:

            all_objects = []

            for card in cards:
                all_objects.append(card)

            for arrow in arrows:
                all_objects.append(arrow)

            self.play(
                FadeIn(
                    Group(*all_objects),
                    shift=UP * 0.15,
                ),
                run_time=1.0 * animation_speed,
            )

            self.wait(
                1.5 * animation_speed
            )

    # ========================================================
    # LOAD CONFIG
    # ========================================================

    def load_config(self):

        try:

            with open(
                CONFIG_PATH,
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except Exception:

            return {
                "steps": [
                    "Array kitni dimensions ka hai?",
                    "Kitne axes hain?",
                    "Har axis ki length kya hai?",
                    "Shape kya hai?",
                    "Total elements kitne hain?",
                ],
                "card_width": 5.0,
                "card_height": 0.75,
                "font_size": 30,
                "arrow_size": 35,
                "vertical_gap": 0.40,
                "animation_speed": 1.0,
                "show_arrows": True,
                "animate_step_by_step": True,
                "highlight_last": False,
            }

    # ========================================================
    # BACKGROUND
    # ========================================================

    def create_background(self):

        # ----------------------------------------------------
        # Background image
        # ----------------------------------------------------

        background = ImageMobject(
            str(BACKGROUND_PATH)
        )

        background.set_width(
            config.frame_width
        )

        background.set_height(
            config.frame_height
        )

        background.move_to(ORIGIN)

        # ----------------------------------------------------
        # Dark transparent overlay
        # ----------------------------------------------------

        overlay = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=0.28,
        )

        overlay.move_to(ORIGIN)

        # ----------------------------------------------------
        # IMPORTANT:
        # Group instead of VGroup
        # because ImageMobject is not VMobject.
        # ----------------------------------------------------

        return Group(
            background,
            overlay,
        )

    # ========================================================
    # DYNAMIC LAYOUT ENGINE
    # ========================================================

    def calculate_layout(
        self,
        number_of_cards,
        base_width,
        base_height,
        base_font,
        base_gap,
    ):

        """
        Dynamically fits ALL cards inside the 16:9 frame.

        Card width
        Card height
        Font size
        Vertical gap

        are scaled together.

        This prevents the final cards from going
        outside the screen.
        """

        # ----------------------------------------------------
        # FRAME DIMENSIONS
        # ----------------------------------------------------

        frame_width = config.frame_width
        frame_height = config.frame_height

        # ----------------------------------------------------
        # SAFE AREA
        # ----------------------------------------------------

        side_margin = 0.45
        top_bottom_margin = 0.55

        available_width = (
            frame_width
            - (2 * side_margin)
        )

        available_height = (
            frame_height
            - (2 * top_bottom_margin)
        )

        # ----------------------------------------------------
        # Start with user's requested values
        # ----------------------------------------------------

        width = float(base_width)
        height = float(base_height)
        font = float(base_font)
        gap = float(base_gap)

        # ----------------------------------------------------
        # HORIZONTAL FIT
        # ----------------------------------------------------

        if width > available_width:

            width_scale = (
                available_width / width
            )

            width *= width_scale
            height *= width_scale
            font *= width_scale
            gap *= width_scale

        # ----------------------------------------------------
        # VERTICAL FIT
        # ----------------------------------------------------

        total_height = (
            number_of_cards * height
            +
            max(
                0,
                number_of_cards - 1
            ) * gap
        )

        # ----------------------------------------------------
        # Scale EVERYTHING together
        # ----------------------------------------------------

        if total_height > available_height:

            vertical_scale = (
                available_height
                / total_height
            )

            width *= vertical_scale
            height *= vertical_scale
            font *= vertical_scale
            gap *= vertical_scale

        # ----------------------------------------------------
        # SECOND SAFETY PASS
        # ----------------------------------------------------

        total_height = (
            number_of_cards * height
            +
            max(
                0,
                number_of_cards - 1
            ) * gap
        )

        if total_height > available_height:

            extra_scale = (
                available_height
                / total_height
            )

            width *= extra_scale
            height *= extra_scale
            font *= extra_scale
            gap *= extra_scale

        # ----------------------------------------------------
        # Minimum values
        #
        # IMPORTANT:
        # Do NOT force font back to 17/18/etc.
        # Otherwise large diagrams overflow again.
        # ----------------------------------------------------

        width = max(
            width,
            2.6
        )

        height = max(
            height,
            0.38
        )

        font = max(
            font,
            14
        )

        gap = max(
            gap,
            0.10
        )

        # ----------------------------------------------------
        # Final horizontal safety
        # ----------------------------------------------------

        width = min(
            width,
            available_width
        )

        # ----------------------------------------------------
        # Final vertical safety
        #
        # If minimum values caused overflow,
        # calculate one final scale.
        # ----------------------------------------------------

        total_height = (
            number_of_cards * height
            +
            max(
                0,
                number_of_cards - 1
            ) * gap
        )

        if total_height > available_height:

            final_scale = (
                available_height
                / total_height
            )

            width *= final_scale
            height *= final_scale
            font *= final_scale
            gap *= final_scale

        return (
            width,
            height,
            font,
            gap,
        )

    # ========================================================
    # CREATE CARD
    # ========================================================

    def create_card(
        self,
        text,
        index,
        card_width,
        card_height,
        font_size,
    ):

        # ----------------------------------------------------
        # Outer subtle glow
        # ----------------------------------------------------

        glow_outer = RoundedRectangle(
            width=card_width + 0.10,
            height=card_height + 0.10,
            corner_radius=0.18,
            stroke_color=self.YELLOW,
            stroke_width=1.2,
            stroke_opacity=0.10,
            fill_opacity=0,
        )

        # ----------------------------------------------------
        # Frosted inner layer
        # ----------------------------------------------------

        glow_inner = RoundedRectangle(
            width=card_width + 0.04,
            height=card_height + 0.04,
            corner_radius=0.17,
            stroke_width=0,
            fill_color=self.CARD_INNER,
            fill_opacity=0.62,
        )

        # ----------------------------------------------------
        # Main card
        # ----------------------------------------------------

        box = RoundedRectangle(
            width=card_width,
            height=card_height,
            corner_radius=0.16,
            stroke_color=self.YELLOW,
            stroke_width=2.0,
            stroke_opacity=0.65,
            fill_color=self.CARD_FILL,
            fill_opacity=0.84,
        )

        # ----------------------------------------------------
        # Text
        # ----------------------------------------------------

        text_mob = Text(
            text,
            font_size=font_size,
            color=self.WHITE,
            weight=BOLD,
            font="Arial",
        )

        # ----------------------------------------------------
        # Fit text inside card
        # ----------------------------------------------------

        max_text_width = (
            card_width - 0.40
        )

        max_text_height = (
            card_height - 0.18
        )

        if text_mob.width > max_text_width:

            text_mob.scale_to_fit_width(
                max_text_width
            )

        if text_mob.height > max_text_height:

            text_mob.scale_to_fit_height(
                max_text_height
            )

        text_mob.move_to(box)

        # ----------------------------------------------------
        # Final card group
        # ----------------------------------------------------

        return VGroup(
            glow_outer,
            glow_inner,
            box,
            text_mob,
        )

    # ========================================================
    # POSITION CARDS
    # ========================================================

    def position_cards(
        self,
        cards,
        card_height,
        vertical_gap,
    ):

        if not cards:
            return

        number_of_cards = len(cards)

        # ----------------------------------------------------
        # Total height occupied by all cards + gaps
        # ----------------------------------------------------

        total_height = (
            number_of_cards * card_height
            +
            max(
                0,
                number_of_cards - 1
            ) * vertical_gap
        )

        # ----------------------------------------------------
        # Start from the TOP of the complete group.
        #
        # The whole group is centered around ORIGIN.
        # ----------------------------------------------------

        top_y = (
            total_height / 2
            - card_height / 2
        )

        # ----------------------------------------------------
        # Position each card
        # ----------------------------------------------------

        for i, card in enumerate(cards):

            y = (
                top_y
                -
                i * (
                    card_height
                    + vertical_gap
                )
            )

            card.move_to(
                np.array(
                    [0, y, 0]
                )
            )

    # ========================================================
    # CREATE ARROW
    # ========================================================

    def create_arrow(
        self,
        upper_card,
        lower_card,
    ):

        # ----------------------------------------------------
        # Exact card boundaries
        # ----------------------------------------------------

        upper_bottom = (
            upper_card.get_bottom()[1]
        )

        lower_top = (
            lower_card.get_top()[1]
        )

        center_x = (
            upper_card.get_center()[0]
        )

        # ----------------------------------------------------
        # Small padding
        # ----------------------------------------------------

        padding = 0.06

        start = np.array(
            [
                center_x,
                upper_bottom - padding,
                0,
            ]
        )

        end = np.array(
            [
                center_x,
                lower_top + padding,
                0,
            ]
        )

        # ----------------------------------------------------
        # Arrow
        # ----------------------------------------------------

        arrow = Arrow(
            start=start,
            end=end,
            color=self.YELLOW,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.45,
            buff=0,
        )

        return arrow

    # ========================================================
    # ANIMATION
    # ========================================================

    def animate_step_by_step(
        self,
        cards,
        arrows,
        animation_speed,
        show_arrows,
    ):

        # ----------------------------------------------------
        # Animate cards one by one
        # ----------------------------------------------------

        for i, card in enumerate(cards):

            self.play(
                FadeIn(
                    card,
                    shift=UP * 0.12,
                ),
                run_time=(
                    0.70
                    * animation_speed
                ),
            )

            # ------------------------------------------------
            # Small reading pause
            # ------------------------------------------------

            self.wait(
                0.25
                * animation_speed
            )

            # ------------------------------------------------
            # Arrow after card
            # ------------------------------------------------

            if (
                show_arrows
                and
                i < len(arrows)
            ):

                self.play(
                    GrowArrow(
                        arrows[i]
                    ),
                    run_time=(
                        0.45
                        * animation_speed
                    ),
                )

                self.wait(
                    0.12
                    * animation_speed
                )

        # ----------------------------------------------------
        # Final hold
        # ----------------------------------------------------

        self.wait(
            1.5
            * animation_speed
        )
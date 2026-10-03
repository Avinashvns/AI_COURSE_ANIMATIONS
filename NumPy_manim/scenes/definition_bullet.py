from manim import *
import json
from pathlib import Path


# ============================================================
# COLORS
# ============================================================

BG = "#07111F"
CARD = "#101C2D"
CARD_2 = "#0E1928"

YELLOW = "#FFD84D"
CYAN = "#55E6FF"
BLUE = "#4DB8FF"

WHITE = "#F5F7FA"
MUTED = "#A9B7C6"


# ============================================================
# CONFIG PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONFIG_PATH = (
    PROJECT_ROOT
    / "config"
    / "definition_bullet.json"
)


# ============================================================
# LOAD CONFIG
# ============================================================

def load_config():

    with open(
        CONFIG_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# ============================================================
# HELPERS
# ============================================================

def glass_card(
    width,
    height,
    stroke_color=YELLOW,
    fill_color=CARD,
):

    return RoundedRectangle(
        corner_radius=0.16,
        width=width,
        height=height,
        stroke_color=stroke_color,
        stroke_width=2,
        stroke_opacity=0.72,
        fill_color=fill_color,
        fill_opacity=0.90,
    )


def make_positioned_text(
    text,
    font_size,
    color,
    x,
    y,
    weight=BOLD,
):

    obj = Text(
        text,
        font_size=font_size,
        color=color,
        weight=weight,
    )

    obj.move_to(
        np.array([
            x,
            y,
            0
        ])
    )

    return obj


def make_bullet(
    text,
    font_size,
):

    dot = Dot(
        radius=0.055,
        color=YELLOW,
    )

    label = Text(
        text,
        font_size=font_size,
        color=WHITE,
        weight=BOLD,
    )

    return VGroup(
        dot,
        label,
    ).arrange(
        RIGHT,
        buff=0.18,
    )


# ============================================================
# SCENE
# ============================================================

class DefinitionBullet(Scene):

    def construct(self):

        config = load_config()


        # ====================================================
        # BACKGROUND
        # ====================================================

        self.camera.background_color = BG


        # ====================================================
        # ANIMATION SETTINGS
        # ====================================================

        animation_speed = float(
            config["animation"].get(
                "speed",
                1.0,
            )
        )

        bullet_delay = float(
            config["animation"].get(
                "bullet_delay",
                0.12,
            )
        )

        section_pause = float(
            config["animation"].get(
                "section_pause",
                0.35,
            )
        )


        # ====================================================
        # TITLE
        # ====================================================

        title = None

        if config["title"].get(
            "show",
            True,
        ):

            title_cfg = config["title"]

            title = make_positioned_text(
                text=title_cfg["text"],
                font_size=title_cfg["font_size"],
                color=WHITE,
                x=title_cfg["x"],
                y=title_cfg["y"],
            )

            self.play(
                FadeIn(
                    title,
                    shift=DOWN * 0.15,
                ),
                run_time=0.55 * animation_speed,
            )

            self.wait(
                0.20 * animation_speed
            )


        # ====================================================
        # DEFINITION
        # ====================================================

        definition_group = None
        numpy_text = None
        numerical_text = None

        if config["definition"].get(
            "show",
            True,
        ):

            definition_cfg = config["definition"]


            # =================================================
            # NUMPY HEADING
            # =================================================

            numpy_text = Text(
                definition_cfg["numpy"],
                font_size=definition_cfg["numpy_font_size"],
                color=CYAN,
                weight=BOLD,
            )

            numpy_text.move_to(
                np.array([
                    definition_cfg["x"],
                    definition_cfg["y"],
                    0
                ])
            )


            # =================================================
            # SUBTITLE / NUMERICAL PYTHON
            # =================================================

            numerical_text = Text(
                definition_cfg["numerical_python"].replace("\\n", "\n"),
                font_size=definition_cfg["numerical_font_size"],
                color=WHITE,
                weight=BOLD,
                line_spacing=0.8,
            )


            # -------------------------------------------------
            # SUBTITLE POSITION
            # -------------------------------------------------

            numerical_text.move_to(
                np.array([
                    definition_cfg.get(
                        "numerical_x",
                        definition_cfg["x"],
                    ),
                    definition_cfg.get(
                        "numerical_y",
                        definition_cfg["y"] - 0.6,
                    ),
                    0
                ])
            )


            # -------------------------------------------------
            # GROUP
            # -------------------------------------------------

            # Group sirf cleanup / arrow ke liye hai.
            # Dono objects ki actual position independent hai.
            definition_group = VGroup(
                numpy_text,
                numerical_text,
            )


            # =================================================
            # NUMPY ANIMATION
            # =================================================

            self.play(
                FadeIn(
                    numpy_text,
                    shift=UP * 0.15,
                ),
                run_time=0.50 * animation_speed,
            )


            # =================================================
            # SUBTITLE ANIMATION
            # =================================================

            self.play(
                FadeIn(
                    numerical_text,
                    shift=UP * 0.10,
                ),
                run_time=0.40 * animation_speed,
            )


            self.wait(
                section_pause * animation_speed
            )


        # ====================================================
        # NDARRAY
        # ====================================================

        ndarray_group = None

        if config["ndarray"].get(
            "show",
            True,
        ):

            ndarray_cfg = config["ndarray"]


            # ------------------------------------------------
            # CARD
            # ------------------------------------------------

            ndarray_card = glass_card(
                width=ndarray_cfg["width"],
                height=ndarray_cfg["height"],
            )


            # ------------------------------------------------
            # TEXT
            # ------------------------------------------------

            ndarray_text = Text(
                ndarray_cfg["text"],
                font_size=ndarray_cfg["font_size"],
                color=YELLOW,
                weight=BOLD,
            )

            ndarray_text.move_to(
                ndarray_card
            )


            # ------------------------------------------------
            # GROUP
            # ------------------------------------------------

            ndarray_group = VGroup(
                ndarray_card,
                ndarray_text,
            )


            # ------------------------------------------------
            # POSITION
            # ------------------------------------------------

            ndarray_group.move_to(
                np.array([
                    ndarray_cfg["x"],
                    ndarray_cfg["y"],
                    0
                ])
            )


            # =================================================
            # ARROW
            # =================================================

            if (
                config["arrow"].get(
                    "show",
                    True,
                )
                and definition_group is not None
            ):

                arrow_cfg = config["arrow"]

                arrow = Arrow(
                    start=definition_group.get_right(),
                    end=ndarray_group.get_left(),
                    color=YELLOW,
                    stroke_width=arrow_cfg.get(
                        "stroke_width",
                        5,
                    ),
                    max_tip_length_to_length_ratio=arrow_cfg.get(
                        "tip_ratio",
                        0.18,
                    ),
                    buff=arrow_cfg.get(
                        "gap",
                        0.18,
                    ),
                )

                self.play(
                    GrowArrow(
                        arrow
                    ),
                    run_time=0.45 * animation_speed,
                )


            # ------------------------------------------------
            # NDARRAY ANIMATION
            # ------------------------------------------------

            self.play(
                FadeIn(
                    ndarray_group,
                    shift=LEFT * 0.15,
                ),
                run_time=0.55 * animation_speed,
            )

            self.wait(
                section_pause * animation_speed
            )


        # ====================================================
        # CAPABILITY SECTION
        # ====================================================

        capability_title = None
        bullets_group = None

        if config["capability"].get(
            "show",
            True,
        ):

            capability_cfg = config["capability"]


            # =================================================
            # CAPABILITY TITLE
            # =================================================

            capability_title = Text(
                capability_cfg["title"],
                font_size=capability_cfg["font_size"],
                color=CYAN,
                weight=BOLD,
            )

            capability_title.move_to(
                np.array([
                    capability_cfg["x"],
                    capability_cfg["y"],
                    0
                ])
            )


            self.play(
                FadeIn(
                    capability_title,
                    shift=RIGHT * 0.12,
                ),
                run_time=0.45 * animation_speed,
            )


            # =================================================
            # BULLETS
            # =================================================

            if config["bullets"].get(
                "show",
                True,
            ):

                bullet_cfg = config["bullets"]

                bullet_items = []


                for text in bullet_cfg.get(
                    "items",
                    [],
                ):

                    if len(text) < 28:

                        font_size = bullet_cfg.get(
                            "font_size",
                            23,
                        )

                    else:

                        font_size = bullet_cfg.get(
                            "long_font_size",
                            21,
                        )


                    bullet_items.append(
                        make_bullet(
                            text,
                            font_size,
                        )
                    )


                if bullet_items:

                    bullets_group = VGroup(
                        *bullet_items
                    )


                    bullets_group.arrange(
                        DOWN,
                        aligned_edge=LEFT,
                        buff=capability_cfg.get(
                            "bullet_spacing",
                            0.10,
                        ),
                    )


                    bullets_group.move_to(
                        np.array([
                            capability_cfg.get(
                                "bullet_x",
                                capability_cfg["x"],
                            ),
                            capability_cfg.get(
                                "bullet_y",
                                capability_cfg["y"] - 0.60,
                            ),
                            0,
                        ])
                    )


                    # =========================================
                    # BULLET ANIMATION
                    # =========================================

                    for bullet in bullets_group:

                        self.play(
                            FadeIn(
                                bullet,
                                shift=RIGHT * 0.15,
                            ),
                            run_time=0.35 * animation_speed,
                        )

                        self.wait(
                            bullet_delay
                        )


            self.wait(
                section_pause * animation_speed
            )


        # ====================================================
        # IMPORT CODE
        # ====================================================

        import_group = None

        if config["import"].get(
            "show",
            False,
        ):

            import_cfg = config["import"]


            # ------------------------------------------------
            # CARD
            # ------------------------------------------------

            import_card = glass_card(
                width=import_cfg["width"],
                height=import_cfg["height"],
                stroke_color=CYAN,
                fill_color=CARD_2,
            )


            # ------------------------------------------------
            # CODE
            # ------------------------------------------------

            import_code = Text(
                import_cfg["code"],
                font_size=import_cfg["font_size"],
                color=WHITE,
                font="DejaVu Sans Mono",
            )

            import_code.move_to(
                import_card
            )


            # ------------------------------------------------
            # GROUP
            # ------------------------------------------------

            import_group = VGroup(
                import_card,
                import_code,
            )


            import_group.move_to(
                np.array([
                    import_cfg["x"],
                    import_cfg["y"],
                    0
                ])
            )


            self.play(
                FadeIn(
                    import_group,
                    shift=LEFT * 0.15,
                ),
                run_time=0.55 * animation_speed,
            )


            self.wait(
                section_pause * animation_speed
            )


        # ====================================================
        # ALIAS
        # ====================================================

        alias_group = None
        alias_label = None

        if config["alias"].get(
            "show",
            False,
        ):

            alias_cfg = config["alias"]


            # ------------------------------------------------
            # NUMPY
            # ------------------------------------------------

            alias_numpy = Text(
                alias_cfg["numpy"],
                font_size=alias_cfg["numpy_font_size"],
                color=WHITE,
                weight=BOLD,
            )


            # ------------------------------------------------
            # NP
            # ------------------------------------------------

            alias_np = Text(
                alias_cfg["np"],
                font_size=alias_cfg["np_font_size"],
                color=YELLOW,
                weight=BOLD,
            )


            # ------------------------------------------------
            # ARROW
            # ------------------------------------------------

            alias_arrow = Arrow(
                ORIGIN,
                RIGHT * 1.0,
                color=YELLOW,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.25,
            )


            # ------------------------------------------------
            # GROUP
            # ------------------------------------------------

            alias_group = VGroup(
                alias_numpy,
                alias_arrow,
                alias_np,
            ).arrange(
                RIGHT,
                buff=alias_cfg.get(
                    "gap",
                    0.18,
                ),
            )


            alias_group.move_to(
                np.array([
                    alias_cfg["x"],
                    alias_cfg["y"],
                    0
                ])
            )


            # ------------------------------------------------
            # LABEL
            # ------------------------------------------------

            alias_label = Text(
                alias_cfg["label"],
                font_size=alias_cfg["label_font_size"],
                color=MUTED,
            )

            alias_label.next_to(
                alias_group,
                DOWN,
                buff=0.08,
            )


            self.play(
                FadeIn(alias_group),
                FadeIn(alias_label),
                run_time=0.50 * animation_speed,
            )


            self.wait(
                section_pause * animation_speed
            )


        # ====================================================
        # FINAL
        # ====================================================

        final_group = None

        if config["final"].get(
            "show",
            True,
        ):

            final_cfg = config["final"]


            # ------------------------------------------------
            # TOP
            # ------------------------------------------------

            final_top = Text(
                final_cfg["numpy"],
                font_size=final_cfg["numpy_font_size"],
                color=CYAN,
                weight=BOLD,
            )


            # ------------------------------------------------
            # ARROW
            # ------------------------------------------------

            final_arrow = Arrow(
                UP * 0.45,
                DOWN * 0.45,
                color=YELLOW,
                stroke_width=6,
            )


            # ------------------------------------------------
            # BOTTOM
            # ------------------------------------------------

            final_bottom = Text(
                final_cfg["bottom"],
                font_size=final_cfg["bottom_font_size"],
                color=YELLOW,
                weight=BOLD,
            )


            # ------------------------------------------------
            # GROUP
            # ------------------------------------------------

            final_group = VGroup(
                final_top,
                final_arrow,
                final_bottom,
            ).arrange(
                DOWN,
                buff=final_cfg.get(
                    "vertical_gap",
                    0.18,
                ),
            )


            final_group.move_to(
                np.array([
                    final_cfg["x"],
                    final_cfg["y"],
                    0
                ])
            )


        # ====================================================
        # CLEANUP BEFORE FINAL
        # ====================================================

        objects_to_remove = []

        for obj in [
            capability_title,
            bullets_group,
            import_group,
            alias_group,
            alias_label,
            definition_group,
            ndarray_group,
        ]:

            if obj is not None:

                objects_to_remove.append(
                    obj
                )


        if objects_to_remove:

            self.play(
                *[
                    FadeOut(obj)
                    for obj in objects_to_remove
                ],
                run_time=0.65 * animation_speed,
            )


        # ====================================================
        # FINAL ANIMATION
        # ====================================================

        if final_group is not None:

            final_top = final_group[0]
            final_arrow = final_group[1]
            final_bottom = final_group[2]


            self.play(
                FadeIn(
                    final_top,
                    shift=UP * 0.15,
                ),
                GrowArrow(
                    final_arrow
                ),
                FadeIn(
                    final_bottom,
                    shift=DOWN * 0.15,
                ),
                run_time=0.80 * animation_speed,
            )


            self.play(
                Indicate(
                    final_bottom,
                    color=YELLOW,
                    scale_factor=1.06,
                ),
                run_time=0.65 * animation_speed,
            )


            self.wait(
                1.8 * animation_speed
            )
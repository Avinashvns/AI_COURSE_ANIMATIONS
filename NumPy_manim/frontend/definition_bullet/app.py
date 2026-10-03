import json
import subprocess
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_PATH = (
    PROJECT_ROOT
    / "config"
    / "definition_bullet.json"
)

SCENE_PATH = (
    PROJECT_ROOT
    / "scenes"
    / "definition_bullet.py"
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NumPy Definition Controller",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM UI
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .block-container {
        max-width: 1500px;
        padding-top: 2.2rem;
        padding-bottom: 2rem;
    }

    /* Main title */
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.15rem;
    }

    .subtitle {
        color: #8f9baa;
        margin-bottom: 1.2rem;
    }

    /* Section cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(15, 27, 43, 0.45);
    }

    /* Compact headings */
    h3 {
        margin-top: 0.2rem !important;
        margin-bottom: 0.6rem !important;
    }

    /* Reduce widget spacing */
    div[data-testid="stWidgetLabel"] {
        margin-bottom: 0.1rem;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        min-height: 2.2rem;
    }

    /* Number inputs */
    input {
        border-radius: 7px !important;
    }

    /* Dividers */
    hr {
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
    }

    /* Render area */
    .render-box {
        text-align: center;
        padding: 0.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    "## 🎬 NumPy — Definition Animation Controller"
)

st.markdown(
    '<div class="subtitle">'
    'Content • Show/Hide • Position • Gap • Font Size • Render'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# CONFIG FUNCTIONS
# ============================================================

def load_config():

    if not CONFIG_PATH.exists():

        st.error(
            f"Config file nahi mili:\n{CONFIG_PATH}"
        )

        st.stop()

    with open(
        CONFIG_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def save_config(data):

    temp_path = CONFIG_PATH.with_suffix(".tmp")

    with open(
        temp_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    temp_path.replace(CONFIG_PATH)


# ============================================================
# SESSION STATE
# ============================================================

if "data" not in st.session_state:
    st.session_state.data = load_config()

data = st.session_state.data


# ============================================================
# HELPER
# ============================================================

def position_controls(
    obj,
    prefix,
    label="Position",
):

    st.caption(label)

    col1, col2 = st.columns(2)

    with col1:

        obj["x"] = st.number_input(
            "X",
            min_value=-8.0,
            max_value=8.0,
            value=float(
                obj.get("x", 0.0)
            ),
            step=0.05,
            key=f"{prefix}_x",
        )

    with col2:

        obj["y"] = st.number_input(
            "Y",
            min_value=-5.0,
            max_value=5.0,
            value=float(
                obj.get("y", 0.0)
            ),
            step=0.05,
            key=f"{prefix}_y",
        )


def show_card_title(number, title):

    st.markdown(
        f"### {number}️⃣ {title}"
    )


# ============================================================
# ROW 1
# ============================================================

col1, col2, col3 = st.columns(
    3,
    gap="medium",
)


# ============================================================
# 1. TITLE
# ============================================================

with col1:

    with st.container(border=True):

        show_card_title(
            "1",
            "Main Title",
        )

        data["title"]["show"] = st.checkbox(
            "Show Title",
            value=data["title"].get(
                "show",
                True,
            ),
            key="show_title",
        )

        if data["title"]["show"]:

            data["title"]["text"] = st.text_input(
                "Title Text",
                value=data["title"].get(
                    "text",
                    "NUMPY KYA HAI?",
                ),
                key="title_text",
            )

            position_controls(
                data["title"],
                "title",
            )

            data["title"]["font_size"] = st.slider(
                "Font Size",
                15,
                80,
                int(
                    data["title"].get(
                        "font_size",
                        38,
                    )
                ),
                1,
                key="title_font",
            )


# ============================================================
# 2. DEFINITION
# ============================================================

with col2:

    with st.container(border=True):

        show_card_title(
            "2",
            "NumPy Definition",
        )

        # ----------------------------------------------------
        # SHOW / HIDE
        # ----------------------------------------------------

        data["definition"]["show"] = st.checkbox(
            "Show Definition",
            value=data["definition"].get(
                "show",
                True,
            ),
            key="show_definition",
        )

        if data["definition"]["show"]:

            # ====================================================
            # NUMPY TEXT
            # ====================================================

            data["definition"]["numpy"] = st.text_input(
                "NumPy Text",
                value=data["definition"].get(
                    "numpy",
                    "NumPy = Numerical Python",
                ),
                key="definition_numpy",
            )

            # ====================================================
            # NUMPY POSITION
            # ====================================================

            st.caption("NumPy Position")

            numpy_x, numpy_y = st.columns(2)

            with numpy_x:

                data["definition"]["x"] = st.number_input(
                    "NumPy X",
                    min_value=-8.0,
                    max_value=8.0,
                    value=float(
                        data["definition"].get(
                            "x",
                            -2.8,
                        )
                    ),
                    step=0.05,
                    key="definition_x",
                )

            with numpy_y:

                data["definition"]["y"] = st.number_input(
                    "NumPy Y",
                    min_value=-5.0,
                    max_value=5.0,
                    value=float(
                        data["definition"].get(
                            "y",
                            2.4,
                        )
                    ),
                    step=0.05,
                    key="definition_y",
                )

            # ====================================================
            # SUBTITLE TEXT
            # ====================================================

            data["definition"]["numerical_python"] = st.text_area(
                "Subtitle",
                value=data["definition"].get(
                    "numerical_python",
                    "NumPy Python ki ek library hai\n"
                    "jo primarily numerical aur scientific computing ke liye use hoti hai.",
                ),
                height=90,
                key="definition_numerical",
            )

            # ====================================================
            # SUBTITLE POSITION
            # ====================================================

            st.caption("Subtitle Position")

            sub_x, sub_y = st.columns(2)

            with sub_x:

                data["definition"]["numerical_x"] = st.number_input(
                    "Subtitle X",
                    min_value=-8.0,
                    max_value=8.0,
                    value=float(
                        data["definition"].get(
                            "numerical_x",
                            -2.0,
                        )
                    ),
                    step=0.05,
                    key="numerical_x",
                )

            with sub_y:

                data["definition"]["numerical_y"] = st.number_input(
                    "Subtitle Y",
                    min_value=-5.0,
                    max_value=5.0,
                    value=float(
                        data["definition"].get(
                            "numerical_y",
                            1.8,
                        )
                    ),
                    step=0.05,
                    key="numerical_y",
                )

            # ====================================================
            # NUMPY FONT
            # ====================================================

            data["definition"]["numpy_font_size"] = st.slider(
                "NumPy Font",
                20,
                80,
                int(
                    data["definition"].get(
                        "numpy_font_size",
                        30,
                    )
                ),
                1,
                key="numpy_font",
            )

            # ====================================================
            # SUBTITLE FONT
            # ====================================================

            data["definition"]["numerical_font_size"] = st.slider(
                "Subtitle Font",
                15,
                60,
                int(
                    data["definition"].get(
                        "numerical_font_size",
                        22,
                    )
                ),
                1,
                key="numerical_font",
            )

            # ====================================================
            # TEXT GAP
            # ====================================================

            data["definition"]["internal_gap"] = st.slider(
                "Text Gap",
                0.0,
                1.0,
                float(
                    data["definition"].get(
                        "internal_gap",
                        0.12,
                    )
                ),
                0.01,
                key="definition_gap",
            )

# ============================================================
# 3. NDARRAY
# ============================================================

with col3:

    with st.container(border=True):

        show_card_title(
            "3",
            "ndarray",
        )

        data["ndarray"]["show"] = st.checkbox(
            "Show ndarray",
            value=data["ndarray"].get(
                "show",
                True,
            ),
            key="show_ndarray",
        )

        if data["ndarray"]["show"]:

            data["ndarray"]["text"] = st.text_input(
                "Text",
                value=data["ndarray"].get(
                    "text",
                    "ndarray",
                ),
                key="ndarray_text",
            )

            position_controls(
                data["ndarray"],
                "ndarray",
            )

            data["ndarray"]["font_size"] = st.slider(
                "Font Size",
                15,
                70,
                int(
                    data["ndarray"].get(
                        "font_size",
                        36,
                    )
                ),
                1,
                key="ndarray_font",
            )

            data["ndarray"]["width"] = st.number_input(
                "Card Width",
                1.0,
                7.0,
                float(
                    data["ndarray"].get(
                        "width",
                        3.1,
                    )
                ),
                0.1,
                key="ndarray_width",
            )

            data["ndarray"]["height"] = st.number_input(
                "Card Height",
                0.5,
                3.0,
                float(
                    data["ndarray"].get(
                        "height",
                        1.25,
                    )
                ),
                0.05,
                key="ndarray_height",
            )


# ============================================================
# ROW 2
# ============================================================

st.write("")

col1, col2, col3 = st.columns(
    3,
    gap="medium",
)


# ============================================================
# 4. ARROW
# ============================================================

with col1:

    with st.container(border=True):

        show_card_title(
            "4",
            "Arrow",
        )

        data["arrow"]["show"] = st.checkbox(
            "Show Arrow",
            value=data["arrow"].get(
                "show",
                True,
            ),
            key="show_arrow",
        )

        if data["arrow"]["show"]:

            data["arrow"]["gap"] = st.slider(
                "Arrow Gap",
                0.0,
                1.0,
                float(
                    data["arrow"].get(
                        "gap",
                        0.18,
                    )
                ),
                0.01,
                key="arrow_gap",
            )

            data["arrow"]["stroke_width"] = st.slider(
                "Thickness",
                1,
                12,
                int(
                    data["arrow"].get(
                        "stroke_width",
                        5,
                    )
                ),
                1,
                key="arrow_width",
            )

            data["arrow"]["tip_ratio"] = st.slider(
                "Arrow Tip",
                0.05,
                0.5,
                float(
                    data["arrow"].get(
                        "tip_ratio",
                        0.18,
                    )
                ),
                0.01,
                key="arrow_tip",
            )


# ============================================================
# 5. CAPABILITY
# ============================================================

with col2:

    with st.container(border=True):

        show_card_title(
            "5",
            "Capability",
        )

        data["capability"]["show"] = st.checkbox(
            "Show Capability",
            value=data["capability"].get(
                "show",
                True,
            ),
            key="show_capability",
        )

        if data["capability"]["show"]:

            data["capability"]["title"] = st.text_input(
                "Heading",
                value=data["capability"].get(
                    "title",
                    "NumPy se hum efficiently kaam kar sakte hain",
                ),
                key="capability_heading",
            )

            position_controls(
                data["capability"],
                "capability",
                "Heading Position",
            )

            data["capability"]["font_size"] = st.slider(
                "Heading Font",
                15,
                50,
                int(
                    data["capability"].get(
                        "font_size",
                        24,
                    )
                ),
                1,
                key="capability_font",
            )

            st.caption("Bullets Position")

            bcol1, bcol2 = st.columns(2)

            with bcol1:

                data["capability"]["bullet_x"] = st.number_input(
                    "Bullet X",
                    -8.0,
                    8.0,
                    float(
                        data["capability"].get(
                            "bullet_x",
                            -5.10,
                        )
                    ),
                    0.05,
                    key="bullet_x",
                )

            with bcol2:

                data["capability"]["bullet_y"] = st.number_input(
                    "Bullet Y",
                    -5.0,
                    5.0,
                    float(
                        data["capability"].get(
                            "bullet_y",
                            0.35,
                        )
                    ),
                    0.05,
                    key="bullet_y",
                )

            data["capability"]["bullet_spacing"] = st.slider(
                "Bullet Spacing",
                0.0,
                0.5,
                float(
                    data["capability"].get(
                        "bullet_spacing",
                        0.10,
                    )
                ),
                0.01,
                key="bullet_spacing",
            )


# ============================================================
# 6. BULLETS
# ============================================================

with col3:

    with st.container(border=True):

        show_card_title(
            "6",
            "Bullets",
        )

        data["bullets"]["show"] = st.checkbox(
            "Show Bullets",
            value=data["bullets"].get(
                "show",
                True,
            ),
            key="show_bullets",
        )

        if data["bullets"]["show"]:

            if "items" not in data["bullets"]:
                data["bullets"]["items"] = []

            remove_index = None

            for i in range(
                len(
                    data["bullets"]["items"]
                )
            ):

                bcol1, bcol2 = st.columns(
                    [6, 1]
                )

                with bcol1:

                    data["bullets"]["items"][i] = st.text_input(
                        f"Bullet {i + 1}",
                        value=data["bullets"]["items"][i],
                        key=f"bullet_item_{i}",
                    )

                with bcol2:

                    if st.button(
                        "×",
                        key=f"remove_bullet_{i}",
                    ):

                        remove_index = i


            if remove_index is not None:

                data["bullets"]["items"].pop(
                    remove_index
                )

                st.rerun()


            if st.button(
                "＋ Add Bullet",
                key="add_bullet",
            ):

                data["bullets"]["items"].append(
                    "New Bullet"
                )

                st.rerun()


            bcol1, bcol2 = st.columns(2)

            with bcol1:

                data["bullets"]["font_size"] = st.slider(
                    "Normal Font",
                    15,
                    40,
                    int(
                        data["bullets"].get(
                            "font_size",
                            23,
                        )
                    ),
                    1,
                    key="bullet_font",
                )

            with bcol2:

                data["bullets"]["long_font_size"] = st.slider(
                    "Long Font",
                    15,
                    40,
                    int(
                        data["bullets"].get(
                            "long_font_size",
                            21,
                        )
                    ),
                    1,
                    key="long_bullet_font",
                )


# ============================================================
# ROW 3
# ============================================================

st.write("")

col1, col2, col3 = st.columns(
    3,
    gap="medium",
)


# ============================================================
# 7. IMPORT
# ============================================================

with col1:

    with st.container(border=True):

        show_card_title(
            "7",
            "Import Code",
        )

        data["import"]["show"] = st.checkbox(
            "Show Import Code",
            value=data["import"].get(
                "show",
                False,
            ),
            key="show_import",
        )

        if data["import"]["show"]:

            data["import"]["code"] = st.text_input(
                "Code",
                value=data["import"].get(
                    "code",
                    "import numpy as np",
                ),
                key="import_code",
            )

            position_controls(
                data["import"],
                "import",
            )

            data["import"]["font_size"] = st.slider(
                "Code Font",
                15,
                50,
                int(
                    data["import"].get(
                        "font_size",
                        28,
                    )
                ),
                1,
                key="import_font",
            )

            data["import"]["width"] = st.number_input(
                "Card Width",
                2.0,
                7.0,
                float(
                    data["import"].get(
                        "width",
                        4.7,
                    )
                ),
                0.1,
                key="import_width",
            )

            data["import"]["height"] = st.number_input(
                "Card Height",
                0.5,
                2.5,
                float(
                    data["import"].get(
                        "height",
                        1.0,
                    )
                ),
                0.05,
                key="import_height",
            )


# ============================================================
# 8. ALIAS
# ============================================================

with col2:

    with st.container(border=True):

        show_card_title(
            "8",
            "Alias",
        )

        data["alias"]["show"] = st.checkbox(
            "Show Alias",
            value=data["alias"].get(
                "show",
                False,
            ),
            key="show_alias",
        )

        if data["alias"]["show"]:

            acol1, acol2 = st.columns(2)

            with acol1:

                data["alias"]["numpy"] = st.text_input(
                    "Left",
                    value=data["alias"].get(
                        "numpy",
                        "numpy",
                    ),
                    key="alias_numpy",
                )

            with acol2:

                data["alias"]["np"] = st.text_input(
                    "Right",
                    value=data["alias"].get(
                        "np",
                        "np",
                    ),
                    key="alias_np",
                )

            data["alias"]["label"] = st.text_input(
                "Label",
                value=data["alias"].get(
                    "label",
                    "alias",
                ),
                key="alias_label",
            )

            position_controls(
                data["alias"],
                "alias",
            )

            acol1, acol2 = st.columns(2)

            with acol1:

                data["alias"]["numpy_font_size"] = st.slider(
                    "numpy Font",
                    15,
                    50,
                    int(
                        data["alias"].get(
                            "numpy_font_size",
                            29,
                        )
                    ),
                    1,
                    key="alias_numpy_font",
                )

            with acol2:

                data["alias"]["np_font_size"] = st.slider(
                    "np Font",
                    15,
                    60,
                    int(
                        data["alias"].get(
                            "np_font_size",
                            34,
                        )
                    ),
                    1,
                    key="alias_np_font",
                )

            data["alias"]["label_font_size"] = st.slider(
                "Label Font",
                12,
                40,
                int(
                    data["alias"].get(
                        "label_font_size",
                        22,
                    )
                ),
                1,
                key="alias_label_font",
            )


# ============================================================
# 9. FINAL
# ============================================================

with col3:

    with st.container(border=True):

        show_card_title(
            "9",
            "Final",
        )

        data["final"]["show"] = st.checkbox(
            "Show Final Section",
            value=data["final"].get(
                "show",
                True,
            ),
            key="show_final",
        )

        if data["final"]["show"]:

            data["final"]["numpy"] = st.text_input(
                "Top Text",
                value=data["final"].get(
                    "numpy",
                    "NumPy",
                ),
                key="final_numpy",
            )

            data["final"]["bottom"] = st.text_input(
                "Bottom Text",
                value=data["final"].get(
                    "bottom",
                    "ARRAY MODEL",
                ),
                key="final_bottom",
            )

            position_controls(
                data["final"],
                "final",
            )

            data["final"]["numpy_font_size"] = st.slider(
                "Top Font",
                20,
                80,
                int(
                    data["final"].get(
                        "numpy_font_size",
                        50,
                    )
                ),
                1,
                key="final_top_font",
            )

            data["final"]["bottom_font_size"] = st.slider(
                "Bottom Font",
                20,
                80,
                int(
                    data["final"].get(
                        "bottom_font_size",
                        46,
                    )
                ),
                1,
                key="final_bottom_font",
            )

            data["final"]["vertical_gap"] = st.slider(
                "Vertical Gap",
                0.0,
                1.0,
                float(
                    data["final"].get(
                        "vertical_gap",
                        0.18,
                    )
                ),
                0.01,
                key="final_gap",
            )


# ============================================================
# SAVE CONTROLS
# ============================================================

st.divider()

save_col1, save_col2, save_col3 = st.columns(
    [1, 1, 1],
    gap="medium",
)


with save_col1:

    if st.button(
        "💾 Save Configuration",
        use_container_width=True,
    ):

        save_config(data)

        st.success(
            "Configuration saved!"
        )


with save_col2:

    if st.button(
        "🔄 Reload JSON",
        use_container_width=True,
    ):

        st.session_state.data = load_config()

        st.rerun()


with save_col3:

    if st.button(
        "📄 Show JSON",
        use_container_width=True,
    ):

        st.json(data)


# ============================================================
# ANIMATION SETTINGS
# ============================================================

st.divider()

st.subheader(
    "⚙️ Animation Settings"
)

anim1, anim2, anim3 = st.columns(
    3,
    gap="medium",
)


with anim1:

    data["animation"]["speed"] = st.slider(
        "Animation Speed",
        0.25,
        2.0,
        float(
            data["animation"].get(
                "speed",
                1.0,
            )
        ),
        0.05,
        key="animation_speed",
    )


with anim2:

    data["animation"]["bullet_delay"] = st.slider(
        "Bullet Delay",
        0.0,
        1.0,
        float(
            data["animation"].get(
                "bullet_delay",
                0.12,
            )
        ),
        0.05,
        key="animation_bullet_delay",
    )


with anim3:

    data["animation"]["section_pause"] = st.slider(
        "Section Pause",
        0.0,
        2.0,
        float(
            data["animation"].get(
                "section_pause",
                0.35,
            )
        ),
        0.05,
        key="animation_section_pause",
    )


# ============================================================
# RENDER
# ============================================================

st.divider()

st.subheader(
    "🎬 Render"
)

st.caption(
    "Fixed output: 1920 × 1080 • 60 FPS"
)


render_col1, render_col2, render_col3 = st.columns(
    [1, 1.5, 1],
)


with render_col2:

    if st.button(
        "▶️ Render 1080p • 60 FPS",
        type="primary",
        use_container_width=True,
    ):

        # Save latest settings
        save_config(data)

        command = [
            "manim",
            "-p",
            "--resolution",
            "1920,1080",
            "--fps",
            "60",
            str(SCENE_PATH),
            "DefinitionBullet",
        ]

        with st.spinner(
            "Rendering Manim animation..."
        ):

            result = subprocess.run(
                command,
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
            )

        if result.returncode != 0:

            st.error(
                "❌ Render failed!"
            )

            with st.expander(
                "Show Error"
            ):

                st.code(
                    result.stderr
                )

        else:

            st.success(
                "✅ Render complete!"
            )

            with st.expander(
                "Show Render Log"
            ):

                st.code(
                    result.stdout[-3000:]
                )


# ============================================================
# PROJECT INFO
# ============================================================

with st.expander(
    "🔧 Project Information"
):

    st.write(
        "Project Root:",
        str(PROJECT_ROOT),
    )

    st.write(
        "Config:",
        str(CONFIG_PATH),
    )

    st.write(
        "Scene:",
        str(SCENE_PATH),
    )
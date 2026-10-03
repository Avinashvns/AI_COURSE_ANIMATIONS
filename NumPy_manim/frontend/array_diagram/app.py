import streamlit as st
import json
import subprocess
from pathlib import Path


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent.parent
)

CONFIG_PATH = (
    PROJECT_ROOT
    / "config"
    / "array_diagram.json"
)

SCENE_PATH = (
    PROJECT_ROOT
    / "scenes"
    / "array_diagram.py"
)

MEDIA_DIR = (
    PROJECT_ROOT
    / "media"
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Array Diagram - Manim",
    page_icon="📊",
    layout="wide",
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .sub-title {
        color: #9CA3AF;
        font-size: 15px;
        margin-bottom: 25px;
    }

    .preview-card {
        background: #101C2D;
        border: 2px solid #7898BE;
        border-radius: 10px;
        padding: 12px 18px;
        text-align: center;
        color: #F4F7FB;
        font-weight: 600;
        margin: 0 auto;
        max-width: 550px;
    }

    .preview-arrow {
        text-align: center;
        color: #FFD166;
        font-size: 24px;
        height: 30px;
        line-height: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DEFAULT CONFIG
# =========================================================

DEFAULT_CONFIG = {

    "steps": [
        "Array kitni dimensions ka hai?",
        "Kitne axes hain?",
        "Har axis ki length kya hai?",
        "Shape kya hai?",
        "Total elements kitne hain?"
    ],

    "card_width": 5.0,

    "card_height": 0.75,

    "font_size": 30,

    "arrow_size": 35,

    "vertical_gap": 0.40,

    "animation_speed": 1.0,

    "show_arrows": True,

    "animate_step_by_step": True,

    "highlight_last": False
}


# =========================================================
# LOAD CONFIG
# =========================================================

def load_config():

    if not CONFIG_PATH.exists():

        CONFIG_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            CONFIG_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                DEFAULT_CONFIG,
                file,
                indent=4,
                ensure_ascii=False
            )

        return DEFAULT_CONFIG.copy()


    with open(
        CONFIG_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)


    # Safety defaults

    for key, value in DEFAULT_CONFIG.items():

        if key not in data:

            data[key] = value


    return data


# =========================================================
# SAVE CONFIG
# =========================================================

def save_config(data):

    CONFIG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        CONFIG_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# FIND LATEST VIDEO
# =========================================================

def find_latest_video():

    if not MEDIA_DIR.exists():

        return None


    videos = list(
        MEDIA_DIR.rglob("*.mp4")
    )


    if not videos:

        return None


    return max(
        videos,
        key=lambda file: file.stat().st_mtime
    )


# =========================================================
# RENDER MANIM
# =========================================================

def render_animation(quality):

    MEDIA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    quality_flags = {

        "Low": "-ql",

        "Medium": "-qm",

        "High": "-qh",

        "Production": "-qp"
    }


    command = [

        "manim",

        quality_flags[quality],

        str(SCENE_PATH),

        "ArrayDiagram",

        "--media_dir",

        str(MEDIA_DIR)
    ]


    result = subprocess.run(

        command,

        cwd=str(PROJECT_ROOT),

        capture_output=True,

        text=True,

        encoding="utf-8",

        errors="replace"
    )


    if result.returncode != 0:

        return False, result.stderr


    return True, result.stdout


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    '📊 NumPy Array Diagram'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Dynamic Manim motion-graphics diagram'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# LOAD
# =========================================================

config_data = load_config()


# =========================================================
# SESSION STATE
# =========================================================

if "steps" not in st.session_state:

    st.session_state.steps = list(
        config_data["steps"]
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Diagram Settings")


    # =====================================================
    # STEP MANAGEMENT
    # =====================================================

    st.markdown("### 📝 Diagram Steps")


    st.caption(
        f"Total Steps: {len(st.session_state.steps)}"
    )


    # -----------------------------------------------------
    # Add Step
    # -----------------------------------------------------

    if st.button(
        "➕ Add Step",
        use_container_width=True
    ):

        st.session_state.steps.append(
            f"New Step {len(st.session_state.steps) + 1}"
        )

        st.rerun()


    # -----------------------------------------------------
    # Remove Last Step
    # -----------------------------------------------------

    if (

        len(st.session_state.steps) > 1

        and

        st.button(
            "➖ Remove Last Step",
            use_container_width=True
        )

    ):

        st.session_state.steps.pop()

        st.rerun()


    # -----------------------------------------------------
    # Step Inputs
    # -----------------------------------------------------

    updated_steps = []


    for index, step in enumerate(
        st.session_state.steps
    ):

        value = st.text_input(

            f"Step {index + 1}",

            value=step,

            key=f"dynamic_step_{index}"
        )


        updated_steps.append(
            value
        )


    st.session_state.steps = (
        updated_steps
    )


    st.divider()


    # =====================================================
    # CARD
    # =====================================================

    st.markdown("### 🟦 Card")


    card_width = st.slider(

        "Card Width",

        min_value=3.5,

        max_value=7.0,

        value=float(
            config_data.get(
                "card_width",
                5.0
            )
        ),

        step=0.1
    )


    card_height = st.slider(

        "Card Height",

        min_value=0.50,

        max_value=1.20,

        value=float(
            config_data.get(
                "card_height",
                0.75
            )
        ),

        step=0.05
    )


    font_size = st.slider(

        "Font Size",

        min_value=18,

        max_value=40,

        value=int(
            config_data.get(
                "font_size",
                30
            )
        ),

        step=1
    )


    st.divider()


    # =====================================================
    # SPACING
    # =====================================================

    st.markdown("### ↕️ Spacing")


    vertical_gap = st.slider(

        "Vertical Gap",

        min_value=0.20,

        max_value=1.0,

        value=float(
            config_data.get(
                "vertical_gap",
                0.40
            )
        ),

        step=0.05
    )


    st.divider()


    # =====================================================
    # ANIMATION
    # =====================================================

    st.markdown("### 🎬 Animation")


    animation_speed = st.slider(

        "Animation Speed",

        min_value=0.5,

        max_value=2.0,

        value=float(
            config_data.get(
                "animation_speed",
                1.0
            )
        ),

        step=0.1
    )


    show_arrows = st.checkbox(

        "Show Arrows",

        value=bool(
            config_data.get(
                "show_arrows",
                True
            )
        )
    )


    animate_step_by_step = st.checkbox(

        "Step-by-Step Animation",

        value=bool(
            config_data.get(
                "animate_step_by_step",
                True
            )
        )
    )


    # Green highlight intentionally disabled

    highlight_last = False


    st.divider()


    # =====================================================
    # QUALITY
    # =====================================================

    st.markdown("### 🎥 Render Quality")


    quality = st.selectbox(

        "Quality",

        [
            "Low",
            "Medium",
            "High",
            "Production"
        ],

        index=0
    )


# =========================================================
# FINAL CONFIG
# =========================================================

new_config = {

    "steps": st.session_state.steps,

    "card_width": card_width,

    "card_height": card_height,

    "font_size": font_size,

    "arrow_size": 35,

    "vertical_gap": vertical_gap,

    "animation_speed": animation_speed,

    "show_arrows": show_arrows,

    "animate_step_by_step":
        animate_step_by_step,

    "highlight_last": False
}


# =========================================================
# MAIN COLUMNS
# =========================================================

left_col, right_col = st.columns(

    [1, 1.4],

    gap="large"
)


# =========================================================
# LEFT COLUMN
# =========================================================

with left_col:

    st.subheader(
        "📋 Diagram Preview"
    )


    with st.container(
        border=True
    ):

        for index, step in enumerate(
            st.session_state.steps
        ):

            st.markdown(

                f"""
                <div class="preview-card">
                    {step}
                </div>
                """,

                unsafe_allow_html=True
            )


            if (

                index
                <
                len(st.session_state.steps) - 1

                and

                show_arrows

            ):

                st.markdown(

                    """
                    <div class="preview-arrow">
                        ↓
                    </div>
                    """,

                    unsafe_allow_html=True
                )


    st.write("")


    # =====================================================
    # SAVE
    # =====================================================

    if st.button(

        "💾 Save Configuration",

        use_container_width=True
    ):

        save_config(
            new_config
        )

        st.success(
            "Configuration saved."
        )


    # =====================================================
    # RENDER
    # =====================================================

    render_clicked = st.button(

        "🎬 Render Animation",

        type="primary",

        use_container_width=True
    )


# =========================================================
# RIGHT COLUMN
# =========================================================

with right_col:

    st.subheader(
        "🎥 Rendered Video"
    )


    if render_clicked:

        # ---------------------------------------------
        # Save
        # ---------------------------------------------

        save_config(
            new_config
        )


        # ---------------------------------------------
        # Render
        # ---------------------------------------------

        with st.spinner(
            "Rendering Manim animation..."
        ):

            success, output = (
                render_animation(
                    quality
                )
            )


        if success:

            st.success(
                "Animation rendered successfully."
            )


            video_file = (
                find_latest_video()
            )


            if video_file:

                st.video(
                    str(video_file)
                )


                with open(
                    video_file,
                    "rb"
                ) as video:

                    st.download_button(

                        "⬇️ Download Video",

                        data=video,

                        file_name="ArrayDiagram.mp4",

                        mime="video/mp4",

                        use_container_width=True
                    )


            else:

                st.warning(
                    "Video file नहीं मिला."
                )


        else:

            st.error(
                "Manim render failed."
            )


            with st.expander(
                "🔍 Show Render Error"
            ):

                st.code(
                    output
                )


    else:

        video_file = (
            find_latest_video()
        )


        if video_file:

            st.video(
                str(video_file)
            )


            with open(
                video_file,
                "rb"
            ) as video:

                st.download_button(

                    "⬇️ Download Video",

                    data=video,

                    file_name="ArrayDiagram.mp4",

                    mime="video/mp4",

                    use_container_width=True
                )

        else:

            st.info(
                "🎬 Render Animation दबाकर video generate करें."
            )


# =========================================================
# JSON
# =========================================================

with st.expander(
    "🔧 Current JSON Configuration"
):

    st.json(
        new_config
    )
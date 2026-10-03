import json
import subprocess
from pathlib import Path

import streamlit as st


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_PATH = PROJECT_ROOT / "config" / "basic_code.json"
SCENE_PATH = PROJECT_ROOT / "scenes" / "basic_code.py"

MEDIA_DIR = PROJECT_ROOT / "media"
OUTPUT_DIR = PROJECT_ROOT / "output"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NumPy Basic Code",
    page_icon="🔢",
    layout="wide",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .main-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        color: #9CA3AF;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 650;
        margin-top: 0.8rem;
        margin-bottom: 0.6rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DEFAULT CONFIG
# ============================================================

DEFAULT_CONFIG = {
    "array": [
        10,
        20,
        30,
        40
    ],
    "array_label": "ARRAY",
    "index_label": "INDEX",
    "element_label": "Each value is an element",
    "animation_speed": 1.0
}


# ============================================================
# CONFIG HELPERS
# ============================================================

def load_config():

    if not CONFIG_PATH.exists():
        return DEFAULT_CONFIG.copy()

    try:

        with open(
            CONFIG_PATH,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        return data

    except Exception as error:

        st.error(
            f"Configuration load failed: {error}"
        )

        return DEFAULT_CONFIG.copy()


def save_config(data):

    CONFIG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        CONFIG_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )


# ============================================================
# SESSION STATE
# ============================================================

if "config" not in st.session_state:

    st.session_state.config = load_config()


data = st.session_state.config


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🔢 NumPy — Basic Code Animation</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="sub-title">'
    'Array → Index → Element mental model'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Animation Settings")

    data["animation_speed"] = st.slider(
        "Animation Speed",
        min_value=0.5,
        max_value=2.0,
        value=float(
            data.get(
                "animation_speed",
                1.0,
            )
        ),
        step=0.1,
    )

    st.divider()

    st.caption(
        "Render: 1920 × 1080 • 60 FPS"
    )


# ============================================================
# ARRAY SECTION
# ============================================================

st.markdown(
    '<div class="section-title">📦 Array</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Array ke elements yahan modify karo."
)


# ------------------------------------------------------------
# ARRAY CONTROLS
# ------------------------------------------------------------

col1, col2, col3 = st.columns(
    [1, 1, 1]
)


with col1:

    if st.button(
        "➕ Add Element",
        use_container_width=True,
    ):

        data["array"].append(0)

        st.rerun()


with col2:

    if st.button(
        "➖ Remove Last",
        use_container_width=True,
    ):

        if len(data["array"]) > 1:

            data["array"].pop()

            st.rerun()


with col3:

    if st.button(
        "🔄 Reset Array",
        use_container_width=True,
    ):

        data["array"] = [
            10,
            20,
            30,
            40
        ]

        st.rerun()


# ============================================================
# ARRAY ELEMENT EDITORS
# ============================================================

st.markdown("### Elements")

new_array = []

for i, value in enumerate(
    data["array"]
):

    col1, col2 = st.columns(
        [1, 5]
    )

    with col1:

        st.markdown(
            f"**Index {i}**"
        )

    with col2:

        new_value = st.text_input(
            f"Value {i}",
            value=str(value),
            key=f"array_value_{i}",
            label_visibility="collapsed",
        )

        # Try to preserve numeric values
        try:

            if "." in new_value:

                converted_value = float(
                    new_value
                )

            else:

                converted_value = int(
                    new_value
                )

        except ValueError:

            converted_value = new_value

        new_array.append(
            converted_value
        )


data["array"] = new_array


# ============================================================
# ARRAY LABELS
# ============================================================

st.markdown(
    '<div class="section-title">🏷️ Labels</div>',
    unsafe_allow_html=True,
)

label_col1, label_col2, label_col3 = st.columns(
    3
)


with label_col1:

    data["array_label"] = st.text_input(
        "Array Label",
        value=data.get(
            "array_label",
            "ARRAY",
        ),
    )


with label_col2:

    data["index_label"] = st.text_input(
        "Index Label",
        value=data.get(
            "index_label",
            "INDEX",
        ),
    )


with label_col3:

    data["element_label"] = st.text_input(
        "Element Label",
        value=data.get(
            "element_label",
            "Each value is an element",
        ),
    )


# ============================================================
# LIVE ARRAY PREVIEW
# ============================================================

st.markdown(
    '<div class="section-title">👀 Array Preview</div>',
    unsafe_allow_html=True,
)

preview = ", ".join(
    str(value)
    for value in data["array"]
)

st.code(
    f'arr = np.array([{preview}])',
    language="python",
)


# ============================================================
# SAVE CONFIGURATION
# ============================================================

st.divider()

save_col, reload_col = st.columns(
    2
)


with save_col:

    if st.button(
        "💾 Save Configuration",
        type="primary",
        use_container_width=True,
    ):

        save_config(data)

        st.success(
            "Configuration saved."
        )


with reload_col:

    if st.button(
        "🔄 Reload JSON",
        use_container_width=True,
    ):

        st.session_state.config = load_config()

        st.rerun()


# ============================================================
# JSON PREVIEW
# ============================================================

with st.expander(
    "📄 Show JSON"
):

    st.json(
        data
    )


# ============================================================
# RENDER
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🎬 Render</div>',
    unsafe_allow_html=True,
)

if st.button(
    "🎬 Render 1080p • 60 FPS",
    type="primary",
    use_container_width=True,
):

    # --------------------------------------------
    # Save configuration first
    # --------------------------------------------

    save_config(data)

    MEDIA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------
    # Manim command
    # --------------------------------------------

    command = [
        "manim",
        "-p",
        "--resolution",
        "1920,1080",
        "--fps",
        "60",
        str(SCENE_PATH),
        "BasicCode",
    ]

    st.code(
        " ".join(
            f'"{part}"'
            if " " in part
            else part
            for part in command
        ),
        language="powershell",
    )

    # --------------------------------------------
    # Run Manim
    # --------------------------------------------

    with st.spinner(
        "Rendering animation..."
    ):

        try:

            result = subprocess.run(
                command,
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
            )

        except Exception as error:

            st.error(
                f"Manim start nahi ho saka:\n\n{error}"
            )

            st.stop()

    # --------------------------------------------
    # Render result
    # --------------------------------------------

    if result.returncode != 0:

        st.error(
            "❌ Render failed."
        )

        with st.expander(
            "Manim Error"
        ):

            st.code(
                result.stderr,
                language="text",
            )

        st.stop()

    # --------------------------------------------
    # Find generated video
    # --------------------------------------------

    video_files = list(
        MEDIA_DIR.rglob(
            "BasicCode.mp4"
        )
    )

    if not video_files:

        # fallback
        video_files = list(
            PROJECT_ROOT.rglob(
                "BasicCode.mp4"
            )
        )

    if not video_files:

        st.warning(
            "Render complete hua, "
            "lekin BasicCode.mp4 locate nahi hua."
        )

        with st.expander(
            "Manim Output"
        ):

            st.code(
                result.stdout,
                language="text",
            )

        st.stop()

    # Latest file
    video_file = max(
        video_files,
        key=lambda path: path.stat().st_mtime,
    )

    # --------------------------------------------
    # Preview
    # --------------------------------------------

    st.success(
        "✅ Render complete!"
    )

    st.video(
        str(video_file)
    )

    # --------------------------------------------
    # Download
    # --------------------------------------------

    with open(
        video_file,
        "rb",
    ) as video:

        st.download_button(
            label="⬇️ Download Video",
            data=video,
            file_name="basic_code.mp4",
            mime="video/mp4",
            use_container_width=True,
        )

import json
import subprocess
from pathlib import Path

import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NumPy Operation Animator",
    page_icon="🔢",
    layout="wide",
)


# =========================================================
# TITLE
# =========================================================

st.title("🔢 NumPy Operation Animator")

st.caption(
    "Control panel for NumPy Manim animations"
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def parse_value(value):
    """
    Convert string input into int or float.

    Examples:
        "5"     -> 5
        "5.0"   -> 5
        "5.5"   -> 5.5
        "-10"   -> -10
    """

    value = value.strip()

    number = float(value)

    if number.is_integer():
        return int(number)

    return number


def format_value(value):
    """
    Display numbers cleanly.

    Examples:
        5       -> "5"
        5.0     -> "5"
        5.25    -> "5.25"
        True    -> "True"
    """

    if isinstance(value, bool):
        return str(value)

    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


# =========================================================
# MAIN COLUMNS
# =========================================================

left, center, right = st.columns(
    [1.15, 1.7, 1.15],
    gap="large",
)


# =========================================================
# LEFT — OPERATION + ARRAY
# =========================================================

with left:

    st.subheader("Operation")

    operation = st.selectbox(
        "NumPy Operation",
        [
            "Addition",
            "Subtraction",
            "Multiplication",
            "Division",
            "Power",
            "Modulus",
            "Comparison",
            "Broadcasting",
            "Sum",
            "Mean",
            "Minimum",
            "Maximum",
            "Dot Product",
            "Matrix Multiplication",
            "Transpose",
        ],
        index=2,
    )


    # -----------------------------------------------------
    # INPUT ARRAY
    # -----------------------------------------------------

    st.subheader("Input Array")

    input_array = st.text_input(
        "Values",
        value="5, 10, 15, 20",
        help="Example: 5, 10, 15, 20",
    )


    # -----------------------------------------------------
    # CONVERT STRING → LIST
    # -----------------------------------------------------

    try:

        values = [
            parse_value(x)
            for x in input_array.split(",")
            if x.strip()
        ]

        array_size = len(values)

    except ValueError:

        values = []

        array_size = 0

        st.error(
            "Array values comma-separated numbers hone chahiye."
        )


    st.metric(
        "Array Size",
        array_size,
    )


    # -----------------------------------------------------
    # OPERAND
    # -----------------------------------------------------

    st.subheader("Operand")

    operand = st.number_input(
        "Value",
        value=2.0,
        step=1.0,
    )


# =========================================================
# CENTER — PREVIEW
# =========================================================

with center:

    st.subheader("Preview")


    # -----------------------------------------------------
    # INPUT PREVIEW
    # -----------------------------------------------------

    if values:

        input_text = "   ".join(
            f"[ {format_value(v)} ]"
            for v in values
        )

    else:

        input_text = "[ Invalid Array ]"


    st.markdown("### Input")

    st.code(
        input_text,
        language="text",
    )


    # -----------------------------------------------------
    # OPERATION SYMBOL
    # -----------------------------------------------------

    st.markdown("### Operation")

    operation_symbols = {

        "Addition": "+",

        "Subtraction": "−",

        "Multiplication": "×",

        "Division": "÷",

        "Power": "^",

        "Modulus": "%",

        "Comparison": ">",

        "Broadcasting": "↔",

        "Sum": "Σ",

        "Mean": "μ",

        "Minimum": "min",

        "Maximum": "max",

        "Dot Product": "·",

        "Matrix Multiplication": "@",

        "Transpose": "T",

    }


    symbol = operation_symbols.get(
        operation,
        "?",
    )


    operand_operations = {
        "Addition",
        "Subtraction",
        "Multiplication",
        "Division",
        "Power",
        "Modulus",
        "Comparison",
    }


    operand_text = (
        f" {format_value(operand)}"
        if operation in operand_operations
        else ""
    )


    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:32px;
            font-weight:700;
            padding:10px;
            color:#FFD166;
        ">
            {symbol}{operand_text}
        </div>
        """,
        unsafe_allow_html=True,
    )


    # -----------------------------------------------------
    # OUTPUT PREVIEW
    # -----------------------------------------------------

    st.markdown("### Output")

    results = None


    if values:

        try:

            if operation == "Addition":

                results = [
                    v + operand
                    for v in values
                ]


            elif operation == "Subtraction":

                results = [
                    v - operand
                    for v in values
                ]


            elif operation == "Multiplication":

                results = [
                    v * operand
                    for v in values
                ]


            elif operation == "Division":

                if operand == 0:

                    st.warning(
                        "Division by zero allowed nahi hai."
                    )

                else:

                    results = [
                        v / operand
                        for v in values
                    ]


            elif operation == "Power":

                results = [
                    v ** operand
                    for v in values
                ]


            elif operation == "Modulus":

                if operand == 0:

                    st.warning(
                        "Modulus by zero allowed nahi hai."
                    )

                else:

                    results = [
                        v % operand
                        for v in values
                    ]


            elif operation == "Comparison":

                results = [
                    v > operand
                    for v in values
                ]


            elif operation == "Sum":

                results = [
                    sum(values)
                ]


            elif operation == "Mean":

                results = [
                    sum(values) / len(values)
                ]


            elif operation == "Minimum":

                results = [
                    min(values)
                ]


            elif operation == "Maximum":

                results = [
                    max(values)
                ]


            else:

                # Operations not implemented in
                # the simple preview yet.
                results = values


        except Exception as error:

            st.error(
                f"Preview calculation error: {error}"
            )


    # -----------------------------------------------------
    # OUTPUT DISPLAY
    # -----------------------------------------------------

    if results is not None:

        output_text = "   ".join(
            f"[ {format_value(v)} ]"
            for v in results
        )

        st.code(
            output_text,
            language="text",
        )


# =========================================================
# RIGHT — LAYOUT & POSITION
# =========================================================

with right:

    st.subheader("Layout")


    # -----------------------------------------------------
    # DIRECTION
    # -----------------------------------------------------

    layout = st.radio(
        "Direction",
        [
            "Vertical",
            "Horizontal",
        ],
        horizontal=True,
        label_visibility="collapsed",
    )


    # -----------------------------------------------------
    # POSITION
    # -----------------------------------------------------

    st.markdown("**Position**")

    pos_col1, pos_col2 = st.columns(2)


    with pos_col1:

        st.caption("Input")

        input_x = st.number_input(
            "X",
            min_value=-6.0,
            max_value=6.0,
            value=0.0,
            step=0.1,
            key="input_x",
        )

        input_y = st.number_input(
            "Y",
            min_value=-3.5,
            max_value=3.5,
            value=1.15,
            step=0.1,
            key="input_y",
        )


    with pos_col2:

        st.caption("Output")

        output_x = st.number_input(
            "X",
            min_value=-6.0,
            max_value=6.0,
            value=0.0,
            step=0.1,
            key="output_x",
        )

        output_y = st.number_input(
            "Y",
            min_value=-3.5,
            max_value=3.5,
            value=-1.55,
            step=0.1,
            key="output_y",
        )


    # -----------------------------------------------------
    # ARRAY
    # -----------------------------------------------------

    st.markdown("**Array**")

    array_col1, array_col2 = st.columns(2)


    with array_col1:

        cell_size = st.slider(
            "Cell Size",
            0.45,
            1.5,
            0.95,
            0.05,
        )


    with array_col2:

        cell_spacing = st.slider(
            "Cell Gap",
            0.0,
            0.30,
            0.08,
            0.01,
        )


    # -----------------------------------------------------
    # CANVAS MARGINS
    # -----------------------------------------------------

    st.markdown("**Canvas Margins**")

    margin_col1, margin_col2 = st.columns(2)


    with margin_col1:

        left_space = st.slider(
            "Left",
            0.0,
            2.0,
            0.8,
            0.05,
        )

        top_space = st.slider(
            "Top",
            0.0,
            2.0,
            0.4,
            0.05,
        )


    with margin_col2:

        right_space = st.slider(
            "Right",
            0.0,
            2.0,
            0.8,
            0.05,
        )

        bottom_space = st.slider(
            "Bottom",
            0.0,
            2.0,
            0.3,
            0.05,
        )


# =========================================================
# CURRENT SETTINGS
# =========================================================

st.divider()

st.subheader("Current Settings")

settings_col1, settings_col2, settings_col3 = st.columns(3)


with settings_col1:

    st.write(
        f"**Operation:** {operation}"
    )

    st.write(
        f"**Array:** {values}"
    )

    st.write(
        f"**Array Size:** {array_size}"
    )


with settings_col2:

    st.write(
        f"**Layout:** {layout}"
    )

    st.write(
        f"**Input:** ({input_x}, {input_y})"
    )

    st.write(
        f"**Output:** ({output_x}, {output_y})"
    )


with settings_col3:

    st.write(
        f"**Cell Size:** {cell_size}"
    )

    st.write(
        f"**Cell Spacing:** {cell_spacing}"
    )

    st.write(
        f"**Operand:** {operand}"
    )


# =========================================================
# STATUS
# =========================================================

st.success(
    "Array, Layout aur Spacing controls ready."
)


# =========================================================
# MANIM RENDER PREVIEW
# =========================================================

st.divider()

st.subheader("🎬 Manim Preview")


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_DIR = PROJECT_ROOT / "config"

CONFIG_FILE = (
    CONFIG_DIR / "numpy_operation.json"
)

SCENE_FILE = (
    PROJECT_ROOT
    / "scenes"
    / "numpy_preview.py"
)

MEDIA_DIR = (
    PROJECT_ROOT
    / "output"
    / "manim"
)


# =========================================================
# RENDER BUTTON
# =========================================================

render_clicked = st.button(
    "▶ Render Preview",
    type="primary",
    use_container_width=True,
)


if render_clicked:

    # =====================================================
    # VALIDATION
    # =====================================================

    if not values:

        st.error(
            "Pehle valid input array enter karo."
        )

        st.stop()


    if not SCENE_FILE.exists():

        st.error(
            "numpy_preview.py nahi mili."
        )

        st.code(
            str(SCENE_FILE),
            language="text",
        )

        st.stop()


    try:

        # =================================================
        # CREATE CONFIG DIRECTORY
        # =================================================

        CONFIG_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )


        # =================================================
        # BUILD JSON CONFIG
        # =================================================

        animation_config = {

            "operation": operation,

            "input_values": values,

            "operand": operand,

            "layout": layout.lower(),

            "input_position": {
                "x": input_x,
                "y": input_y,
            },

            "output_position": {
                "x": output_x,
                "y": output_y,
            },

            "cell_size": cell_size,

            "cell_spacing": cell_spacing,

            "number_font_size": 29,

            "index_font_size": 21,

            "show_indices": True,

            "show_code": True,

            "animation_speed": 1.0,

            "element_delay": 0.15,

            "margins": {
                "left": left_space,
                "right": right_space,
                "top": top_space,
                "bottom": bottom_space,
            },
        }


        # =================================================
        # WRITE JSON
        # =================================================

        with open(
            CONFIG_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                animation_config,
                file,
                indent=4,
            )


        st.success(
            "✓ Configuration saved."
        )


        # =================================================
        # CREATE MEDIA DIRECTORY
        # =================================================

        MEDIA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )


        # =================================================
        # MANIM COMMAND
        # =================================================

        command = [

            "python",

            "-m",

            "manim",

            "-ql",

            "--media_dir",

            str(MEDIA_DIR),

            str(SCENE_FILE),

            "StyleTest",
        ]


        # =================================================
        # RENDER
        # =================================================

        with st.spinner(
            "🎬 Manim animation render ho rahi hai..."
        ):

            result = subprocess.run(

                command,

                cwd=str(PROJECT_ROOT),

                capture_output=True,

                text=True,
            )


        # =================================================
        # RENDER FAILED
        # =================================================

        if result.returncode != 0:

            st.error(
                "❌ Manim render failed."
            )

            with st.expander(
                "🔍 Show Manim Error"
            ):

                if result.stderr:

                    st.code(
                        result.stderr,
                        language="text",
                    )

                elif result.stdout:

                    st.code(
                        result.stdout,
                        language="text",
                    )

                else:

                    st.code(
                        "Unknown Manim error.",
                        language="text",
                    )

            st.stop()


        # =================================================
        # FIND MP4
        # =================================================

        video_files = list(
            MEDIA_DIR.rglob("*.mp4")
        )


        if not video_files:

            st.error(
                "❌ Render complete hua, "
                "lekin MP4 file nahi mili."
            )

            st.stop()


        # =================================================
        # GET LATEST VIDEO
        # =================================================

        video_file = max(
            video_files,
            key=lambda file: file.stat().st_mtime,
        )


        # =================================================
        # SUCCESS
        # =================================================

        st.success(
            "✅ Animation successfully rendered!"
        )


        # =================================================
        # VIDEO PREVIEW
        # =================================================

        st.markdown("### 🎥 Preview")

        # Video preview
        st.video(
            str(video_file)
        )

        # Download button
        with open(video_file, "rb") as video:

            st.download_button(
                label="⬇️ Download Video",
                data=video,
                file_name=video_file.name,
                mime="video/mp4",
                use_container_width=True,
            )

        st.caption(
            f"Output: {video_file}"
        )


    except Exception as error:

        st.error(
            "❌ Render process mein error aaya."
        )

        with st.expander(
            "🔍 Error Details"
        ):

            st.exception(error)

import json
import subprocess
from pathlib import Path
from copy import deepcopy

import streamlit as st


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_PATH = PROJECT_ROOT / "config" / "question_diagram.json"
SCENE_PATH = PROJECT_ROOT / "scenes" / "question_diagram.py"

MEDIA_DIR = PROJECT_ROOT / "media"
OUTPUT_DIR = PROJECT_ROOT / "output"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NumPy Question Diagram",
    page_icon="🧠",
    layout="wide",
)


# ============================================================
# DEFAULT CONFIG
# ============================================================

DEFAULT_CONFIG = {
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


# ============================================================
# LOAD CONFIG FROM DISK
# ============================================================

def load_config():
    """
    Always reads the actual question_diagram.json file.
    """

    if not CONFIG_PATH.exists():

        CONFIG_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        save_config(
            deepcopy(DEFAULT_CONFIG)
        )

        return deepcopy(DEFAULT_CONFIG)

    try:

        with open(
            CONFIG_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data

    except Exception as error:

        st.error(
            f"Could not read config file: {error}"
        )

        return deepcopy(DEFAULT_CONFIG)


# ============================================================
# SAVE CONFIG TO DISK
# ============================================================

def save_config(data):
    """
    Writes current configuration directly to
    question_diagram.json.
    """

    CONFIG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_path = CONFIG_PATH.with_suffix(
        ".json.tmp"
    )

    try:

        with open(
            temp_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        temp_path.replace(
            CONFIG_PATH
        )

        return True

    except Exception as error:

        if temp_path.exists():
            temp_path.unlink()

        st.error(
            f"Could not save config: {error}"
        )

        return False


# ============================================================
# UPDATE + SAVE
# ============================================================

def update_config(data):

    st.session_state.config_data = deepcopy(
        data
    )

    save_config(
        st.session_state.config_data
    )


# ============================================================
# FIND LATEST VIDEO
# ============================================================

def find_rendered_video():

    if not MEDIA_DIR.exists():
        return None

    videos = list(
        MEDIA_DIR.rglob(
            "QuestionDiagram.mp4"
        )
    )

    if not videos:
        return None

    videos.sort(
        key=lambda path: path.stat().st_mtime,
        reverse=True
    )

    return videos[0]


# ============================================================
# RENDER SCENE
# ============================================================

def render_scene():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    command = [
        "manim",

        "-p",

        "--resolution",
        "1920,1080",

        "--fps",
        "60",

        str(SCENE_PATH),

        "QuestionDiagram",
    ]

    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "config_data" not in st.session_state:

    st.session_state.config_data = load_config()


if "config_version" not in st.session_state:

    st.session_state.config_version = 0


data = st.session_state.config_data


# ============================================================
# HEADER
# ============================================================

st.title(
    "🧠 NumPy — Question Diagram"
)

st.caption(
    "Create and render the NumPy Array Fundamentals opening scene."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "⚙️ Scene Controls"
    )

    # --------------------------------------------------------
    # Animation Speed
    # --------------------------------------------------------

    animation_speed = st.slider(

        "Animation Speed",

        min_value=0.5,

        max_value=2.0,

        value=float(
            data.get(
                "animation_speed",
                1.0
            )
        ),

        step=0.1,

        key=f"animation_speed_{st.session_state.config_version}",
    )


    # --------------------------------------------------------
    # Question Delay
    # --------------------------------------------------------

    question_delay = st.slider(

        "Question Delay",

        min_value=0.0,

        max_value=3.0,

        value=float(
            data.get(
                "question_delay",
                0.65
            )
        ),

        step=0.05,

        key=f"question_delay_{st.session_state.config_version}",
    )

    st.caption(
        "Time between questions."
    )


    # --------------------------------------------------------
    # Flow Delay
    # --------------------------------------------------------

    flow_delay = st.slider(

        "Flow Delay After Questions",

        min_value=0.0,

        max_value=5.0,

        value=float(
            data.get(
                "flow_delay",
                1.5
            )
        ),

        step=0.1,

        key=f"flow_delay_{st.session_state.config_version}",
    )

    st.caption(
        "Time before ARRAY DIMENSION flow."
    )


    # --------------------------------------------------------
    # Detect timing changes
    # --------------------------------------------------------

    timing_changed = (
        animation_speed
        != data.get("animation_speed", 1.0)
        or
        question_delay
        != data.get("question_delay", 0.65)
        or
        flow_delay
        != data.get("flow_delay", 1.5)
    )


    if timing_changed:

        data["animation_speed"] = animation_speed
        data["question_delay"] = question_delay
        data["flow_delay"] = flow_delay

        update_config(
            data
        )


    # --------------------------------------------------------
    # Render settings
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🎬 Render Settings"
    )

    st.info(
        """
**Resolution:** 1920 × 1080

**FPS:** 60

**Format:** MP4
"""
    )


    # --------------------------------------------------------
    # Reload JSON
    # --------------------------------------------------------

    st.divider()

    if st.button(
        "🔄 Reload JSON",
        use_container_width=True
    ):

        st.session_state.config_data = load_config()

        st.session_state.config_version += 1

        st.rerun()


# ============================================================
# MAIN COLUMNS
# ============================================================

left_col, right_col = st.columns(
    [1, 1],
    gap="large"
)


# ============================================================
# LEFT — NUMPY ARRAY
# ============================================================

with left_col:

    st.subheader(
        "🔢 NumPy Array"
    )

    st.caption(
        "Array is generated directly from question_diagram.json."
    )


    array = data.get(
        "array",
        []
    )


    # --------------------------------------------------------
    # Shape
    # --------------------------------------------------------

    rows = len(array)

    columns = (
        len(array[0])
        if rows > 0
        else 0
    )

    elements = sum(
        len(row)
        for row in array
    )


    info1, info2 = st.columns(2)

    with info1:

        st.metric(
            "Shape",
            f"({rows}, {columns})"
        )

    with info2:

        st.metric(
            "Elements",
            elements
        )


    st.divider()


    # ========================================================
    # ARRAY EDITOR
    # ========================================================

    edited_array = []

    delete_row_index = None


    for row_index, row in enumerate(array):

        if not row:
            continue


        cols = st.columns(
            len(row) + 1
        )


        new_row = []


        for col_index, value in enumerate(row):

            widget_key = (
                f"array_"
                f"{st.session_state.config_version}_"
                f"{row_index}_"
                f"{col_index}"
            )


            new_value = cols[col_index].number_input(

                f"R{row_index + 1} C{col_index + 1}",

                value=float(value),

                step=1.0,

                key=widget_key,

            )


            if float(new_value).is_integer():

                new_value = int(
                    new_value
                )


            new_row.append(
                new_value
            )


        # ----------------------------------------------------
        # Delete Row
        # ----------------------------------------------------

        if cols[-1].button(
            "🗑️",
            key=(
                f"delete_row_"
                f"{st.session_state.config_version}_"
                f"{row_index}"
            )
        ):

            delete_row_index = row_index


        edited_array.append(
            new_row
        )


    # ========================================================
    # DELETE ROW
    # ========================================================

    if delete_row_index is not None:

        edited_array.pop(
            delete_row_index
        )

        data["array"] = edited_array

        update_config(
            data
        )

        st.session_state.config_version += 1

        st.rerun()


    # ========================================================
    # DETECT CELL CHANGES
    # ========================================================

    if edited_array != array:

        data["array"] = edited_array

        update_config(
            data
        )


    # ========================================================
    # ARRAY ACTIONS
    # ========================================================

    st.divider()

    action1, action2 = st.columns(2)


    # --------------------------------------------------------
    # ADD ROW
    # --------------------------------------------------------

    with action1:

        if st.button(
            "➕ Add Row",
            use_container_width=True
        ):

            current_array = deepcopy(
                data.get(
                    "array",
                    []
                )
            )


            if current_array:

                column_count = len(
                    current_array[0]
                )

                current_array.append(
                    [0] * column_count
                )

            else:

                current_array.append(
                    [0]
                )


            data["array"] = current_array

            update_config(
                data
            )

            st.session_state.config_version += 1

            st.rerun()


    # --------------------------------------------------------
    # ADD COLUMN
    # --------------------------------------------------------

    with action2:

        if st.button(
            "➕ Add Column",
            use_container_width=True
        ):

            current_array = deepcopy(
                data.get(
                    "array",
                    []
                )
            )


            if current_array:

                for row in current_array:

                    row.append(0)

            else:

                current_array = [
                    [0]
                ]


            data["array"] = current_array

            update_config(
                data
            )

            st.session_state.config_version += 1

            st.rerun()


    action3, action4 = st.columns(2)


    # --------------------------------------------------------
    # REMOVE COLUMN
    # --------------------------------------------------------

    with action3:

        if st.button(
            "➖ Remove Column",
            use_container_width=True
        ):

            current_array = deepcopy(
                data.get(
                    "array",
                    []
                )
            )


            for row in current_array:

                if row:

                    row.pop()


            data["array"] = current_array

            update_config(
                data
            )

            st.session_state.config_version += 1

            st.rerun()


    # --------------------------------------------------------
    # RESET ARRAY
    # --------------------------------------------------------

    with action4:

        if st.button(
            "↻ Reset Array",
            use_container_width=True
        ):

            data["array"] = deepcopy(
                DEFAULT_CONFIG["array"]
            )

            update_config(
                data
            )

            st.session_state.config_version += 1

            st.rerun()


# ============================================================
# RIGHT — FLOW
# ============================================================

with right_col:

    st.subheader(
        "🧩 Array Dimension Flow"
    )

    st.caption(
        "Every flow step is generated dynamically."
    )


    flow_steps = data.get(
        "flow_steps",
        []
    )


    edited_flow = []

    delete_flow_index = None


    for index, step in enumerate(flow_steps):

        col1, col2 = st.columns(
            [6, 1]
        )


        flow_key = (
            f"flow_"
            f"{st.session_state.config_version}_"
            f"{index}"
        )


        with col1:

            value = st.text_input(

                f"Step {index + 1}",

                value=str(step),

                key=flow_key,
            )


        with col2:

            if st.button(
                "🗑️",
                key=(
                    f"delete_flow_"
                    f"{st.session_state.config_version}_"
                    f"{index}"
                )
            ):

                delete_flow_index = index


        edited_flow.append(
            value
        )


    # --------------------------------------------------------
    # Delete Flow
    # --------------------------------------------------------

    if delete_flow_index is not None:

        edited_flow.pop(
            delete_flow_index
        )

        data["flow_steps"] = edited_flow

        update_config(
            data
        )

        st.session_state.config_version += 1

        st.rerun()


    # --------------------------------------------------------
    # Detect Flow Changes
    # --------------------------------------------------------

    if edited_flow != flow_steps:

        data["flow_steps"] = edited_flow

        update_config(
            data
        )


    # --------------------------------------------------------
    # Add Flow Step
    # --------------------------------------------------------

    if st.button(
        "➕ Add Flow Step",
        use_container_width=True
    ):

        current_flow = deepcopy(
            data.get(
                "flow_steps",
                []
            )
        )

        current_flow.append(
            "New Concept"
        )

        data["flow_steps"] = current_flow

        update_config(
            data
        )

        st.session_state.config_version += 1

        st.rerun()


# ============================================================
# QUESTIONS
# ============================================================

st.divider()

st.subheader(
    "❓ Questions"
)

st.caption(
    "Questions remain visible one below another in the animation."
)


questions = data.get(
    "questions",
    []
)


edited_questions = []

delete_question_index = None


for index, question in enumerate(questions):

    col1, col2 = st.columns(
        [8, 1]
    )


    question_key = (
        f"question_"
        f"{st.session_state.config_version}_"
        f"{index}"
    )


    with col1:

        value = st.text_input(

            f"Question {index + 1}",

            value=str(question),

            key=question_key,
        )


    with col2:

        if st.button(
            "🗑️",
            key=(
                f"delete_question_"
                f"{st.session_state.config_version}_"
                f"{index}"
            )
        ):

            delete_question_index = index


    edited_questions.append(
        value
    )


# ============================================================
# DELETE QUESTION
# ============================================================

if delete_question_index is not None:

    edited_questions.pop(
        delete_question_index
    )

    data["questions"] = edited_questions

    update_config(
        data
    )

    st.session_state.config_version += 1

    st.rerun()


# ============================================================
# DETECT QUESTION CHANGES
# ============================================================

if edited_questions != questions:

    data["questions"] = edited_questions

    update_config(
        data
    )


# ============================================================
# ADD QUESTION
# ============================================================

if st.button(
    "➕ Add Question",
    use_container_width=True
):

    current_questions = deepcopy(
        data.get(
            "questions",
            []
        )
    )

    current_questions.append(
        "New question?"
    )

    data["questions"] = current_questions

    update_config(
        data
    )

    st.session_state.config_version += 1

    st.rerun()


# ============================================================
# ACTION BUTTONS
# ============================================================

st.divider()

save_col, render_col, json_col = st.columns(3)


# ============================================================
# SAVE
# ============================================================

with save_col:

    if st.button(
        "💾 Save Configuration",
        use_container_width=True
    ):

        # Read current UI state
        st.session_state.config_data = data

        if save_config(data):

            st.success(
                "question_diagram.json updated successfully."
            )


# ============================================================
# RENDER
# ============================================================

with render_col:

    if st.button(
        "🎬 Render 1080p • 60 FPS",
        use_container_width=True
    ):

        # IMPORTANT:
        # Save latest configuration first.
        save_config(
            data
        )

        st.session_state.config_data = load_config()

        with st.spinner(
            "Rendering 1920 × 1080 • 60 FPS..."
        ):

            result = render_scene()


        if result.returncode == 0:

            st.success(
                "Render completed successfully!"
            )

            st.rerun()

        else:

            st.error(
                "Render failed."
            )

            with st.expander(
                "🔴 Render Error"
            ):

                st.code(
                    result.stderr
                    or result.stdout
                    or "Unknown error."
                )


# ============================================================
# SHOW ACTUAL JSON FILE
# ============================================================

with json_col:

    if st.button(
        "👁️ Show JSON",
        use_container_width=True
    ):

        # IMPORTANT:
        # DO NOT show session_state.
        # Read actual file from disk.
        actual_json = load_config()

        st.json(
            actual_json
        )


# ============================================================
# JSON FILE LOCATION
# ============================================================

st.divider()

st.subheader(
    "📄 JSON Source of Truth"
)

st.code(
    str(CONFIG_PATH),
    language="text"
)


# ============================================================
# RENDERED VIDEO
# ============================================================

st.divider()

st.subheader(
    "🎥 Rendered Video"
)


video_file = find_rendered_video()


if video_file and video_file.exists():

    st.success(
        "Latest render: 1920 × 1080 • 60 FPS"
    )


    st.video(
        str(video_file)
    )


    with open(
        video_file,
        "rb"
    ) as video:

        st.download_button(

            label="⬇️ Download 1080p • 60 FPS Video",

            data=video,

            file_name=(
                "question_diagram_1080p_60fps.mp4"
            ),

            mime="video/mp4",

            use_container_width=True,
        )

else:

    st.info(
        "No rendered video found yet. "
        "Click Render to generate the video."
    )


# ============================================================
# PROJECT INFORMATION
# ============================================================

with st.expander(
    "📁 Project Information"
):

    st.write(
        f"**Project Root:** `{PROJECT_ROOT}`"
    )

    st.write(
        f"**Config:** `{CONFIG_PATH}`"
    )

    st.write(
        f"**Scene:** `{SCENE_PATH}`"
    )

    st.write(
        f"**Media:** `{MEDIA_DIR}`"
    )

    st.write(
        "**Resolution:** 1920 × 1080"
    )

    st.write(
        "**FPS:** 60"
    )

    st.write(
        "**Format:** MP4"
    )
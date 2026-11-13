"""
modules/crop_helper.py - Module 2: Crop & Farming Helper
KrishiVaani (Voice of Agriculture)

Provides:
1. Dynamic crop selector synced with the farmer's profile in st.session_state.
2. Stage-by-stage agricultural guidance (Sowing, Vegetative, Flowering/Fruiting, Harvesting)
   covering fertilizer dosage, irrigation schedules, and pest/disease management.
3. Interactive task checklist and reminder management synced to active crops.
4. Pure English & Marathi mode rendering via translations.py.
"""

import streamlit as st
from sample_data import CROP_GUIDES
from translations import t, get_lang


def detect_crop_key(crop_name):
    """
    Helper function to map varied farmer crop profile strings
    (e.g., 'Grapes - Thomson Seedless (द्राक्ष)') to standardized CROP_GUIDES keys.
    """
    crop_lower = crop_name.lower()
    if "grape" in crop_lower or "द्राक्ष" in crop_lower:
        return "Grapes"
    elif "onion" in crop_lower or "कांदा" in crop_lower:
        return "Onion"
    elif "soybean" in crop_lower or "सोयाबीन" in crop_lower:
        return "Soybean"
    elif "sugarcane" in crop_lower or "ऊस" in crop_lower:
        return "Sugarcane"
    return "Grapes"


def render_crop_stages(crop_info):
    """Renders the 4 sequential agricultural growth stages inside interactive tabs."""
    stages = crop_info.get("stages", [])
    if not stages:
        st.info("Information for this crop will be available soon.")
        return

    tab_labels = [
        t("stage_1_tab"),
        t("stage_2_tab"),
        t("stage_3_tab"),
        t("stage_4_tab")
    ]
    
    tabs = st.tabs(tab_labels[:len(stages)])

    for index, stage in enumerate(stages):
        with tabs[index]:
            st.markdown(f"### {stage['stage_name']}")
            st.caption(f"⏱️ **{t('duration_label')}:** {stage['duration']}")

            col1, col2 = st.columns(2)
            
            with col1:
                with st.container(border=True):
                    st.markdown(f"#### 🧪 {t('fertilizer_heading')}")
                    st.write(stage["fertilizer"])
                
                with st.container(border=True):
                    st.markdown(f"#### 💧 {t('irrigation_heading')}")
                    st.write(stage["irrigation"])

            with col2:
                with st.container(border=True):
                    st.markdown(f"#### 🐛 {t('pest_heading')}")
                    st.write(stage["pest_disease"])
                
                with st.container(border=True):
                    st.markdown(f"#### 💡 {t('pro_tip_heading')}")
                    st.info(f"**Tip / सल्ला:** {stage['pro_tip']}")


def render_task_checklist(selected_crop_key):
    """
    Renders an interactive farm task checklist stored in st.session_state.crop_tasks.
    Farmers can toggle completion, view priority badges, and add new tasks.
    """
    st.markdown(f"### 📝 {t('checklist_title')}")
    st.caption(t("checklist_caption"))

    if "crop_tasks" not in st.session_state:
        st.session_state.crop_tasks = []

    tasks = st.session_state.crop_tasks

    # Filter selector: View tasks for current crop vs all crops
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        task_filter = st.radio(
            t("filter_tasks_label"),
            options=[t("filter_current_crop"), t("filter_all_tasks")],
            horizontal=True
        )

    # Filter tasks list
    if task_filter == t("filter_current_crop"):
        visible_tasks = [t_item for t_item in tasks if t_item.get("crop", "").lower() == selected_crop_key.lower()]
    else:
        visible_tasks = tasks

    # Progress Metric
    if visible_tasks:
        completed_count = sum(1 for item in visible_tasks if item.get("status", False))
        total_count = len(visible_tasks)
        progress = completed_count / total_count if total_count > 0 else 0
        st.progress(progress, text=f"{t('progress_label')}: {completed_count}/{total_count} {t('completed_label')} ({int(progress*100)}%)")
    else:
        st.caption("No pending tasks for this crop.")

    # Render individual task checkboxes
    for idx, task in enumerate(visible_tasks):
        # Priority badge formatting
        p_raw = task.get("priority", "Medium")
        if p_raw == "High":
            p_badge = f"🔴 {t('priority_high')}"
        elif p_raw == "Medium":
            p_badge = f"🟡 {t('priority_med')}"
        else:
            p_badge = f"🟢 {t('priority_low')}"
        
        with st.container(border=True):
            col_check, col_meta = st.columns([4, 2])
            
            with col_check:
                is_done = st.checkbox(
                    f"**{task['title']}**",
                    value=task.get("status", False),
                    key=f"task_check_{task.get('id', idx)}"
                )
                if is_done != task.get("status", False):
                    task["status"] = is_done
                    st.rerun()

            with col_meta:
                st.caption(f"🌾 **Crop:** {task.get('crop')} | **Stage:** {task.get('stage', 'General')}")
                st.markdown(f"**Priority:** `{p_badge}` | ⏰ **Due:** `{task.get('due_date', 'N/A')}`")

    st.markdown("<br>", unsafe_allow_html=True)

    # Expander to add a new customized task
    with st.expander(t("add_task_expander")):
        with st.form("add_new_task_form"):
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                new_title = st.text_input(t("task_desc_label"), placeholder="e.g. 0:52:34 drip fertigation or neem spray")
                new_crop = st.selectbox(
                    t("task_crop_label"),
                    options=["Grapes", "Onion", "Soybean", "Sugarcane", "General Farm"]
                )
            with t_col2:
                new_stage = st.text_input(t("task_stage_label"), placeholder="e.g. Flowering or Sowing")
                new_due = st.text_input(t("task_due_label"), placeholder="e.g. Next 3 Days / Upcoming")
                new_priority = st.selectbox(t("task_priority_label"), options=["High", "Medium", "Low"], index=1)

            submit_task = st.form_submit_button(t("btn_save_task"), use_container_width=True)
            if submit_task:
                if new_title.strip():
                    new_entry = {
                        "id": f"TSK-{len(tasks) + 1:03d}",
                        "crop": new_crop,
                        "title": new_title.strip(),
                        "stage": new_stage.strip() or "General",
                        "due_date": new_due.strip() or "Upcoming",
                        "priority": new_priority,
                        "status": False
                    }
                    st.session_state.crop_tasks.append(new_entry)
                    st.success(t("task_saved_success"))
                    st.rerun()
                else:
                    st.warning(t("task_input_warning"))


def render_crop_helper():
    """
    Main entry point for Module 2: Crop & Farming Helper.
    Syncs with farmer profile crops and renders stage-by-stage guidance and action checklist.
    """
    profile = st.session_state.get("farmer_profile", {})
    farmer_crops = profile.get("crops_grown", ["Grapes", "Onion", "Soybean"])

    # Top Header Banner
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #2e7d32 0%, #1565c0 100%);
                    padding: 20px 24px; border-radius: 12px; color: white; margin-bottom: 22px;">
            <h2 style="margin: 0; color: white;">🌱 {t('crop_helper_banner_title')}</h2>
            <p style="margin: 6px 0 0 0; font-size: 14px; opacity: 0.94;">
                {t('crop_helper_banner_subtitle')}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Crop Selector linked to farmer's active crops
    st.markdown(f"### 🌾 {t('select_crop_title')}")
    
    crop_options = {}
    for c_raw in farmer_crops:
        k = detect_crop_key(c_raw)
        if k in CROP_GUIDES:
            crop_options[f"🌿 {c_raw} ({t('your_farm_crop')})"] = k

    for k, v in CROP_GUIDES.items():
        if k not in crop_options.values():
            disp_crop = v['marathi_name'] if get_lang() == "mr" else v['display_name']
            crop_options[f"📖 {disp_crop} ({t('other_crop')})"] = k

    selected_label = st.selectbox(
        t("crop_name_label"),
        options=list(crop_options.keys()),
        index=0
    )
    
    selected_crop_key = crop_options[selected_label]
    crop_info = CROP_GUIDES.get(selected_crop_key, {})

    # Overview Metrics Card for Selected Crop
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"**{t('crop_name_label')}:** `{crop_info.get('display_name', selected_crop_key)}`")
            st.markdown(f"**{t('marathi_name_label')}:** `{crop_info.get('marathi_name', '')}`")
        with c2:
            st.markdown(f"**{t('season_label')}:** `{crop_info.get('season', 'N/A')}`")
        with c3:
            st.markdown(f"**{t('soil_label')}:** {crop_info.get('recommended_soil', 'N/A')}")

    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Stage-by-Stage Guidance
    render_crop_stages(crop_info)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # 2. Interactive Task Checklist & Reminders
    render_task_checklist(selected_crop_key)

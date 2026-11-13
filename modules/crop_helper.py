"""
modules/crop_helper.py - Module 2: Crop & Farming Helper
KrishiVaani (Voice of Agriculture)

Provides:
1. Dynamic crop selector synced with the farmer's profile in st.session_state.
2. Stage-by-stage agricultural guidance (Sowing, Vegetative, Flowering/Fruiting, Harvesting)
   covering fertilizer dosage, irrigation schedules, and pest/disease management.
3. Interactive task checklist and reminder management synced to active crops.
"""

import streamlit as st
from sample_data import CROP_GUIDES


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
    return "Grapes"  # Default fallback


def render_crop_stages(crop_info):
    """Renders the 4 sequential agricultural growth stages inside interactive tabs."""
    stages = crop_info.get("stages", [])
    if not stages:
        st.info("या पिकाची टप्प्याटप्प्याने माहिती लवकरच उपलब्ध होईल.")
        return

    tab_labels = [
        "🌱 टप्पा १: लागवड/छाटणी",
        "🌿 टप्पा २: शाकीय वाढ",
        "🌸 टप्पा ३: फुलधारणा/फळधारणा",
        "🌾 टप्पा ४: काढणी व साठवण"
    ]
    
    # Ensure tab count matches stage count
    tabs = st.tabs(tab_labels[:len(stages)])

    for index, stage in enumerate(stages):
        with tabs[index]:
            st.markdown(f"### {stage['stage_name']}")
            st.caption(f"⏱️ **कालावधी (Duration / Window):** {stage['duration']}")

            col1, col2 = st.columns(2)
            
            with col1:
                with st.container(border=True):
                    st.markdown("#### 🧪 खत व्यवस्थापन (Fertilizer Management)")
                    st.write(stage["fertilizer"])
                
                with st.container(border=True):
                    st.markdown("#### 💧 पाणी व्यवस्थापन (Irrigation Schedule)")
                    st.write(stage["irrigation"])

            with col2:
                with st.container(border=True):
                    st.markdown("#### 🐛 रोग व कीड नियंत्रण (Pest & Disease Prevention)")
                    st.write(stage["pest_disease"])
                
                with st.container(border=True):
                    st.markdown("#### 💡 कृषी तज्ज्ञ सल्ला (Pro Agronomy Tip)")
                    st.info(f"**टीप:** {stage['pro_tip']}")


def render_task_checklist(selected_crop_key):
    """
    Renders an interactive farm task checklist stored in st.session_state.crop_tasks.
    Farmers can toggle completion, view priority badges, and add new tasks.
    """
    st.markdown("### 📝 शेतकाम चेकलिस्ट व स्मरणपत्रे (Farm Tasks & Action Checklist)")
    st.caption("तुमच्या पिकांच्या चालू टप्प्यानुसार आवश्यक शेती कामांची नोंद व स्मरणपत्रे.")

    if "crop_tasks" not in st.session_state:
        st.session_state.crop_tasks = []

    tasks = st.session_state.crop_tasks

    # Filter selector: View tasks for current crop vs all crops
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        task_filter = st.radio(
            "फिल्टर निवडा (Filter Tasks):",
            options=["केवळ निवडलेले पीक (Current Crop Only)", "सर्व पिकांची कामे (All Farm Tasks)"],
            horizontal=True
        )

    # Filter tasks list
    if task_filter == "केवळ निवडलेले पीक (Current Crop Only)":
        visible_tasks = [t for t in tasks if t.get("crop", "").lower() == selected_crop_key.lower()]
    else:
        visible_tasks = tasks

    # Progress Metric
    if visible_tasks:
        completed_count = sum(1 for t in visible_tasks if t.get("status", False))
        total_count = len(visible_tasks)
        progress = completed_count / total_count if total_count > 0 else 0
        st.progress(progress, text=f"प्रगती (Progress): {completed_count}/{total_count} कामे पूर्ण ({int(progress*100)}%)")
    else:
        st.caption("या पिकासाठी कोणतीही कामे प्रलंबित नाहीत (No pending tasks for this crop).")

    # Render individual task checkboxes
    for idx, task in enumerate(visible_tasks):
        # Priority badge formatting
        p_badge = "🔴 उच्च (High)" if task.get("priority") == "High" else (
            "🟡 मध्यम (Med)" if task.get("priority") == "Medium" else "🟢 सामान्य (Low)"
        )
        
        with st.container(border=True):
            col_check, col_meta = st.columns([4, 2])
            
            with col_check:
                # Find task in original list by ID for safe state updates
                is_done = st.checkbox(
                    f"**{task['title']}**",
                    value=task.get("status", False),
                    key=f"task_check_{task.get('id', idx)}"
                )
                if is_done != task.get("status", False):
                    task["status"] = is_done
                    st.rerun()

            with col_meta:
                st.caption(f"🌾 **पीक:** {task.get('crop')} | **टप्पा:** {task.get('stage', 'General')}")
                st.markdown(f"**प्राधान्य:** `{p_badge}` | ⏰ **मुदत:** `{task.get('due_date', 'N/A')}`")

    st.markdown("<br>", unsafe_allow_html=True)

    # Expander to add a new customized task
    with st.expander("➕ नवीन शेतकाम / स्मरणपत्र जोडा (Add New Farm Task)"):
        with st.form("add_new_task_form"):
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                new_title = st.text_input("कामाचे नाव (Task Description)", placeholder="उदा. ०:५२:३४ खताचा डोस देणे किंवा फवारणी")
                new_crop = st.selectbox(
                    "संबंधित पीक (Related Crop)",
                    options=["Grapes", "Onion", "Soybean", "Sugarcane", "General Farm"]
                )
            with t_col2:
                new_stage = st.text_input("टप्पा / विभाग (Stage)", placeholder="उदा. फुलधारणा किंवा पुनर्लागवड")
                new_due = st.text_input("अपेक्षित वेळ / मुदत (Due Period)", placeholder="उदा. पुढील ३ दिवसात किंवा तातडीने")
                new_priority = st.selectbox("प्राधान्य (Priority)", options=["High", "Medium", "Low"], index=1)

            submit_task = st.form_submit_button("✅ काम सेव्ह करा (Save Task)", use_container_width=True)
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
                    st.success("✅ नवीन काम यशस्वीरीत्या जोडले! (Task added to checklist)")
                    st.rerun()
                else:
                    st.warning("कृपया कामाचे नाव प्रविष्ट करा (Please enter a task title).")


def render_crop_helper():
    """
    Main entry point for Module 2: Crop & Farming Helper.
    Syncs with farmer profile crops and renders stage-by-stage guidance and action checklist.
    """
    profile = st.session_state.get("farmer_profile", {})
    farmer_crops = profile.get("crops_grown", ["Grapes", "Onion", "Soybean"])

    # Top Header Banner
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #2e7d32 0%, #1565c0 100%);
                    padding: 20px 24px; border-radius: 12px; color: white; margin-bottom: 22px;">
            <h2 style="margin: 0; color: white;">🌱 पीक सल्लागार व शेती मार्गदर्शन (Crop & Farming Helper)</h2>
            <p style="margin: 6px 0 0 0; font-size: 14px; opacity: 0.94;">
                महाराष्ट्रातील हवामानानुसार पिकांचे टप्प्याटप्प्याने खत, पाणी व रोग नियंत्रण मार्गदर्शन आणि दैनंदिन शेतकाम चेकलिस्ट.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Crop Selector linked to farmer's active crops
    st.markdown("### 🌾 तुमचे पीक निवडा (Select Crop to Inspect)")
    
    # Build options list combining farmer crops with available guides
    crop_options = {}
    for c_raw in farmer_crops:
        k = detect_crop_key(c_raw)
        if k in CROP_GUIDES:
            crop_options[f"🌿 {c_raw} (तुमच्या शेतातील)"] = k

    # Add other Maharashtra crops if not already in farmer profile
    for k, v in CROP_GUIDES.items():
        if k not in crop_options.values():
            crop_options[f"📖 {v['display_name']} (इतर उपलब्ध)"] = k

    selected_label = st.selectbox(
        "पीक निवडा (Select Crop):",
        options=list(crop_options.keys()),
        index=0
    )
    
    selected_crop_key = crop_options[selected_label]
    crop_info = CROP_GUIDES.get(selected_crop_key, {})

    # Overview Metrics Card for Selected Crop
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"**पीक नाव:** `{crop_info.get('display_name', selected_crop_key)}`")
            st.markdown(f"**मराठी नाव:** `{crop_info.get('marathi_name', '')}`")
        with c2:
            st.markdown(f"**हंगाम (Season):** `{crop_info.get('season', 'N/A')}`")
        with c3:
            st.markdown(f"**योग्य जमीन (Recommended Soil):** {crop_info.get('recommended_soil', 'N/A')}")

    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Stage-by-Stage Guidance
    render_crop_stages(crop_info)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # 2. Interactive Task Checklist & Reminders
    render_task_checklist(selected_crop_key)

"""
components/page_components/page_header.py
--------------------------------------------
PHASE 6B: a reusable Sahay page header (icon + title + short description
+ optional badge/action), replacing the `st.markdown("### Title")` every
one of the 14 pages currently hand-rolls (see
PHASE6A_INDIVIDUAL_PAGE_AUDIT.md §3/§8 — the single most duplicated
pattern found across all 14 pages).

Visual hierarchy is adapted from LearnMate's `frontend/components.py`
`hero()` (eyebrow/title/subtitle shape) — presentation only; no
LearnMate copy, no LearnMate data. Content (title/description) always
comes from the calling page's own existing text; this component never
invents copy.
"""

from __future__ import annotations

from typing import Callable

import streamlit as st

from components.theme import COLORS


def render_page_header(
    title: str,
    description: str | None = None,
    icon: str | None = None,
    badge: str | None = None,
    action: Callable[[], None] | None = None,
) -> None:
    """Render a page header.

    Args:
        title: the page's existing heading text (unchanged from whatever
            the page currently passes to `st.markdown`).
        description: the page's existing subtitle/intro text, if any.
        icon: an emoji or short glyph shown beside the title (e.g. the
            "🇮🇳" Government Services already uses inline in its own
            heading, or "🚨" for a page needing an alert-adjacent tone).
        badge: a short label chip (e.g. "Demo data") rendered top-right.
            Purely decorative text supplied by the caller — this
            component never invents a badge's wording.
        action: an optional zero-argument callable. If given, the page
            renders its OWN widget (e.g. a language selectbox) inside a
            right-hand column this header lays out — the header itself
            never creates the widget, its key, or any session-state
            write; that stays entirely the calling page's
            responsibility, per the "components don't own navigation or
            session state" rule.
    """
    dark = st.session_state.get("sahay_dark_mode", False)
    muted = COLORS["muted_dark"] if dark else COLORS["muted_light"]

    if action is not None:
        left, right = st.columns([4, 1])
        with left:
            _render_title_block(title, description, icon, badge, muted)
        with right:
            action()
    else:
        _render_title_block(title, description, icon, badge, muted)


def _render_title_block(
    title: str,
    description: str | None,
    icon: str | None,
    badge: str | None,
    muted: str,
) -> None:
    icon_html = f"<span style='font-size:22px;'>{icon}</span>" if icon else ""
    badge_html = (
        f"<span style='background:{COLORS['soft_teal']}22;color:{COLORS['soft_teal']};"
        f"padding:2px 10px;border-radius:999px;font-size:11px;font-weight:600;"
        f"margin-left:8px;vertical-align:middle;'>{badge}</span>"
        if badge else ""
    )
    st.markdown(
        f"""
        <div style="margin-bottom:4px;">
            <div style="display:flex;align-items:center;gap:8px;">
                {icon_html}
                <span class="sahay-display" style="font-size:22px;font-weight:700;">{title}</span>
                {badge_html}
            </div>
            {f'<p style="color:{muted};margin:4px 0 0 0;font-size:14.5px;">{description}</p>' if description else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )

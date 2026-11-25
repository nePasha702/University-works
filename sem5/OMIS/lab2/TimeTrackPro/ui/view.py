from base64 import b64encode
from functools import lru_cache
from html import escape
from pathlib import Path

import streamlit as st


DIR = Path(__file__).parent


@lru_cache
def component():
    icons = b64encode((DIR / "icons.png").read_bytes()).decode("ascii")
    css = (DIR / "screen.css").read_text(encoding="utf-8").replace("ICON_ATLAS", icons)
    return st.components.v2.component(
        "timetrackpro_screen",
        html='<div id="screen-root"></div>',
        css=css,
        js=(DIR / "screen.js").read_text(encoding="utf-8"),
    )


def render(markup, revision):
    st.html(DIR / "streamlit.css")
    component()(data={"markup": markup, "revision": revision}, key="screen", on_event_change=lambda: None)


def esc(value):
    return escape(str(value), quote=True)


def icon(name, size=18):
    return f'<span class="icon i-{name}" style="--size:{size}px" aria-hidden="true"></span>'


def action(label, name, style="blue", *, target=None, disabled=False, submit=False, title=None):
    kind = "submit" if submit else "button"
    attrs = f'data-action="{name}"'
    if target is not None:
        attrs += f' data-target="{esc(target)}"'
    if title:
        attrs += f' title="{esc(title)}"'
    if disabled:
        attrs += " disabled"
    return f'<button type="{kind}" class="button {style}" {attrs}>{label}</button>'


def heading(text):
    return f'<h2>{esc(text)}</h2>'


def field(label, name, *, value="", placeholder="", kind="text", required=True, options=None):
    attrs = f'name="{name}"' + (" required" if required else "")
    if options is not None:
        choices = "".join(
            f'<option value="{esc(key)}"' + (" selected" if key == value else "") + f'>{esc(text)}</option>'
            for key, text in options.items()
        )
        prompt = f'<option value="" disabled selected>{esc(placeholder)}</option>' if placeholder else ""
        control = f'<select {attrs}>{prompt}{choices}</select>'
    else:
        min_length = ' minlength="6"' if name == "new_password" else ""
        control = (f'<input type="{kind}" {attrs} value="{esc(value)}"'
                   f' placeholder="{esc(placeholder)}"{min_length}>')
    return f'<label class="field"><span>{esc(label)}</span>{control}</label>'


def date_field(label, name, value=None):
    display = value.strftime("%d.%m.%Y") if value else ""
    iso = value.isoformat() if value else ""
    return f"""
    <div class="field">
      <label for="{name}">{esc(label)}</label>
      <div class="date-control">
        <input id="{name}" name="{name}" type="text" inputmode="numeric" value="{display}"
          placeholder="дд . мм . гггг" maxlength="10" pattern="[0-9]{{2}}[.][0-9]{{2}}[.][0-9]{{4}}" required>
        <input type="date" value="{iso}" aria-label="Выбрать дату в календаре — {esc(label)}">
        {icon("date", 19)}
      </div>
    </div>"""


def buttons(*items):
    return f'<div class="button-row">{"".join(items)}</div>'


def form(name, body, submit, *, target=None, css="stack"):
    attrs = f' data-target="{esc(target)}"' if target is not None else ""
    return f'<form class="{css}" data-form="{name}"{attrs}>{body}{submit}</form>'


def card(title, description, content="", *, color="green", symbol="person", attrs=""):
    return f"""
      <article class="card stripe-{color}" {attrs}>
        <h3>{icon(symbol, 23)} {esc(title)}</h3>
        <div class="card-description">{description}</div>
        {content}
      </article>"""


def details(summary, body, css="", *, keep=None):
    state = f' data-keep="{keep}"' if keep else ""
    return f'<details class="{css}"{state}><summary>{summary}</summary><div>{body}</div></details>'


def panel(title, body, css=""):
    return f'<section class="detail-panel {css}" data-reveal><h3>{title}</h3>{body}</section>'

# -*- coding: utf-8 -*-
"""
Spark Hub · 教授邀请函（Streamlit 版 · 原版排版）

说明：真正的邀请函是同目录下的 invite.html（老师确认的原版横向排版，
图片已全部内联）。本文件把它整页嵌入 Streamlit，从而获得一个
xxx.streamlit.app 的公网网址。

部署要求：仓库根目录至少有 app.py 和 invite.html 两个文件。

专属链接：https://你的域名.streamlit.app/?name=李老师
（不带 ?name= 时默认显示「诚邀您担任」）

回复收集：教授点「愿意进一步交流」后跳转问卷星问卷，
回复统一在问卷星后台查看（记得开启新答卷提醒）。
"""
import os
import html as _html

import streamlit as st
import streamlit.components.v1 as components

BASE = os.path.dirname(os.path.abspath(__file__))
INVITE_FILE = os.path.join(BASE, "invite.html")

st.set_page_config(page_title="Spark Hub · 教授邀请函", page_icon="✳", layout="wide")
st.markdown(
    "<style>.stApp{background:#fff;} #MainMenu{visibility:hidden;}"
    "footer{visibility:hidden;} header{visibility:hidden;}</style>",
    unsafe_allow_html=True,
)

# ---------------- 姓名注入 ----------------
params = st.query_params
raw_name = params.get("name", "").strip()
# 只留安全字符，防止破坏内嵌脚本的字符串引号
safe = "".join(ch for ch in raw_name if ch not in "'\"\\<>;")
prof_name = _html.escape(safe) or "您"

with open(INVITE_FILE, "r", encoding="utf-8") as f:
    page = f.read()
page = page.replace("var DEFAULT_NAME = '李老师';",
                    "var DEFAULT_NAME = '" + prof_name + "';", 1)

# ---------------- 整页嵌入原版排版 ----------------
components.html(page, height=812, scrolling=False)

# ---------------- 组织方说明 ----------------
with st.sidebar:
    st.markdown("### Spark Hub · 组织方")
    st.caption("教授点「愿意进一步交流」后会跳转问卷星问卷，"
               "回复统一在问卷星后台查看（记得开新答卷提醒）。")
    st.caption("给每位老师的专属链接：网址后加 ?name=老师称呼，"
               "页面会自动显示「诚邀 XX 担任」。")

# -*- coding: utf-8 -*-
"""
Spark Hub · 教授邀请函（Streamlit 版）

部署：把整个文件夹传到 GitHub，在 Streamlit Community Cloud 新建 App、
选 app.py、设为 Public，即可得到一个 xxx.streamlit.app 链接。
给每位老师的专属链接：https://你的域名.streamlit.app/?name=李老师
组织方：打开同一链接，在左侧栏输入管理口令，即可查看并导出回复记录。
"""
import os
import csv
import html
import base64
from datetime import datetime

import streamlit as st

# ===================== 只需要改这一块 =====================
CONTACT    = "【姓名】"
EMAIL      = "【邮箱】"
WECHAT_LINK = "【公众号文章链接】"

ADMIN_CODE = "【管理口令】"   # 务必改成自己的口令，别写进发给教授的链接里
DATA_FILE  = "responses.csv"
# ========================================================

st.set_page_config(page_title="Spark Hub · 邀请函", page_icon="✳", layout="wide")

params = st.query_params
prof_name = html.escape(params.get("name", "").strip())

BASE = os.path.dirname(os.path.abspath(__file__))
def IMG(name):
    """兼容 GitHub 网页上传时把 images/ 平铺到根目录的情况"""
    nested = os.path.join(BASE, "images", name)
    return nested if os.path.exists(nested) else os.path.join(BASE, name)

def data_uri(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

LOGO_MARK = data_uri(IMG("logo-mark.png"))
LOGO_FULL = data_uri(IMG("logo-full.png"))

def ph(text):
    """把待填信息高亮出来，方便上线前一眼找齐"""
    return '<span class="sh-ph">' + html.escape(text) + '</span>'

CSS = """
<style>
  .stApp { background:#FFFCFD; }
  .block-container { max-width:1180px; padding-top:2rem; padding-bottom:3rem; }
  .sh-head { display:flex; justify-content:space-between; align-items:center;
             border-bottom:1px solid #F2E4EE; padding-bottom:14px; }
  .sh-brand { display:flex; align-items:center; gap:12px; }
  .sh-logo { width:46px; height:46px; object-fit:contain; display:block; flex:none; }
  .sb-logo { width:130px; display:block; margin:0 auto 12px; }
  .sh-name { font-size:19px; font-weight:800; letter-spacing:.14em; line-height:1.1;
             background:linear-gradient(90deg,#F0502A,#E4235E 55%,#A81B6B);
             -webkit-background-clip:text; background-clip:text;
             color:transparent; -webkit-text-fill-color:transparent; }
  .sh-sub { font-size:11px; color:#5E5878; margin-top:4px; }
  .sh-right { text-align:right; }
  .sh-kicker { font-size:10px; font-weight:800; letter-spacing:.2em; color:#FF4FA3; }
  .sh-meta { font-size:11px; color:#5E5878; margin-top:5px; }
  .sh-hero { display:flex; gap:36px; align-items:center; padding:26px 0 22px; }
  .sh-hero-l { width:52%; }
  .sh-eyebrow { font-size:10px; font-weight:800; letter-spacing:.14em;
                color:#FF6C8B; margin-bottom:12px; }
  .sh-hero h1 { font-size:42px; line-height:1.18; font-weight:800; color:#211B4B;
                margin:0 0 12px; letter-spacing:-.01em; }
  .sh-hero h1 span { color:#FF4FA3; }
  .sh-subline { font-size:13px; color:#5E5878; }
  .sh-hero-r { flex:1; border-left:1px solid #F2E4EE; padding-left:28px; }
  .sh-badge { display:inline-block; background:#FFF0F6; color:#C02E72;
              border:1px solid #FFD7E8; font-size:11px; font-weight:700;
              padding:6px 12px; border-radius:99px; margin-bottom:14px; }
  .sh-invite { font-size:16px; font-weight:800; color:#211B4B; line-height:1.6; }
  .sh-light { font-size:12px; color:#5E5878; margin-top:8px; }
  .sh-sign { font-size:10px; color:#8A83A0; margin-top:14px; }
  .sh-tag { font-size:11px; font-weight:700; color:#211B4B; background:#fff;
            border-radius:99px; padding:4px 10px; display:inline-block; margin-top:8px;
            box-shadow:0 2px 8px rgba(30,15,45,.12); }
  .sh-card { background:#fff; border:1px solid #F2E4EE; border-radius:18px;
             padding:20px 20px 18px; height:100%; }
  .sh-card .ico { width:30px; height:30px; border-radius:9px; color:#fff;
                  display:flex; align-items:center; justify-content:center;
                  font-size:15px; font-weight:800; margin-bottom:12px; }
  .sh-card .ce { font-size:9px; font-weight:800; letter-spacing:.14em; color:#A79FB8; }
  .sh-card h2 { font-size:15px; font-weight:800; color:#211B4B; margin:5px 0 10px; }
  .sh-card p, .sh-card li { font-size:12px; line-height:1.7; color:#5E5878; }
  .sh-card ul { padding-left:16px; margin:0; }
  .sh-card li { margin-bottom:5px; }
  .sh-card b { color:#211B4B; }
  .sh-ft { border-top:1px solid #F2E4EE; margin-top:22px; padding-top:16px; }
  .sh-say { font-size:15px; font-weight:800; color:#211B4B; }
  .sh-say span { color:#FF4FA3; }
  .sh-say2 { font-size:12px; color:#5E5878; margin-top:5px; }
  .sh-contact { font-size:11px; color:#5E5878; margin-top:6px; }
  div.stButton > button { border-radius:99px; font-weight:800; font-size:14px;
                          padding:10px 22px; border:1px solid #E6D9E5;
                          color:#5E5878; background:#fff; }
  div.stButton > button:hover { border-color:#FF4FA3; color:#FF4FA3; }
  div.stButton > button[kind="primary"] { background:#FF4FA3; color:#fff;
    border:0; box-shadow:0 6px 16px rgba(255,79,163,.28); }
  .sh-thanks { background:#FFF0F6; border:1px solid #FFD7E8; border-radius:18px;
               padding:22px; text-align:center; color:#211B4B; font-size:20px; font-weight:800; }
  .sh-thanks span { display:block; font-size:13px; font-weight:400;
                    color:#5E5878; margin-top:8px; }
  .sh-ph { background:#FFF1F7; color:#C9317A; border-bottom:1px dashed #FF8CC2;
           padding:0 3px; border-radius:3px; font-weight:600; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

salutation = prof_name if prof_name else "您"

# ---------------- header ----------------
st.markdown(f"""
<div class="sh-head">
  <div class="sh-brand">
    <img class="sh-logo" src="{LOGO_MARK}">
    <div>
      <div class="sh-name">SPARK HUB</div>
      <div class="sh-sub">香港城市大学（东莞）· 科技创新与创业协会</div>
    </div>
  </div>
  <div class="sh-right">
    <div class="sh-kicker">FACULTY INVITATION</div>
    <div class="sh-meta">星火初创，光耀未来　·　Spark Innovation · Light the Future</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------------- hero ----------------
st.markdown(f"""
<div class="sh-hero">
  <div class="sh-hero-l">
    <div class="sh-eyebrow">诚　邀　·　SPARK-HUB 指导老师邀请函</div>
    <h1>诚邀您，与我们一起<br>让创新的星火<span>走向实践</span></h1>
    <div class="sh-subline">担任 Spark-Hub 指导老师，以专业启发探索，陪伴学生把创意逐步变为现实。</div>
  </div>
  <div class="sh-hero-r">
    <div class="sh-badge">✳ 香港城市大学（东莞）· 学生事务处（SDO）指导 · 官方学生组织</div>
    <div class="sh-invite">诚邀{salutation}担任 Spark-Hub 指导老师</div>
    <div class="sh-light">围绕您的专业方向开展交流，参与方式与时间安排由双方商定。</div>
    <div class="sh-sign">Spark-Hub　|　科技创新与创业协会　|　星火初创，光耀未来</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------------- photos ----------------
c1, c2, c3 = st.columns([1.62, 1, 1])
for col, img, tag in [
    (c1, "photo-brainstorm.jpg", "01　跨学科协作"),
    (c2, "photo-pitch.jpg", "02　机器人项目实践"),
    (c3, "photo-mentor.jpg", "03　师生交流与指导"),
]:
    with col:
        st.image(IMG(img), width="stretch")
        st.markdown(f'<div class="sh-tag">{tag}</div>', unsafe_allow_html=True)

# ---------------- cards ----------------
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown("""
    <div class="sh-card">
      <div class="ico" style="background:#FF4FA3">✳</div>
      <div class="ce">01 / 我们是谁</div><h2>由学校指导，连接跨学科创新</h2>
      <p>Spark-Hub，即香港城市大学（东莞）科技创新与创业协会，是由<b>学生事务处（SDO）指导</b>、师生共同建设的官方学生创新创业组织。</p>
      <p>我们为学生提供赛事资讯、项目孵化、资源对接与交流机会，汇聚工程、计算机、数据科学及商科等专业背景，开展机器人、无人机、AI 与数据分析等方向的实践。</p>
      <p>我们希望帮助学生在项目中学会发现问题、解决问题，并在持续探索中成长。</p>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown("""
    <div class="sh-card">
      <div class="ico" style="background:#211B4B">◻</div>
      <div class="ce">02 / 期待您的指导</div><h2>用您的专业，帮助学生找准方向</h2>
      <p>诚邀您结合研究兴趣与时间安排，选择适合的方式参与：</p>
      <ul>
        <li><b>项目指导</b>：对选题、技术路线与实施方案提出建议。</li>
        <li><b>阶段点评</b>：参与项目展示、竞赛准备或成果讨论。</li>
        <li><b>专题交流</b>：分享专业视角、研究方法与行业观察。</li>
      </ul>
      <p>日常组织与项目跟进由团队负责，交流前提前整理材料和问题。具体参与频次、形式及指导范围，与您协商确定。</p>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown("""
    <div class="sh-card">
      <div class="ico" style="background:#7C5CFF">◈</div>
      <div class="ce">03 / 共同探索</div><h2>让专业知识，在学生实践中延伸</h2>
      <p>通过 Spark-Hub，您可以与不同专业的学生团队交流，围绕感兴趣的问题探索跨学科合作与创新应用。</p>
      <p>水下机器人、陆地机器人及无人机团队已取得全国性赛事奖项，为进一步开展项目指导与实践育人提供了基础。</p>
      <p>我们将协助整理指导过程与活动记录；经您同意后，在网站展示您的专业方向与指导内容，促进师生之间的交流与连接。</p>
    </div>""", unsafe_allow_html=True)

# ---------------- footer + reply ----------------
st.markdown(f"""
<div class="sh-ft">
  <div class="sh-say">每一个正在探索的想法，都期待一次专业的启发。</div>
  <div class="sh-say2">诚邀您加入 Spark-Hub，与我们共同支持学生的创新实践。</div>
  <div class="sh-contact">香港城市大学（东莞）科技创新与创业协会　·　联系人 {ph(CONTACT)}　联系邮箱 {ph(EMAIL)}　·　了解我们 {ph(WECHAT_LINK)}</div>
</div>
""", unsafe_allow_html=True)

FIELDS = ["时间", "教授", "选择", "学院", "来源"]

def save_response(name, choice):
    row = {
        "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "教授": name or "未署名",
        "选择": choice,
        "学院": params.get("dept", ""),
        "来源": "Spark Hub 邀请函网页",
    }
    exists = os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0
    with open(DATA_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow(row)

if "choice" not in st.session_state:
    st.session_state.choice = None

if st.session_state.choice is None:
    if not prof_name:
        typed = st.text_input("方便留个称呼吗？（可留空，不影响回复）", placeholder="如：李老师")
        prof_name = html.escape(typed.strip()) if typed else ""
    b1, b2, _ = st.columns([1, 1.25, 2])
    with b1:
        if st.button("暂不考虑", width="stretch"):
            save_response(prof_name, "暂不考虑")
            st.session_state.choice = "decline"
            st.rerun()
    with b2:
        if st.button("愿意进一步交流 ↗", type="primary", width="stretch"):
            save_response(prof_name, "愿意进一步交流")
            st.session_state.choice = "agree"
            st.rerun()
else:
    if st.session_state.choice == "agree":
        st.markdown("""<div class="sh-thanks">✓ 已收到，谢谢您！
          <span>后续由我们主动联系您，您不用回复邮件，也不必做任何安排。</span></div>""",
          unsafe_allow_html=True)
    else:
        st.markdown("""<div class="sh-thanks" style="background:#F5F2FF;border-color:#E4DCFF">♡ 没关系，谢谢您抽空看完
          <span>这封信就到这里，不打扰了。以后若想合作，随时都欢迎。</span></div>""",
          unsafe_allow_html=True)

# ---------------- organizer area ----------------
with st.sidebar:
    st.markdown(f'<img class="sb-logo" src="{LOGO_FULL}">', unsafe_allow_html=True)
    st.markdown("### Spark Hub · 组织方")
    code = st.text_input("管理口令", type="password")
    if code and code == ADMIN_CODE:
        rows = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8-sig", newline="") as f:
                rows = list(csv.DictReader(f))
        st.markdown(f"**共 {len(rows)} 条回复**")
        if rows:
            st.table(rows)
            with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
                st.download_button("导出 CSV", data=f.read(),
                                   file_name="sparkhub-responses.csv", mime="text/csv")
        else:
            st.info("还没有收到回复")
        st.caption("提示：免费版休眠重启后本地记录可能重置，重要数据请及时导出 CSV。")
    elif code:
        st.error("口令不对")
    else:
        st.caption("输入管理口令后可查看谁同意了，并导出名单。")

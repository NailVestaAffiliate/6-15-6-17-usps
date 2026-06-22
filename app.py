"""
NailVesta 達人補發追蹤 — Streamlit 操作介面
執行：streamlit run app.py
"""
import io
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="達人補發追蹤", page_icon="💅", layout="wide")

SAVE_FILE = "達人補發追蹤_state.csv"

# 達人, 日期, 姓名, Email, 電話, 地址, 款式, 尺寸, 物流單號(LV/HB), USPS Tracking
RAW = [
 ("xiomaradenise_","2026/06/15","Xiomara DiGiovanna","xiomaradigiovanna@gmail.com","8654123598","1748 Quail Ridge Loop, Kissimmee, FL 34744","Pastel Coast, Sunlit Petals, Aloha Bloom","M","LV068190166US","9300110993319120459047"),
 ("uhhhnegin-4","2026/06/15","Negin Mandavi","neginmandavi@gmail.com","8912354789","15950 Chase Hill Blvd, San Antonio, TX 78256","Berry Bowtie, Mochi Blossom","S","LV068190197US","9300110993319120459061"),
 ("anaiddm","2026/06/15","Diana Medina","Anaiddm13@gmail.com","8654932147","10223 San Luis Ave, South Gate, CA 90280","Fairy Nectar, Pastel Bloom, Coraline Glow","S","LV068190152US","9300110993319120459023"),
 ("akroulette","2026/06/15","Jamal Wint","Akroulettepromotions@gmail.com","5214896325","745 Scenic Hwy Apt 5208, Lawrenceville, GA 30045","Aqua Blush, Golden Hibiscus, Petal Throne","M","LV068190206US","9300110993319120459078"),
 ("life_witheb","2026/06/15","Eboni Logan","lifewitheb01@gmail.com","1547896325","3123 Calvary Drive Apt B3, Raleigh, NC 27604","Rosé Petal, Seaside Sundae, Tidal Flower","M","LV068190183US","9300110993319120459054"),
 ("keanna.edit","2026/06/15","Keanna Barocas","keanna.ugc@gmail.com","4589312475","14824 Faversham Cir, Orlando, FL 32826","Rouge Letter, Teal Blossom, Aloha Bloom","L","LV068190170US","9300110993319120459030"),
 ("avibeinpisces","2026/06/15","Salina Spain","salina.spain@outlook.com","8654125983","14624 Fieldcrest Lane, Burnsville, MN 55306","Teal Blossom, Jade Garden, Petal Throne","M","LV068190245US","9300110993319120459115"),
 ("glambeatzbyzee","2026/06/15","Zatese Brown","makeupbyzatese@gmail.com","9563214789","5001 Cypress Creek Ave E Apt 1010, Tuscaloosa, AL 35405","Jade Garden, Mochi Blossom","M","LV068190210US","9300110993319120459085"),
 ("saydizzle-2","2026/06/15","Sada Policar","Hello@sadaarika.com","4589632147","2020 Barranca St Unit 410, Los Angeles, CA 90031","Fairy Nectar, Champagne Blossom, Jade Garden","S","LV068190237US","9300110993319120459108"),
 ("cyaira.a","2026/06/15","Cyaira Angeliq","cyairaangeliq@gmail.com","2679920486","650 Kerper St, Philadelphia, PA 19111","Aqua Blush, Cowgirl Charm, Pearl Tide","S","LV068190223US","9300110993319120459092"),
 ("findsbykayla","2026/06/16","Kayla Ring","kaylanicolering@gmail.com","612-978-7166","17619 Grant Street NW, Elk River, MN 55330","Island Paradise, Citrus Veil, Tidal Flower","S","LV068316224US","9300110993319120584749"),
 ("shelives.on.whimsylane","2026/06/16","Mia Walker","knottycroture@gmail.com","5488641235","8958 River Island Drive Apt 203, Savage, MD 20763","Apricot Cream, Rosé Angel, Marine Glow","M","LV068316255US","9300110993319120584763"),
 ("samantharose.__","2026/06/16","Samantha Rosario","Ssamantharosee6@gmail.com","6587423915","211 Meade St, Perth Amboy, NJ 08861","Acai Bloom, Seaside Sundae, Sunflower Safari","M","LV068316215US","9300110993319120584725"),
 ("clarityhome","2026/06/16","Clarity Home","clarityhomeco@gmail.com","8456912354","8035 100th Ct, Vero Beach, FL 32967","Mint Petal, Silk Blossom","S","LV068316241US","9300110993319120584732"),
 ("skyepalafoxx","2026/06/16","Skyleynn Palafox","skyepalafox@gmail.com","1254789632","10809 Colony Wood Pl, Spring, TX 77380","Coraline Glow, Mochi Blossom, Petal Throne","M","LV068316238US","9300110993319120584756"),
 ("tutugoldd_","2026/06/16","Jade Rivera","Tutugoldd@gmail.com","4562157893","1892 English Court, Virginia Beach, VA 23454","Peach Ember, Tidal Flower, Sunflower Safari","L","LV068316269US","9300110993319120584770"),
 ("lindseyingleee","2026/06/17","Lindsey Hedrick","lindseyingleeee@gmail.com","4589623157","1301 S Park St Trlr C-39, Sapulpa, OK 74066","Royal Treasure, Jade Blossom, Papaya Bloom","L","HB089165365US","9300110663319120128877"),
 ("grwmm.gabi-5","2026/06/17","Esperanza Reyes","grwmm.gabi@gmail.com","912-331-9345","33 Villa St Apt 5, Douglas, GA 31533","Royal Treasure, Seaside Sundae, Tropical Breeze","M","HB089165405US","9300110663319120128914"),
 ("lovebeaches1","2026/06/17","Chelsea Chimere Brown","Chichibad.nco@gmail.com","5412863459","1386 Oakdale Ave Apt G, El Cajon, CA 92021","Citrus Daisy, Petal Throne, Pearl Tide","L","HB089165374US","9300110663319120128884"),
 ("tyetaughtuwell_","2026/06/17","Tyesha Draughn","tyetaughtuwell@gmail.com","5846231457","320 Eliza Way, Winterville, NC 28590","Sunset Treasure, Ocean Picnic, Honey Petal","M","HB089165388US","9300110663319120128891"),
 ("misamoresx3","2026/06/17","Melissa Penaloza","mellypcollabz@gmail.com","4521896325","3628 Cardamon Dr, Bakersfield, CA 93309","Fairy Garden, Island Paradise, Opal Dynasty","S","HB089165391US","9300110663319120128907"),
 ("prestonandtina7","2026/06/17","Tina Vielot","Prestonandtina7@gmail.com","4521369874","14261 Heritage Landing Blvd Apt 1627, Punta Gorda, FL 33955","Tropical Breeze, Pastel Coast, Golden Hibiscus","M","HB089165414US","9300110663319120128921"),
 ("allthingssdee","2026/06/17","Diamond Gray","diamondhen25@gmail.com","16562421138","809 Alpine Ct, Kissimmee, FL 34758","Rosé Petal, Fairy Garden","M","HB089165431US","9300110663319120128945"),
 ("dannastewart","2026/06/17","D'anna Stewart","hello.dannastewart@gmail.com","8956471235","1226 Tolkien Rd, Riverside, CA 92506","Ruby Bloom, Fairy Garden, Jade Garden","L","HB089165428US","9300110663319120128938"),
 ("candylites","2026/06/17","Elba Aguirre","elbadarling@gmail.com","4856789231","1557 Flamingo St, Beaumont, CA 92223","Royal Treasure, Petal Throne","M","HB089165459US","9300110663319120128969"),
 ("fggvron","2026/06/17","Veronica Ford","","12569321439","100 Edison Ave NW Apt 6302, Madison, AL 35757","Pastel Coast, Golden Hibiscus, Silk Blossom","M","HB089165445US","9300110663319120128952"),
 ("lexbillionzz-76","2026/06/17","Lex Billionz","Lexb.business@gmail.com","4589612354","3580 E Commerce Way, Sacramento, CA 95834","Prism Aura, Citrus Veil, Cowgirl Charm, Sunflower Safari","M","HB089165462US","9300110663319120128976"),
]

COLS = ["達人 Handle","日期","姓名","Email","電話","地址","款式","尺寸",
        "物流單號(LV/HB)","USPS Tracking","達人是否通知","我們是否補發","備註"]


def base_df():
    df = pd.DataFrame(RAW, columns=COLS[:10])
    df["達人是否通知"] = False
    df["我們是否補發"] = False
    df["備註"] = ""
    return df[COLS]


def load_df():
    if os.path.exists(SAVE_FILE):
        df = pd.read_csv(SAVE_FILE, dtype=str).fillna("")
        for c in ["達人是否通知", "我們是否補發"]:
            df[c] = df[c].astype(str).str.lower().isin(["true", "1", "✓", "yes"])
        return df[COLS]
    return base_df()


def to_excel(df):
    """用 openpyxl 產生帶格式的 Excel；若環境沒裝 openpyxl 則回傳 None。"""
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        return None
    wb = Workbook(); ws = wb.active; ws.title = "達人補發追蹤"
    navy = PatternFill("solid", fgColor="1F3864"); alt = PatternFill("solid", fgColor="EAEFF7")
    white = Font(name="Arial", bold=True, color="FFFFFF", size=10); base = Font(name="Arial", size=10)
    thin = Side(style="thin", color="BFBFBF"); border = Border(thin, thin, thin, thin)
    ctr = Alignment("center", "center", wrap_text=True); lft = Alignment("left", "center", wrap_text=True)
    out_cols = ["序號"] + COLS
    ws.append(out_cols)
    for c in range(1, len(out_cols) + 1):
        cell = ws.cell(1, c); cell.fill = navy; cell.font = white; cell.alignment = ctr; cell.border = border
    for i, (_, r) in enumerate(df.iterrows(), start=1):
        ws.append([i, r["達人 Handle"], r["日期"], r["姓名"], r["Email"], str(r["電話"]).strip(),
                   r["地址"], r["款式"], r["尺寸"], r["物流單號(LV/HB)"], str(r["USPS Tracking"]).replace(" ", ""),
                   "✓" if r["達人是否通知"] else "", "✓" if r["我們是否補發"] else "", r["備註"]])
        rn = i + 1
        for c in range(1, len(out_cols) + 1):
            cell = ws.cell(rn, c); cell.font = base; cell.border = border
            cell.alignment = ctr if c in (1, 3, 9, 12, 13) else lft
            if i % 2 == 0: cell.fill = alt
        for col in (6, 10, 11):
            ws.cell(rn, col).number_format = "@"
    widths = [6, 20, 12, 20, 28, 16, 38, 26, 8, 18, 24, 12, 12, 22]
    for idx, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = w
    ws.freeze_panes = "A2"; ws.row_dimensions[1].height = 28
    buf = io.BytesIO(); wb.save(buf); return buf.getvalue()


# ---------- UI ----------
st.title("💅 NailVesta 達人補發追蹤")
st.caption("未收到包裹的達人清單 · 2026/06/15–06/17 · 共 27 位")

if "df" not in st.session_state:
    st.session_state.df = load_df()
df = st.session_state.df

c1, c2, c3, c4 = st.columns(4)
c1.metric("達人總數", len(df))
c2.metric("已通知我們", int(df["達人是否通知"].sum()))
c3.metric("已補發", int(df["我們是否補發"].sum()))
pending = int((df["達人是否通知"] & ~df["我們是否補發"]).sum())
c4.metric("待補發", pending)

f1, f2 = st.columns([3, 1])
kw = f1.text_input("🔍 搜尋（達人 / 姓名 / 款式 / 單號）", "")
flt = f2.selectbox("篩選", ["全部", "已通知未補發", "未通知", "已補發"])

view = df.copy()
if kw:
    m = pd.Series(False, index=view.index)
    for col in ["達人 Handle", "姓名", "款式", "物流單號(LV/HB)", "USPS Tracking"]:
        m |= view[col].astype(str).str.contains(kw, case=False, na=False)
    view = view[m]
if flt == "已通知未補發":
    view = view[view["達人是否通知"] & ~view["我們是否補發"]]
elif flt == "未通知":
    view = view[~view["達人是否通知"]]
elif flt == "已補發":
    view = view[view["我們是否補發"]]

edited = st.data_editor(
    view, use_container_width=True, hide_index=True, num_rows="fixed", key="editor",
    column_config={
        "達人是否通知": st.column_config.CheckboxColumn("達人是否通知", width="small"),
        "我們是否補發": st.column_config.CheckboxColumn("我們是否補發", width="small"),
        "備註": st.column_config.TextColumn("備註", width="medium"),
        "地址": st.column_config.TextColumn("地址", width="large"),
        "款式": st.column_config.TextColumn("款式", width="large"),
        "Email": st.column_config.TextColumn("Email", width="medium"),
    },
    disabled=["達人 Handle", "日期", "姓名", "Email", "電話", "地址", "款式", "尺寸",
              "物流單號(LV/HB)", "USPS Tracking"],
)

st.session_state.df.loc[edited.index] = edited

b1, b2, b3 = st.columns(3)
if b1.button("💾 儲存進度", use_container_width=True):
    st.session_state.df.to_csv(SAVE_FILE, index=False)
    st.success("已儲存")

xlsx = to_excel(st.session_state.df)
if xlsx is not None:
    b2.download_button("📥 匯出 Excel", xlsx, "達人補發追蹤.xlsx",
                       use_container_width=True)
else:
    b2.download_button("📥 匯出 CSV",
                       st.session_state.df.to_csv(index=False).encode("utf-8-sig"),
                       "達人補發追蹤.csv", use_container_width=True)

if b3.button("🔄 重置勾選", use_container_width=True):
    st.session_state.df = base_df()
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    st.rerun()

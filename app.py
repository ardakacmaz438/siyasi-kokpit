import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import feedparser

# SAYFA AYARLARI
st.set_page_config(
    page_title="Siyasi Strateji & Karar Destek Kokpiti", 
    page_icon="🏛️", 
    layout="wide"
)

st.title("🏛️ Siyasi Strateji & Karar Destek Platformu")
st.caption("Gerçek Zamanlı Ekonomi, Gündem ve Analiz Ekranı")
st.markdown("---")

# CANLI VERİ FONKSİYONLARI
@st.cache_data(ttl=300)
def get_live_finance():
    try:
        usd = yf.Ticker("USDTRY=X").history(period="1d")["Close"].iloc[-1]
        eur = yf.Ticker("EURTRY=X").history(period="1d")["Close"].iloc[-1]
        bist = yf.Ticker("XU100.IS").history(period="1d")["Close"].iloc[-1]
        return round(usd, 2), round(eur, 2), round(bist, 2)
    except:
        return "N/A", "N/A", "N/A"

@st.cache_data(ttl=600)
def get_live_news():
    feed_url = "https://www.trthaber.com/gundem_articles.rss"
    feed = feedparser.parse(feed_url)
    news_items = []
    for entry in feed.entries[:5]:
        news_items.append({"Başlık": entry.title, "Link": entry.link})
    return news_items

# SEKMELER
tabs = st.tabs([
    "📊 Anket & Seçmen Radarı",
    "⚖️ Hukuk & Anayasa",
    "📈 Canlı Ekonomi",
    "🌐 Canlı Gündem",
    "📜 Siyasi Tarih & Felsefe"
])

# MODÜL 1: ANKET
with tabs[0]:
    st.subheader("📊 Anket Konsolidasyonu")
    col1, col2 = st.columns([2, 1])
    with col1:
        df_anket = pd.DataFrame({
            "Parti / Blok": ["Cumhur İttifakı", "Millet İttifakı", "Diğer Partiler", "Kararsızlar"],
            "Oy Oranı (%)": [35.4, 33.1, 14.5, 17.0]
        })
        fig = px.pie(df_anket, values="Oy Oranı (%)", names="Parti / Blok", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.metric("Kritik Kararsız Seçmen", "%17.0", "Ana Hedef Kitle")

# MODÜL 2: HUKUK
with tabs[1]:
    st.subheader("⚖️ Anayasa ve Meclis Gündemi")
    st.text_input("Mevzuat / Madde Arama:", "Kuvvetler Ayrılığı")
    st.success("📌 **Anayasa Madde 7:** Yasama yetkisi Türk Milleti adına Türkiye Büyük Millet Meclisinindir.")

# MODÜL 3: EKONOMİ (CANLI)
with tabs[2]:
    st.subheader("📈 Canlı Piyasa Göstergeleri")
    usd, eur, bist = get_live_finance()
    c1, c2, c3 = st.columns(3)
    c1.metric("USD / TRY (Canlı)", f"₺{usd}")
    c2.metric("EUR / TRY (Canlı)", f"₺{eur}")
    c3.metric("BIST 100 (Canlı)", f"{bist}")

# MODÜL 4: GÜNDEM (CANLI)
with tabs[3]:
    st.subheader("🌐 Canlı Son Dakika Haber Akışı")
    haberler = get_live_news()
    if haberler:
        for item in haberler:
            st.markdown(f"🔴 **[{item['Başlık']}]({item['Link']})**")

# MODÜL 5: FELSEFE
with tabs[4]:
    st.subheader("📜 Düşünürlerin Gözünden Karar Destek")
    dusunur = st.selectbox("Stratejik Süzgeç Seçin:", ["Aristoteles", "Machiavelli", "Hobbes", "Marx"])
    st.info(f"🧠 **Seçilen Süzgeç:** {dusunur} perspektifi aktif.")

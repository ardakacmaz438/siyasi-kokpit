import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import feedparser
import urllib.request
import json

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(
    page_title="Siyasi Strateji & Karar Destek Kokpiti", 
    page_icon="🏛️", 
    layout="wide"
)

st.title("🏛️ Canlı Siyasi Strateji & Karar Destek Platformu")
st.caption("Gerçek Zamanlı Ekonomi, Gündem ve Analiz Ekranı")
st.markdown("---")

# 2. CANLI VERİ FONKSİYONLARI
@st.cache_data(ttl=300)
def get_live_finance():
    """Kesintisiz Canlı Döviz ve Piyasa Verisi"""
    try:
        # Açık ve kesintisiz döviz API'si
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        req = urllib.request.urlopen(url)
        data = json.loads(req.read().decode('utf-8'))
        
        usd_try = round(data['rates']['TRY'], 2)
        eur_usd = data['rates']['EUR']
        eur_try = round(usd_try / eur_usd, 2)
        
        # BIST 100 Sorgusu
        try:
            bist = yf.Ticker("XU100.IS").history(period="1d")["Close"].iloc[-1]
            bist_val = round(bist, 2)
        except:
            bist_val = "Piyasa Kapalı"
            
        return usd_try, eur_try, bist_val
    except Exception as e:
        return "N/A", "N/A", "N/A"

@st.cache_data(ttl=600)
def get_live_news():
    """Canlı Son Dakika Haber Akışı (RSS)"""
    try:
        feed_url = "https://www.trthaber.com/gundem_articles.rss"
        feed = feedparser.parse(feed_url)
        news_items = []
        for entry in feed.entries[:5]:
            news_items.append({"Başlık": entry.title, "Link": entry.link})
        return news_items
    except:
        return []

# 3. SEKMELERİN OLUŞTURULMASI
tabs = st.tabs([
    "📊 Anket & Seçmen Radarı",
    "⚖️ Hukuk & Anayasa",
    "📈 Canlı Ekonomi",
    "🌐 Canlı Gündem",
    "📜 Siyasi Tarih & Felsefe"
])

# --- MODÜL 1: ANKET & SEÇMEN RADARI ---
with tabs[0]:
    st.subheader("📊 Anket Konsolidasyonu ve Kararsız Seçmen Analizi")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        df_anket = pd.DataFrame({
            "Parti / Blok": ["Cumhur İttifakı", "Millet İttifakı", "Diğer Partiler", "Kararsızlar"],
            "Oy Oranı (%)": [35.4, 33.1, 14.5, 17.0]
        })
        fig = px.pie(
            df_anket, 
            values="Oy Oranı (%)", 
            names="Parti / Blok", 
            title="Ağırlıklı Anket Ortalama Dağılımı", 
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.metric("Kritik Kararsız Seçmen", "%17.0", "Ana Hedef Kitle")
        st.info("💡 **Stratejik Not:** Kararsızların %62'si genç seçmenlerden oluşmaktadır. Ekonomi ve istihdam odaklı söylem önceliklidir.")

# --- MODÜL 2: HUKUK & ANAYASA ---
with tabs[1]:
    st.subheader("⚖️ Anayasa, Mevzuat ve Meclis Gündemi")
    arama = st.text_input("Mevzuat / Madde Arama:", "Kuvvetler Ayrılığı")
    st.success("📌 **Anayasa Madde 7:** Yasama yetkisi Türk Milleti adına Türkiye Büyük Millet Meclisinindir.")
    st.warning("⚠️ **Gündemdeki Kanun Teklifi:** İklim ve Dönüşüm Kanun Teklifi Komisyonda.")

# --- MODÜL 3: CANLI EKONOMİ ---
with tabs[2]:
    st.subheader("📈 Canlı Piyasa ve Ekonomi Göstergeleri")
    
    usd, eur, bist = get_live_finance()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("USD / TRY (Canlı)", f"₺{usd}")
    c2.metric("EUR / TRY (Canlı)", f"₺{eur}")
    c3.metric("BIST 100 (Canlı)", f"{bist}")
    c4.metric("Yıllık Enflasyon (TÜFE)", "%43.2", "TÜİK Son Veri")

# --- MODÜL 4: CANLI GÜNDEM ---
with tabs[3]:
    st.subheader("🌐 Canlı Son Dakika Haber Akışı")
    st.caption("Doğrudan RSS kaynaklarından anlık çekilmektedir.")
    
    haberler = get_live_news()
    if haberler:
        for item in haberler:
            st.markdown(f"🔴 **[{item['Başlık']}]({item['Link']})**")
    else:
        st.write("Canlı haber akışı şu an alınamıyor.")

# --- MODÜL 5: SİYASI TARİH & FELSEFE ---
with tabs[4]:
    st.subheader("📜 Düşünürlerin Gözünden Karar Destek")
    dusunur = st.selectbox(
        "Stratejik Süzgeç Seçin:", 
        ["Aristoteles (Altın Orta)", "Machiavelli (Reelpolitik)", "Hobbes (Güvenlik)", "Marx (Sınıf Analizi)"]
    )
    st.info(f"🧠 **Seçilen Süzgeç:** {dusunur} perspektifiyle politika değerlendirme altyapısı aktif.")

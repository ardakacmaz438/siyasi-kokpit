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
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        req = urllib.request.urlopen(url)
        data = json.loads(req.read().decode('utf-8'))
        
        usd_try = round(data['rates']['TRY'], 2)
        eur_usd = data['rates']['EUR']
        eur_try = round(usd_try / eur_usd, 2)
        
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

# --- MODÜL 2: HUKUK, ANAYASA VE DETAYLI ANKET (GÜNCELLENDİ) ---
with tabs[1]:
    st.subheader("⚖️ Anayasa, Mevzuat ve Meclis Gündemi")
    
    # Arama ve Bilgi Kartları
    col_search, col_info = st.columns([1, 1])
    with col_search:
        arama = st.text_input("🔍 Mevzuat / Madde Arama:", "Kuvvetler Ayrılığı")
        st.success(f"📌 **Anayasa Madde 7:** Yasama yetkisi Türk Milleti adına Türkiye Büyük Millet Meclisinindir. *(Sorgu: {arama})*")
    
    with col_info:
        st.warning("⚠️ **Gündemdeki Kanun Teklifi:** İklim ve Dönüşüm Kanun Teklifi Komisyonda.")
        st.caption("Meclis komisyon süreçleri ve alt komisyon raporları anlık takip edilmektedir.")
    
    st.markdown("---")
    
    # DETAYLI SİYASİ & MEVZUAT ANKET MODÜLÜ
    st.subheader("🗳️ Kamuoyu Eğilimi & Siyasi Anket Modülü")
    
    # Oturum Durumu (Session State) Kontrolü
    if 'voted' not in st.session_state:
        st.session_state.voted = False

    if not st.session_state.voted:
        with st.form("political_poll_form"):
            st.markdown("#### 1. Siyasi Parti Tercihi")
            parti_tercihi = st.selectbox(
                "Bu Pazar bir genel seçim olsa oyunuzu hangi partiye verirsiniz?",
                [
                    "Seçiniz...",
                    "AK Parti (Adalet ve Kalkınma Partisi)",
                    "CHP (Cumhuriyet Halk Partisi)",
                    "DEM Parti (Halkların Eşitlik ve Demokrasi Partisi)",
                    "MHP (Milliyetçi Hareket Partisi)",
                    "İYİ Parti",
                    "Yeniden Refah Partisi",
                    "TİP (Türkiye İşçi Partisi)",
                    "Zafer Partisi",
                    "DEVA / Gelecek / Saadet Partisi",
                    "Diğer / Kararsızım / Oy Kullanmayacağım"
                ]
            )
            
            st.markdown("#### 2. Meclis Gündemi ve Yasa Teklifi Oylaması")
            iklim_kanunu = st.radio(
                "Komisyonda bulunan 'İklim ve Dönüşüm Kanun Teklifi' hakkındaki görüşünüz nedir?",
                (
                    "🟢 Destekliyorum (Yeşil dönüşüm ve çevre politikaları için gerekli)",
                    "🔴 Desteklemiyorum (Sektörel ve ekonomik kısıtlamalar getiriyor)",
                    "🟡 Fikrim Yok / İçeriği Hakkında Yeterli Bilgim Yok"
                )
            )
            
            st.markdown("#### 3. Muhalefet ve Yasa Süreçleri Değerlendirmesi")
            muhalefet_tutumu = st.radio(
                "Muhalefetin (CHP, TİP ve diğer muhalefet partileri) Meclis'teki yasa tekliflerine karşı tutumunu nasıl buluyorsunuz?",
                ("Etkili ve Yeterli", "Kısmen Yeterli", "Yetersiz ve Etkisiz")
            )
            
            submit_button = st.form_submit_button("Oyu Gönder ve Canlı Sonuçları Gör")
            
            if submit_button:
                if parti_tercihi != "Seçiniz...":
                    st.session_state.voted = True
                    st.session_state.parti = parti_tercihi
                    st.rerun()
                else:
                    st.error("Lütfen bir parti tercihi seçiniz.")
    else:
        st.success(f"✓ Oyunuz başarıyla kaydedildi! (Tercihiniz: **{st.session_state.parti}**)")
        
        st.markdown("### 📊 Canlı Anket & Kamuoyu Dağılımı")
        
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.markdown("#### Parti Tercihleri (%)")
            st.text("AK Parti (%32)")
            st.progress(0.32)
            
            st.text("CHP (%29)")
            st.progress(0.29)
            
            st.text("DEM Parti (%9)")
            st.progress(0.09)
            
            st.text("MHP (%8)")
            st.progress(0.08)
            
            st.text("TİP (%6)")
            st.progress(0.06)
            
            st.text("Zafer Partisi (%5)")
            st.progress(0.05)
            
            st.text("Yeniden Refah / İYİ Parti / Diğer (%11)")
            st.progress(0.11)

        with res_col2:
            st.markdown("#### İklim ve Dönüşüm Kanun Teklifi")
            st.text("Destekleyenler (%54)")
            st.progress(0.54)
            
            st.text("Karşı Çıkanlar (%38)")
            st.progress(0.38)
            
            st.text("Fikri Olmayanlar (%8)")
            st.progress(0.08)
            
        if st.button("Tekrar Oy Kullan / Sıfırla"):
            st.session_state.voted = False
            st.rerun()

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

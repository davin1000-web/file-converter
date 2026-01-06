"""
만능 파일 변환기 - Streamlit 웹 애플리케이션
이미지 및 엑셀/CSV 파일을 원하는 포맷으로 변환합니다.
"""

import streamlit as st
import pandas as pd
from PIL import Image
import io
import zipfile
from datetime import datetime
import random


# ==================== 쿠팡 파트너스 설정 ====================
# 아래 링크를 본인의 쿠팡 파트너스 링크로 교체하세요!
COUPANG_LINKS = {
    "이미지_외장하드": "https://link.coupang.com/a/dmmJ15",
    "이미지_SD카드": "https://link.coupang.com/a/dmmMov",
    "엑셀_키보드": "https://link.coupang.com/a/dmmOeD",
    "엑셀_모니터": "https://link.coupang.com/a/dmmRD1",
}

# 배너 정보 설정
AD_BANNERS = {
    "이미지": [
        {
            "title": "사진 작업 필수템",
            "subtitle": "가성비 외장하드 추천",
            "icon": "💾",
            "link": COUPANG_LINKS["이미지_외장하드"]
        },
        {
            "title": "대용량 SD카드 특가",
            "subtitle": "사진 저장 걱정 끝",
            "icon": "📸",
            "link": COUPANG_LINKS["이미지_SD카드"]
        },
    ],
    "엑셀": [
        {
            "title": "업무 효율 UP",
            "subtitle": "인기 기계식 키보드",
            "icon": "⌨️",
            "link": COUPANG_LINKS["엑셀_키보드"]
        },
        {
            "title": "눈이 편한 대화면",
            "subtitle": "모니터 베스트셀러",
            "icon": "🖥️",
            "link": COUPANG_LINKS["엑셀_모니터"]
        },
    ],
}


def show_context_ad(tab_type: str):
    """탭에 맞는 프리미엄 문맥 광고를 표시합니다."""
    if tab_type in AD_BANNERS:
        ad = random.choice(AD_BANNERS[tab_type])
        st.markdown(
            f"""
            <a href="{ad['link']}" target="_blank" style="text-decoration: none;">
                <div class="premium-ad-card">
                    <div class="ad-icon">{ad['icon']}</div>
                    <div class="ad-content">
                        <div class="ad-title">{ad['title']}</div>
                        <div class="ad-subtitle">{ad['subtitle']}</div>
                    </div>
                    <div class="ad-arrow">→</div>
                    <span class="ad-badge">AD</span>
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )


def show_loading_ad(tab_type: str):
    """로딩 중 프리미엄 광고를 표시합니다."""
    if tab_type in AD_BANNERS:
        ad = random.choice(AD_BANNERS[tab_type])
        st.markdown(
            f"""
            <div class="loading-ad-container">
                <div class="loading-ad-label">⏳ 잠시만 기다려주세요</div>
                <a href="{ad['link']}" target="_blank" style="text-decoration: none;">
                    <div class="loading-ad-card">
                        <span class="loading-ad-icon">{ad['icon']}</span>
                        <span class="loading-ad-text">{ad['title']} · {ad['subtitle']}</span>
                        <span class="loading-ad-cta">확인하기 →</span>
                    </div>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )


# Google 인증 파일 제공
query_params = st.query_params
if "google-verification" in query_params:
    st.markdown("google-site-verification: google2abad1d81a343e2b.html", unsafe_allow_html=True)
    st.stop()

# 페이지 설정
st.set_page_config(
    page_title="만능 파일 변환기",
    page_icon="🔄",
    layout="wide"
)

# Google Site Verification 메타 태그를 head에 동적으로 추가
st.markdown("""
<script>
    var meta = document.createElement('meta');
    meta.name = 'google-site-verification';
    meta.content = 'hhGxSnXxIruu9q1nPuyZ1b5upZB0dznXuhpCJfl01LY';
    document.getElementsByTagName('head')[0].appendChild(meta);
</script>
""", unsafe_allow_html=True)

# 커스텀 CSS
st.markdown("""
<style>
    /* ==================== 전체 레이아웃 ==================== */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* ==================== 메인 헤더 ==================== */
    .main-header-container {
        text-align: center;
        padding: 3rem 1rem;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    
    .main-logo {
        font-size: 4rem;
        margin-bottom: 0.5rem;
    }
    
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    
    .main-subtitle {
        color: #666;
        font-size: 1rem;
        font-weight: 400;
        margin-top: 0.5rem;
    }
    
    .main-badges {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }
    
    .badge {
        background: white;
        padding: 8px 16px;
        border-radius: 50px;
        font-size: 0.8rem;
        color: #555;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .badge-icon {
        font-size: 1rem;
    }
    
    /* ==================== 탭 스타일 ==================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8f9fa;
        padding: 8px;
        border-radius: 16px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        padding: 0 24px;
        font-weight: 500;
        font-size: 0.95rem;
        border-radius: 12px;
        background: transparent;
        border: none;
        color: #666;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: white;
        color: #333;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #667eea !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }
    
    /* ==================== 프리미엄 광고 카드 ==================== */
    .premium-ad-card {
        display: flex;
        align-items: center;
        gap: 16px;
        background: linear-gradient(135deg, #fafbfc 0%, #f0f2f5 100%);
        border: 1px solid #e8eaed;
        padding: 16px 20px;
        border-radius: 14px;
        margin: 16px 0;
        position: relative;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .premium-ad-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border-color: #667eea;
    }
    
    .ad-icon {
        font-size: 2rem;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    .ad-content {
        flex: 1;
    }
    
    .ad-title {
        font-weight: 600;
        color: #333;
        font-size: 0.95rem;
    }
    
    .ad-subtitle {
        color: #888;
        font-size: 0.85rem;
        margin-top: 2px;
    }
    
    .ad-arrow {
        color: #667eea;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .ad-badge {
        position: absolute;
        top: 8px;
        right: 12px;
        font-size: 0.65rem;
        color: #aaa;
        background: #f0f0f0;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 500;
    }
    
    /* ==================== 로딩 광고 ==================== */
    .loading-ad-container {
        margin: 16px 0;
    }
    
    .loading-ad-label {
        font-size: 0.8rem;
        color: #888;
        margin-bottom: 8px;
    }
    
    .loading-ad-card {
        display: flex;
        align-items: center;
        gap: 12px;
        background: linear-gradient(90deg, #667eea08 0%, #764ba208 100%);
        border: 1px dashed #667eea40;
        padding: 14px 18px;
        border-radius: 10px;
        transition: all 0.2s ease;
    }
    
    .loading-ad-card:hover {
        background: linear-gradient(90deg, #667eea15 0%, #764ba215 100%);
        border-style: solid;
    }
    
    .loading-ad-icon {
        font-size: 1.3rem;
    }
    
    .loading-ad-text {
        flex: 1;
        color: #555;
        font-size: 0.9rem;
    }
    
    .loading-ad-cta {
        color: #667eea;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    /* ==================== 섹션 헤더 ==================== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f0f2f5;
    }
    
    .section-icon {
        font-size: 1.8rem;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-radius: 14px;
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #333;
        margin: 0;
    }
    
    .section-desc {
        color: #888;
        font-size: 0.9rem;
        margin: 4px 0 0 0;
    }
    
    /* ==================== 버튼 스타일 ==================== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border: none;
        border-radius: 12px;
        padding: 14px 32px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(17, 153, 142, 0.4);
    }
    
    /* ==================== 파일 업로더 ==================== */
    .stFileUploader > div > div {
        border: 2px dashed #e0e0e0;
        border-radius: 16px;
        background: #fafbfc;
        transition: all 0.2s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #667eea;
        background: #f8f9ff;
    }
    
    /* ==================== 카드 스타일 ==================== */
    .info-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        border: 1px solid #f0f2f5;
    }
    
    /* ==================== 푸터 ==================== */
    .premium-footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eaed 100%);
        border-radius: 20px;
    }
    
    .footer-text {
        color: #888;
        font-size: 0.85rem;
        margin: 0;
    }
    
    .footer-brand {
        color: #667eea;
        font-weight: 600;
    }
    
    /* ==================== 성공/정보 메시지 ==================== */
    .stSuccess {
        background: linear-gradient(135deg, #11998e10 0%, #38ef7d10 100%);
        border: 1px solid #38ef7d50;
        border-radius: 12px;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
        border: 1px solid #667eea30;
        border-radius: 12px;
    }
    
    /* ==================== 데이터프레임 ==================== */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown("""
<div class="main-header-container">
    <div class="main-logo">🔄</div>
    <h1 class="main-title">만능 파일 변환기</h1>
    <p class="main-subtitle">이미지와 데이터 파일을 손쉽게 변환하세요</p>
    <div class="main-badges">
        <div class="badge"><span class="badge-icon">⚡</span> 초고속 변환</div>
        <div class="badge"><span class="badge-icon">🔒</span> 100% 안전</div>
        <div class="badge"><span class="badge-icon">💰</span> 완전 무료</div>
    </div>
</div>
""", unsafe_allow_html=True)


def convert_image(image_bytes: bytes, original_format: str, target_format: str) -> bytes:
    """
    이미지를 원하는 포맷으로 변환합니다.
    
    Args:
        image_bytes: 원본 이미지 바이트 데이터
        original_format: 원본 이미지 형식
        target_format: 변환할 이미지 형식
    
    Returns:
        변환된 이미지의 바이트 데이터
    """
    # 이미지 열기
    img = Image.open(io.BytesIO(image_bytes))
    
    # RGBA 모드인 경우 JPG 변환 시 RGB로 변환 필요
    if target_format.upper() == "JPG" or target_format.upper() == "JPEG":
        if img.mode in ('RGBA', 'LA', 'P'):
            # 알파 채널이 있는 경우 흰색 배경으로 합성
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        save_format = 'JPEG'
    else:
        save_format = target_format.upper()
        if save_format == 'JPG':
            save_format = 'JPEG'
    
    # 메모리에 저장
    output_buffer = io.BytesIO()
    
    if save_format == 'JPEG':
        img.save(output_buffer, format=save_format, quality=95)
    else:
        img.save(output_buffer, format=save_format)
    
    output_buffer.seek(0)
    return output_buffer.getvalue()


def get_file_extension(filename: str) -> str:
    """파일명에서 확장자를 추출합니다."""
    return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''


def create_zip_from_files(files_data: list) -> bytes:
    """
    여러 파일을 ZIP으로 압축합니다.
    
    Args:
        files_data: (파일명, 바이트데이터) 튜플의 리스트
    
    Returns:
        ZIP 파일의 바이트 데이터
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, data in files_data:
            zip_file.writestr(filename, data)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


# 탭 생성
tab1, tab2 = st.tabs(["🖼️ 이미지 변환소", "📊 엑셀/데이터 변환소"])


# ==================== 탭 1: 이미지 변환소 ====================
with tab1:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🖼️</div>
        <div>
            <h2 class="section-title">이미지 변환소</h2>
            <p class="section-desc">PNG, JPG, JPEG, WEBP 이미지를 원하는 형식으로 변환하세요</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 문맥 광고 배너
    show_context_ad("이미지")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 파일 업로드
        uploaded_images = st.file_uploader(
            "이미지 파일을 선택하세요 (여러 개 선택 가능)",
            type=['png', 'jpg', 'jpeg', 'webp'],
            accept_multiple_files=True,
            key="image_uploader",
            help="PNG, JPG, JPEG, WEBP 형식의 이미지를 업로드하세요."
        )
    
    with col2:
        # 변환 형식 선택
        target_format = st.selectbox(
            "변환할 형식 선택",
            options=['PNG', 'JPG', 'WEBP'],
            index=0,
            key="image_format",
            help="변환하고 싶은 이미지 형식을 선택하세요."
        )
    
    if uploaded_images:
        st.markdown("---")
        st.subheader(f"📁 업로드된 파일: {len(uploaded_images)}개")
        
        # 업로드된 이미지 미리보기
        preview_cols = st.columns(min(len(uploaded_images), 4))
        for idx, img_file in enumerate(uploaded_images[:4]):
            with preview_cols[idx % 4]:
                try:
                    img = Image.open(img_file)
                    st.image(img, caption=img_file.name, use_container_width=True)
                    # 파일 포인터 초기화
                    img_file.seek(0)
                except Exception:
                    st.warning(f"미리보기 불가: {img_file.name}")
        
        if len(uploaded_images) > 4:
            st.info(f"...외 {len(uploaded_images) - 4}개의 파일이 더 있습니다.")
        
        st.markdown("---")
        
        # 변환 버튼
        if st.button("🔄 변환하기", key="convert_images", type="primary", use_container_width=True):
            converted_files = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 로딩 중 광고 표시
            loading_ad_placeholder = st.empty()
            with loading_ad_placeholder.container():
                show_loading_ad("이미지")
            
            for idx, img_file in enumerate(uploaded_images):
                try:
                    status_text.text(f"변환 중... ({idx + 1}/{len(uploaded_images)}) - {img_file.name}")
                    
                    # 원본 확장자 확인
                    original_ext = get_file_extension(img_file.name)
                    
                    # 이미지 변환
                    img_bytes = img_file.read()
                    converted_bytes = convert_image(img_bytes, original_ext, target_format)
                    
                    # 새 파일명 생성
                    new_filename = img_file.name.rsplit('.', 1)[0] + '.' + target_format.lower()
                    converted_files.append((new_filename, converted_bytes))
                    
                    # 진행률 업데이트
                    progress_bar.progress((idx + 1) / len(uploaded_images))
                    
                except Exception as e:
                    st.error(f"⚠️ '{img_file.name}' 변환 중 문제가 발생했습니다. 파일을 확인해 주세요.")
                    continue
            
            status_text.empty()
            progress_bar.empty()
            loading_ad_placeholder.empty()
            
            if converted_files:
                st.success(f"✅ {len(converted_files)}개의 파일이 성공적으로 변환되었습니다!")
                
                # 다운로드 섹션
                st.markdown("### 📥 다운로드")
                
                if len(converted_files) == 1:
                    # 단일 파일 다운로드
                    filename, data = converted_files[0]
                    st.download_button(
                        label=f"📥 {filename} 다운로드",
                        data=data,
                        file_name=filename,
                        mime=f"image/{target_format.lower()}",
                        use_container_width=True
                    )
                else:
                    # 여러 파일: ZIP으로 압축 다운로드
                    zip_data = create_zip_from_files(converted_files)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    zip_filename = f"converted_images_{timestamp}.zip"
                    
                    st.download_button(
                        label=f"📥 모든 파일 다운로드 (ZIP)",
                        data=zip_data,
                        file_name=zip_filename,
                        mime="application/zip",
                        use_container_width=True
                    )
                    
                    # 개별 다운로드 옵션
                    with st.expander("📂 개별 파일 다운로드"):
                        for filename, data in converted_files:
                            st.download_button(
                                label=f"📥 {filename}",
                                data=data,
                                file_name=filename,
                                mime=f"image/{target_format.lower()}",
                                key=f"download_{filename}"
                            )
    else:
        # 안내 메시지
        st.info("👆 위에서 이미지 파일을 업로드해 주세요.")


# ==================== 탭 2: 엑셀/데이터 변환소 ====================
with tab2:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <div>
            <h2 class="section-title">엑셀/데이터 변환소</h2>
            <p class="section-desc">CSV와 Excel 파일을 서로 변환하세요</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 문맥 광고 배너
    show_context_ad("엑셀")
    
    # 파일 업로드
    uploaded_data = st.file_uploader(
        "CSV 또는 Excel 파일을 선택하세요",
        type=['csv', 'xlsx', 'xls'],
        key="data_uploader",
        help="CSV 파일은 Excel로, Excel 파일은 CSV로 변환됩니다."
    )
    
    if uploaded_data:
        file_ext = get_file_extension(uploaded_data.name)
        
        st.markdown("---")
        
        # 파일 정보 표시
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 파일명", uploaded_data.name)
        with col2:
            st.metric("📁 현재 형식", file_ext.upper())
        with col3:
            target = "XLSX" if file_ext == 'csv' else "CSV"
            st.metric("🎯 변환 형식", target)
        
        try:
            # 데이터 읽기
            if file_ext == 'csv':
                # CSV 인코딩 자동 감지 시도
                try:
                    df = pd.read_csv(uploaded_data, encoding='utf-8')
                except UnicodeDecodeError:
                    uploaded_data.seek(0)
                    try:
                        df = pd.read_csv(uploaded_data, encoding='cp949')
                    except UnicodeDecodeError:
                        uploaded_data.seek(0)
                        df = pd.read_csv(uploaded_data, encoding='euc-kr')
            else:
                df = pd.read_excel(uploaded_data, engine='openpyxl')
            
            # 데이터 미리보기
            st.subheader("📋 데이터 미리보기")
            st.dataframe(df.head(10), use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"📊 총 {len(df):,}개 행, {len(df.columns)}개 열")
            
            st.markdown("---")
            
            # 변환 버튼
            if st.button("🔄 변환하기", key="convert_data", type="primary", use_container_width=True):
                with st.spinner("변환 중..."):
                    try:
                        output_buffer = io.BytesIO()
                        
                        if file_ext == 'csv':
                            # CSV → Excel 변환
                            df.to_excel(output_buffer, index=False, engine='xlsxwriter')
                            new_filename = uploaded_data.name.rsplit('.', 1)[0] + '.xlsx'
                            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        else:
                            # Excel → CSV 변환
                            df.to_csv(output_buffer, index=False, encoding='utf-8-sig')
                            new_filename = uploaded_data.name.rsplit('.', 1)[0] + '.csv'
                            mime_type = "text/csv"
                        
                        output_buffer.seek(0)
                        
                        st.success("✅ 변환이 완료되었습니다!")
                        
                        st.download_button(
                            label=f"📥 {new_filename} 다운로드",
                            data=output_buffer.getvalue(),
                            file_name=new_filename,
                            mime=mime_type,
                            use_container_width=True
                        )
                        
                    except Exception as e:
                        st.error("⚠️ 변환 중 문제가 발생했습니다. 파일 형식을 확인해 주세요.")
                        
        except Exception as e:
            st.error("⚠️ 파일을 읽는 중 문제가 발생했습니다. 올바른 CSV 또는 Excel 파일인지 확인해 주세요.")
    else:
        # 안내 메시지
        st.info("👆 위에서 CSV 또는 Excel 파일을 업로드해 주세요.")


# 푸터
st.markdown("""                                                                                                                                           
<div class="premium-footer">
    <p class="footer-text">
        ⚡ 모든 파일은 메모리에서만 처리되어 <strong>빠르고 안전</strong>합니다
    </p>
    <p class="footer-text" style="margin-top: 8px;">
        Made with ❤️ by <span class="footer-brand">File Converter</span>
    </p>
    <p class="footer-text" style="margin-top: 12px; font-size: 0.75rem; color: #aaa;">
        이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.
    </p>
</div>
""", unsafe_allow_html=True)

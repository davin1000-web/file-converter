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


# 페이지 설정
st.set_page_config(
    page_title="만능 파일 변환기",
    page_icon="🔄",
    layout="wide"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 20px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown('<h1 class="main-header">🔄 만능 파일 변환기</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">이미지와 데이터 파일을 손쉽게 변환하세요!</p>', unsafe_allow_html=True)


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
    st.header("🖼️ 이미지 변환소")
    st.markdown("PNG, JPG, JPEG, WEBP 이미지를 원하는 형식으로 변환하세요.")
    
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
    st.header("📊 엑셀/데이터 변환소")
    st.markdown("CSV와 Excel 파일을 서로 변환하세요.")
    
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
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #888; padding: 1rem;">
        <p>💡 <strong>Tip:</strong> 이 앱은 모든 파일 처리를 메모리에서 수행하여 빠르고 안전합니다.</p>
        <p>Made with ❤️ using Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)

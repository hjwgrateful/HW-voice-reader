import streamlit as st
import PyPDF2
import os
from pathlib import Path
import edge_tts
import asyncio

def extract_text_from_pdf(pdf_file):
    """从PDF文件中提取文本"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

async def text_to_speech(text, output_file="output.mp3"):
    """将文本转换为语音"""
    voice = "zh-CN-XiaoxiaoNeural"  # 中文女声
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def main():
    st.title("PDF语音阅读器")
    
    uploaded_file = st.file_uploader("上传PDF文件", type="pdf")
    
    if uploaded_file is not None:
        # 提取文本
        with st.spinner("正在提取文本..."):
            text = extract_text_from_pdf(uploaded_file)
            st.text_area("提取的文本", text, height=200)
        
        if st.button("转换为语音"):
            with st.spinner("正在生成语音..."):
                # 创建异步事件循环
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # 生成语音
                output_file = "output.mp3"
                loop.run_until_complete(text_to_speech(text, output_file))
                
                # 读取生成的音频文件
                with open(output_file, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    
                # 显示音频播放器
                st.audio(audio_bytes, format="audio/mp3")
                
                # 提供下载按钮
                st.download_button(
                    label="下载音频文件",
                    data=audio_bytes,
                    file_name="audio.mp3",
                    mime="audio/mp3"
                )

if __name__ == "__main__":
    main()
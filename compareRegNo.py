import streamlit as st
import re

def format_data(data, library_code):
    data = data.upper().strip()
    regex2 = "^[A-Za-z]{2}\d+$"
    regex3 = "^[A-Za-z]{3}\d+$"
    
    if re.match(regex2, data):
        prefix, number = data[:2], data[2:]
        formatted_number = number.zfill(9)
        return (library_code + prefix + formatted_number) if library_code else (prefix + formatted_number)
    elif re.match(regex3, data):
        prefix, number = data[:3], data[3:]
        return prefix + number.zfill(9)
    return None

def compare_data(a_data, b_data, library_code):
    a_list = [format_data(item, library_code) for item in a_data.split("\n") if item.strip()]
    b_list = [format_data(item, library_code) for item in b_data.split("\n") if item.strip()]
    
    a_list = list(filter(None, a_list))
    b_list = list(filter(None, b_list))
    
    intersection = sorted(set(a_list) & set(b_list))
    union = sorted(set(a_list) | set(b_list))
    a_minus_b = sorted(set(a_list) - set(b_list))
    b_minus_a = sorted(set(b_list) - set(a_list))
    
    return intersection, union, a_minus_b, b_minus_a

# Streamlit UI 시작
st.title("📌 등록번호 비교 프로그램")

# 입력 필드
a_data = st.text_area("A 데이터 입력", placeholder="예시: ABC12345, AB12345", height=150, key="a_data")
b_data = st.text_area("B 데이터 입력", placeholder="예시: ABC12345, AB12345", height=150, key="b_data")

# 도서관 부호 입력
library_code = st.text_input("도서관 부호 (선택 사항)", key="library_code").upper()

if st.button("🔍 비교하기"):
    if not a_data.strip() or not b_data.strip():
        st.warning("A 데이터와 B 데이터를 입력하세요.")
    else:
        intersection, union, a_minus_b, b_minus_a = compare_data(a_data, b_data, library_code)
        
        st.subheader("🔗 비교 결과")
        st.text_area(f"✅ 교집합 (A ∩ B): {len(intersection)}개", "\n".join(intersection) if intersection else "없음", height=150)
        st.text_area(f"🔀 합집합 (A ∪ B): {len(union)}개", "\n".join(union), height=150)
        st.text_area(f"➖ A - B: {len(a_minus_b)}개", "\n".join(a_minus_b) if a_minus_b else "없음", height=150)
        st.text_area(f"➖ B - A: {len(b_minus_a)}개", "\n".join(b_minus_a) if b_minus_a else "없음", height=150)
        
        if len(a_minus_b) == 0 and len(b_minus_a) == 0 and len(intersection) > 0:
            st.success("🎉 두 데이터가 완전히 일치합니다!")

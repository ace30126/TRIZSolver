# gemini_client.py
import google.generativeai as genai
import os # API 키를 환경 변수에서 가져올 경우 사용 가능

# API 키 설정 (중요: 실제 사용 시에는 직접 코드에 넣기보다 환경 변수나 안전한 설정 파일 사용 권장)
# 예: genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# 여기서는 main.py에서 사용자가 입력한 키를 받아 사용하도록 함수 설계

def generate_with_gemini(api_key: str, prompt_text: str, temperature: float = 0.9, model_name: str = "gemini-1.5-flash-latest"):
    """
    Gemini API를 사용하여 주어진 프롬프트에 대한 텍스트를 생성합니다.

    Args:
        api_key (str): Gemini API 키.
        prompt_text (str): Gemini 모델에 전달할 프롬프트.
        temperature (float): 생성 다양성을 위한 온도 값 (0.0 ~ 1.0). 높을수록 창의적.
        model_name (str): 사용할 Gemini 모델 이름.

    Returns:
        str: 생성된 텍스트 또는 오류 메시지.
    """
    if not api_key:
        return "오류: Gemini API 키가 제공되지 않았습니다."

    try:
        genai.configure(api_key=api_key)

        generation_config = genai.types.GenerationConfig(
            candidate_count=1,
            temperature=temperature
        )

        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            # safety_settings 설정 (필요에 따라 조정)
            # 예:
            # safety_settings=[
            #     {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            #     {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            #     {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            #     {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            # ]
        )

        response = model.generate_content(prompt_text)
        
        if response.candidates:
            # 첫 번째 후보의 텍스트 콘텐츠 반환
            # response.text가 간단하지만, 좀 더 안정적으로 content.parts 에서 텍스트를 추출
            if response.candidates[0].content and response.candidates[0].content.parts:
                return "".join(part.text for part in response.candidates[0].content.parts if hasattr(part, 'text'))
            elif hasattr(response, 'text'): # Fallback for simpler cases or older API versions
                 return response.text
            else:
                return "오류: 응답에서 텍스트를 찾을 수 없습니다."
        else:
            # 프롬프트 피드백 확인 (차단된 경우 등)
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                return f"오류: 콘텐츠 생성 차단됨. 이유: {response.prompt_feedback.block_reason_message or response.prompt_feedback.block_reason}"
            return "오류: Gemini로부터 응답을 받지 못했습니다. (No candidates)"

    except Exception as e:
        return f"Gemini API 호출 중 오류 발생: {e}"

if __name__ == '__main__':
    # 테스트용 코드 (직접 실행 시)
    print("Gemini 클라이언트 테스트 시작...")
    test_api_key = input("테스트용 Gemini API 키를 입력하세요: ") # 실제 API 키 입력
    if test_api_key:
        test_prompt = "대한민국의 수도는 어디인가요? 한 문장으로 답해주세요."
        print(f"프롬프트: {test_prompt}")
        result = generate_with_gemini(test_api_key, test_prompt, temperature=0.5)
        print("\nGemini 응답:")
        print(result)
    else:
        print("API 키가 입력되지 않아 테스트를 건너뜁니다.")
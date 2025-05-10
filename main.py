# main.py
import customtkinter as ctk
from tkinter import messagebox, Toplevel, END, filedialog
import datetime
import scamper_core # scamper_core.py 임포트
import triz_core    # triz_core.py 임포트
import gemini_client # gemini_client.py 임포트
import configparser
import os
from ui_components import ScamperUI, TrizUI # ui_components.py 에서 클래스 임포트

# CustomTkinter 기본 설정
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "triz_solver_config.ini"

class TRIZSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TRIZSolver - 아이디어 발상 도우미")
        self.root.geometry("1000x750")

        self.gemini_api_key = ctk.StringVar()
        self.load_api_key()

        # SCAMPER 모듈용 변수
        self.current_product_idea = ctk.StringVar()
        self.scamper_ui_instance = None # ScamperUI 인스턴스 저장용
        self.scamper_details_frame = None # ScamperUI가 관리 (참조용)
        self.scamper_gemini_result_textbox = None # ScamperUI가 관리 (참조용)


        # TRIZ 모듈용 변수
        self.triz_improving_param = ctk.StringVar()
        self.triz_worsening_param = ctk.StringVar()
        self.triz_ui_instance = None # TrizUI 인스턴스 저장용
        self.triz_suggested_principles_frame = None # TrizUI가 관리 (참조용)
        self.triz_principle_details_textbox = None # TrizUI가 관리 (참조용)
        self.triz_problem_context_entry = None # TrizUI가 관리 (참조용)
        self.triz_gemini_result_textbox = None # TrizUI가 관리 (참조용)
        self.triz_selected_principle_details = None

        self.create_main_widgets()

    def load_api_key(self):
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE):
            try:
                config.read(CONFIG_FILE, encoding='utf-8')
                if 'Gemini' in config and 'ApiKey' in config['Gemini']:
                    self.gemini_api_key.set(config['Gemini']['ApiKey'])
            except Exception:
                pass

    def save_api_key(self):
        config = configparser.ConfigParser()
        current_key = self.gemini_api_key.get()
        if not current_key.strip():
            messagebox.showwarning("API 키 없음", "저장할 API 키를 먼저 입력해주세요.")
            return
        config['Gemini'] = {'ApiKey': current_key}
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
                config.write(configfile)
            messagebox.showinfo("저장 완료", "API 키가 성공적으로 저장되었습니다.")
        except Exception as e:
            messagebox.showerror("저장 실패", f"API 키 저장 중 오류가 발생했습니다:\n{e}")

    def create_main_widgets(self):
        top_controls_frame = ctk.CTkFrame(self.root)
        top_controls_frame.pack(fill="x", padx=10, pady=(10,5))

        ctk.CTkLabel(top_controls_frame, text="Gemini API Key:", font=ctk.CTkFont(size=13)).pack(side="left", padx=(10,5), pady=10)
        api_key_entry = ctk.CTkEntry(top_controls_frame, textvariable=self.gemini_api_key, width=250, font=ctk.CTkFont(size=13))
        api_key_entry.pack(side="left", padx=5, pady=10)
        save_key_button = ctk.CTkButton(top_controls_frame, text="키 저장", command=self.save_api_key, width=60)
        save_key_button.pack(side="left", padx=(0,10), pady=10)

        mode_label = ctk.CTkLabel(top_controls_frame, text="모드 선택:", font=ctk.CTkFont(size=13))
        mode_label.pack(side="left", padx=(10, 5), pady=10)

        triz_button = ctk.CTkButton(top_controls_frame, text="TRIZ", command=self.open_triz_module, width=70)
        triz_button.pack(side="left", padx=5, pady=10)
        triz_help_button = ctk.CTkButton(top_controls_frame, text="TRIZ 도움말", command=self.show_triz_general_help, width=100, fg_color="gray")
        triz_help_button.pack(side="left", padx=(0,5), pady=10)

        scamper_button = ctk.CTkButton(top_controls_frame, text="SCAMPER", command=self.open_scamper_module, width=80)
        scamper_button.pack(side="left", padx=5, pady=10)
        scamper_help_button = ctk.CTkButton(top_controls_frame, text="SCAMPER 도움말", command=self.show_scamper_general_help, width=120, fg_color="gray")
        scamper_help_button.pack(side="left", padx=(0,5), pady=10)

        self.content_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=(5,10))
        self.show_initial_message()

    def show_help_window(self, title, content_text):
        help_win = Toplevel(self.root)
        help_win.title(title)
        help_win.geometry("500x400")
        help_win.attributes("-topmost", True)
        text_area = ctk.CTkTextbox(help_win, wrap="word", font=("Arial", 12))
        text_area.pack(fill="both", expand=True, padx=10, pady=10)
        text_area.insert(END, content_text)
        text_area.configure(state="disabled")
        close_button = ctk.CTkButton(help_win, text="닫기", command=help_win.destroy, width=80)
        close_button.pack(pady=10)
        help_win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (help_win.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (help_win.winfo_height() // 2)
        help_win.geometry(f"+{x}+{y}")

    def show_scamper_general_help(self):
        title = "SCAMPER 기법이란?"
        content = """
SCAMPER는 창의적인 아이디어 발상을 위한 질문 기법입니다.
기존 제품, 서비스, 또는 문제에 대해 다음 7가지 관점에서 질문을 던져 새로운 아이디어를 도출합니다:

S - Substitute (대체하기):
    기존의 것을 다른 것으로 바꾸면 어떨까요? (부품, 재료, 사람, 규칙, 과정, 장소, 시간 등)
    새로운 가능성이나 개선점을 찾을 수 있습니다.

C - Combine (결합하기):
    서로 다른 아이디어나 기능, 목적을 합치면 어떨까요?
    새로운 시너지 효과나 독창적인 해결책을 만들 수 있습니다.

A - Adapt (응용하기):
    다른 분야의 아이디어, 기술, 해결책을 현재 문제에 맞게 변형하여 적용하면 어떨까요?
    새로운 관점에서 문제를 바라보고 해결의 실마리를 찾을 수 있습니다.

M - Modify/Magnify/Minify (수정/확대/축소하기):
    기존 아이디어나 제품의 특정 부분을 변경하거나, 크기, 형태, 기능 등을 확대 또는 축소하면 어떨까요?
    새로운 가치를 창출하거나 문제점을 개선할 수 있습니다.

P - Put to other uses (다른 용도로 사용하기):
    현재 제품이나 아이디어를 원래 목적 외에 다른 새로운 용도로 사용할 수 있을까요?
    숨겨진 잠재력을 발견하고 새로운 시장을 개척할 수도 있습니다.

E - Eliminate (제거하기):
    제품이나 프로세스에서 불필요하거나 비효율적인 부분을 없애거나 단순화하면 어떨까요?
    핵심 가치에 집중하고 효율성을 높일 수 있습니다.

R - Reverse/Rearrange (재배열/역발상하기):
    구성 요소의 순서, 배치, 방향을 바꾸거나 기존의 생각이나 과정을 거꾸로 뒤집어 보면 어떨까요?
    새로운 관점과 혁신적인 아이디어를 얻을 수 있습니다.

SCAMPER 모듈에서 각 기법을 선택하면 해당 기법에 대한 더 구체적인 질문 목록과 개별 도움말을 볼 수 있습니다.
        """
        self.show_help_window(title, content)

    def show_triz_general_help(self):
        title = "TRIZ 사용법 안내"
        content = """
TRIZ (Teoriya Resheniya Izobretatelskikh Zadach, 창의적 문제 해결 이론)는
러시아의 겐리히 알트슐러에 의해 개발된 문제 해결 및 발명을 위한 체계적이고 과학적인 방법론입니다.
주로 기술 시스템의 문제를 분석하고 혁신적인 해결책을 찾는 데 사용됩니다.

TRIZ의 핵심 원리:
1.  모순(Contradiction): 어떤 특성을 개선하려 할 때 다른 특성이 악화되는 상황을 '기술 모순'이라고 합니다. TRIZ는 이러한 모순을 회피하거나 극복하는 방법을 제시합니다.
2.  이상성(Ideality): 시스템은 시간이 지남에 따라 유용한 기능은 증가하고 유해한 기능과 비용은 감소하는 방향으로 진화한다는 개념입니다. 이상적인 최종 결과(IFR)를 상상하는 것이 중요합니다.
3.  자원(Resources): 문제 해결에 사용할 수 있는 모든 시스템 내부 및 주변 환경의 요소를 의미합니다. TRIZ는 숨겨진 자원을 발견하고 활용하도록 돕습니다.
4.  발명 원리(Inventive Principles): 과거의 수많은 특허 분석을 통해 도출된, 모순을 해결하는 데 효과적인 40가지 보편적인 원리입니다.
5.  기술 진화의 법칙(Laws of Technical System Evolution): 기술 시스템이 특정 패턴과 경향을 따라 발전한다는 법칙들입니다.

이 프로그램에서의 TRIZ 활용 단계:
1.  문제 정의: 해결하고자 하는 문제를 명확히 합니다.
2.  기술 특성 선택:
    - '개선하려는 특성': 문제 해결을 통해 향상시키고 싶은 기술적 지표 (예: 속도, 강도, 무게 등 39가지 표준 특성 중 선택)
    - '악화되는 특성': 개선을 시도할 때 원치 않게 나빠지는 다른 기술적 지표 (39가지 표준 특성 중 선택)
3.  모순 매트릭스 활용: 선택한 '개선 특성'과 '악화 특성'의 조합에 해당하는 발명 원리를 모순 매트릭스에서 찾습니다. 이 프로그램에서는 '원리 찾기' 버튼을 누르면 자동으로 추천됩니다. (CSV 파일에 모순 매트릭스 데이터가 정확히 입력되어 있어야 합니다.)
4.  발명 원리 적용: 추천된 발명 원리들의 설명을 참고하여, 현재 문제에 창의적으로 적용할 아이디어를 구체화합니다.
5.  Gemini 활용: 도출된 원리와 문제 상황을 바탕으로 Gemini에게 더 확장된 아이디어를 요청하여 아이디어 발상을 지원받을 수 있습니다.

40가지 발명 원리에 대한 상세 설명은 좌측 '추천 발명 원리' 목록에서 특정 원리를 선택하면 우측 상세 설명 창에 표시됩니다.
        """
        self.show_help_window(title, content)


    def save_ideas_to_file(self, content_to_save, source_module=""):
        if not content_to_save.strip() or "Gemini 버튼을 누르면" in content_to_save or "가져오는 중입니다" in content_to_save :
            messagebox.showinfo("저장할 내용 없음", "저장할 아이디어가 없습니다.\n먼저 Gemini로부터 아이디어를 생성해주세요.")
            return
        now = datetime.datetime.now()
        default_filename = f"{source_module}_아이디어_{now.strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=default_filename, title="아이디어 저장 위치 선택"
        )
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content_to_save)
                messagebox.showinfo("저장 완료", f"아이디어가 다음 경로에 저장되었습니다:\n{filepath}")
            except Exception as e:
                messagebox.showerror("저장 실패", f"파일 저장 중 오류가 발생했습니다:\n{e}")

    def show_initial_message(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="TRIZ 또는 SCAMPER 버튼을 눌러 시작하세요.",
                       font=ctk.CTkFont(size=18, weight="bold")).pack(pady=50, padx=20)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        # UI 인스턴스 참조도 초기화
        self.scamper_ui_instance = None
        self.triz_ui_instance = None
        # 개별 UI 요소 참조도 초기화 (ui_components에서 관리하므로 여기서는 필수 아님, 필요시 유지)
        self.scamper_details_frame = None
        self.scamper_gemini_result_textbox = None
        self.triz_suggested_principles_frame = None
        self.triz_principle_details_textbox = None
        self.triz_problem_context_entry = None
        self.triz_gemini_result_textbox = None


    def open_scamper_module(self):
        self.clear_content_frame()
        # ScamperUI 인스턴스 생성 및 self.content_frame에 UI 빌드
        self.scamper_ui_instance = ScamperUI(self.content_frame, self)

    def open_triz_module(self):
        self.clear_content_frame()
        # TrizUI 인스턴스 생성 및 self.content_frame에 UI 빌드
        self.triz_ui_instance = TrizUI(self.content_frame, self)

    # --- 핵심 로직 (Gemini 호출 등) ---
    # get_gemini_scamper_ideas, get_gemini_triz_ideas는 여기에 유지됩니다.
    # ui_components의 버튼들은 self.app.get_gemini_scamper_ideas(...) 와 같이 호출합니다.

    def get_gemini_scamper_ideas(self, category, user_ideas_text):
        # 이전에 scamper_gemini_result_textbox를 직접 참조하던 부분을
        # self.scamper_ui_instance.gemini_result_textbox (또는 app에 저장된 참조)를 사용하도록 해야 합니다.
        # 여기서는 self.scamper_gemini_result_textbox가 ScamperUI 생성 시 app에 업데이트 된다고 가정합니다.
        if not self.scamper_gemini_result_textbox:
            # UI 인스턴스가 아직 없거나, 해당 텍스트박스가 UI에 없는 경우 처리
            # print("SCAMPER Gemini 결과 텍스트 박스를 찾을 수 없습니다.")
            return

        api_key = self.gemini_api_key.get()
        product_idea = self.current_product_idea.get()

        if not api_key:
            messagebox.showerror("API 키 오류", "Gemini API 키를 입력해주세요. (상단 입력창)")
            return
        if not product_idea:
            messagebox.showwarning("입력 필요", "분석할 제품/아이디어/문제를 입력해주세요.")
            return

        self.scamper_gemini_result_textbox.configure(state="normal")
        self.scamper_gemini_result_textbox.delete("1.0", "end")
        self.scamper_gemini_result_textbox.insert("0.0", f"Gemini로부터 '{category.split(' ')[0]}'에 대한 아이디어를 가져오는 중입니다...\n잠시만 기다려주세요...")
        self.scamper_gemini_result_textbox.configure(state="disabled")
        self.root.update_idletasks()

        prompt = f"""
        당신은 세계 최고의 창의적 아이디어 발상 전문가입니다.
        SCAMPER 기법의 '{category}' 단계를 사용하여 '{product_idea}'에 대한 혁신적이고 실행 가능한 아이디어 5가지를 제안해주세요.
        SCAMPER의 '{category}'는 다음과 같은 질문을 통해 아이디어를 찾는 방법입니다:
        {", ".join(scamper_core.get_questions_for_category(category))}
        사용자가 이미 다음과 같은 아이디어를 생각해 보았습니다 (만약 비어있다면, 완전히 새로운 아이디어를 제안해주세요):
        '{user_ideas_text}'
        이 아이디어를 참고하거나, 더 발전시키거나, 전혀 다른 새로운 관점의 아이디어를 제안해도 좋습니다.
        각 아이디어는 명확하게 번호(#1, #2 등)를 매기고, 왜 해당 아이디어가 좋은지 또는 어떤 효과를 기대할 수 있는지 간략한 설명을 포함해주세요.
        답변은 반드시 한국어로 해주세요. 창의성을 최대한 발휘해주세요.
        """
        try:
            generated_ideas = gemini_client.generate_with_gemini(api_key=api_key, prompt_text=prompt, temperature=0.9)
            self.scamper_gemini_result_textbox.configure(state="normal")
            self.scamper_gemini_result_textbox.delete("1.0", "end")
            if "오류:" in generated_ideas:
                 self.scamper_gemini_result_textbox.insert("0.0", generated_ideas)
                 messagebox.showerror("Gemini 응답 오류", generated_ideas)
            else:
                self.scamper_gemini_result_textbox.insert("0.0", generated_ideas)
        except Exception as e:
            self.scamper_gemini_result_textbox.configure(state="normal")
            self.scamper_gemini_result_textbox.delete("1.0", "end")
            error_message = f"Gemini 아이디어 생성 중 예상치 못한 오류 발생:\n{e}"
            self.scamper_gemini_result_textbox.insert("0.0", error_message)
            messagebox.showerror("Gemini 호출 오류", error_message)
        finally:
            if self.scamper_gemini_result_textbox:
                self.scamper_gemini_result_textbox.configure(state="disabled")

    def get_gemini_triz_ideas(self):
        # 여기도 self.triz_gemini_result_textbox 와 self.triz_problem_context_entry 가
        # TrizUI 생성 시 app에 업데이트 된다고 가정합니다.
        if not self.triz_gemini_result_textbox or not self.triz_problem_context_entry:
            # print("TRIZ Gemini 결과 또는 문제 컨텍스트 텍스트 박스를 찾을 수 없습니다.")
            return

        api_key = self.gemini_api_key.get()
        # TrizUI의 problem_context_entry에서 값을 가져와야 함
        user_problem = self.triz_problem_context_entry.get("1.0", "end-1c").strip()


        if not api_key:
            messagebox.showerror("API 키 오류", "Gemini API 키를 입력해주세요.")
            return
        if not self.triz_selected_principle_details: # 이것은 main_app이 여전히 관리
            messagebox.showwarning("원리 선택 필요", "먼저 좌측에서 발명 원리를 선택해주세요.")
            return
        if not user_problem:
            messagebox.showwarning("문제 상황 입력 필요", "이 원리를 적용할 문제 상황이나 아이디어 컨텍스트를 입력해주세요.")
            return

        principle_name = self.triz_selected_principle_details['name']
        principle_desc = self.triz_selected_principle_details['description']
        principle_id = self.triz_selected_principle_details['id']

        self.triz_gemini_result_textbox.configure(state="normal")
        self.triz_gemini_result_textbox.delete("1.0", "end")
        self.triz_gemini_result_textbox.insert("0.0", f"Gemini로부터 '{principle_name.split(' (')[0]}' 원리에 대한 아이디어를 가져오는 중입니다...\n잠시만 기다려주세요...")
        self.triz_gemini_result_textbox.configure(state="disabled")
        self.root.update_idletasks()

        prompt = f"""
        당신은 TRIZ 방법론과 창의적 문제 해결의 대가입니다.
        현재 해결하고자 하는 문제 또는 아이디어 컨텍스트는 다음과 같습니다:
        '{user_problem}'
        이 문제를 해결하기 위해, TRIZ의 40가지 발명 원리 중 '{principle_id}. {principle_name}' 원리를 적용하려고 합니다.
        이 원리의 핵심 설명은 다음과 같습니다: '{principle_desc}'
        '{principle_name}' 원리를 활용하여 위의 '{user_problem}' 문제를 해결할 수 있는 구체적이고 혁신적인 아이디어 5가지를 제안해주십시오.
        각 아이디어는 명확하게 번호(#1, #2 등)를 매기고, 해당 원리가 아이디어에 어떻게 적용되었는지 간략히 설명해주세요.
        답변은 반드시 한국어로 해주세요. 창의성을 최대한 발휘하여(temperature 0.9) 답변해주시기 바랍니다.
        """
        try:
            generated_ideas = gemini_client.generate_with_gemini(api_key=api_key, prompt_text=prompt, temperature=0.9)
            self.triz_gemini_result_textbox.configure(state="normal")
            self.triz_gemini_result_textbox.delete("1.0", "end")
            if "오류:" in generated_ideas:
                 self.triz_gemini_result_textbox.insert("0.0", generated_ideas)
                 messagebox.showerror("Gemini 응답 오류", generated_ideas)
            else:
                self.triz_gemini_result_textbox.insert("0.0", generated_ideas)
        except Exception as e:
            self.triz_gemini_result_textbox.configure(state="normal")
            self.triz_gemini_result_textbox.delete("1.0", "end")
            error_message = f"Gemini 아이디어 생성 중 예상치 못한 오류 발생:\n{e}"
            self.triz_gemini_result_textbox.insert("0.0", error_message)
            messagebox.showerror("Gemini 호출 오류", error_message)
        finally:
            if self.triz_gemini_result_textbox:
                self.triz_gemini_result_textbox.configure(state="disabled")

if __name__ == "__main__":
    root = ctk.CTk()
    app = TRIZSolverApp(root)
    root.mainloop()

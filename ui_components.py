# ui_components.py
import customtkinter as ctk
from tkinter import messagebox
import scamper_core # scamper_core.py 임포트
import triz_core    # triz_core.py 임포트
# gemini_client는 main_app을 통해 호출되므로 여기서는 직접 임포트 불필요

class ScamperUI:
    def __init__(self, parent_frame, app_instance):
        self.parent_frame = parent_frame
        self.app = app_instance  # TRIZSolverApp 인스턴스에 접근하기 위함
        self.details_frame = None
        self.gemini_result_textbox = None
        self.build_ui()

    def build_ui(self):
        scamper_main_frame = ctk.CTkFrame(self.parent_frame)
        scamper_main_frame.pack(fill="both", expand=True)

        item_input_frame = ctk.CTkFrame(scamper_main_frame, fg_color="transparent")
        item_input_frame.pack(fill="x", padx=20, pady=(20,10))
        ctk.CTkLabel(item_input_frame, text="분석할 제품/아이디어/문제:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0,10))
        item_entry = ctk.CTkEntry(item_input_frame, textvariable=self.app.current_product_idea, width=400, font=ctk.CTkFont(size=14))
        item_entry.pack(side="left", fill="x", expand=True)

        bottom_frame = ctk.CTkFrame(scamper_main_frame, fg_color="transparent")
        bottom_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))

        categories_frame = ctk.CTkScrollableFrame(bottom_frame, width=200, label_text="SCAMPER 기법", label_font=ctk.CTkFont(size=14, weight="bold"))
        categories_frame.pack(side="left", fill="y", padx=(0,10), pady=(5,0))
        scamper_categories = scamper_core.get_scamper_categories()
        for category_full_text in scamper_categories:
            category_short_text = category_full_text.split(" ")[0] + " " + category_full_text.split(" ")[1] + ")"
            if "Modify" in category_full_text:
                 category_short_text = "M (수정·확대·축소)"
            btn = ctk.CTkButton(categories_frame, text=category_short_text, command=lambda c=category_full_text: self.display_questions(c))
            btn.pack(fill="x", pady=3)

        self.details_frame = ctk.CTkFrame(bottom_frame)
        self.details_frame.pack(side="left", fill="both", expand=True, pady=(5,0))
        ctk.CTkLabel(self.details_frame, text="좌측에서 SCAMPER 기법을 선택하세요.", font=ctk.CTkFont(size=14)).pack(pady=20, padx=20)
        
        # app_instance의 scamper_details_frame, scamper_gemini_result_textbox를 현재 UI 요소로 업데이트
        self.app.scamper_details_frame = self.details_frame 


    def display_questions(self, category_full_text):
        if not self.details_frame:
            return
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        if not self.app.current_product_idea.get():
            messagebox.showwarning("입력 필요", "먼저 분석할 제품/아이디어/문제를 입력해주세요.", parent=self.parent_frame)
            ctk.CTkLabel(self.details_frame, text="좌측에서 SCAMPER 기법을 선택하세요.\n(제품/아이디어를 먼저 입력해야 합니다.)", font=ctk.CTkFont(size=14)).pack(pady=20, padx=20)
            return

        title_help_frame = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        title_help_frame.pack(fill="x", padx=20, pady=(10,0))
        category_display_text = category_full_text.split(" ")[0] + " " + category_full_text.split(" ")[1] + ")"
        if "Modify" in category_full_text:
            category_display_text = "M (수정·확대·축소하기)"

        title_label = ctk.CTkLabel(title_help_frame, text=f"{category_display_text}", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(side="left", anchor="w")
        help_button = ctk.CTkButton(title_help_frame, text="?", width=28, height=28,
                                    command=lambda c=category_full_text: self.app.show_help_window(f"{c} 도움말", scamper_core.get_help_text_for_category(c)))
        help_button.pack(side="left", padx=(10,0), anchor="w")

        questions_label = ctk.CTkLabel(self.details_frame, text="다음 질문들을 참고하여 아이디어를 떠올려 보세요:", font=ctk.CTkFont(size=13))
        questions_label.pack(pady=(5,5), padx=20, anchor="w")
        
        questions = scamper_core.get_questions_for_category(category_full_text)
        questions_textbox = ctk.CTkTextbox(self.details_frame, height=150, wrap="word", font=ctk.CTkFont(size=13))
        questions_textbox.pack(fill="x", expand=True, padx=20, pady=5)
        for q_idx, q in enumerate(questions):
            questions_textbox.insert("end", f"▶ {q}\n" + ("\n" if q_idx < len(questions) -1 else ""))
        questions_textbox.configure(state="disabled")

        ctk.CTkLabel(self.details_frame, text="나의 아이디어:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15,5), padx=20, anchor="w")
        user_idea_textbox = ctk.CTkTextbox(self.details_frame, height=100, wrap="word", font=ctk.CTkFont(size=13))
        user_idea_textbox.pack(fill="x", padx=20, pady=5)
        user_idea_textbox.insert("0.0", f"'{self.app.current_product_idea.get()}'에 대한 {category_display_text} 아이디어를 적어보세요...")

        action_buttons_frame = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        action_buttons_frame.pack(fill="x", padx=20, pady=10)

        gemini_button = ctk.CTkButton(action_buttons_frame, text="Gemini 아이디어", command=lambda c=category_full_text, uit=user_idea_textbox: self.app.get_gemini_scamper_ideas(c, uit.get("1.0", "end-1c")))
        gemini_button.pack(side="left", expand=True, padx=(0,5))

        save_button = ctk.CTkButton(action_buttons_frame, text="파일로 저장", command=lambda: self.app.save_ideas_to_file(self.gemini_result_textbox.get("1.0", "end-1c") if self.gemini_result_textbox else "", "SCAMPER"))
        save_button.pack(side="left", expand=True, padx=(5,0))

        ctk.CTkLabel(self.details_frame, text="Gemini 제안 아이디어:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(5,5), padx=20, anchor="w")
        self.gemini_result_textbox = ctk.CTkTextbox(self.details_frame, wrap="word", font=ctk.CTkFont(size=13))
        self.gemini_result_textbox.pack(fill="both", expand=True, padx=20, pady=(0,20))
        self.gemini_result_textbox.insert("0.0", "Gemini 버튼을 누르면 여기에 아이디어가 표시됩니다.")
        self.gemini_result_textbox.configure(state="disabled")
        self.app.scamper_gemini_result_textbox = self.gemini_result_textbox # app 인스턴스의 textbox 참조 업데이트


class TrizUI:
    def __init__(self, parent_frame, app_instance):
        self.parent_frame = parent_frame
        self.app = app_instance
        self.suggested_principles_frame = None
        self.principle_details_textbox = None
        self.problem_context_entry = None
        self.gemini_result_textbox = None
        self.build_ui()

    def build_ui(self):
        triz_main_frame = ctk.CTkFrame(self.parent_frame)
        triz_main_frame.pack(fill="both", expand=True)

        params_frame = ctk.CTkFrame(triz_main_frame)
        params_frame.pack(fill="x", padx=20, pady=(20,10))
        parameters = triz_core.get_engineering_parameters()

        ctk.CTkLabel(params_frame, text="개선하려는 특성:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0,5))
        improving_combo = ctk.CTkComboBox(params_frame, variable=self.app.triz_improving_param, values=parameters, width=280, font=ctk.CTkFont(size=12), state="readonly")
        improving_combo.pack(side="left", padx=(0,10))
        improving_combo.set(parameters[0] if parameters else "")

        ctk.CTkLabel(params_frame, text="악화되는 특성:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0,5))
        worsening_combo = ctk.CTkComboBox(params_frame, variable=self.app.triz_worsening_param, values=parameters, width=280, font=ctk.CTkFont(size=12), state="readonly")
        worsening_combo.pack(side="left", padx=(0,10))
        worsening_combo.set(parameters[1] if len(parameters)>1 else "")

        find_button = ctk.CTkButton(params_frame, text="원리 찾기", command=self.find_principles)
        find_button.pack(side="left", padx=10)

        results_outer_frame = ctk.CTkFrame(triz_main_frame, fg_color="transparent")
        results_outer_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))

        self.suggested_principles_frame = ctk.CTkScrollableFrame(results_outer_frame, width=250, label_text="추천 발명 원리", label_font=ctk.CTkFont(size=14, weight="bold"))
        self.suggested_principles_frame.pack(side="left", fill="y", padx=(0,10), pady=(5,0))
        ctk.CTkLabel(self.suggested_principles_frame, text="특성 선택 후 '원리 찾기' 클릭").pack(pady=10)

        triz_details_interactions_frame = ctk.CTkFrame(results_outer_frame)
        triz_details_interactions_frame.pack(side="left", fill="both", expand=True, pady=(5,0))
        
        ctk.CTkLabel(triz_details_interactions_frame, text="선택된 원리 상세 설명:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10,0), padx=10, anchor="w")
        self.principle_details_textbox = ctk.CTkTextbox(triz_details_interactions_frame, height=100, wrap="word", font=ctk.CTkFont(size=13))
        self.principle_details_textbox.pack(fill="x", padx=10, pady=5)
        self.principle_details_textbox.insert("0.0", "좌측에서 추천된 원리를 선택하면 상세 설명이 표시됩니다.\n이 설명이 해당 원리에 대한 가이드입니다.")
        self.principle_details_textbox.configure(state="disabled")

        ctk.CTkLabel(triz_details_interactions_frame, text="이 원리를 적용할 문제 상황/아이디어 컨텍스트:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10,0), padx=10, anchor="w")
        self.problem_context_entry = ctk.CTkTextbox(triz_details_interactions_frame, height=80, wrap="word", font=ctk.CTkFont(size=13))
        self.problem_context_entry.pack(fill="x", padx=10, pady=5)
        self.problem_context_entry.insert("0.0", "예: 우리 회사 자전거의 무게를 줄이고 싶은데, 강도가 약해지는 것이 문제입니다...")

        triz_action_buttons_frame = ctk.CTkFrame(triz_details_interactions_frame, fg_color="transparent")
        triz_action_buttons_frame.pack(fill="x", padx=10, pady=10)

        triz_gemini_button = ctk.CTkButton(triz_action_buttons_frame, text="Gemini 아이디어 (원리 기반)", command=self.app.get_gemini_triz_ideas)
        triz_gemini_button.pack(side="left", expand=True, padx=(0,5))

        triz_save_button = ctk.CTkButton(triz_action_buttons_frame, text="파일로 저장", command=lambda: self.app.save_ideas_to_file(self.gemini_result_textbox.get("1.0", "end-1c") if self.gemini_result_textbox else "", "TRIZ"))
        triz_save_button.pack(side="left", expand=True, padx=(5,0))

        ctk.CTkLabel(triz_details_interactions_frame, text="Gemini 제안 아이디어 (TRIZ 기반):", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(5,0), padx=10, anchor="w")
        self.gemini_result_textbox = ctk.CTkTextbox(triz_details_interactions_frame, wrap="word", font=ctk.CTkFont(size=13))
        self.gemini_result_textbox.pack(fill="both", expand=True, padx=10, pady=(5,10))
        self.gemini_result_textbox.insert("0.0", "Gemini 버튼을 누르면 여기에 아이디어가 표시됩니다.")
        self.gemini_result_textbox.configure(state="disabled")
        
        # app 인스턴스의 UI 요소 참조 업데이트
        self.app.triz_suggested_principles_frame = self.suggested_principles_frame
        self.app.triz_principle_details_textbox = self.principle_details_textbox
        self.app.triz_problem_context_entry = self.problem_context_entry
        self.app.triz_gemini_result_textbox = self.gemini_result_textbox


    def find_principles(self):
        if not self.suggested_principles_frame: return

        for widget in self.suggested_principles_frame.winfo_children():
            widget.destroy()
        
        if self.principle_details_textbox:
            self.principle_details_textbox.configure(state="normal")
            self.principle_details_textbox.delete("1.0", "end")
            self.principle_details_textbox.insert("0.0", "좌측에서 추천된 원리를 선택하면 상세 설명이 표시됩니다.\n이 설명이 해당 원리에 대한 가이드입니다.")
            self.principle_details_textbox.configure(state="disabled")
        if self.gemini_result_textbox:
            self.gemini_result_textbox.configure(state="normal")
            self.gemini_result_textbox.delete("1.0", "end")
            self.gemini_result_textbox.insert("0.0", "Gemini 버튼을 누르면 여기에 아이디어가 표시됩니다.")
            self.gemini_result_textbox.configure(state="disabled")
        self.app.triz_selected_principle_details = None

        improving_param_text = self.app.triz_improving_param.get()
        worsening_param_text = self.app.triz_worsening_param.get()

        if not improving_param_text or not worsening_param_text:
            messagebox.showwarning("선택 필요", "개선하려는 특성과 악화되는 특성을 모두 선택해주세요.", parent=self.parent_frame)
            ctk.CTkLabel(self.suggested_principles_frame, text="양쪽 특성을 모두 선택해주세요.").pack(pady=10)
            return

        parameters_list = triz_core.get_engineering_parameters()
        try:
            improving_idx = parameters_list.index(improving_param_text)
            worsening_idx = parameters_list.index(worsening_param_text)
        except ValueError:
            messagebox.showerror("오류", "선택된 특성을 찾을 수 없습니다.", parent=self.parent_frame)
            ctk.CTkLabel(self.suggested_principles_frame, text="특성 선택 오류.").pack(pady=10)
            return
        
        if improving_idx == worsening_idx:
            messagebox.showinfo("정보", "개선 특성과 악화 특성이 동일합니다.\n모순이 발생하지 않습니다.", parent=self.parent_frame)
            ctk.CTkLabel(self.suggested_principles_frame, text="개선/악화 특성이 동일합니다.").pack(pady=10)
            return

        principle_ids = triz_core.get_principles_from_contradiction(improving_idx, worsening_idx)

        if not principle_ids:
            ctk.CTkLabel(self.suggested_principles_frame, text="해당 모순에 대한 추천 원리를\n찾을 수 없습니다.\n(모순 매트릭스 데이터 확인 필요)").pack(pady=10, padx=5)
            return

        for pid in principle_ids:
            details = triz_core.get_principle_details(pid)
            if details:
                text = f"{pid}. {details['name'].split(' (')[0]}"
                btn = ctk.CTkButton(self.suggested_principles_frame, text=text, command=lambda d=details, p_id=pid: self.display_principle_details(d, p_id))
                btn.pack(fill="x", pady=2, padx=2)
            else:
                ctk.CTkLabel(self.suggested_principles_frame, text=f"원리 {pid} (정보 없음)").pack(pady=2)

    def display_principle_details(self, principle_details, principle_id):
        if not self.principle_details_textbox: return

        self.app.triz_selected_principle_details = principle_details.copy()
        self.app.triz_selected_principle_details['id'] = principle_id

        self.principle_details_textbox.configure(state="normal")
        self.principle_details_textbox.delete("1.0", "end")
        text_to_display = f"원리 {principle_id}: {principle_details['name']}\n\n"
        text_to_display += f"설명: {principle_details['description']}"
        self.principle_details_textbox.insert("0.0", text_to_display)
        self.principle_details_textbox.configure(state="disabled")

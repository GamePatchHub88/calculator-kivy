import re

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


# حجم نافذة الاختبار على الكمبيوتر
Window.size = (400, 600)


# -----------------------------
# الحساب الآمن
# -----------------------------
def safe_eval(expr):
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expr):
        raise ValueError("Invalid characters")

    return eval(
        expr,
        {"__builtins__": {}},
        {}
    )


# -----------------------------
# التطبيق
# -----------------------------
class CalculatorApp(App):

    def build(self):

        # النافذة الرئيسية
        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        # -----------------------------
        # شاشة الآلة الحاسبة
        # -----------------------------
        self.screen = TextInput(
            text="",
            multiline=False,
            readonly=True,
            halign="right",
            font_size=40,
            size_hint_y=None,
            height=dp(100),
            background_color=(0.08, 0.08, 0.08, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )

        root.add_widget(self.screen)

        # -----------------------------
        # أزرار الآلة الحاسبة
        # -----------------------------
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "C", "+"]
        ]

        for row in buttons:

            row_layout = BoxLayout(
                orientation="horizontal",
                spacing=dp(5)
            )

            for text in row:

                button = Button(
                    text=text,
                    font_size=30,
                    background_normal="",
                    background_color=(0.12, 0.35, 0.75, 1)
                )

                button.bind(
                    on_press=lambda instance, t=text:
                    self.button_click(t)
                )

                row_layout.add_widget(button)

            root.add_widget(row_layout)

        # -----------------------------
        # أزرار الحذف والحساب
        # -----------------------------
        bottom = BoxLayout(
            orientation="horizontal",
            spacing=dp(5),
            size_hint_y=None,
            height=dp(70)
        )

        # زر الحذف
        backspace_button = Button(
            text="⌫",
            font_size=25,
            background_normal="",
            background_color=(0.12, 0.35, 0.75, 1)
        )

        backspace_button.bind(
            on_press=self.backspace
        )

        # زر =
        equal_button = Button(
            text="=",
            font_size=25,
            background_normal="",
            background_color=(0.18, 0.65, 0.45, 1)
        )

        equal_button.bind(
            on_press=self.calculate
        )

        bottom.add_widget(backspace_button)
        bottom.add_widget(equal_button)

        root.add_widget(bottom)

        return root

    # -----------------------------
    # إضافة رقم أو عملية
    # -----------------------------
    def button_click(self, value):

        self.screen.text += str(value)

    # -----------------------------
    # الحساب
    # -----------------------------
    def calculate(self, instance=None):

        expr = self.screen.text

        if not expr:
            return

        try:

            result = safe_eval(expr)

            self.screen.text = str(result)

        except ZeroDivisionError:

            self.screen.text = "Cannot divide by 0"

        except Exception:

            self.screen.text = "خطأ اكتب تاني يا ذكيييي 😎"

    # -----------------------------
    # مسح الشاشة
    # -----------------------------
    def clear(self, instance=None):

        self.screen.text = ""

    # -----------------------------
    # حذف آخر حرف
    # -----------------------------
    def backspace(self, instance=None):

        self.screen.text = self.screen.text[:-1]

    # -----------------------------
    # لوحة المفاتيح
    # -----------------------------
    def on_key_down(
        self,
        window,
        key,
        scancode,
        codepoint,
        modifier
    ):

        # الأرقام والعمليات
        if codepoint and codepoint in "0123456789+-*/.()":

            self.button_click(codepoint)

            return True

        # Enter
        if key == 13:

            self.calculate()

            return True

        # Backspace
        if key == 8:

            self.backspace()

            return True

        # Escape
        if key == 27:

            self.clear()

            return True

        return False

    # -----------------------------
    # تشغيل لوحة المفاتيح
    # -----------------------------
    def on_start(self):

        Window.bind(
            on_key_down=self.on_key_down
        )


# تشغيل التطبيق
if __name__ == "__main__":
    CalculatorApp().run()
import math
import re
from knowledge_base import KNOWLEDGE_BASE


class MiniAIAgent:
    def __init__(self):
        self.chat_history = []

    def add_to_history(self, role: str, content: str) -> None:
        self.chat_history.append({"role": role, "content": content})
        if len(self.chat_history) > 20:
            self.chat_history.pop(0)

    def is_math_expression(self, text: str) -> bool:
        text = text.strip().lower()
        allowed_pattern = r"^[0-9\.\+\-\*\/\(\)\s]+$"
        return bool(re.match(allowed_pattern, text))

    def safe_calculate(self, text: str) -> str:
        try:
            expression = text.strip().replace("^", "**")
            result = eval(expression, {"__builtins__": {}}, {})
            return f"计算结果是：{result}"
        except Exception:
            return "这个数学表达式我暂时没算出来。"

    def detect_intent(self, user_input: str) -> str:
        text = user_input.lower().strip()

        if self.is_math_expression(text):
            return "calculator"

        chat_keywords = [
            "你好", "hello", "hi", "hey",
            "你是谁", "who are you",
            "谢谢", "thanks", "thank you",
            "再见", "bye",
            "你会什么", "what can you do",
            "你几岁", "how old are you", "年龄"
        ]
        for kw in chat_keywords:
            if kw in text:
                return "chat"

        subject_keywords = {
            "math": ["数学", "方程", "导数", "积分", "几何", "勾股", "函数", "圆"],
            "physics": ["物理", "牛顿", "力", "速度", "加速度", "动能", "引力"],
            "chemistry": ["化学", "酸", "碱", "氧气", "二氧化碳", "化学式", "h2o", "co2"],
            "biology": ["生物", "细胞", "dna", "光合作用", "呼吸作用", "遗传"],
            "astronomy": ["天文", "太阳", "月球", "地球", "黑洞", "光年"]
        }

        for subject, keywords in subject_keywords.items():
            for kw in keywords:
                if kw in text:
                    return subject

        return "unknown"

    def handle_chat(self, user_input: str) -> str:
        text = user_input.lower().strip()

        if any(x in text for x in ["你好", "hello", "hi", "hey"]):
            return "你好，我是一个简单的 AI agent，可以陪你聊天，也可以回答基础数学、物理、化学、生物和天文问题。"

        if "你是谁" in text or "who are you" in text:
            return "我是一个用 Python 编写的 mini AI agent，适合做入门级开源项目演示。"

        if "你会什么" in text or "what can you do" in text:
            return "我目前可以做简单聊天、回答基础科学知识问题，还能进行一些简单数学计算。"

        if "你几岁" in text or "how old are you" in text or "年龄" in text:
            return "我没有真实年龄，因为我是一个程序。不过你可以把我当作一个刚起步的 mini AI agent。"

        if "谢谢" in text or "thanks" in text or "thank you" in text:
            return "不客气，很高兴帮到你。"

        if "再见" in text or "bye" in text:
            return "再见，欢迎下次再来。"

        return "这个我能聊一点，但我目前更擅长基础科学知识问答和简单计算。"

    def search_knowledge(self, user_input: str, subject: str) -> str:
        entries = KNOWLEDGE_BASE.get(subject, {})
        text = user_input.lower()

        for key, answer in entries.items():
            if key.lower() in text:
                return answer

        if subject == "math":
            return "这是一个数学相关问题，但我目前主要支持勾股定理、导数、积分、圆的面积、一元二次方程等基础概念。"
        if subject == "physics":
            return "这是一个物理相关问题，但我目前主要支持牛顿三定律、动能、万有引力等基础概念。"
        if subject == "chemistry":
            return "这是一个化学相关问题，但我目前主要支持水、氧气、二氧化碳、酸和碱等基础概念。"
        if subject == "biology":
            return "这是一个生物相关问题，但我目前主要支持细胞、DNA、光合作用、呼吸作用、遗传等基础概念。"
        if subject == "astronomy":
            return "这是一个天文相关问题，但我目前主要支持太阳、月球、地球、黑洞和光年等基础概念。"

        return "我暂时还不能回答这个问题。"

    def reply(self, user_input: str) -> str:
        self.add_to_history("user", user_input)

        intent = self.detect_intent(user_input)

        if intent == "calculator":
            response = self.safe_calculate(user_input)
        elif intent == "chat":
            response = self.handle_chat(user_input)
        elif intent in ["math", "physics", "chemistry", "biology", "astronomy"]:
            response = self.search_knowledge(user_input, intent)
        else:
            response = "我还比较基础。你可以试试问我：勾股定理、牛顿第二定律、水的化学式、DNA，或者直接输入 1+1 这类计算。"

        self.add_to_history("assistant", response)
        return response

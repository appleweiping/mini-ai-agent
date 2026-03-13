from knowledge_base import KNOWLEDGE_BASE


class MiniAIAgent:
    def __init__(self):
        self.chat_history = []

    def add_to_history(self, role: str, content: str) -> None:
        self.chat_history.append({"role": role, "content": content})
        if len(self.chat_history) > 10:
            self.chat_history.pop(0)

    def detect_intent(self, user_input: str) -> str:
        text = user_input.lower()

        # 简单闲聊判断
        chat_keywords = ["你好", "hello", "hi", "你是谁", "在吗", "谢谢", "再见"]
        for kw in chat_keywords:
            if kw in text:
                return "chat"

        # 学科判断
        subject_keywords = {
            "math": ["数学", "方程", "导数", "积分", "几何", "勾股", "函数", "圆"],
            "physics": ["物理", "牛顿", "力", "速度", "加速度", "动能", "引力"],
            "chemistry": ["化学", "酸", "碱", "氧气", "二氧化碳", "化学式"],
            "biology": ["生物", "细胞", "dna", "光合作用", "呼吸作用", "遗传"],
            "astronomy": ["天文", "太阳", "月球", "地球", "黑洞", "光年"]
        }

        for subject, keywords in subject_keywords.items():
            for kw in keywords:
                if kw in text:
                    return subject

        return "unknown"

    def handle_chat(self, user_input: str) -> str:
        text = user_input.lower()

        if "你好" in text or "hello" in text or "hi" in text:
            return "你好，我是一个简单的 AI agent，可以陪你聊天，也可以回答基础数学、物理、化学、生物和天文问题。"
        if "你是谁" in text:
            return "我是一个开源 mini AI agent，专注于简单对话和基础数理自然科学知识问答。"
        if "谢谢" in text:
            return "不客气，很高兴帮到你。"
        if "再见" in text:
            return "再见，欢迎下次再来问我问题。"

        return "我可以陪你简单聊天，也可以回答基础数理自然科学知识。"

    def search_knowledge(self, user_input: str, subject: str) -> str:
        entries = KNOWLEDGE_BASE.get(subject, {})
        text = user_input.lower()

        for key, answer in entries.items():
            if key.lower() in text:
                return answer

        if subject == "math":
            return "这是一个数学相关问题，但我目前只能回答基础概念，例如勾股定理、导数、积分、圆的面积、一元二次方程。"
        if subject == "physics":
            return "这是一个物理相关问题，但我目前只能回答基础概念，例如牛顿三定律、动能、万有引力。"
        if subject == "chemistry":
            return "这是一个化学相关问题，但我目前只能回答基础概念，例如水、氧气、二氧化碳、酸和碱。"
        if subject == "biology":
            return "这是一个生物相关问题，但我目前只能回答基础概念，例如细胞、DNA、光合作用、呼吸作用、遗传。"
        if subject == "astronomy":
            return "这是一个天文相关问题，但我目前只能回答基础概念，例如太阳、月球、地球、黑洞和光年。"

        return "我暂时还不能回答这个问题。"

    def reply(self, user_input: str) -> str:
        self.add_to_history("user", user_input)

        intent = self.detect_intent(user_input)

        if intent == "chat":
            response = self.handle_chat(user_input)
        elif intent in ["math", "physics", "chemistry", "biology", "astronomy"]:
            response = self.search_knowledge(user_input, intent)
        else:
            response = "我目前主要支持简单聊天，以及基础数学、物理、化学、生物和天文知识问答。"

        self.add_to_history("assistant", response)
        return response

from agent import MiniAIAgent


def main():
    agent = MiniAIAgent()
    print("Mini AI Agent 已启动，输入 quit 退出。")

    while True:
        user_input = input("你：").strip()

        if user_input.lower() in {"quit", "exit", "退出"}:
            print("AI：再见。")
            break

        response = agent.reply(user_input)
        print("AI：" + response)


if __name__ == "__main__":
    main()

import time


def _load_runtime_dependencies():
    if __package__ in (None, ""):
        # Support direct execution: `python3 src/zyron_linux/main.py`
        import sys
        from pathlib import Path

        project_src = Path(__file__).resolve().parents[1]
        if str(project_src) not in sys.path:
            sys.path.insert(0, str(project_src))

        from zyron_linux.core.voice import listen_for_command, take_user_input, speak
        from zyron_linux.core.brain import process_command
        from zyron_linux.agents.system import execute_command
    else:
        from .core.voice import listen_for_command, take_user_input, speak
        from .core.brain import process_command
        from .agents.system import execute_command

    return listen_for_command, take_user_input, speak, process_command, execute_command


def main():
    try:
        listen_for_command, take_user_input, speak, process_command, execute_command = _load_runtime_dependencies()
    except ModuleNotFoundError as exc:
        print(f"❌ Missing dependency: {exc.name}. Install project dependencies before running Zyron.")
        return

    print("⚡ ZYRON ONLINE: Say 'Hey Pikachu' to start...")

    while True:
        if listen_for_command():
            user_query = take_user_input()

            if user_query:
                action_json = process_command(user_query)

                if action_json:
                    response_text = execute_command(action_json)

                    if response_text and isinstance(response_text, str) and not response_text.endswith(".png"):
                        speak(response_text)
                    else:
                        speak("Done.")
                else:
                    speak("I am not sure how to do that yet.")

            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚡ System shutting down.")

import os
import subprocess


class TmuxSessionGenerator:
    def __init__(self, session_name):
        self.session_name = session_name
        self.windows = []

    def add_window(self, name, commands=None):
        """Adds a new window with optional commands."""
        self.windows.append({"name": name, "commands": commands if commands else []})

    def generate_script(self):
        """Creates a tmux session script based on user configuration."""
        script = [
            "#!/bin/bash",
            f"tmux attach -t {self.session_name} 2>/dev/null",
            "if [ $? -ne 0 ]; then",
            f"\ttmux new-session -d -s {self.session_name} -n {self.windows[0]['name']}",
        ]

        # Add commands for the first window
        for cmd in self.windows[0]["commands"]:
            script.append(f'\ttmux send-keys -t {self.session_name}:1 "{cmd}" C-m')

        # Create additional windows
        for i, window in enumerate(self.windows[1:], start=2):
            script.append(
                f"\ttmux new-window -t {self.session_name} -n {window['name']}"
            )

            for cmd in window["commands"]:
                script.append(
                    f'\ttmux send-keys -t {self.session_name}:{i} "{cmd}" C-m'
                )

        # Selects the first window
        script.append(f"\ttmux select-window -t {self.session_name}:1")
        script.append(f"\ttmux attach-session -t {self.session_name}")
        script.append("fi")

        return "\n".join(script)

    def save_script(self, filename="tmux.sh"):
        """Saves the script and makes it executable."""
        filename = input("\nEnter the filename: ")
        script_content = self.generate_script()
        with open(filename, "w") as script_file:
            script_file.write(script_content)
        os.chmod(filename, 0o755)
        print(f'\nTmux Script "{filename}" generated!')


class TmuxSessionizerGenerator:
    def __init__(self, session_name):
        self.session_name = session_name
        self.windows = []

    def add_window(self, name, commands=None):
        """Adds a new window with optional commands."""
        self.windows.append({"name": name, "commands": commands if commands else []})

    def generate_script(self):
        """Creates a tmux session script based on user configuration."""
        script = [
            "#!/bin/bash",
        ]

        # Add commands for the first window
        for cmd in self.windows[0]["commands"]:
            script.append(
                f'tmux rename-window -t {self.session_name}:1 {self.windows[0]["name"]}'
            )
            script.append(f'tmux send-keys -t {self.session_name}:1 "{cmd}" C-m')

        # Create additional windows
        for i, window in enumerate(self.windows[1:], start=2):
            script.append(f"tmux new-window -t {self.session_name} -n {window['name']}")

            for cmd in window["commands"]:
                script.append(f'tmux send-keys -t {self.session_name}:{i} "{cmd}" C-m')

        # Selects the first window
        script.append(f"tmux select-window -t {self.session_name}:1")
        return "\n".join(script)

    def save_script(self, filename=".tmux-sessionizer"):
        """Saves the script and makes it executable."""
        while True:
            confirmation = input('Overwrite any exiting .tmux-sessionizer file? (y/n): ')
            match confirmation:
                case "y":
                    break
                case "n":
                    print('exiting')
                    return
                case _:
                    print("Invalid value, choose (y/n): ")
        script_content = self.generate_script()
        with open(filename, "w") as script_file:
            script_file.write(script_content)
        os.chmod(filename, 0o755)
        print(f'\nTmux Script "{filename}" generated!')


def clear_terminal():
    subprocess.run("clear")


def menu():
    session_name = input("\nEnter the tmux session name: ")
    generator = TmuxSessionGenerator(session_name)

    while True:
        window_name = input("\nEnter window name (or press Enter to finish): ")
        if not window_name:
            break

        commands = input(
            f"Enter commands to run in {window_name} (separated by semicolon): "
        ).split(";")
        generator.add_window(window_name, [cmd.strip() for cmd in commands])

    return generator


def sessionizer_menu():
    directory_name = input("\nEnter the directory name: ")
    generator = TmuxSessionizerGenerator(directory_name)

    while True:
        window_name = input("\nEnter window name (or press Enter to finish): ")
        if not window_name:
            break

        commands = input(
            f"Enter commands to run in {window_name} (separated by semicolon): "
        ).split(";")
        generator.add_window(window_name, [cmd.strip() for cmd in commands])

    return generator


def is_sessionizer():
    while True:
        menu_type = input("\nAre you using the tmux-sessionizer? (y/n): ")
        match menu_type:
            case "y":
                return True
            case "n":
                return False
            case _:
                print("Invalid value, choose (y/n): ")


def main():
    clear_terminal()
    print("\n=== Tmux Session Generator ===")
    sessionizer = is_sessionizer()
    if sessionizer:
        generator = sessionizer_menu()
        generator.save_script()
    else:
        generator = menu()
        generator.save_script()


if __name__ == "__main__":
    main()

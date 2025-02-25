import subprocess

def get_clipboard():
    return subprocess.run(["xclip", "-selection", "clipboard", "-o"], capture_output=True, text=True).stdout.strip()

def set_clipboard(text):
    subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), check=True)

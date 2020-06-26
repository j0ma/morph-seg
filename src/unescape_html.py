import sys
import html

if __name__ == '__main__':
    line = sys.stdin.read()
    unescaped = html.unescape(line)
    sys.stdout.write(f"{unescaped}\n")

import re


def split_text(text: str, max_length: int = 4096) -> list[str]:
    return [text[i : i + max_length] for i in range(0, len(text), max_length)]


def create_clickable_links(text_data):
    # Альтернативная версия с HTML (более надежная)
    """
    Преобразует текст в кликабельные ссылки с HTML разметкой
    """
    lines = text_data.split("\n")

    formatted_lines = []
    for line in lines:
        if not line.strip():
            continue

        if line.startswith("[") and "](" in line and line.endswith(")"):
            end_text = line.find("](")
            link_text = line[1:end_text]
            url = line[end_text + 2 : -1]

            # Форматируем как HTML ссылку
            formatted_line = f'<a href="{url}">{link_text}</a>'
            formatted_lines.append(formatted_line)
        else:
            formatted_lines.append(line)

    formatted_text = "\n".join(formatted_lines)

    return formatted_text


def escape_markdown(text):
    escape_chars = r"[_*[\]()~`>#+\-=|{}.!]"
    return re.sub(escape_chars, r"\\\g<0>", text)


def split_md(text):
    if text.startswith("[") and "](" in text and text.endswith(")"):
        end_text = text.find("](")
        link_text = text[1:end_text]
        url = text[end_text + 2 : -1]
        return link_text, url


def fix_link(links):
    fixed_links = []
    for link in links:
        # Экранируем дефисы в тексте ссылки (между [ и ])
        start = link.find("[") + 1
        end = link.find("]")
        text = link[start:end]

        # Экранируем дефисы в тексте
        text_escaped = text.replace("-", "\\-")

        # Собираем ссылку обратно
        fixed_link = link[:start] + text_escaped + link[end:]
        fixed_links.append(fixed_link)
        result = "\n".join(fixed_links)

    return result


def resources_list(mainpages: dict):
    output = []
    for key, value in mainpages.items():
        formatted_line = f'<a href="{value}">{key}</a>'
        output.append(formatted_line)

    formatted_text = "\n".join(output)
    return formatted_text


if __name__ == "__main__":
    print("You must use main.py")

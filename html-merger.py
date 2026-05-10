from pathlib import Path
from bs4 import BeautifulSoup

def merge_html_bodies(input_folder, output_file="merged_output.html"):
    folder = Path(input_folder)

    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Folder does not exist: {folder}")

    html_files = [
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in {".html", ".htm"}
    ]

    if not html_files:
        raise ValueError("No HTML files found in the folder.")

    # Oldest modified file first
    html_files.sort(key=lambda f: f.stat().st_mtime)

    combined_body_parts = []
    head_content = None

    for index, file_path in enumerate(html_files):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")

        if head_content is None:
            head_tag = soup.head
            head_content = str(head_tag) if head_tag else "<head></head>"

            # Add CSS once
            extra_css = """
            <style>
                .merged-section {
                    padding: 20px 0;
                }

                .merged-section + .merged-section {
                    border-top: 2px solid #ccc;
                    margin-top: 24px;
                    padding-top: 24px;
                }

                @media print {
                    .merged-section {
                        break-before: page;
                        page-break-before: always;
                    }

                    .merged-section:first-child {
                        break-before: auto;
                        page-break-before: auto;
                    }
                }
            </style>
            """

            # Inject CSS into head
            head_content = head_content.replace("</head>", extra_css + "\n</head>")

        body_tag = soup.body
        if body_tag:
            body_inner_html = "".join(str(child) for child in body_tag.contents)

            if index == 0:
                combined_body_parts.append(f'<div class="merged-section">{body_inner_html}</div>')
            else:
                combined_body_parts.append(f'<div class="merged-section">{body_inner_html}</div>')
        else:
            print(f"Warning: No <body> found in {file_path.name}, skipping.")

    final_html = f"""<!DOCTYPE html>
<html>
{head_content}
<body>
{chr(10).join(combined_body_parts)}
</body>
</html>
"""

    output_path = folder / output_file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Merged {len(combined_body_parts)} files into: {output_path}")

if __name__ == "__main__":
    input_folder = r"C:\Users\Srinivas Hemadri\Desktop\leetcode-problems-explanations"
    merge_html_bodies(input_folder)
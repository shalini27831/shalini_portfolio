from pypdf import PdfReader
from bs4 import BeautifulSoup

# Read resume PDF
pdf_path = "Shalini_G_Resume.pdf"

reader = PdfReader(pdf_path)

resume_text = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        resume_text += text + "\n"


# Read portfolio HTML
html_path = "Shalini_G_Portfolio (4).html"

with open(html_path, "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

portfolio_text = soup.get_text(
    separator="\n",
    strip=True
)


# Combine both
knowledge = f"""
===== RESUME =====

{resume_text}

===== PORTFOLIO =====

{portfolio_text}
"""


# Save knowledge
with open("knowledge.txt", "w", encoding="utf-8") as file:
    file.write(knowledge)

print("Knowledge file created successfully!")
print("Saved as: knowledge.txt")
import os
import re
import cohere
from dotenv import load_dotenv
from fpdf import FPDF

# Load API key
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def extract_resume_text(file_path):
    if not os.path.exists(file_path):
        print("❌ File does not exist.")
        return None
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def generate_roadmap_with_cohere(resume_text, job_title, interview_timeline):
    print("🧠 Generating roadmap using Cohere...")

    prompt = f"""
You are an expert career coach. A person is preparing for the role of {job_title} and has an interview scheduled in {interview_timeline}.
Their resume is:
\"\"\"
{resume_text}
\"\"\"

Based on this information, create a personalized learning roadmap only for the given interview timeline. Include:
- If interview is in 2 days, give roadmap for day 1 and day 2, else if interview is in 1 week, give roadmap for day 1 to day 7, else if interview is in 2 weeks, give roadmap for week 1 and week 2, else if interview is in 1 month, give roadmap for week 1 to week 4
- Roadmap must be limited to the timeline
- Weekly goals (strictly if timeline allows)
- Include what the user must do on each day is day based and each week if week based
- Prioritized skill areas
- One project per week (if timeline allows)

Only show the roadmap. Do not greet or explain anything. Avoid phrases like "here is your roadmap" or "let me know...".
"""

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=800,
        temperature=0.6
    )
    return response.generations[0].text.strip()

def generate_tailored_resume_with_cohere(resume_text, job_title):
    print("📄 Tailoring resume using Cohere...")

    prompt = f"""
You are a resume generation engine.

Given the resume below and the target job role **{job_title}**, generate a tailored, professional resume that includes **only the most relevant skills, experiences, and projects** for this role. Eliminate all unrelated content.

Strictly follow these rules:
- Write in the **first person** as if the candidate is speaking.
- Format as a **clean, bullet-pointed resume**
- Do NOT include any chatbot-like phrases such as:
  - "Here's your resume"
  - "Let me know if..."
  - "As a resume assistant"
  - Or any explanation
- Only include:
  - Name
  - Contact Info (if available)
  - Short summary (relevant to role)
  - Relevant Skills
  - Relevant Experience
  - Relevant Projects

Output ONLY the formatted resume, ready to be submitted.

Resume:
\"\"\"{resume_text}\"\"\"
"""

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=1000,
        temperature=0.5
    )
    return response.generations[0].text.strip()

def remove_unicode_symbols(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

def save_resume_to_pdf(text, filename="personalized_resume.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    cleaned_text = remove_unicode_symbols(text)

    for line in cleaned_text.split('\n'):
        if line.strip() == "":
            pdf.ln()
        elif line.endswith(":") or line.endswith(": "):
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, line.strip(), ln=True)
            pdf.set_font("Arial", '', 12)
        elif line.startswith("-") or line.startswith("•"):
            pdf.multi_cell(0, 10, line.strip())
        else:
            pdf.multi_cell(0, 10, line.strip())

    pdf.output(filename)
    print(f"✅ Personalized resume saved as: {filename}")

def main():
    print("🔍 Personalized Roadmap + Resume Generator")

    resume_path = input("Enter the path to your resume (.txt format): ").strip().strip('"')
    resume_text = extract_resume_text(resume_path)
    if not resume_text:
        return

    job_title = input("Enter the target job role: ").strip()
    print("Interview time options: [2 days, 1 week, 2 weeks, 1 month]")
    interview_timeline = input("Enter interview timeline: ").strip()

    roadmap = generate_roadmap_with_cohere(resume_text, job_title, interview_timeline)
    tailored_resume = generate_tailored_resume_with_cohere(resume_text, job_title)

    print("\n📈 Personalized Roadmap:\n")
    print(roadmap)

    save_resume_to_pdf(tailored_resume)

if __name__ == "__main__":
    main()

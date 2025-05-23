Personalized Resume & Learning Roadmap Generator

This project allows you to upload a general resume, specify a target job role and interview timeline, and get:

- A tailored, ATS-ready resume focused only on relevant skills and experience  
- A personalized skill enhancement roadmap based on your timeline  
- The final resume exported as a clean, formatted PDF  

---

## Features

- Uses Cohere's LLM (`command` model) for intelligent resume tailoring  
- Filters only the relevant content for the job role (skills, projects, experience)  
- Builds a timeline-based roadmap (daily or weekly)  
- Auto-generates and saves the resume as a PDF file  
- Prompts optimized to eliminate AI-sounding phrases and focus on professional output

---

## Tech Stack

- Python 3.7+
- [Cohere API](https://cohere.com)
- `fpdf` for PDF export
- `python-dotenv` for environment variable management

---

## Installation

```bash
pip install cohere fpdf python-dotenv

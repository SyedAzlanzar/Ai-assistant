from fpdf import FPDF
from openai import OpenAI
from app.core.config import settings

openAiApiClient = OpenAI(api_key=settings.openai_api_key)



def run_ai(job_description: str, user_skills: str, tone: str, applicant: dict,lng:str) -> str:
    try:
        user_content = (
            f"Job description:\n{job_description}\n\n"
            f"Applicant's skills & experience:\n{user_skills}\n\n"
            f"Applicant Details:\n"
            f"{applicant['fullName']}\n"
            f"{applicant['address']}\n"
            f"{applicant['email']}\n"
            f"{applicant['phone']}\n\n"
            f"Please draft a {tone}-tone cover letter tailored to the job above in {lng}. "
            "Open with a strong introduction, explain how your skills align with the role, "
            "and close politely with your name. "
            "Make sure to not include any dates."
            "Ensure that you generate the text in user selected language, however if no language is provided, use English as default."
            "Format it compactly to fit within one page, using single spacing and minimal blank lines."
            
        )

        response = openAiApiClient.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a professional career coach."},
                {"role": "user", "content": user_content}
            ],
            max_tokens=4096
        )

        ai_text = response.choices[0].message.content

       # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=1)

        # Add Roboto font with unicode support
        pdf.add_font('Roboto', '', '"assets/fonts/Roboto-Regular.ttf', uni=True)
        pdf.set_font('Roboto', size=12)

        # Split text into lines so that it fits inside the PDF width
        lines = ai_text.split('\n')
        for line in lines:
            pdf.multi_cell(0, 8, line)

        pdf_file_name = "generated_cover_letter.pdf"
        pdf.output(pdf_file_name)

        print(f"PDF generated and saved as {pdf_file_name}")

        return pdf_file_name  # You can return the file path to your caller

    except Exception as e:
        print(f"Error: {e}")
        return ""

    # formatted = prompt_template.format(role=role, tone=tone, prompt=prompt)
    # return llm.invoke(formatted)

from flask import Flask, request, send_file
from flask_cors import CORS
from fpdf import FPDF
import io

app = Flask(__name__)
CORS(app)

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    try:
        data = request.get_json()
        pdf = FPDF()
        pdf.add_page()
        
        # Header - Name
        pdf.set_font("Arial", 'B', 22)
        pdf.set_text_color(40, 40, 110)
        pdf.cell(0, 15, txt=data.get('name', '').upper(), ln=True, align='L')
        
        # Sub-header: Links & Email
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(80, 80, 80)
        contact_info = f"Email: {data.get('email')} | LinkedIn: {data.get('linkedin')} | GitHub: {data.get('github')}"
        pdf.cell(0, 5, txt=contact_info, ln=True)
        pdf.ln(5)
        pdf.line(10, 35, 200, 35) # Horizontal Line
        pdf.ln(5)

        # Helper Function to add sections
        def add_section(title, content):
            pdf.set_font("Arial", 'B', 14)
            pdf.set_text_color(40, 40, 110)
            pdf.cell(0, 10, txt=title, ln=True)
            pdf.set_font("Arial", size=11)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 7, txt=content)
            pdf.ln(5)

        # Adding all sections
        add_section("EDUCATION", data.get('education', 'N/A'))
        add_section("WORK EXPERIENCE", data.get('experience', 'N/A'))
        add_section("PROJECTS", data.get('projects', 'N/A'))
        add_section("SKILLS", data.get('skills', 'N/A'))

        pdf_raw = pdf.output(dest='S')
        if isinstance(pdf_raw, str):
            pdf_raw = pdf_raw.encode('latin-1')

        return send_file(io.BytesIO(pdf_raw), mimetype='application/pdf', as_attachment=True, download_name='Resume.pdf')

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
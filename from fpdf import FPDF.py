from fpdf import FPDF
from datetime import datetime
from io import BytesIO

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Rapport d\'Installation LINAC', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(report_data):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    
    # Informations du projet
    pdf.cell(0, 10, f"Projet: {report_data['project_name']}", ln=1)
    pdf.cell(0, 10, f"Site: {report_data['site']}", ln=1)
    pdf.cell(0, 10, f"Statut: {report_data['status']}", ln=1)
    pdf.cell(0, 10, f"Progression: {report_data['progress']}%", ln=1)
    pdf.ln(10)
    
    # Checklist
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Checklist d'Installation", ln=1)
    
    for phase in report_data['phases']:
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 8, phase['name'], ln=1)
        pdf.set_font("Arial", '', 10)
        
        for task in phase['tasks']:
            status = "✓" if task['completed'] else "✗"
            pdf.cell(0, 6, f"  {status} {task['name']}", ln=1)
            if task['notes']:
                pdf.set_font("Arial", 'I', 8)
                pdf.multi_cell(0, 5, f"    Notes: {task['notes']}")
                pdf.set_font("Arial", '', 10)
        pdf.ln(3)
    
    # Pied de page
    pdf.set_y(-30)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, f"Généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 0, 'L')
    
    # Générer le PDF en mémoire
    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    
    return pdf_bytes.getvalue()
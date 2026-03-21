import os
import uuid
import traceback
from flask import Flask, render_template, request, redirect, url_for, make_response, send_file
import pdfkit
import io
from database import init_db, save_resume, get_resume, update_resume_template

app = Flask(__name__)
app.secret_key = 'super_secret_premium_key'

# Initialize database
init_db()

# WKHTMLTOPDF config - adjust path if necessary based on user's system
WKHTMLTOPDF_PATHS = [
    r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
    r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe"
]
config = None
for path in WKHTMLTOPDF_PATHS:
    if os.path.exists(path):
        config = pdfkit.configuration(wkhtmltopdf=path)
        break

if not config:
    try:
        config = pdfkit.configuration()
    except Exception:
        config = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        resume_id = str(uuid.uuid4())
        
        data = {
            'name': request.form.get('name', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'address': request.form.get('address', ''),
            'linkedin': request.form.get('linkedin', ''),
            'github': request.form.get('github', '')
        }
        
        skills = request.form.getlist('skills[]')
        
        education_degrees = request.form.getlist('edu_degree[]')
        education_schools = request.form.getlist('edu_school[]')
        education_years = request.form.getlist('edu_year[]')
        education = [{'degree': d, 'school': s, 'year': y} for d, s, y in zip(education_degrees, education_schools, education_years) if d]
        
        exp_titles = request.form.getlist('exp_title[]')
        exp_companies = request.form.getlist('exp_company[]')
        exp_years = request.form.getlist('exp_year[]')
        exp_descs = request.form.getlist('exp_desc[]')
        experience = [{'title': t, 'company': c, 'year': y, 'desc': d} for t, c, y, d in zip(exp_titles, exp_companies, exp_years, exp_descs) if t]
        
        proj_titles = request.form.getlist('proj_title[]')
        proj_descs = request.form.getlist('proj_desc[]')
        projects = [{'title': t, 'desc': d} for t, d in zip(proj_titles, proj_descs) if t]
        
        data['skills'] = skills
        data['education'] = education
        data['experience'] = experience
        data['projects'] = projects
        data['template'] = 'simple'
        
        save_resume(resume_id, data)
        return redirect(url_for('choose_template', resume_id=resume_id))
        
    return render_template('form.html')

@app.route('/templates/<resume_id>', methods=['GET'])
def choose_template(resume_id):
    resume_data = get_resume(resume_id)
    if not resume_data:
        return redirect(url_for('index'))
    return render_template('choose_template.html', resume_id=resume_id)

@app.route('/preview/<resume_id>/<template_id>')
def preview(resume_id, template_id):
    resume_data = get_resume(resume_id)
    if not resume_data:
        return redirect(url_for('index'))
    
    update_resume_template(resume_id, template_id)
    resume_data['template'] = template_id
    
    return render_template('preview.html', resume=resume_data, template_id=template_id, resume_id=resume_id)

@app.route('/preview_raw/<resume_id>/<template_id>')
def preview_raw(resume_id, template_id):
    resume_data = get_resume(resume_id)
    if not resume_data:
        return "Invalid resume.", 404
    return render_template(f'resumes/{template_id}.html', resume=resume_data, is_pdf=False)

@app.route('/download/<resume_id>')
def download(resume_id):
    resume_data = get_resume(resume_id)
    if not resume_data:
        return redirect(url_for('index'))
    
    template_id = resume_data['template']
    rendered_html = render_template(f'resumes/{template_id}.html', resume=resume_data, is_pdf=True)
    
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0',
            'margin-right': '0',
            'margin-bottom': '0',
            'margin-left': '0',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
        
        if config:
            pdf = pdfkit.from_string(rendered_html, False, options=options, configuration=config)
        else:
            pdf = pdfkit.from_string(rendered_html, False, options=options)
            
        return send_file(
            io.BytesIO(pdf),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'resume_{resume_data["name"].replace(" ", "_").strip()}.pdf'
        )
    except Exception as e:
        error_details = traceback.format_exc()
        return f"Error generating PDF. Please ensure wkhtmltopdf is installed and in path.<br>Exception: {str(e)}<br><pre>{error_details}</pre>"

if __name__ == '__main__':
    os.makedirs('templates/resumes', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, port=5000)

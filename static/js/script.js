// Add multiple skills
function addSkill() {
    const list = document.getElementById('skills-list');
    const div = document.createElement('div');
    div.className = 'dynamic-item form-group';
    div.innerHTML = `
        <input type="text" name="skills[]" class="form-control" placeholder="E.g. JavaScript, Project Management">
        <button type="button" class="remove-btn" onclick="this.parentElement.remove()">
            <i class="fa-solid fa-xmark"></i>
        </button>
    `;
    list.appendChild(div);
}

// Add Education
function addEducation() {
    const list = document.getElementById('education-list');
    const div = document.createElement('div');
    div.className = 'dynamic-group';
    div.innerHTML = `
        <button type="button" class="remove-btn dynamic-group-btn" onclick="this.parentElement.remove()">
            <i class="fa-solid fa-trash"></i>
        </button>
        <div class="grid grid-2">
            <div class="form-group">
                <label>Degree / Qualification</label>
                <input type="text" name="edu_degree[]" class="form-control" placeholder="B.Sc Computer Science">
            </div>
            <div class="form-group">
                <label>Graduation Year</label>
                <input type="text" name="edu_year[]" class="form-control" placeholder="2024">
            </div>
        </div>
        <div class="form-group">
            <label>Institution Name</label>
            <input type="text" name="edu_school[]" class="form-control" placeholder="University of Technology">
        </div>
    `;
    list.appendChild(div);
}

// Add Experience
function addExperience() {
    const list = document.getElementById('experience-list');
    const div = document.createElement('div');
    div.className = 'dynamic-group';
    div.innerHTML = `
        <button type="button" class="remove-btn dynamic-group-btn" onclick="this.parentElement.remove()">
            <i class="fa-solid fa-trash"></i>
        </button>
        <div class="grid grid-2">
            <div class="form-group">
                <label>Job Title</label>
                <input type="text" name="exp_title[]" class="form-control" placeholder="Software Engineer">
            </div>
            <div class="form-group">
                <label>Duration / Year</label>
                <input type="text" name="exp_year[]" class="form-control" placeholder="2022 - Present">
            </div>
        </div>
        <div class="form-group">
            <label>Company Name</label>
            <input type="text" name="exp_company[]" class="form-control" placeholder="Tech Innovations Inc.">
        </div>
        <div class="form-group">
            <label>Description</label>
            <textarea name="exp_desc[]" class="form-control" rows="3" placeholder="Developed new features..."></textarea>
        </div>
    `;
    list.appendChild(div);
}

// Add Project
function addProject() {
    const list = document.getElementById('project-list');
    const div = document.createElement('div');
    div.className = 'dynamic-group';
    div.innerHTML = `
        <button type="button" class="remove-btn dynamic-group-btn" onclick="this.parentElement.remove()">
            <i class="fa-solid fa-trash"></i>
        </button>
        <div class="form-group">
            <label>Project Title</label>
            <input type="text" name="proj_title[]" class="form-control" placeholder="E-commerce Website">
        </div>
        <div class="form-group">
            <label>Description</label>
            <textarea name="proj_desc[]" class="form-control" rows="3" placeholder="Description of the tech stack and output..."></textarea>
        </div>
    `;
    list.appendChild(div);
}

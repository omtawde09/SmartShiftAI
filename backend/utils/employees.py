# -------------------------------------------------------------------
# Mock Employee Pool — diverse skills, balanced performance scores
# so that skill_match drives ranking differences across task types.
# -------------------------------------------------------------------

EMPLOYEES = [
    # ── Backend Development ──────────────────────────────────────────
    {
        "name": "Priya Desai",
        "id": "EMP-001",
        "employee_primary_skill": "Backend Development",
        "skill_level": 4,
        "experience_years": 6,
        "is_intern": 0,
        "employee_performance_score": 4.5,
        "employee_availability_score": 0.90,
    },
    {
        "name": "Rohan Shah",
        "id": "EMP-007",
        "employee_primary_skill": "Backend Development",
        "skill_level": 4,
        "experience_years": 5,
        "is_intern": 0,
        "employee_performance_score": 4.3,
        "employee_availability_score": 0.80,
    },
    {
        "name": "Ananya Singh",
        "id": "EMP-011",
        "employee_primary_skill": "Backend Development",
        "skill_level": 3,
        "experience_years": 3,
        "is_intern": 0,
        "employee_performance_score": 3.8,
        "employee_availability_score": 0.88,
    },

    # ── DevOps ───────────────────────────────────────────────────────
    {
        "name": "Siddharth Rao",
        "id": "EMP-014",
        "employee_primary_skill": "DevOps",
        "skill_level": 4,
        "experience_years": 6,
        "is_intern": 0,
        "employee_performance_score": 4.4,
        "employee_availability_score": 0.85,
    },
    {
        "name": "Vikrant Naik",
        "id": "EMP-016",
        "employee_primary_skill": "DevOps",
        "skill_level": 5,
        "experience_years": 8,
        "is_intern": 0,
        "employee_performance_score": 4.6,
        "employee_availability_score": 0.92,
    },

    # ── Frontend Development ─────────────────────────────────────────
    {
        "name": "Kiran Reddy",
        "id": "EMP-010",
        "employee_primary_skill": "Frontend Development",
        "skill_level": 4,
        "experience_years": 4,
        "is_intern": 0,
        "employee_performance_score": 4.0,
        "employee_availability_score": 0.78,
    },
    {
        "name": "Pooja Iyer",
        "id": "EMP-008",
        "employee_primary_skill": "Frontend Development",
        "skill_level": 3,
        "experience_years": 3,
        "is_intern": 0,
        "employee_performance_score": 4.1,
        "employee_availability_score": 0.88,
    },

    # ── Data Science / Machine Learning ──────────────────────────────
    {
        "name": "Kavya Joshi",
        "id": "EMP-004",
        "employee_primary_skill": "Data Science",
        "skill_level": 5,
        "experience_years": 5,
        "is_intern": 0,
        "employee_performance_score": 4.8,
        "employee_availability_score": 0.95,
    },
    {
        "name": "Arjun Mehta",
        "id": "EMP-012",
        "employee_primary_skill": "Data Science",
        "skill_level": 4,
        "experience_years": 6,
        "is_intern": 0,
        "employee_performance_score": 4.4,
        "employee_availability_score": 0.82,
    },
    {
        "name": "Neha Sharma",
        "id": "EMP-009",
        "employee_primary_skill": "Machine Learning",
        "skill_level": 5,
        "experience_years": 4,
        "is_intern": 0,
        "employee_performance_score": 4.7,
        "employee_availability_score": 0.92,
    },
    {
        "name": "Riya Patel",
        "id": "EMP-017",
        "employee_primary_skill": "Machine Learning",
        "skill_level": 4,
        "experience_years": 3,
        "is_intern": 0,
        "employee_performance_score": 4.2,
        "employee_availability_score": 0.87,
    },

    # ── Operations Management / Project Management ────────────────────
    {
        "name": "Rahul Nair",
        "id": "EMP-002",
        "employee_primary_skill": "Operations Management",
        "skill_level": 4,
        "experience_years": 8,
        "is_intern": 0,
        "employee_performance_score": 4.2,
        "employee_availability_score": 0.85,
    },
    {
        "name": "Divya Kaur",
        "id": "EMP-013",
        "employee_primary_skill": "Project Management",
        "skill_level": 5,
        "experience_years": 9,
        "is_intern": 0,
        "employee_performance_score": 4.6,
        "employee_availability_score": 0.85,
    },
    {
        "name": "Suresh Kumar",
        "id": "EMP-018",
        "employee_primary_skill": "Operations Management",
        "skill_level": 4,
        "experience_years": 7,
        "is_intern": 0,
        "employee_performance_score": 4.3,
        "employee_availability_score": 0.80,
    },

    # ── Customer Service / Human Resources ───────────────────────────
    {
        "name": "Sneha Kulkarni",
        "id": "EMP-003",
        "employee_primary_skill": "Customer Service",
        "skill_level": 3,
        "experience_years": 4,
        "is_intern": 0,
        "employee_performance_score": 3.8,
        "employee_availability_score": 0.75,
    },
    {
        "name": "Meera Pillai",
        "id": "EMP-015",
        "employee_primary_skill": "Human Resources",
        "skill_level": 4,
        "experience_years": 5,
        "is_intern": 0,
        "employee_performance_score": 4.2,
        "employee_availability_score": 0.88,
    },

    # ── Finance ──────────────────────────────────────────────────────
    {
        "name": "Vikram More",
        "id": "EMP-005",
        "employee_primary_skill": "Finance",
        "skill_level": 4,
        "experience_years": 10,
        "is_intern": 0,
        "employee_performance_score": 4.0,
        "employee_availability_score": 0.70,
    },

    # ── Security Management ──────────────────────────────────────────
    {
        "name": "Amit Patil",
        "id": "EMP-006",
        "employee_primary_skill": "Security Management",
        "skill_level": 4,
        "experience_years": 7,
        "is_intern": 0,
        "employee_performance_score": 4.1,
        "employee_availability_score": 0.78,
    },

    # ── Quality Assurance ─────────────────────────────────────────────
    {
        "name": "Tanvi Shah",
        "id": "EMP-019",
        "employee_primary_skill": "Quality Assurance",
        "skill_level": 4,
        "experience_years": 5,
        "is_intern": 0,
        "employee_performance_score": 4.3,
        "employee_availability_score": 0.86,
    },
]

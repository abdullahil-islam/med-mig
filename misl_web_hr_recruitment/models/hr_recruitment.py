# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class Applicant(models.Model):
    _inherit = "hr.applicant"

    university = fields.Char("University")
    total_experience = fields.Integer("Total Experience")
    current_salary = fields.Float('Current Salary')
    # salary_expected = fields.Integer("Expected Salary")
    notice_period = fields.Selection(
        [
            ("0", "Immediately"),
            ("15", "15 Days"),
            ("30", "1 Month"),
            ("45", "45 Days"),
            ("60", "2 Months"),
        ],
        string="Notice Period",
    )

    first_name = fields.Char(
        string="First Name",
    )
    last_name = fields.Char(
        string="Last Name",
    )

    date_of_birth = fields.Date(
        string="Date of Birth",
    )

    age = fields.Integer(
        string="Age",
    )

    father_name = fields.Char(
        string="Father's Name",
    )

    marital_status = fields.Selection([
            ("single", "Single"),
            ("married", "Married"),
            ("divorced", "Divorced"),
            ("widow", "Widow"),
            ("widower", "Widower"),
        ],
        string="Marital Status",
    )

    place_of_birth = fields.Selection(
        [
            ("bagerhat", "Bagerhat"),
            ("bandarban", "Bandarban"),
            ("barguna", "Barguna"),
            ("barisal", "Barisal"),
            ("bhola", "Bhola"),
            ("bogra", "Bogra"),
            ("brahmanbaria", "Brahmanbaria"),
            ("chandpur", "Chandpur"),
            ("chapainawabganj", "Chapainawabganj"),
            ("chattogram", "Chattogram"),
            ("chuadanga", "Chuadanga"),
            ("comilla", "Comilla"),
            ("coxsbazar", "Cox's Bazar"),
            ("dhaka", "Dhaka"),
            ("dinajpur", "Dinajpur"),
            ("faridpur", "Faridpur"),
            ("feni", "Feni"),
            ("gaibandha", "Gaibandha"),
            ("gazipur", "Gazipur"),
            ("gopalganj", "Gopalganj"),
            ("habiganj", "Habiganj"),
            ("jamalpur", "Jamalpur"),
            ("jashore", "Jashore"),
            ("jhalokati", "Jhalokati"),
            ("jhenaidah", "Jhenaidah"),
            ("joypurhat", "Joypurhat"),
            ("khagrachari", "Khagrachari"),
            ("khulna", "Khulna"),
            ("kishoreganj", "Kishoreganj"),
            ("kurigram", "Kurigram"),
            ("kushtia", "Kushtia"),
            ("lakshmipur", "Lakshmipur"),
            ("lalmonirhat", "Lalmonirhat"),
            ("madaripur", "Madaripur"),
            ("magura", "Magura"),
            ("manikganj", "Manikganj"),
            ("meherpur", "Meherpur"),
            ("moulvibazar", "Moulvibazar"),
            ("munshiganj", "Munshiganj"),
            ("mymensingh", "Mymensingh"),
            ("naogaon", "Naogaon"),
            ("narail", "Narail"),
            ("narayanganj", "Narayanganj"),
            ("narsingdi", "Narsingdi"),
            ("natore", "Natore"),
            ("netrokona", "Netrokona"),
            ("nilphamari", "Nilphamari"),
            ("noakhali", "Noakhali"),
            ("pabna", "Pabna"),
            ("panchagarh", "Panchagarh"),
            ("patuakhali", "Patuakhali"),
            ("pirojpur", "Pirojpur"),
            ("rajbari", "Rajbari"),
            ("rajshahi", "Rajshahi"),
            ("rangamati", "Rangamati"),
            ("rangpur", "Rangpur"),
            ("satkhira", "Satkhira"),
            ("shariatpur", "Shariatpur"),
            ("sherpur", "Sherpur"),
            ("sirajganj", "Sirajganj"),
            ("sunamganj", "Sunamganj"),
            ("sylhet", "Sylhet"),
            ("tangail", "Tangail"),
            ("thakurgaon", "Thakurgaon"),
        ],
        string="Place of Birth",
    )

    present_address = fields.Char(
        string="Present Address",
    )

    permanent_address = fields.Char(
        string="Permanent Address",
    )

    id_number = fields.Char(
        string="NID/Birth Certificate/Driving License/Passport Number",
    )

    extra_curricular_activity_ids = fields.One2many(
        "extra_curricular.activity", "applicant_extra_curricular_id"
    )
    employment_history_ids = fields.One2many("employment.history", "applicat_id")
    academic_education_ids = fields.One2many("academic.profile", "applicant_id")
    professional_qualification_ids = fields.One2many(
        "professional.qualification", "applicant_professional_id"
    )
    training_information_ids = fields.One2many(
        "trining.information", "applicant_training_id"
    )
    computer_skill_ids = fields.One2many(
        "other.computer.skill", "applicant_computer_skill_id"
    )
    english_proficiency_ids = fields.One2many(
        "english.proficiency", "applicant_proficiency_id"
    )
    referee_ids = fields.One2many("applicant.referee", "applicat_referee_id")
    ms_word = fields.Boolean(string="MS Word", default=False)
    ms_excel = fields.Boolean(string="MS Excel", default=False)
    ms_power_point = fields.Boolean(string="MS Power Point", default=False)
    ms_outlook = fields.Boolean(string="MS Outlook", default=False)
    fathers_profession = fields.Char(string="Father's Profession")

    religion = fields.Selection(
        [
            ("islam", "Islam"),
            ("hindu", "Hindu"),
            ("christian", "Christian"),
            ("buddhist", "Buddhist"),
            ("tribe", "Tribe"),
            ("others", "Others"),
        ],
        string="Religion")

    image = fields.Binary(string="Image", attachment=True)
    resume = fields.Binary(string="Resume", attachment=True)

    @api.depends("ms_word")
    def _compute_has_ms_word_text(self):
        for student in self:
            student.has_ms_word_text = "Yes" if student.ms_word else "No"

    @api.depends("ms_excel")
    def _compute_has_ms_excel_text(self):
        for student in self:
            student.has_ms_excel_text = "Yes" if student.ms_excel else "No"

    @api.depends("ms_power_point")
    def _compute_has_ms_power_point_text(self):
        for student in self:
            student.has_ms_power_point_text = "Yes" if student.ms_power_point else "No"

    @api.depends("ms_outlook")
    def _compute_has_ms_outlook_text(self):
        for student in self:
            student.has_ms_outlook_text = "Yes" if student.ms_outlook else "No"


class EmploymentHistory(models.Model):
    _name = "employment.history"

    applicat_id = fields.Many2one("hr.applicant", string="Application")

    work_experiance = fields.Char(
        string="Work Experience",
    )
    organization_name = fields.Char(
        string="Organization Name",
    )
    organization_type = fields.Char(
        string="Organization Type",
    )
    department = fields.Char(
        string="Department",
    )
    job_location = fields.Char(
        string="Job Location",
    )

    major_responsibilities = fields.Text(
        string="Major Responsibilities",
    )

    organization_address = fields.Char(
        string="Organization Address",
    )

    from_date = fields.Date(
        string="From",
    )

    end_date = fields.Date(
        string="End",
        default=fields.Date.context_today,
    )


class AcademicProfile(models.Model):
    _name = "academic.profile"
    applicant_id = fields.Many2one("hr.applicant", string="Applicant ID")

    name = fields.Char(
        string="Education Level",
    )
    group = fields.Char(
        string="Group/Subject/Major",
    )
    passingYear = fields.Char(
        string="Passing Year",
    )
    grade = fields.Char(
        string="Division/Class/Grade",
    )
    institution = fields.Char(
        string="Name of Institution",
    )


class ProfessionalQualification(models.Model):
    _name = "professional.qualification"
    applicant_professional_id = fields.Many2one("hr.applicant", string="Applicant ID")

    degree = fields.Char(
        string="Degree/Certificate Name",
    )

    award = fields.Char(
        string="Awarding Body",
    )

    duration = fields.Char(
        string="Duration",
    )

    result = fields.Char(
        string="Result",
    )

    location = fields.Char(
        string="Location of Awarding Body",
    )


class TrainingInformation(models.Model):
    _name = "trining.information"
    applicant_training_id = fields.Many2one("hr.applicant", string="Applicant ID")

    title = fields.Char(
        string="Training/Workshop Title",
    )

    award = fields.Char(
        string="Awarding Body",
    )

    duration = fields.Char(
        string="Duration",
    )

    result = fields.Char(
        string="Result",
    )

    location = fields.Char(
        string="Location of Training/Workshop",
    )


class ComputerSkill(models.Model):
    _name = "other.computer.skill"
    _rec_name = "description"

    applicant_computer_skill_id = fields.Many2one("hr.applicant", string="Applicant ID")
    description = fields.Text(string="Description")


class EmglishProficiency(models.Model):
    _name = "english.proficiency"
    applicant_proficiency_id = fields.Many2one("hr.applicant", string="Applicant ID")

    level = fields.Char(
        string="Level",
    )
    reading = fields.Boolean(
        string="Reading",
    )
    writing = fields.Boolean(
        string="Writing",
    )
    speaking = fields.Boolean(
        string="Speaking",
    )
    listening = fields.Boolean(
        string="Listening",
    )


class ExtraCurricularActivities(models.Model):
    _name = "extra_curricular.activity"
    applicant_extra_curricular_id = fields.Many2one(
        "hr.applicant", string="Applicant ID"
    )

    description = fields.Text()


class EmploymentReferee(models.Model):
    _name = "applicant.referee"

    applicat_referee_id = fields.Many2one("hr.applicant", string="Application")

    name = fields.Char(
        string="Name",
    )
    organization_name = fields.Char(
        string="Organization Name",
    )
    mobile = fields.Char(
        string="Mobile",
    )
    designation = fields.Char(
        string="Designation",
    )
    organization_phone = fields.Char(
        string="Organization Phone Number",
    )
    email = fields.Char(
        string="Email Address",
    )

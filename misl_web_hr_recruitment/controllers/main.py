# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.http import request
from werkzeug.exceptions import NotFound
from odoo.addons.website.controllers.form import WebsiteForm
import base64
from datetime import date, datetime


class WebsiteHrRecruitment(http.Controller):
    def sitemap_jobs(env, rule, qs):
        if not qs or qs.lower() in "/jobs":
            yield {"loc": "/jobs"}

    @http.route(
        [
            "/jobs",
            '/jobs/country/<model("res.country"):country>',
            '/jobs/department/<model("hr.department"):department>',
            '/jobs/country/<model("res.country"):country>/department/<model("hr.department"):department>',
            "/jobs/office/<int:office_id>",
            '/jobs/country/<model("res.country"):country>/office/<int:office_id>',
            '/jobs/department/<model("hr.department"):department>/office/<int:office_id>',
            '/jobs/country/<model("res.country"):country>/department/<model("hr.department"):department>/office/<int:office_id>',
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=sitemap_jobs,
    )
    def jobs(self, country=None, department=None, office_id=None, **kwargs):
        env = request.env(
            context=dict(request.env.context, show_address=True, no_tag_br=True)
        )

        Country = env["res.country"]
        Jobs = env["hr.job"]

        # List jobs available to current UID
        domain = request.website.website_domain()
        job_ids = Jobs.search(domain).ids
        # Browse jobs as superuser, because address is restricted
        jobs = Jobs.sudo().browse(job_ids)

        # Default search by user country
        if not (country or department or office_id or kwargs.get("all_countries")):
            country_code = request.session["geoip"].get("country_code")
            if country_code:
                countries_ = Country.search([("code", "=", country_code)])
                country = countries_[0] if countries_ else None
                if not any(
                    j
                    for j in jobs
                    if j.address_id and j.address_id.country_id == country
                ):
                    country = False

        # Filter job / office for country
        if country and not kwargs.get("all_countries"):
            jobs = [
                j
                for j in jobs
                if not j.address_id or j.address_id.country_id.id == country.id
            ]
            offices = set(
                j.address_id
                for j in jobs
                if not j.address_id or j.address_id.country_id.id == country.id
            )
        else:
            offices = set(j.address_id for j in jobs if j.address_id)

        # Deduce departments and countries offices of those jobs
        departments = set(j.department_id for j in jobs if j.department_id)
        countries = set(o.country_id for o in offices if o.country_id)

        if department:
            jobs = [
                j
                for j in jobs
                if j.department_id and j.department_id.id == department.id
            ]
        if office_id and office_id in [x.id for x in offices]:
            jobs = [j for j in jobs if j.address_id and j.address_id.id == office_id]
        else:
            office_id = False

        # Render page
        return request.render(
            "website_hr_recruitment.index",
            {
                "jobs": jobs,
                "countries": countries,
                "departments": departments,
                "offices": offices,
                "country_id": country,
                "department_id": department,
                "office_id": office_id,
            },
        )

    @http.route("/jobs/add", type="http", auth="user", website=True)
    def jobs_add(self, **kwargs):
        # avoid branding of website_description by setting rendering_bundle in context
        job = (
            request.env["hr.job"]
            .with_context(rendering_bundle=True)
            .create(
                {
                    "name": _("Job Title"),
                }
            )
        )
        return request.redirect("/jobs/detail/%s?enable_editor=1" % slug(job))

    @http.route(
        """/jobs/detail/<model("hr.job"):job>""",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def jobs_detail(self, job, **kwargs):
        return request.render(
            "website_hr_recruitment.detail",
            {
                "job": job,
                "main_object": job,
            },
        )

    @http.route(
        """/jobs/apply/<model("hr.job"):job>""",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def jobs_apply(self, job, **kwargs):
        error = {}
        default = {}
        if "website_hr_recruitment_error" in request.session:
            error = request.session.pop("website_hr_recruitment_error")
            default = request.session.pop("website_hr_recruitment_default")
        return request.render(
            "website_hr_recruitment.apply",
            {
                "job": job,
                "error": error,
                "default": default,
            },
        )


class WebsiteFormCustom(WebsiteForm):
    """we can add the education, certification, and work details
    in a model, we can use the function for mapping"""

    def process_work_history(self, params, applicant_id):
        eh_items = [
            (key, value) for key, value in params.items() if key.startswith("eh")
        ]
        grouped_values = {}

        for key, value in eh_items:
            suffix = key.split("_")[-1]
            prefix = key.split("_", 1)[1].rsplit("_", 1)[0]
            index = int(suffix)
            if index not in grouped_values:
                grouped_values[index] = {}

            grouped_values[index][prefix] = value
        output_list = []
        for index, values in grouped_values.items():
            output_dict = {
                "work_experiance": values.get("work_experiance", ""),
                "organization_name": values.get("organization_name", ""),
                "organization_type": values.get("organization_type", ""),
                "department": values.get("department", ""),
                "job_location": values.get("job_location", ""),
                "major_responsibilities": values.get("major_responsibilities", ""),
                "organization_address": values.get("organization_address", ""),
                "from_date": values.get("from_date", ""),
                "end_date": values.get("end_date", ""),
                "applicat_id": applicant_id,
            }
            output_list.append(output_dict)
        return output_list

    def process_professional_qualification(self, params, applicant_professional_id):
        pq_items = [
            (key, value) for key, value in params.items() if key.startswith("pq")
        ]
        grouped_values = {}
        for key, value in pq_items:
            suffix = key.split("_")[-1]
            prefix = key.split("_", 1)[1].rsplit("_", 1)[0]
            index = int(suffix)
            if index not in grouped_values:
                grouped_values[index] = {}

            grouped_values[index][prefix] = value
        pq_output_list = []
        for index, values in grouped_values.items():
            pq_output_dict = {
                "degree": values.get("degree", ""),
                "award": values.get("award", ""),
                "duration": values.get("duration", ""),
                "result": values.get("result", ""),
                "location": values.get("location", ""),
                "applicant_professional_id": applicant_professional_id,
            }
            pq_output_list.append(pq_output_dict)

        return pq_output_list

    def process_training_qualification(self, params, applicant_training_id):
        ti_items = [
            (key, value) for key, value in params.items() if key.startswith("ti")
        ]
        grouped_values = {}
        for key, value in ti_items:
            suffix = key.split("_")[-1]
            prefix = key.split("_", 1)[1].rsplit("_", 1)[0]
            index = int(suffix)
            if index not in grouped_values:
                grouped_values[index] = {}

            grouped_values[index][prefix] = value
        ti_output_list = []
        for index, values in grouped_values.items():
            ti_output_dict = {
                "title": values.get("title", ""),
                "award": values.get("award", ""),
                "duration": values.get("duration", ""),
                "result": values.get("result", ""),
                "location": values.get("location", ""),
                "applicant_training_id": applicant_training_id,
            }
            ti_output_list.append(ti_output_dict)

        return ti_output_list

    def process_referee(self, params, applicat_referee_id):
        referee_items = [
            (key, value) for key, value in params.items() if key.startswith("referee")
        ]
        grouped_values = {}

        for key, value in referee_items:
            prefix = key.split("_", 1)[1].rsplit("_", 1)[0]
            index = int(key.split("_")[-1])
            if index not in grouped_values:
                grouped_values[index] = {}

            grouped_values[index][prefix] = value
        referee_output_list = []
        for index, values in grouped_values.items():
            referee_output_dict = {
                "name": values.get("name", ""),
                "designation": values.get("designation", ""),
                "organization_name": values.get("organization_name", ""),
                "organization_phone": values.get("organization_phone", ""),
                "mobile": values.get("mobile", ""),
                "email": values.get("email", ""),
                "applicat_referee_id": applicat_referee_id,
            }
            referee_output_list.append(referee_output_dict)

        return referee_output_list

    def process_language_profeciency(self, params, applicant_proficiency_id):
        reading_values = [
            key.split("_")[0]
            for key, value in params.items()
            if key.endswith("reading") and value == "on"
        ]

        writing_values = [
            key.split("_")[0]
            for key, value in params.items()
            if key.endswith("writing") and value == "on"
        ]

        speaking_values = [
            key.split("_")[0]
            for key, value in params.items()
            if key.endswith("speaking") and value == "on"
        ]

        listening_values = [
            key.split("_")[0]
            for key, value in params.items()
            if key.endswith("listening") and value == "on"
        ]

        professional_dict = {
            "applicant_proficiency_id": applicant_proficiency_id,
            "level": "professional",
            "reading": True if "professional" in reading_values else False,
            "writing": True if "professional" in writing_values else False,
            "speaking": True if "professional" in speaking_values else False,
            "listening": True if "professional" in listening_values else False,
        }
        business_dict = {
            "applicant_proficiency_id": applicant_proficiency_id,
            "level": "business",
            "reading": True if "business" in reading_values else False,
            "writing": True if "business" in writing_values else False,
            "speaking": True if "business" in speaking_values else False,
            "listening": True if "business" in listening_values else False,
        }
        basic_dict = {
            "applicant_proficiency_id": applicant_proficiency_id,
            "level": "basic",
            "reading": True if "basic" in reading_values else False,
            "writing": True if "basic" in writing_values else False,
            "speaking": True if "basic" in speaking_values else False,
            "listening": True if "basic" in listening_values else False,
        }

        return professional_dict, business_dict, basic_dict

    def academic_edu_process(self, params, applicant_id):
        academic_edu_lists = []
        ep_values = [
            (key, value) for key, value in params.items() if key.startswith("ep")
        ]
        sorted_data = sorted(ep_values, key=lambda x: x[0])
        last_value = sorted_data[-1][0].split("_")[1]
        for i in range(1, int(last_value) + 1):
            this_dict = {
                "name": None,
                "group": None,
                "passingYear": None,
                "grade": None,
                "institution": None,
                "applicant_id": applicant_id,
            }
            for key, value in ep_values:
                if key.startswith(f"ep_{i}_"):
                    this_dict.update({key.split("_")[-1]: value})
            academic_edu_lists.append(this_dict)
        return academic_edu_lists

    def computer_skill_process(self, params, applicant_computer_skill_id):
        main_skills = {
            "ms_word": True if params.get("ms_word", False) == "on" else False,
            "ms_excel": True if params.get("ms_excel", False) == "on" else False,
            "ms_power_point": True
            if params.get("ms_power_point", False) == "on"
            else False,
            "ms_outlook": True if params.get("ms_outlook", False) == "on" else False,
        }
        other_lists = [
            {
                "applicant_computer_skill_id": applicant_computer_skill_id,
                "description": value,
            }
            for key, value in params.items()
            if key.startswith("computer_skill")
        ]
        return main_skills, other_lists

    def extra_curricular_process(self, params, applicant_extra_curricular_id):
        extra_curricular = [
            {
                "applicant_extra_curricular_id": applicant_extra_curricular_id,
                "description": value,
            }
            for key, value in params.items()
            if key.startswith("extra_curricular_activity")
        ]
        return extra_curricular

    def process_main_applicant(self, params):
        data = {
            "first_name": "",
            "last_name": "",
            "date_of_birth": "",
            "age": "",
            "father_name": "",
            "university": "",
            "place_of_birth": "",
            "present_address": "",
            "permanent_address": "",
            "id_number": "",
            "ms_word": False,
            "ms_excel": False,
            "ms_power_point": False,
            "ms_outlook": False,
            "fathers_profession": "",
            "religion": "",
            "image": False,
            "marital_status": "",
            "current_salary": 0,
            "salary_expected": 0,
        }
        for key, value in params.items():
            if key == "image[0][0]":
                img_att = params.get("image[0][0]").read()
                data["image"] = base64.b64encode(img_att)
            if key in data.keys():
                if key.startswith("ms"):
                    data[key] = True
                else:
                    data[key] = value
            if key == "date_of_birth":
                today = date.today()
                birthdate = datetime.strptime(params["date_of_birth"], "%Y-%m-%d")
                age = (
                    today.year
                    - birthdate.year
                    - ((today.month, today.day) < (birthdate.month, birthdate.day))
                )
                data["age"] = age
        return data

    def insert_record(self, request, model, values, custom, meta=None):
        """Inserting the values from the forms use the function"""

        if model.model == "hr.applicant":
            print('processing recruitment data')
            applicant_id = super(WebsiteFormCustom, self).insert_record(
                request, model, values, custom, meta=None
            )
            this_applicant_id = request.env["hr.applicant"].sudo().browse(applicant_id)

            params_data = request.__dict__.get("params")

            if this_applicant_id:
                main_data = self.process_main_applicant(params=params_data)

                work_history_data = self.process_work_history(
                    params=params_data, applicant_id=this_applicant_id.id
                )

                education_data = self.academic_edu_process(
                    params=params_data, applicant_id=this_applicant_id.id
                )

                professional_qualification_data = (
                    self.process_professional_qualification(
                        params=params_data,
                        applicant_professional_id=this_applicant_id.id,
                    )
                )
                training_information_data = self.process_training_qualification(
                    params=params_data, applicant_training_id=this_applicant_id.id
                )
                (
                    professional_language,
                    business_language,
                    basic_language,
                ) = self.process_language_profeciency(
                    params=params_data, applicant_proficiency_id=this_applicant_id.id
                )
                main_computer_skill, other_descripotions = self.computer_skill_process(
                    params=params_data, applicant_computer_skill_id=this_applicant_id.id
                )
                extra_curricular = self.extra_curricular_process(
                    params=params_data,
                    applicant_extra_curricular_id=this_applicant_id.id,
                )
                referee_data = self.process_referee(
                    params=params_data, applicat_referee_id=this_applicant_id.id
                )

                work_history_model = request.env["employment.history"].sudo()
                education_model = request.env["academic.profile"].sudo()
                professional_qualification_model = request.env[
                    "professional.qualification"
                ].sudo()
                training_information_model = request.env["trining.information"].sudo()
                language_model = request.env["english.proficiency"].sudo()
                computer_skill_model = request.env["other.computer.skill"].sudo()
                extra_curricular_model = request.env["extra_curricular.activity"].sudo()
                referee_model = request.env["applicant.referee"].sudo()
                this_applicant_id.write(main_data)
                for wh_data in work_history_data:
                    work_history_model.create(wh_data)

                for edu_data in education_data:
                    education_model.create(edu_data)

                for pq_data in professional_qualification_data:
                    professional_qualification_model.create(pq_data)

                for ti_data in training_information_data:
                    training_information_model.create(ti_data)

                language_model.create(professional_language)
                language_model.create(business_language)
                language_model.create(basic_language)

                for descripotion in other_descripotions:
                    computer_skill_model.create(descripotion)

                for extra in extra_curricular:
                    extra_curricular_model.create(extra)

                for referee in referee_data:
                    referee_model.create(referee)

            return applicant_id

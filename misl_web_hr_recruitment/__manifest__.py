# -*- coding: utf-8 -*-
{
    "name": "Online Jobs",
    "category": "Website/Website",
    "sequence": 310,
    "version": "1.0",
    "summary": "Manage your online hiring process",
    "description": "This module allows to publish your available job positions on your website and keep track of application submissions easily. It comes as an add-on of *Recruitment* app.",
    "depends": [
        "website_hr_recruitment",
        "website",
        # "website_form",
        "website_mail",
        # "misl_reports",
    ],
    "data": [
        "data/config_data.xml",
        "security/ir.model.access.csv",
        "views/website_hr_recruitment_templates.xml",
        "views/hr_applicant_views.xml",
        # "views/assets.xml",
        "views/inherit_hr_applicant_view.xml",
        "reports/job_report.xml",
        "reports/application_card.xml",
    ],
    "installable": True,
    "application": True,
    # "auto_install": ["hr_recruitment", "website_mail"],
    "assets": {
        'web.assets_frontend': [
            'misl_web_hr_recruitment/static/src/js/job_application_data.js',
            'misl_web_hr_recruitment/static/src/scss/website_sale_form.scss',
        ],
        # 'website.assets_editor': [
        #     'website_hr_recruitment/static/src/js/**/*',
        # ],
    },
    "license": "LGPL-3",
}

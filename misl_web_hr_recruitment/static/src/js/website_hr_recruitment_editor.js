odoo.define('website_hr_recruitment.form', function (require) {
'use strict';

var core = require('web.core');
var FormEditorRegistry = require('website.form_editor_registry');

var _t = core._t;

FormEditorRegistry.add('apply_job', {
    formFields: [{
        type: 'char',
        modelRequired: true,
        name: 'partner_name',
        fillWith: 'name',
        string: 'Your Name',
    },{
        type: 'email',
        required: true,
        fillWith: 'email',
        name: 'email_from',
        string: 'Your Email',
    }, {
        type: 'char',
        required: true,
        fillWith: 'phone',
        name: 'partner_phone',
        string: 'Phone Number',
    },{
        type: 'char',
        required: true,
        name: 'university',
        string: 'University',
    },{
        type: 'integer',
        modelRequired: true,
        name: 'total_experience',
        string: 'Total Years of Experience',
    },{
        type: 'integer',
        required: true,
        name: 'salary_expected',
        string: 'Expected Salary',
    },{
        type: 'selection',
        modelRequired: true,
        name: 'notice_period',
        string: 'Notice Reriod',
        fillWith: 'notice',
        selection: [['0', "Immediately"], ['15', "15 Days"], ['30', "1 Month"], ['45', "45 Days"], ['60', "2 Months"]],
    },{
        type: 'many2one',
        name: 'medium_id',
        string: 'Mdium',
        fillWith: 'medium',
    }, {
        type: 'text',
        name: 'description',
        string: 'Cover Letter',
    }, {
        type: 'binary',
        custom: true,
        name: 'Resume',
    }],
    fields: [{
        name: 'job_id',
        type: 'many2one',
        relation: 'hr.job',
        string: _t('Applied Job'),
    }, {
        name: 'department_id',
        type: 'many2one',
        relation: 'hr.department',
        string: _t('Department'),
    }],
    successPage: '/job-thank-you',
});

});

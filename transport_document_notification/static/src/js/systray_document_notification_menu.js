/** @odoo-module **/

import { registerPatch } from '@mail/model/model_core';

registerPatch({
    name: 'ActivityGroupView',
    recordMethods: {
        /**
         * @override
         */
        onClickFilterButton(ev) {
            const $el = $(ev.currentTarget);
            const data = _.extend({}, $el.data());

            if(data.res_model == 'repair.order'){
                this.env.services['action'].doAction({
                    type: 'ir.actions.act_window',
                    name: data.model_name,
                    res_model:  data.res_model,
                    views: [[false, 'kanban'], [false, 'form']],
                    search_view_id: [false],
                    domain: [['is_new_request', '=', true],
                            ['type', '=', false]],
                    context: {},
                });
            } else if(data.res_model == 'maintenance.request'){
                this.env.services['action'].doAction({
                    type: 'ir.actions.act_window',
                    name: data.model_name,
                    res_model:  data.res_model,
                    views: [[false, 'kanban'], [false, 'form']],
                    search_view_id: [false],
                    domain: [['reminder_time', '!=', false],
                    ['reminder_time', '=', moment().format('YYYY-MM-DD')]],
                    context: {},
                });
            } else {
                this._super.apply(this, arguments);
            }
        },
    },
});

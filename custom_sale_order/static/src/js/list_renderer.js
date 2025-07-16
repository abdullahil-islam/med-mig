odoo.define('custom_sale_order.ListRenderer', function (require) {
"use strict";

var ListRenderer = require('web.ListRenderer');

ListRenderer.include({
    /**
     * Editable rows are possibly extended with a trash icon on their right, to
     * allow deleting the corresponding record.
     * For many2many editable lists, the trash bin is replaced by X.
     *
     * @override
     * @param {any} record
     * @param {any} index
     * @returns {jQueryElement}
     */
    _renderRow: function (record, index) {
        var $row = this._super.apply(this, arguments);
        if (record.model == "sale.order.line" && record.data.is_master_product == true) {
            $row[0].classList.add('o_master_product_row');
        }
        return $row;
    },
});

});
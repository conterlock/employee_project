/** @odoo-module */

import publicWidget from 'web.public.widget';
import "portal.portal";

publicWidget.registry.PortalHomeCounters.include({
    /**
     * @override
     */
    _getCountersAlwaysDisplayed() {
        return this._super(...arguments).concat(['employee_projetc_count']);
    },
});

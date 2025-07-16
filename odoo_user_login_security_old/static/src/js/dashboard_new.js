/** @odoo-module */

import { registry } from "@web/core/registry";

const { Component, onWillStart, onMounted, useState } = owl;
import { loadJS } from "@web/core/assets";
import { useService } from '@web/core/utils/hooks';


export class SessionDashboard extends Component {
	setup() {
		super.setup();
		this.rpc = useService('rpc')
		this.state = useState({
			browser_sessions : [],
			recent_sessions : [],
			state_counts : []
		})
		onWillStart(() => {
			this.fetch_data()
		});

		onMounted(() => {
			this.on_attach_callback_dash()
		});
	}

	on_attach_callback_dash () {
		this.render_graph();
		var owl = $('.owl-carousel')
		owl.owlCarousel({
			autoplay          : true,
			autoplayHoverPause: true,
			autoplayTimeout   : 2500,
			dots              : false,
			loop              : true,
			nav               : false,
			responsive        : {
				0   : {items: 1},
				600 : {items: 2},
				960 : {items: 3},
				1200: {items: 4},
			}
		});
		owl.on('mousewheel','.owl-stage',function (e) {
			if (e.deltaY>0) {
				owl.trigger('next.owl');
			} else {
				owl.trigger('prev.owl');
			}
			e.preventDefault();
		});
	}

	fetch_data () {
		var self = this;
		return this.rpc('/session/fetch_dashboard_data', {
				tz: Intl.DateTimeFormat().resolvedOptions().timeZone,
			}
		).then(function(result) {
			self.browser_sessions = result.browser_sessions
			self.recent_sessions  = result.recent_sessions
			self.state_counts     = result.state_counts
		});
	}

	async render_graph () {
		var self = this;
		await loadJS("/web/static/lib/Chart/Chart.js")
		self.chart = new Chart('dashboard_pi_chart',{
			type: 'pie',
			data: {
				labels: self.state_counts.map(self => self.status),
				datasets: [{
					data: self.state_counts.map(self => self.count),
					backgroundColor: ['#17a2b8','#28a745','#6c757d','#dc3545','#232528',],
				}],
			},
			options: {
				maintainAspectRatio: false,
				legend: {
					position: 'top',
					labels: {usePointStyle: true},
				},
				onClick (e,i){
					if (i.length) {
						var state = i[0]['_view']['label']
						state = self.state_counts.filter(a => a['status'] === state)[0]['state']
						self.do_action({
							name     : 'Sessions',
							type     : 'ir.actions.act_window',
							res_model: 'session.session',
							views    : [[false,'list'],[false,'form']],
							domain   : [['state','=',state]],
							context  : {'active_test': false},
						});
					}
				},
			},
		});
	}

	on_dashboard_action (e) {
		e.preventDefault();
		var action = $(e.currentTarget);
		var act_window = {
			name     : 'Sessions',
			type     : 'ir.actions.act_window',
			res_model: 'session.session',
			views    : [[false,'list'],[false,'form']],
			domain   : [],
		};

		var id = action.data('id')
		if (id) {
			act_window.res_id = id;
			act_window.views = [[false,'form']];
		}

		var browser = action.data('browser');
		if (browser) {
			act_window.domain.push(['browser','=',browser]);
		}

		var inactive = action.data('inactive');
		if (inactive) {
			act_window.context = {active_test: false};
		}

		this.do_action(act_window);
	}
}

SessionDashboard.template = 'session_dashboard_template'

registry.category('actions').add('session_dashboard_new', SessionDashboard)

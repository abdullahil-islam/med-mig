odoo.define('misl_web_hr_recruitment.job_application_data', function (require) {
    let eh_count = 1;
    let ep_count = 5;
    let pq_count = 1;
    let ti_count = 1;
    let cs_count = 1;
    let ect_count = 1;
    let referee_count = 1;
    console.log('Hello hi ========>')
    // console.log("Form=======>", eh_form)

    $(document).ready(function () {
            let eh_form = document.getElementById('eh_add_line');
            
            
            let eh_main = document.getElementById('eh_main')
            
            let ep_form = document.getElementById('ep_add_line')

            
            let pq_form = document.getElementById('pq_add_line')

            
            let ti_form = document.getElementById('ti_add_line')

            
            let cs_form = document.getElementById('cs_add_line')


            let ect_form = document.getElementById('ect_add_line')

            
            let referee_form = document.getElementById('ref_add_line')
            let first_name = document.getElementById('first_name')
            let last_name = document.getElementById('last_name')
            let partner_name = document.getElementById('partner_name')

            if(first_name){
                first_name.addEventListener("change", function (event) {
                    let last_name_value = last_name.value
                    if (last_name_value.length > 0){
                        partner_name.value = this.value + ' ' + last_name_value;
                    }
                    else {
                        partner_name.value = this.value
                    }
                });
            }

            if(last_name){
                last_name.addEventListener("change", function (event) {
                    let first_name_value = first_name.value
                    if (first_name_value.length > 0){
                        partner_name.value = first_name_value + ' ' + this.value;
                    }
                    else {
                        partner_name.value = this.value
                    }
                });
            }

            if (eh_form) {
                eh_form.addEventListener('click', function (event) {
                    event.preventDefault();
                    // let eh_div = document.getElementById(`eh_${eh_count}`)
                    // let eh_div = document.getElementById(`eh_1`)
                    let eh_div_all = document.querySelectorAll('[id^="eh_"]');
                    let eh_div = []
                    let regex = /eh_\d+/i
                    for(let d of eh_div_all) {
                        if (regex.test(d.id)){
                            eh_div.push(d)
                        }
                    }
                    console.log(eh_div)
                    let eh_highest_div= 0
                    for (let e = 0; e < eh_div.length; e++){
                        const e_id = Number(eh_div[e].id.split("_")[1])
                        if (e_id > eh_highest_div){
                            eh_highest_div = e_id
                        }
                    }
                    eh_count = eh_highest_div + 1;
                    let selected_eh_div_number = 'eh_' + String(eh_highest_div)
                    let eh_selected_div = document.getElementById(`${selected_eh_div_number}`)
                    let eh_el = document.createElement('div');
                    eh_el.setAttribute('id', `eh_${eh_count}`);
                    eh_el.classList.add('alert', 'alert-dismissible', 'fade', 'show', 'oe_misl_web_form', 'mt-4')
                    eh_el.setAttribute('name', `eh_${eh_count}`)
                    eh_el.innerHTML = `
                        
                            <span class="oe_misl_times"><i id='times-${eh_count}' data-toggle="tooltip" data-placement="top" title="remove this form"  class="fa fa-times"></i></span>
                            <div class="form-group">
                                <label class="col-form-label" for="eh_work_experiance_${eh_count}">Work Experience</label>
                                <textarea class="form-control" name="eh_work_experiance_${eh_count}" rows="1" placeholder="Work Experience"></textarea>
                            </div>
                            <div class="form-row">
                                <div class="form-group col-md-6">
                                    <label class="col-form-label" for="eh_organization_name_${eh_count}">Organization Name</label>
                                    <input type="text" class="form-control" name="eh_organization_name_${eh_count}" placeholder="Organization Name"/>
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="col-form-label" for="eh_organization_type_${eh_count}">Organization Type</label>
                                    <input type="text" class="form-control" name="eh_organization_type_${eh_count}" placeholder="Organization Type"/>
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group col-md-6">
                                    <label class="col-form-label" for="eh_department_${eh_count}">Department</label>
                                    <input type="text" class="form-control" name="eh_department_${eh_count}" placeholder="Department"/>
                                </div>
                                <div class="form-group col-md-6">
                                    <label class="col-form-label" for="eh_job_location_${eh_count}">Job Location</label>
                                    <input type="text" class="form-control" name="eh_job_location_${eh_count}" placeholder="Job Location"/>
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="col-form-label" for="eh_major_responsibilities_${eh_count}">Major Responsibilities</label>
                                <input type="text" class="form-control" name="eh_major_responsibilities_${eh_count}" placeholder="Major Responsibilities"/>
                            </div>
                            <div class="form-group">
                                <label class="col-form-label" for="eh_organization_address_${eh_count}">Organization Address</label>
                                <input type="text" class="form-control" name="eh_organization_address_${eh_count}" placeholder="Organization Address"/>
                            </div>
                            <div class="form-row">
                                <div class="form-group col-md-2 d-flex flex-column">
                                    <label class="col-form-label" for="eh_position_held${eh_count}">
                                        <br/>
                                    </label>
                                    <label class="col-form-label" for="eh_position_held${eh_count}">
                                        Position Held
                                    </label>
                                </div>
                                <div class="form-group col-md-5">
                                    <label class="col-form-label" for="eh_from_date_${eh_count}">From</label>
                                    <input type="date" class="form-control" name="eh_from_date_${eh_count}"/>
                                </div>
                                <div class="form-group col-md-5">
                                    <label class="col-form-label" for="eh_end_date_${eh_count}">End</label>
                                    <input type="date" class="form-control" name="eh_end_date_${eh_count}"/>
                                </div>
                            </div>
                    `;
                    
                    
                    eh_selected_div.after(eh_el)
                    let times = document.getElementById(`times-${eh_count}`)
                    times.addEventListener('click', function (event){
                        document.getElementById(`eh_${times.id.split('-')[1]}`).remove()
            })

                });
            }

            if (ep_form){
                ep_form.addEventListener('click', function (event){
                    event.preventDefault();
                    let ep_last = document.getElementById(`ep${ep_count}`)
                    ++ep_count
                    let ep_el = document.createElement('tr');
                    ep_el.setAttribute('id', `ep${ep_count}`);
                    ep_el.innerHTML = `
                            <th class="col-lg-4 col-mg-4" id="ep${ep_count}_h" name="ep_${ep_count}_name">
                                <textarea class="form-control" id="exampleFormControlTextarea3" style=" border: none;word-wrap: break-word;word-break: break-all;font-weight: bold;" name="ep_${ep_count}_name"></textarea>
                            </th>
                            <td id="ep${ep_count}_group1" class="align-middle">
                                <input type="text" class="form-control" style="border: none;" name="ep_${ep_count}_group"/>
                            </td>
                            <td id="ep${ep_count}_passing-year1" class="align-middle">
                                <input type="text" class="form-control" style="border: none;" name="ep_${ep_count}_passingYear"/>
                            </td>
                            <td id="ep${ep_count}_grade1" class="align-middle">
                                <input type="text" class="form-control" style="border: none;" name="ep_${ep_count}_grade"/>
                            </td>
                            <td id="ep${ep_count}_institution1" class="align-middle">
                                <input type="text" class="form-control" style="border: none;" name="ep_${ep_count}_institution"/>
                            </td>
                    `;
                    
                    ep_last.after(ep_el)

                })
            }

            if(pq_form){
                pq_form.addEventListener('click', function (event){
                    event.preventDefault();
                    

                    let pqLast = document.getElementById(`pq${pq_count}`)
                    ++pq_count
                    let pq_el = document.createElement('tr')
                    pq_el.setAttribute('id', `pq${pq_count}`)
                    pq_el.innerHTML = `
                        <td>
                            <input type="text" id="pqr${pq_count}degreeName" name="pq_degree_${pq_count}" class="form-control" style="border: none;"/>
                        </td>
                        <td>
                            <input type="text" id="pqr${pq_count}awardingBody" name="pq_award_${pq_count}" class="form-control" style="border: none;"/>
                        </td>
                        <td>
                            <input type="text" id="pqr${pq_count}duration" name="pq_duration_${pq_count}" class="form-control" style="border: none;"/>
                        </td>
                        <td>
                            <input type="text" id="pqr${pq_count}result" name="pq_result_${pq_count}" class="form-control" style="border: none;"/>
                        </td>
                        <td>
                            <input type="text" id="pqr${pq_count}awardingLocation" name="pq_location_${pq_count}" class="form-control" style="border: none;"/>
                        </td>
                    `;

                    pqLast.after(pq_el)

                })
            }

            if (ti_form){
                ti_form.addEventListener('click', function (event){
                    event.preventDefault();
                    let ti1 = document.getElementById(`ti${ti_count}`)
                    ++ti_count
                    let ti_el = document.createElement('tr')
                    ti_el.setAttribute('id', `ti${ti_count}`)
                    ti_el.innerHTML = `
                        <td>
                            <input type="text" id="ti_training_title_${ti_count}" class="form-control" style="border: none;" name="ti_title_${ti_count}"/>
                        </td>
                        <td>
                            <input type="text" id="ti_awarding_body${ti_count}" class="form-control" style="border: none;" name="ti_award_${ti_count}"/>
                        </td>
                        <td>
                            <input type="text" id="ti_duration${ti_count}" class="form-control" style="border: none;" name="ti_duration_${ti_count}"/>
                        </td>
                        <td>
                            <input type="text" id="ti_result${ti_count}" class="form-control" style="border: none;" name="ti_result_${ti_count}"/>
                        </td>
                        <td>
                            <input type="text" id="ti_training_location${ti_count}" class="form-control" style="border: none;" name="ti_location_${ti_count}"/>
                        </td>
                    `;
                    ti1.after(ti_el)
                })
            }

            if (cs_form){
                cs_form.addEventListener('click', function (event){
                    event.preventDefault();
                    let cs1 = document.getElementById(`cs${cs_count}`)
                    ++cs_count
                    let cs_el = document.createElement('tr')
                    cs_el.setAttribute('id', `cs${cs_count}`)
                    cs_el.innerHTML = `
                        <td colspan="4">
                            <textarea class="form-control" name="computer_skill_${cs_count}" id="computer_skill_${cs_count}" rows="1"></textarea>
                        </td>
                    `;
                    cs1.after(cs_el)
                })
            }

            if (ect_form){
                ect_form.addEventListener('click', function (event){
                    event.preventDefault();
                    let ect1 = document.getElementById(`extra_curricular_textarea${ect_count}`)
                    ++ect_count
                    let ect_el = document.createElement('div')
                    ect_el.setAttribute('id', `extra_curricular_textarea${ect_count}`)
                    ect_el.style.border = '1px solid black'
                    ect_el.classList.add('mt-2')
                    ect_el.innerHTML = `
                        <textarea class="form-control" name="extra_curricular_activity_${ect_count}" rows="1"></textarea>
                    `;
                    ect1.after(ect_el)
                })
            }

            if (referee_form) {
                referee_form.addEventListener('click', function (event) {
                    event.preventDefault();
                    let referee_div = document.querySelectorAll('[id^="referee_"]');
                    let ref_highest_div = 0
                    for (let rd = 0; rd < referee_div.length; rd++){
                        const rd_id = Number(referee_div[rd].id.split("_")[1])
                        if (rd_id > ref_highest_div){
                            ref_highest_div = rd_id
                        }
                    }
                    referee_count = ref_highest_div + 1;
                    let selected_ref_div_number = 'referee_' + String(ref_highest_div)
                    let ref_selected_div = document.getElementById(`${selected_ref_div_number}`)
                    let referee_el = document.createElement('div');
                    referee_el.setAttribute('id', `referee_${referee_count}`);
                    referee_el.classList.add('alert', 'alert-dismissible', 'fade', 'show', 'oe_misl_web_form', 'mt-4')
                    referee_el.setAttribute('name', `referee_${referee_count}`)
                    referee_el.innerHTML = `
                        <span class="oe_misl_times_ref "><i id='times-${referee_count}' data-toggle="tooltip" data-placement="top" title="remove this form"  class="fa fa-times"></i></span>
                        <div class="form-row">
                            <div class="form-group col-md-6">
                                <label for="inputRrefereeName">Name</label>
                                <input type="text" class="form-control" id="inputrefereeName1" name="referee_name_${referee_count}" placeholder="Referee Name"/>
                            </div>
                            <div class="form-group col-md-6">
                                <label for="inputRrefereeDesignation">Designation</label>
                                <input type="text" class="form-control" id="inputRefereeDesignation1" name="referee_designation_${referee_count}" placeholder="Designation"/>
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group col-md-6">
                                <label for="inputRefereeOrganization">Organization Name</label>
                                <input type="text" class="form-control" id="inputRefereeOrganization1" name="referee_organization_name_${referee_count}" placeholder="Organization Name"/>
                            </div>
                            <div class="form-group col-md-6">
                                <label for="inputRefereeOrganizationPhone">Organization Phone Number</label>
                                <input type="tel" class="form-control" id="inputRefereeOrganizationPhone1" name="referee_organization_phone_${referee_count}" placeholder="Organization Phone Number"/>
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group col-md-6">
                                <label for="inputRefereeMobile">Mobile</label>
                                <input type="text" class="form-control" id="inputRefereeMobile1" name="referee_mobile_${referee_count}" placeholder="Mobile"/>
                            </div>
                            <div class="form-group col-md-6">
                                <label for="inputRefereeEmail">Email Address</label>
                                <input type="text" class="form-control" id="inputRefereeEmail1" name="referee_email_${referee_count}" placeholder="Email Address"/>
                            </div>
                        </div>
                    `;
                    ref_selected_div.after(referee_el);
                    let times = document.getElementById(`times-${referee_count}`)
                    times.addEventListener('click', function (event){
                        document.getElementById(`referee_${times.id.split('-')[1]}`).remove()
            })

                });
            }

        }
    )


})

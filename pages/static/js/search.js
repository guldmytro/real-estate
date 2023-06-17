import { Prediction } from "./predictions.js";

class SearchForm {
    
    constructor(formId) {
        this.form = document.querySelector(formId);
        this.submitButtons = this.form.querySelectorAll('[type="submit"]');
        this.resetButton = this.form.querySelector('[type="reset"]');
        this.activeFiltersContainer = this.form.querySelector('.active-filters');
        this.prediction = new Prediction(this);
        this.selects = this.form.querySelectorAll('select');
        this.radios = this.form.querySelectorAll('[type="radio"]');
        this.numbers = this.form.querySelectorAll('input[type="number"]');
        this.checkboxes = this.form.querySelectorAll('input[type="checkbox"]');
        this.activeFilters = this.initFiltes();
        this.countUrl = this.form.getAttribute('data-count');
        this.listingsCount = null;
        this.initEvents();
        this.updateActiveFilters();
        this.update();
    }
    
    initEvents() {
        this.form.addEventListener('change', () => {
        });
        this.selects.forEach(select => {
            const name = select.getAttribute('name');
            select.addEventListener('change', (e) => {    
                const label = select.querySelector('option:checked').innerText;
                if (e.target.value) {
                    this.activeFilters[name] = {
                        'name': name,
                        'value': e.target.value,
                        'label': label
                    };
                } else {
                    delete this.activeFilters[name];
                }
            });
        });
        this.numbers.forEach(number => {
            const name = number.getAttribute('name');
            let timer = false;
            number.addEventListener('input', (e) => {
                clearTimeout(timer);
                timer = setTimeout(() => {
                    if (e.target.value) {
                        this.activeFilters[name] = {
                            'name': name,
                            'value': e.target.value,
                            'label': e.target.value
                        };
                    } else {
                        delete this.activeFilters[name];
                    }
                    
                }, 800);
            });
        });
        this.radios.forEach(radio => {
            const name = radio.getAttribute('name');
            radio.addEventListener('change', (e) => {    
                const label = `${e.target.value} ${radio.getAttribute('data-suffix') || ''}`;
                if (e.target.value) {
                    this.activeFilters[name] = {
                        'name': name,
                        'value': e.target.value,
                        'label': label
                    };
                } else {
                    delete this.activeFilters[name];
                }
            });
        });
        this.checkboxes.forEach(checkbox => {
            const name = checkbox.getAttribute('name');
            checkbox.addEventListener('change', (e) => {    
                const label = `${checkbox.getAttribute('data-label') || ''}`;
                if (e.target.checked) {
                    this.activeFilters[name] = {
                        'name': name,
                        'value': e.target.value,
                        'label': label
                    };
                } else {
                    delete this.activeFilters[name];
                }
            });
        });
        if (this.resetButton) {
            this.resetButton.addEventListener('click', this.resetForm);
        }
    }

    initFiltes() {
        const filters = {};
        this.selects.forEach(select => {
            const checkedOption = select.querySelector(':checked');
            const name = select.getAttribute('name');
            if (checkedOption && checkedOption.value && name) {
                filters[name] = {
                    name: name,
                    value: checkedOption.value,
                    label: checkedOption.innerText
                };
            }
        });
        this.numbers.forEach(number => {
            const name = number.getAttribute('name');
            const val = number.value;
            if (name && val) {
                filters[name] = {
                    name: name,
                    value: val,
                    label: val
                }
            }
        });
        this.radios.forEach(radio => {       
            if (radio.checked) {
                const name = radio.getAttribute('name');
                const val = radio.value;
                if (name && val) {
                    filters[name] = {
                        name: name,
                        value: val,
                        label: val
                    }
                }
            }
        });
        this.checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                const name = checkbox.getAttribute('name');
                const value = checkbox.value;
                const label = checkbox.getAttribute('data-label');
                filters[name] = {name, value, label};
            }
        });
        const predictionName = this.prediction.input.getAttribute('name');
        const predictionValue = this.prediction.input.value;
        if (predictionValue) {
            filters[predictionName] = {
                name: predictionName,
                value: predictionValue,
                label: predictionValue
            };
        }
        this.prediction.input
        return new Proxy(filters, this.activeFiltersHandler());
    }

    activeFiltersHandler() {
        return {
            set: (target, prop, val) => {
                target[prop] = val;
                this.updateActiveFilters();
                return true;
            },
            deleteProperty: (target, prop) => {
                const input = this.form.querySelector(`[name="${prop}"]`);
                if (input) {
                    const inputType = input.type;
                    if (inputType === 'radio' || inputType == 'checkbox') {
                        const targetInput = this.form.querySelector(`[name="${prop}"][value="${target[prop].value}"]`);
                        if (targetInput) targetInput.checked = false;
                        if (input) input.checked = false;
                    } else {
                        input.value = '';
                    }
                }
                if (prop === 'address_input') {
                    this.prediction.resetFields();
                } 
                if (prop in target) {
                    delete target[prop];
                    this.updateActiveFilters();
                }
                return true;
            }
        }
    }

    updateActiveFilters() { 
        this.activeFiltersContainer.innerHTML = '';
        const filtersCount = Object.keys(this.activeFilters).length;
        for (const [key, filter] of Object.entries(this.activeFilters)) {
            const filterTag = `
            <div class="active-filters__item">
                <span class="active-filters__label">${filter.label}</span>
                <button type="button" data-name="${filter.name}" data-value="${filter.value}" class="active-filters__btn" aria-label="очистити фільтр"></button>
            </div>`;
            this.activeFiltersContainer.insertAdjacentHTML('beforeend', filterTag);
        }
        const filterButtons = document.querySelectorAll('.active-filters__btn');
        filterButtons.forEach((button) => {
            button.addEventListener('click', () => {
                const name = button.dataset.name;
                delete this.activeFilters[name];
                if (name === 'city' || name === 'street') {
                    this.form.querySelector('[name="address_input"]').value = '';
                    this.form.querySelector('[name="address_input"]')?.parentNode?.classList.remove('valid').remove('invalid');
                }
            });
        });
        this.activeFiltersContainer.style.display = filtersCount ? 'flex' : 'none';
        filtersCount > 3 ? (this.addMoreBtn(filtersCount - 3), this.addClearBtn()) : null;
        this.getCount();
    }

    addMoreBtn(cnt) {
        const buttonTag = `
        <button type="button" class="active-filters__btn active-filters__btn_invert show-more-filters" aria-label="показати ще 3">
            <span class="show-text">Ще ${cnt}</span>
            <span class="hide-text">Приховати ${cnt}</span>    
        </button>`;
        this.activeFiltersContainer.insertAdjacentHTML('beforeend', buttonTag);
        const btn = this.activeFiltersContainer.querySelector('.show-more-filters');
        btn.addEventListener('click', () => {
            this.activeFiltersContainer.classList.toggle('all');
        });
    }

    addClearBtn() {
        const buttonTag = `
        <button type="reset" class="active-filters__btn active-filters__btn_invert reset-filters" aria-label="очистити фільтри">
            <span>Очистити все</span>
        </button>`;
        this.activeFiltersContainer.insertAdjacentHTML('beforeend', buttonTag);
        const btn = this.activeFiltersContainer.querySelector('.reset-filters');
        btn.addEventListener('click', this.resetForm);
    }

    async getCount() {
        try {
            this.form.classList.add('disabled');
            const res = await fetch(`${this.countUrl}?${this.convertFormToQuerySring()}`, {method: 'GET'})
            .then(res => {
                if (res.ok) {
                    return res.json();
                }
                throw new Error('Bad request');
            });
            if (res.success === true) {
                this.listingsCount = res.count;
                this.update();
            }
        } catch(e) {
            console.warn(e);
        }
        this.form.classList.remove('disabled');
        
    }
    
    convertFormToQuerySring() {
        const formData = new FormData(this.form);
        const queryString = new URLSearchParams(formData).toString();
        return queryString;
    }

    resetForm = (e) => {
        e.preventDefault();
        this.activeFilters = new Proxy({}, this.activeFiltersHandler());
        [...this.selects, ...this.numbers].forEach(input => input.value = '');
        [...this.radios, ...this.checkboxes].forEach(element => element.checked = false);
        this.updateActiveFilters();
    }

    update() {
        if (this.listingsCount !== null) {
            this.submitButtons.forEach(button => {
                const countTag = button.querySelector('.count');
                countTag.innerText = `(${this.listingsCount})`;
            });
        }
    }

}

new SearchForm('#search-form');

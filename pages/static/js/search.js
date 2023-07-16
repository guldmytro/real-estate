import { Prediction } from "./predictions.js";

class SearchForm {
    
    constructor(formId) {
        this.form = document.querySelector(formId);
        if (this.form) {
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
            this.listingsCount = parseInt(this.form.getAttribute('data-initial-count'), 10);
            this.initEvents();
            this.updateActiveFilters();
            this.update();
        }
    }

    isFormDisabled() {
        return this.prediction.cityInput.value 
               || this.prediction.streetInput.value ? false : true;
    }
    
    initEvents() {
        this.form.addEventListener('change', () => {
        });
        this.selects.forEach(select => {
            const name = select.getAttribute('name');
            select.addEventListener('change', (e) => {    
                if (e.target.value) {
                    this.activeFilters[name] = {
                        'name': name,
                        'value': e.target.value,
                        'label': this.formatSelect(select)
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
                            'label': this.formatNumber(e.target)
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
                        'label': this.formatRadio(e.target)
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
                    label: this.formatSelect(select)
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
                    label: this.formatNumber(number)
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
                        label: this.formatRadio(radio)
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
        const predictionName = this.prediction.cityInput.value 
                               ? this.prediction.cityInput.getAttribute('name') 
                               : this.prediction.streetInput.getAttribute('name');
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
                if (prop === 'address_input') return true;
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
        let filtersCount = Object.keys(this.activeFilters).length;
        for (const [key, filter] of Object.entries(this.activeFilters)) {
            if (key === 'deal') {
                filtersCount--;
                continue;
            }
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
                    this.form.querySelector('[name="address_input"]')?.parentNode?.classList.remove('valid')
                    this.form.querySelector('[name="address_input"]')?.parentNode?.classList.remove('invalid');
                }
            });
        });
        this.activeFiltersContainer.style.display = filtersCount > 1 ||
                (filtersCount === 1 && !this.activeFilters['deal']) ? 'flex' : 'none';
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
        this.form.querySelectorAll('[type="submit"]').forEach(button => {
            const countTag = button.querySelector('.count');
            const textTag = button.querySelector('.text');
            if (this.isFormDisabled()) {
                button.setAttribute('disabled', true);
                countTag.innerText = '';
                textTag.innerText = localization[locale].searchBtn.enter;
            } else if (!this.listingsCount) {
                button.setAttribute('disabled', true);
                countTag.innerText = '';
                textTag.innerText = localization[locale].searchBtn.notFound;
            } else {
                button.removeAttribute('disabled');
                textTag.innerText = localization[locale].searchBtn.found;
                countTag.innerText = `(${this.listingsCount})`;
            }
        });
    }

    shortenNumber(number) {
        const units = {
            'en': ['', 'K', 'M', 'B', 'T'],
            'uk': ['', 'тис.', 'млн.', 'млрд.', 'трлн.']
        }
        
        const scales = units[locale];
      
        if (number < 1000) {
            return number.toString();
        }
      
        let scale = Math.floor(Math.log10(number) / 3);
        scale = scale > scales.length - 1 ? scales.length - 1 : scale; 
        const shortened = number / Math.pow(1000, scale);
        const shortenedText = shortened.toFixed(1).replace(/\.0$/, '');
      
        return shortenedText + ' ' + scales[scale];
    }
    
    formatElement(target, value) {
        const stringArray = [];
        const prefix = target.getAttribute('data-prefix');
        const suffix = target.getAttribute('data-suffix');
    
        if (prefix) {
            stringArray.push(`<small>${prefix}</small>`);
        }
        stringArray.push(value);
        if (suffix) {
            stringArray.push(`<small>${suffix}</small>`);
        }
    
        return stringArray.join(' ');
    }
    
    formatNumber(target) {
        const value = this.shortenNumber(target.value);
        return this.formatElement(target, value);
    }
    
    formatSelect(target) {
        const label = target.querySelector('option:checked').innerText;
        return this.formatElement(target, label);
    }
    
    formatRadio(target) {
        const value = target.value;
        return this.formatElement(target, value);
    }
    

}

new SearchForm('#search-form');


class GoogleMapSearch {
    constructor(formId) {
        this.form = document.querySelector(formId);
        if (this.form) {
            this.action = this.form.getAttribute('action');
            this.prediction = new Prediction(this);
            this.loadGoogleMap();
        }
        this.activeFilters = {};
        this.locations = [];
    }
    async mapUpdate() {
        try {
            const res = await fetch(`${this.action}?${this.convertFormToQuerySring()}`, {method: 'GET'})
            .then(res => {
                if (res.ok) {
                    return res.json();
                }
                throw new Error('Bad request');
            });
            if (res.success === true) {
                this.locations = res.coordicates;
                this.initMap();
            }
        } catch(e) {
            console.warn(e);
        }

    }
    convertFormToQuerySring() {
        const formData = new FormData(this.form);
        const queryString = new URLSearchParams(formData).toString();
        return queryString;
    }
    initMap = async () => {
        this.form.classList.add('inited');
        const { Map } = await google.maps.importLibrary("maps");
        const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
        const map = new Map(document.getElementById("clustered-map"), {
            zoom: 15,
            maxZoom: 19,
            mapId: '315229cfc9e14eab',
            mapTypeControl: false
        });
        const infoWindow = new google.maps.InfoWindow({
            content: "",
            disableAutoPan: false
        });
        const bounds = new google.maps.LatLngBounds();
        const markers = this.locations.map((position, i) => {
            const priceTag = document.createElement("div");
            priceTag.className = "price-tag";
            priceTag.textContent = position?.price + ' $';

            const advancedMarker = new AdvancedMarkerElement({
                position,
                content: priceTag
            });

            bounds.extend(position);

            advancedMarker.addListener("click", () => {
                infoWindow.setContent(position?.content);
                infoWindow.open({
                    anchor: advancedMarker,
                    map,
                });
            });
            return advancedMarker;
        });
        map.fitBounds(bounds);
        new markerClusterer.MarkerClusterer({ markers, map });
    }

    async loadGoogleMap() {
        this.Map = await google.maps.importLibrary("maps");
        this.AdvancedMarkerElement = await google.maps.importLibrary("marker");
    }

}


class MapSearch {
    constructor(formId) {
        this.form = document.querySelector(formId);
        if (this.form) {
            this.locations = [];
            this.activeFilters = {};
            this.action = this.form.getAttribute('action');
            this.prediction = new Prediction(this);
            this.map = false;
            this.markerClusterGroup = false;
        }
    }

    async mapUpdate() {
        try {
            const res = await fetch(`${this.action}?${this.convertFormToQueryString()}`, { method: 'GET' })
                .then(res => {
                    if (res.ok) {
                        return res.json();
                    }
                    throw new Error('Bad request');
                }).then(resJson => {
                    if (resJson.success === true) {
                        this.locations = resJson.coordicates;
                        this.initMap();
                    }
                });
        } catch (e) {
            console.warn(e);
        }
    }

    convertFormToQueryString() {
        const formData = new FormData(this.form);
        const queryString = new URLSearchParams(formData).toString();
        return queryString;
    }

    initMap = () => {
        this.form.classList.add('inited');
        this.map = this.map || L.map('clustered-map').setView([0, 0], 15);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
            maxZoom: 19
        }).addTo(this.map);

        const infoWindow = L.popup({
            closeButton: true,
            autoClose: false,
            closeOnClick: false
        });

        const bounds = L.latLngBounds();
        const markers = [];

        // Удаление существующей группы маркеров
        if (this.markerClusterGroup) {
            this.map.removeLayer(this.markerClusterGroup);
            this.markerClusterGroup.clearLayers();
        }

        this.locations.forEach((position, i) => {
            const priceTag = L.divIcon({
                className: 'price-tag larger-marker',
                html: position?.price + ' $'
            });

            const marker = L.marker(position, {
                icon: priceTag
            });

            bounds.extend(position);

            marker.on('click', () => {
                infoWindow.setContent(position.content);
                infoWindow.setLatLng(marker.getLatLng());
                infoWindow.openOn(this.map);
            });

            markers.push(marker);
        });

        this.map.fitBounds(bounds);
        this.markerClusterGroup = L.markerClusterGroup();
        this.markerClusterGroup.addLayers(markers);
        this.map.addLayer(this.markerClusterGroup);
    }
}


new MapSearch('#map-form');

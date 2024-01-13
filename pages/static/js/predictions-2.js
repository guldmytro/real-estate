export class Prediction {
    constructor(searchForm) {
        this.searchForm = searchForm;
        this.input = this.searchForm.form.querySelector('[name="address_input"]');
        this.inputWrapper = this.input.parentNode;
        this.streetInput = this.searchForm.form.querySelector('[name="street"]');
        this.districtInput = this.searchForm.form.querySelector('[name="district"]');
        this.houseComplexInput = this.searchForm.form.querySelector('[name="house_complex"]');
        this.suggestionWrapper = this.searchForm.form.querySelector('.suggestions-wrapper');
        this.searchPhrase = this?.input?.value;
        if (this.input) this.initEventsAndLibs();
        this.debounceTimer = null;
        this.predictions = false;
        this.showPredictions = false;
        this.update();
    }
    
    async initEventsAndLibs() {
        this.input.addEventListener('input', (e) => this.handleInput(e.target.value));
    }

    handleInput(value) {
        clearTimeout(this.debounceTimer);
        // this.inputWrapper.classList.remove('valid');
        // this.inputWrapper.classList.add('invalid');
        // this.resetFields();
        this.searchForm.update ? this.searchForm.update() : null;

        this.debounceTimer = setTimeout(() => {
            this.searchPhrase = this.trimString(value);
            if (String(this.searchPhrase).length > 0) {
                this.getPredictions();
            } else {
                this.inputWrapper.classList.remove('invalid');
                this.showPredictions = false;
                this.update();
            }
            this.searchForm.update ? this.searchForm.update() : null;
        }, 500);
    }

    handleFocus() {
        this.resetFields();
    }

    async getPredictions() {
        try {
            const options = this.getRequestOptions();
            this.inputWrapper.setAttribute('data-loading', 'yes');
            const res = await fetch(`/${locale}/listings/get_address_predictions/`, options)
                              .then(res => {
                                if (res.ok) {
                                    return res.json();
                                }
                                throw new Error('Bad request')
                              });
            this.predictions = res;
            this.inputWrapper.setAttribute('data-loading', 'no');
            this.updatePredictions();
        } catch(error) {
            console.warn(error);
        }
    }

    getRequestOptions() {
        return {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({'search_query': this.searchPhrase})
        }
    }

    updatePredictions() {
        this.suggestionWrapper.innerHTML = ''; // Clear previous suggestions

        if (!this.predictions?.cities.length && !this.predictions?.streets.length && !this.predictions?.house_complexes.length && !this.predictions?.districts.length) {
            const noResultsMessage = document.createElement('p');
            noResultsMessage.classList.add('no-results-message');
            noResultsMessage.innerText = localization[locale].sugesstions.noAddressFound;
            this.suggestionWrapper.appendChild(noResultsMessage);
        }

        // Add HouseComplex suggestions
        const houseComplexSuggestions = this.predictions?.house_complexes || [];
        if (houseComplexSuggestions.length > 0) {
            const addressCategory = document.createElement('div');
            addressCategory.classList.add('suggestion-category');
    
            const addressTitle = document.createElement('p');
            addressTitle.classList.add('suggestion-category__title');
            addressTitle.innerHTML = `<img src="/static/img/icon-house-complex.svg" alt="маркер"><span>${localization[locale].sugesstions.houseComplex}</span>`;
    
            const addressGroup = document.createElement('ul');
            addressGroup.classList.add('suggestion-category__group');
            let activeHouseComplexes = [];
            if (Array.isArray(this.searchForm.activeFilters.locations)) {
                activeHouseComplexes = this.searchForm.activeFilters.locations.filter(location => location.name === 'house_complex')
                .map(location => parseInt(location.value));
            }
            houseComplexSuggestions.forEach((suggestion) => {
                const addressItem = document.createElement('li');
                addressItem.classList.add('suggestion-category__item');
                addressItem.setAttribute('data-id', suggestion.id);
                addressItem.setAttribute('data-type', 'house_complex');
                if (activeHouseComplexes.includes(parseInt(suggestion.id))) {
                    addressItem.style.opacity = 0.5;
                    addressItem.style.pointerEvents = 'none';
                }
                addressItem.innerHTML = `${suggestion.title}`;
                addressItem.addEventListener('click', (e) => this.fillSearchInput(e, `${suggestion.title}`));
                addressGroup.appendChild(addressItem);
            });
            
            addressCategory.appendChild(addressTitle);
            addressCategory.appendChild(addressGroup);
            this.suggestionWrapper.appendChild(addressCategory);
        }
    
        // Add District suggestions
        const districtSuggestions = this.predictions?.districts || [];
        if (districtSuggestions.length > 0) {
            const addressCategory = document.createElement('div');
            addressCategory.classList.add('suggestion-category');
    
            const addressTitle = document.createElement('p');
            addressTitle.classList.add('suggestion-category__title');
            addressTitle.innerHTML = `<img src="/static/img/icon-district.svg" alt="маркер"><span>${localization[locale].sugesstions.district}</span>`;
    
            const addressGroup = document.createElement('ul');
            addressGroup.classList.add('suggestion-category__group');

            let activeDistricts = [];
            if (Array.isArray(this.searchForm.activeFilters.locations)) {
                activeDistricts = this.searchForm.activeFilters.locations.filter(location => location.name === 'district')
                .map(location => parseInt(location.value));
            }
    
            districtSuggestions.forEach((suggestion) => {
                const addressItem = document.createElement('li');
                addressItem.classList.add('suggestion-category__item');
                addressItem.setAttribute('data-id', suggestion.id);
                addressItem.setAttribute('data-type', 'district');
                if (activeDistricts.includes(parseInt(suggestion.id))) {
                    addressItem.style.opacity = 0.5;
                    addressItem.style.pointerEvents = 'none';
                }
                addressItem.innerHTML = `${suggestion.title}`;
                addressItem.addEventListener('click', (e) => this.fillSearchInput(e, `${suggestion.title}`));
                addressGroup.appendChild(addressItem);
            });
            
            addressCategory.appendChild(addressTitle);
            addressCategory.appendChild(addressGroup);
            this.suggestionWrapper.appendChild(addressCategory);
        }

        // Add Address suggestions
        const addressSuggestions = this.predictions?.streets || [];
        if (addressSuggestions.length > 0) {
            const addressCategory = document.createElement('div');
            addressCategory.classList.add('suggestion-category');
    
            const addressTitle = document.createElement('p');
            addressTitle.classList.add('suggestion-category__title');
            addressTitle.innerHTML = `<img src="/static/img/icon-marker.png" alt="маркер"><span>${localization[locale].sugesstions.address}</span>`;
    
            const addressGroup = document.createElement('ul');
            addressGroup.classList.add('suggestion-category__group');

            let activeStreets = [];
            if (Array.isArray(this.searchForm.activeFilters.locations)) {
                activeStreets = this.searchForm.activeFilters.locations.filter(location => location.name === 'street')
                .map(location => parseInt(location.value));
            }
    
            addressSuggestions.forEach((suggestion) => {
                const addressItem = document.createElement('li');
                addressItem.classList.add('suggestion-category__item');
                addressItem.setAttribute('data-id', suggestion.id);
                addressItem.setAttribute('data-type', 'street');
                if (activeStreets.includes(parseInt(suggestion.id))) {
                    addressItem.style.opacity = 0.5;
                    addressItem.style.pointerEvents = 'none';
                }
                addressItem.innerHTML = `${suggestion.title}`;
                addressItem.addEventListener('click', (e) => this.fillSearchInput(e, `${suggestion.title}`));
                addressGroup.appendChild(addressItem);
            });
    
            addressCategory.appendChild(addressTitle);
            addressCategory.appendChild(addressGroup);
            this.suggestionWrapper.appendChild(addressCategory);
        }

        this.showPredictions = true;
        this.update();
    }

    fillSearchInput(e, value) {
        if (this.input) {
            this.input.value = '';
        }
        this.showPredictions = false;
        
        let streetId = '';
        let houseComplexId = '';
        let districtId = '';
        const dataType = e.target.getAttribute('data-type');
        if (dataType === 'street') {
            streetId = e.target.getAttribute('data-id');
        } else if (dataType === 'house_complex') {
            houseComplexId = e.target.getAttribute('data-id');
        } else if (dataType === 'district') {
            districtId = e.target.getAttribute('data-id');
        }
        let newLocations = [];
        if (this.searchForm.single) {
            newLocations = [{
                name: dataType,
                value: e.target.getAttribute('data-id'),
                label: this.trimString(value)
            }];
        } else {
            newLocations = [...this.searchForm.activeFilters['locations'], {
                name: dataType,
                value: e.target.getAttribute('data-id'),
                label: this.trimString(value)
            }];
        }
        this.updateInputs(newLocations);

        this.searchForm.activeFilters['locations'] = newLocations;

        
        setTimeout(() => {
            this.input.blur();
        }, 10);
        this.update();
        if (this.searchForm.mapUpdate) {
            this.searchForm.mapUpdate();
        }
    }
    updateInputs(locations=false) {
        const newLocations = locations || this.searchForm.activeFilters['locations'];
        this.streetInput.value = newLocations.filter(location => location.name === 'street')
        .map(location => location.value).join(',');
        this.districtInput.value = newLocations.filter(location => location.name === 'district')
            .map(location => location.value).join(',');
        this.houseComplexInput.value = newLocations.filter(location => location.name === 'house_complex')
            .map(location => location.value).join(',');
    }
    trimString(value) {
        return value.trim().replace(/\s{2,}/g, ' ');
    }

    resetFields() {
        this.streetInput.value = '';
        this.districtInput.value = '';
        this.houseComplexInput.value = '';
        try {
            delete this.searchForm.activeFilters['street'];
            delete this.searchForm.activeFilters['district'];
            delete this.searchForm.activeFilters['house_complex'];
        } catch(e) {
            console.warn(e);
        }
        this.update();
    }

    update() {
        this.suggestionWrapper.style.display = this.showPredictions ? 'block' : 'none';
    }
}

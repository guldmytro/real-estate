class Search {
    constructor(inputSelector, suggestionSelector, cityInput, streetInput) {
        this.input = document.querySelector(inputSelector);
        this.inputWrapper = this.input.parentNode;
        this.cityInput = document.querySelector(cityInput);
        this.streetInput = document.querySelector(streetInput);
        this.suggestionWrapper = document.querySelector(suggestionSelector);
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
        this.inputWrapper.classList.remove('valid');
        this.inputWrapper.classList.add('invalid');
        this.resetFields();

        this.debounceTimer = setTimeout(() => {
            this.searchPhrase = this.trimString(value);
            if (String(this.searchPhrase).length > 0) {
                this.getPredictions();
            } else {
                this.inputWrapper.classList.remove('invalid');
                this.showPredictions = false;
                this.update();
            }
        }, 500);
    }

    handleFocus() {
        this.resetFields();
    }

    async getPredictions() {
        try {
            const options = this.getRequestOptions();
            this.inputWrapper.setAttribute('data-loading', 'yes');
            const res = await fetch('/listings/get_address_predictions/', options)
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

        if (!this.predictions?.cities.length && !this.predictions?.streets.length) {
            const noResultsMessage = document.createElement('p');
            noResultsMessage.classList.add('no-results-message');
            noResultsMessage.innerText = 'Не знайдено адрес...';
            this.suggestionWrapper.appendChild(noResultsMessage);
        }
    
        // Add Address suggestions
        const addressSuggestions = this.predictions?.streets || [];
        if (addressSuggestions.length > 0) {
            const addressCategory = document.createElement('div');
            addressCategory.classList.add('suggestion-category');
    
            const addressTitle = document.createElement('p');
            addressTitle.classList.add('suggestion-category__title');
            addressTitle.innerHTML = '<img src="/static/img/icon-marker.png" alt="маркер"><span>Адреса</span>';
    
            const addressGroup = document.createElement('ul');
            addressGroup.classList.add('suggestion-category__group');
    
            addressSuggestions.forEach((suggestion) => {
                const addressItem = document.createElement('li');
                addressItem.classList.add('suggestion-category__item');
                addressItem.setAttribute('data-id', suggestion.id);
                addressItem.setAttribute('data-type', 'street');
                addressItem.innerHTML = `${suggestion.title} <em data-type="street" data-id="${suggestion.id}">(${suggestion.related_city.title})</em>`;
                addressItem.addEventListener('click', (e) => this.fillSearchInput(e, `${suggestion.title} (${suggestion.related_city.title})`));
                addressGroup.appendChild(addressItem);
            });
    
            addressCategory.appendChild(addressTitle);
            addressCategory.appendChild(addressGroup);
            this.suggestionWrapper.appendChild(addressCategory);
        }
    
        // Add City suggestions
        const citySuggestions = this.predictions?.cities || [];
        if (citySuggestions.length > 0) {
            const cityCategory = document.createElement('div');
            cityCategory.classList.add('suggestion-category');
    
            const cityTitle = document.createElement('p');
            cityTitle.classList.add('suggestion-category__title');
            cityTitle.innerHTML = '<img src="/static/img/icon-city.svg" alt="icon of city"><span>Місто</span>';
    
            const cityGroup = document.createElement('ul');
            cityGroup.classList.add('suggestion-category__group');
    
            citySuggestions.forEach((suggestion) => {
                const cityItem = document.createElement('li');
                cityItem.classList.add('suggestion-category__item');
                cityItem.setAttribute('data-id', suggestion.id);
                cityItem.setAttribute('data-type', 'city');
                cityItem.innerText = suggestion.title;
                cityItem.addEventListener('click', (e) => this.fillSearchInput(e, suggestion.title));
                cityGroup.appendChild(cityItem);
            });
    
            cityCategory.appendChild(cityTitle);
            cityCategory.appendChild(cityGroup);
            this.suggestionWrapper.appendChild(cityCategory);
        }
    
        this.showPredictions = true;
        this.update();
    }

    fillSearchInput(e, value) {
        if (this.input) {
            this.input.value = this.trimString(value);
        }
        this.showPredictions = false;
        
        let streetId = '';
        let cityId = '';
        if (e.target.getAttribute('data-type') === 'street') {
            streetId = e.target.getAttribute('data-id');
        } else {
            cityId = e.target.getAttribute('data-id');
        }
        this.streetInput.value = streetId;
        this.cityInput.value = cityId;
        
        this.inputWrapper.classList.remove('invalid');
        this.inputWrapper.classList.add('valid');
        setTimeout(() => {
            this.input.blur();
        }, 10);
        this.update();
    }

    trimString(value) {
        return value.trim().replace(/\s{2,}/g, ' ');
    }

    resetFields() {
        this.cityInput.value = '';
        this.streetInput.value = '';
        this.update();
    }

    update() {
        this.suggestionWrapper.style.display = this.showPredictions ? 'block' : 'none';
    }

}

const search = new Search('#id_address_input', '#address_suggestions-wrapper', "#id_city", "#id_street");
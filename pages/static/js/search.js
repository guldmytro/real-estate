class Search {
    constructor(inputSelector) {
        this.input = document.querySelector(inputSelector);
        this.searchPhrase = this?.input?.value;
        if (this.input) this.initEventsAndLibs();
        this.debounceTimer = null;
    }
    
    async initEventsAndLibs() {
        this.input.addEventListener('input', (e) => this.handleInput(e.target.value));
        const { PlacesService } = await google.maps.importLibrary("places");
        this.service = new PlacesService(document.querySelector('.google-suggestions'));
    }

    handleInput(value) {
        clearTimeout(this.debounceTimer);

        this.debounceTimer = setTimeout(() => {
            this.searchPhrase = value;
            this.getPredictions();
        }, 500);
    }

    async getPredictions() {
        try {
            const predictions = await this.fetchPredictions();
            console.log(predictions);
            console.log(predictions[0].geometry.location.lat());
            console.log(predictions[0].geometry.location.lng());
        } catch(error) {
            console.warn(error);
        }
    }

    fetchPredictions() {
        return new Promise((resolve, reject) => {
            this.service.textSearch({
                'query': this.searchPhrase,
                'language': 'en'
            }, (predictions, status) => {
                if (status === 'OK') {
                    resolve(predictions);
                } else {
                    reject(status)
                }
            });
        });
    }

    update() {

    }

}

const search = new Search('#id_address_input');

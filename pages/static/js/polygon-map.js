export class PolygonMap {
    constructor(polygonMap, locations, form) {
        this.searchForm = form;
        if (document.querySelector(`#${polygonMap}`)) {
            this.polygonMap = polygonMap;
            this.locations = locations;
            this.drawnPolygon = this.getInitialPolygon();
            this.map = null;
            this.markerClusterGroup = null;
            this.initMap();
        }
    }

    initMap = () => {
        this.map = L.map(this.polygonMap, {
            scrollWheelZoom: true, // Включаем масштабирование колесом мыши
            zoomControl: false,
        }).setView([49.989183125556025, 36.23147763480256], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
            maxZoom: 19
        }).addTo(this.map);
        
        const markers = [];

        const infoWindow = L.popup({
            closeButton: true,
            autoClose: false,
            closeOnClick: false
        });

        const bounds = L.latLngBounds();
        if (this.locations) {
            this.locations.forEach((position, i) => {
                const priceTag = L.divIcon({
                    className: 'price-tag larger-marker',
                    html: '<div class="price-tag__content">' + position.price + ' $' + '</div>',
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
            if (!this.drawnPolygon) {
                const paddingValue = 0.00006; // Измените значение по своему усмотрению

                // Вычисляем ширину и высоту карты
                const mapWidth = this.map.getSize().x;
                const mapHeight = this.map.getSize().y;

                // Вычисляем значение отступа в пикселях
                const paddingX = mapWidth * paddingValue;
                const paddingY = mapHeight * paddingValue;

                // Масштабируем карту с учетом отступов
                this.map.fitBounds(bounds.pad(paddingY, paddingX));
            }
        }

        this.markerClusterGroup = L.markerClusterGroup();
        this.markerClusterGroup.addLayers(markers);
        this.map.addLayer(this.markerClusterGroup);

        const drawnItems = new L.FeatureGroup(); // Создаем слой для сохранения рисованных объектов
        this.map.addLayer(drawnItems);
    
        // Инициализируем рисование на карте
        const drawControl = new L.Control.Draw({
          edit: {
            featureGroup: drawnItems,
            poly: {
              allowIntersection: false // Запрещаем пересечение линий
            }
          },
          draw: {
            polygon: true, 
            circle: false,
            rectangle: false,
            marker: false,
            polyline: false
          }
        });
        this.map.addControl(drawControl);
        
        // Инициализируем полигон из get-параметров
        if (this.drawnPolygon) {
            drawnItems.addLayer(this.drawnPolygon);
            this.map.fitBounds(this.drawnPolygon.getBounds());
        }
        // Обработка события "начало рисования"
        this.map.on('draw:drawstart', () => {
            if (this.drawnPolygon) {
                drawnItems.removeLayer(this.drawnPolygon);
            }
        });
        // Обработка события "нарисован полигон"
        this.map.on(L.Draw.Event.CREATED, (e) => {
            this.drawnPolygon = e.layer;
            drawnItems.addLayer(this.drawnPolygon);
            this.formatCoordinates(this.drawnPolygon.getLatLngs()[0]);
        });
        this.map.on('draw:edited', (e) => {
            const layers = e.layers; // Слои, подвергнутые редактированию
            layers.eachLayer((layer) => {
                this.formatCoordinates(layer.getLatLngs()[0]);
            });
        });
        this.map.on('draw:deleted', (e) => {
            this.drawnPolygon = null;
            this.formatCoordinates([]);
        });
    }

    formatCoordinates = (coords) => {
        this.searchForm.coordinates.value = coords.map(coord => `${coord.lng},${coord.lat}`).join(';');
        const changeEvent = new Event('change', {
            bubbles: true,
            cancelable: true
          });
          this.searchForm.coordinates.dispatchEvent(changeEvent);
    }

    getInitialPolygon = () => {
        const urlParams = new URLSearchParams(window.location.search);
        const polygonParam = urlParams.get('polygon');
        if (!polygonParam) {
            return null;
        }
        const polygonCoordinates = polygonParam.split(';').map(coord => {
            const [lng, lat] = coord.split(',');
            return [parseFloat(lat), parseFloat(lng)];
        });
        return L.polygon(polygonCoordinates);
    }
    updateLocations = (locations) => {
        this.locations = locations;
        // Удаление текущих маркеров из markerClusterGroup
        this.map.removeLayer(this.markerClusterGroup );
        this.markerClusterGroup.clearLayers();
        const newMarkers = [];
        if (this.locations) {
            // Создание новых маркеров на основе обновленных locations
            const bounds = L.latLngBounds();
            this.locations.forEach((position, i) => {
                const priceTag = L.divIcon({
                    className: 'price-tag larger-marker',
                    html: '<div class="price-tag__content">' + position.price + ' $' + '</div>',
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

                newMarkers.push(marker);
            });
            if (!this.drawnPolygon) {
                const paddingValue = 0.00006; // Измените значение по своему усмотрению

                // Вычисляем ширину и высоту карты
                const mapWidth = this.map.getSize().x;
                const mapHeight = this.map.getSize().y;

                // Вычисляем значение отступа в пикселях
                const paddingX = mapWidth * paddingValue;
                const paddingY = mapHeight * paddingValue;

                // Масштабируем карту с учетом отступов
                this.map.fitBounds(bounds.pad(paddingY, paddingX));
            } else {
                this.map.fitBounds(this.drawnPolygon.getBounds());
            }
        }
        

        // Добавление новых маркеров в markerClusterGroup
        this.markerClusterGroup.addLayers(newMarkers);
        this.map.addLayer(this.markerClusterGroup);

    }
}
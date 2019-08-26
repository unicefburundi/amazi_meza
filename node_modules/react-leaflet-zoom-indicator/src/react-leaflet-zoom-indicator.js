import { Control, DomUtil } from 'leaflet'
import { MapControl } from 'react-leaflet'
import './react-leaflet-zoom-indicator.css'


export default class ZoomIndicator extends MapControl {

    constructor(props,context) {
        super(props)
        this.div = DomUtil.create(
            'div',
            'leaflet-zoom-indicator-control leaflet-bar-part leaflet-bar',
        );
        this.span = DomUtil.create(
            'span',
            'leaflet-zoom-indicator-control-span',
            this.div
        );
        this.input = DomUtil.create(
            'input',
            'leaflet-zoom-indicator-control-input',
            this.div
        );
        L.DomEvent.disableClickPropagation(this.div);
        L.DomEvent.disableScrollPropagation(this.div);
        this.input.type = 'number'
        this.map = context.map || this.props.leaflet.map;
    }

    componentDidMount() {
        super.componentDidMount();
        this.changeZoomInfoAuto();
        this.input.addEventListener('change', () => {
            if (this.input.value !== '') {
                if (this.input.value < 0) { this.input.value = 0; }
                if (typeof this.map.options.minZoom !== 'undefined' && this.input.value < this.map.options.minZoom) {
                    this.map.setZoom(this.map.options.minZoom);
                    if ( this.map.getZoom() == this.map.options.minZoom) {
                        this.input.value = this.map.options.minZoom
                    }
                }
                if (typeof this.map.options.maxZoom !== 'undefined' && this.input.value > this.map.options.maxZoom) {
                    this.map.setZoom(this.map.options.maxZoom);
                    if ( this.map.getZoom() == this.map.options.maxZoom) {
                        this.input.value = this.map.options.maxZoom
                    }
                } else {
                    this.map.setZoom(this.input.value);
                }
            }
        })
    }

    createLeafletElement(props) {
        const ZoomIndicator = Control.extend({
            onAdd: () => this.div,
            // onRemove: () => { }
        })
        return new ZoomIndicator(props)
    }

    changeZoomInfoAuto() {
        this.updateZoomInfo();
        const mapEvent = () => { this.updateZoomInfo() }
        this.map.on('zoomend', mapEvent)
    }

    updateZoomInfo() {
        this.span.innerHTML = this.props.head
        this.input.value = this.map.getZoom()
    }
}

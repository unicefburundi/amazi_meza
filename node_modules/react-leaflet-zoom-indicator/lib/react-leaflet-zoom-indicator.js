'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _get = function get(object, property, receiver) { if (object === null) object = Function.prototype; var desc = Object.getOwnPropertyDescriptor(object, property); if (desc === undefined) { var parent = Object.getPrototypeOf(object); if (parent === null) { return undefined; } else { return get(parent, property, receiver); } } else if ("value" in desc) { return desc.value; } else { var getter = desc.get; if (getter === undefined) { return undefined; } return getter.call(receiver); } };

var _leaflet = require('leaflet');

var _reactLeaflet = require('react-leaflet');

require('./react-leaflet-zoom-indicator.css');

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var ZoomIndicator = function (_MapControl) {
    _inherits(ZoomIndicator, _MapControl);

    function ZoomIndicator(props, context) {
        _classCallCheck(this, ZoomIndicator);

        var _this = _possibleConstructorReturn(this, (ZoomIndicator.__proto__ || Object.getPrototypeOf(ZoomIndicator)).call(this, props));

        _this.div = _leaflet.DomUtil.create('div', 'leaflet-zoom-indicator-control leaflet-bar-part leaflet-bar');
        _this.span = _leaflet.DomUtil.create('span', 'leaflet-zoom-indicator-control-span', _this.div);
        _this.input = _leaflet.DomUtil.create('input', 'leaflet-zoom-indicator-control-input', _this.div);
        L.DomEvent.disableClickPropagation(_this.div);
        L.DomEvent.disableScrollPropagation(_this.div);
        _this.input.type = 'number';
        _this.map = context.map || _this.props.leaflet.map;
        return _this;
    }

    _createClass(ZoomIndicator, [{
        key: 'componentDidMount',
        value: function componentDidMount() {
            var _this2 = this;

            _get(ZoomIndicator.prototype.__proto__ || Object.getPrototypeOf(ZoomIndicator.prototype), 'componentDidMount', this).call(this);
            this.changeZoomInfoAuto();
            this.input.addEventListener('change', function () {
                if (_this2.input.value !== '') {
                    if (_this2.input.value < 0) {
                        _this2.input.value = 0;
                    }
                    if (typeof _this2.map.options.minZoom !== 'undefined' && _this2.input.value < _this2.map.options.minZoom) {
                        _this2.map.setZoom(_this2.map.options.minZoom);
                        if (_this2.map.getZoom() == _this2.map.options.minZoom) {
                            _this2.input.value = _this2.map.options.minZoom;
                        }
                    }
                    if (typeof _this2.map.options.maxZoom !== 'undefined' && _this2.input.value > _this2.map.options.maxZoom) {
                        _this2.map.setZoom(_this2.map.options.maxZoom);
                        if (_this2.map.getZoom() == _this2.map.options.maxZoom) {
                            _this2.input.value = _this2.map.options.maxZoom;
                        }
                    } else {
                        _this2.map.setZoom(_this2.input.value);
                    }
                }
            });
        }
    }, {
        key: 'createLeafletElement',
        value: function createLeafletElement(props) {
            var _this3 = this;

            var ZoomIndicator = _leaflet.Control.extend({
                onAdd: function onAdd() {
                    return _this3.div;
                }
                // onRemove: () => { }
            });
            return new ZoomIndicator(props);
        }
    }, {
        key: 'changeZoomInfoAuto',
        value: function changeZoomInfoAuto() {
            var _this4 = this;

            this.updateZoomInfo();
            var mapEvent = function mapEvent() {
                _this4.updateZoomInfo();
            };
            this.map.on('zoomend', mapEvent);
        }
    }, {
        key: 'updateZoomInfo',
        value: function updateZoomInfo() {
            this.span.innerHTML = this.props.head;
            this.input.value = this.map.getZoom();
        }
    }]);

    return ZoomIndicator;
}(_reactLeaflet.MapControl);

exports.default = ZoomIndicator;
import Ember from 'ember';
 
export default Ember.Component.extend({
  lat: 53.318602,
  lng: 48.586415,
  zoom: 15,
  markers: [
    {
      title:"marker1",
      description:"this is marker1",
      location: new L.LatLng(53.318602,48.586415)
    }
  ],
  polylines:[
  // some polyline data here.
  ],
  actions: {
    layerControlEvent(event){
 
    }  
  }
});
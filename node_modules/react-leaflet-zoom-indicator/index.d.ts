import { Control, Layer } from 'leaflet'
import { LayerContainer, Map, MapControl, MapControlProps } from "react-leaflet";

export interface ZoomIndicatorProps extends MapControlProps {
  head: string;
  leaflet?: {
    map?: Map;
    pane?: string;
    layerContainer?: LayerContainer;
    popupContainer?: Layer;
  }
}
export interface inputElement extends HTMLElement { type?: string; value?: number }
export class ReactLeafletZoomIndicator extends MapControl<ZoomIndicatorProps> {
  public div: HTMLElement;
  public span: HTMLElement;
  public input: inputElement;
  public map: Map;
  public props: ZoomIndicatorProps;
  public componentDidMount(): void;
  public createLeafletElement(props: ZoomIndicatorProps): Control;
  public changeZoomInfoAuto(): void;
  public updateZoomInfo(): void
}

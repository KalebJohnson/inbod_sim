import {ReactElement} from 'react';

export interface BodyProps {
  origin: Array<number>;
  mass: number;
  radius: any;
  color?: string;
  x_vel?: number;
  y_vel?: number;
  x_acc?: number;
  y_acc?: number;
  others?: any;
  type?: any;
}

import {ReactElement} from 'react';

export interface BodyProps {
  ref: React.RefObject<any>;
  origin: Array<number>;
  mass: number;
  radius: any;
  color?: any;
  x_vel?: number;
  y_vel?: number;
  z_vel?: number;
  x_acc?: number;
  y_acc?: number;
  z_acc?: number;
  others?: Array<any>;
  type?: any;
}

export interface BodyRef {
  ref: {
    current: {
      position: {
        x: number;
        y: number;
        z: number;
      };
      uuid: string;
      radius: number;
    };
  };
}

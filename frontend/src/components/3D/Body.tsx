import React from 'react';
import {BodyProps} from '../../interfaces/3D';
// eslint-disable-next-line node/no-extraneous-import
import {useFrame} from '@react-three/fiber';
import {Sphere} from '@react-three/drei';

const G = 1;
const otherBodyMass = 1;
/*
function getRandomInt(min: number, max: number) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min);
}
*/
const Body: React.FC<BodyProps> = ({
  origin,
  mass,
  radius,
  ref,
  color = 'white',
  x_vel = 0,
  y_vel = 0,
  z_vel = 0,
  x_acc = 0,
  y_acc = 0,
  z_acc = 0,
  others = [],
  type = 'body',
}) => {
  const x_pos = origin[0];
  const y_pos = origin[1];
  const z_pos = origin[2];

  //Calculate acceleration relative to mass/position and the mass/position of other bodies
  function gravitate(ref: any, otherBodyRef: any) {
    // get distance of other body relative to current position
    const dx = Math.abs(
      ref!.ref.current.position.x - otherBodyRef.current.position.x
    );
    const dy = Math.abs(
      ref!.ref.current.position.y - otherBodyRef.current.position.y
    );

    if (dx < ref!.radius * 2 && dy < ref!.radius * 2) {
      // if bodies get too close (collision) you get crazy acceleration
      // we are just going to shut off gravity when this happens and let the bodies no clip
    } else {
      // r = distance between bodies
      const r = Math.sqrt(dx ** 2 + dy ** 2);

      if (Number.isFinite(dy / r)) {
        // acceleration = gravity * other_body.mass * distance squared
        // UPDATE TO REAL BODY MASS
        const a = (G * otherBodyMass) / r ** 2;
        // theta = angle between hypotenuse and adjacent where body.pos and other_body.pos define the hypotenuse

        const theta = Math.asin(dy / r);

        if (ref!.ref.current.position.y > otherBodyRef.current.position.y)
          // set negative acceleration
          y_acc = -Math.sin(theta) * a;
        // set positive acceleration
        else y_acc = Math.sin(theta) * a;

        if (ref!.ref.current.position.x > otherBodyRef.current.position.x)
          // set negative acceleration
          x_acc = -Math.cos(theta) * a;
        // set positive acceleration
        else x_acc = Math.cos(theta) * a;

        if (ref!.ref.current.position.z > otherBodyRef.current.position.z)
          // set negative acceleration
          z_acc = -Math.sin(theta) * a;
        // set positive acceleration
        else z_acc = Math.sin(theta) * a;
      }
    }
  }

  //const bodyRef = useRef()

  useFrame(() => {
    if (ref!.current) {
      const thisRef = others.find(
        (body: any) => body.ref.current.uuid === ref!.current.uuid
      );
      const index = others.indexOf(ref);

      if (index > -1) {
        others.splice(index, 1);
      }

      others.map((otherBody: any, ind: any) => {
        gravitate(thisRef, otherBody.ref);
      });
      update();
    }
  });

  let xv = 0;
  let yv = 0;
  let zv = 0;

  function update() {
    if (type !== 'star') {
      xv += x_acc;
      yv += y_acc;
      zv += z_acc;
      ref!.current.position.x += xv;
      ref!.current.position.y += yv;
      ref!.current.position.z += zv;
    }
  }

  const size = radius * 2;

  return (
    <Sphere ref={ref} position={[x_pos, y_pos, z_pos]} args={[size, 256, 256]}>
      <meshBasicMaterial color={color} />
    </Sphere>
  );
};

export default Body;

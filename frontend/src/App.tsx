import {
  ReactElement,
  useRef,
  useState,
  useEffect,
  createRef,
  Suspense,
} from 'react';
import {
  Canvas,
  useFrame,
  extend,
  useThree,
  useLoader,
} from '@react-three/fiber';
import {Sphere, Stars, OrbitControls} from '@react-three/drei';
import {uuid} from 'uuidv4';
import './App.css';

import Body from './comps/3D/Body';

function Header({title}: {title?: string}): ReactElement {
  return <h1>{title}</h1>;
}

function App() {

  const bodies = Array(10).fill(0);

  function getRandomInt(min: number, max: number) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min);
  }

  const allBodies = bodies.map(body => {
    const getMass = getRandomInt(10, 200);

    return (body = {
      ref: useRef<ReactElement>(),
      origin: [
        getRandomInt(-50, 50),
        getRandomInt(-50, 50),
        getRandomInt(-50, 50),
      ],
      mass: 10,
      radius: 2,
    });
  });

  allBodies.push({
    ref: useRef<ReactElement>(),
    origin: [0, 0, 0],
    mass: 100,
    radius: 5,
    color: 'red',
    type: 'star',
  });

  console.log(allBodies);

  return (
    <div className="wrapper">
      <Canvas shadows camera={{position: [0, 0, 100], fov: 50}}>
        <Suspense fallback={null}>
          {allBodies.map((body: object, ind: number) => (
            <Body
              origin={body.origin}
              mass={body.mass}
              radius={body.radius}
              others={allBodies}
              ref={body.ref}
              {...body}
              key={ind}
            />
          ))}
          <OrbitControls />
        </Suspense>
      </Canvas>
    </div>
  );
}

export default App;

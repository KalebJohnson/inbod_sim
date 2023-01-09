import {createRef, Suspense} from 'react';
import {
  Canvas,
  // eslint-disable-next-line node/no-extraneous-import
} from '@react-three/fiber';
import {OrbitControls} from '@react-three/drei';
import './App.css';

import Body from './components/3D/Body';

function App() {
  const bodies = Array(10).fill(0);

  function getRandomInt(min: number, max: number) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min);
  }

  const allBodies = bodies.map(body => {
    return (body = {
      ref: createRef(),
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
    ref: createRef(),
    origin: [0, 0, 0],
    mass: 100,
    radius: 5,
    //color: 'red',
    //type: 'star',
  });

  return (
    <div className="wrapper">
      <Canvas shadows camera={{position: [0, 0, 100], fov: 50}}>
        <Suspense fallback={null}>
          {allBodies.map(body => (
            <Body {...body} others={allBodies} />
          ))}
          <OrbitControls />
        </Suspense>
      </Canvas>
    </div>
  );
}

export default App;

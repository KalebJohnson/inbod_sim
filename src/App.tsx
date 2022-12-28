import {ReactElement, useRef, useState, useEffect, createRef, Suspense} from 'react';
import { Canvas, useFrame, extend, useThree, useLoader} from '@react-three/fiber';
import { Sphere, Stars, OrbitControls } from '@react-three/drei';
import { uuid } from 'uuidv4';
import './App.css';

import Body from './comps/3D/Body';

function Header({title}: {title?: string}): ReactElement {
  return <h1>{title}</h1>;
}

function App() {
  const [count, setCount] = useState<number>(0);

  function getPermutations(array, size) {

    function p(t, i) {
        if (t.length === size) {
            result.push(t);
            return;
        }
        if (i + 1 > array.length) {
            return;
        }
        p(t.concat(array[i]), i + 1);
        p(t, i + 1);
    }

    let result = [];
    p([], 0);
    return result;
  }

  let bodies = Array(10).fill(0)

  function getRandomInt(min, max) {
    min = Math.ceil(min)
    max = Math.floor(max)
    return Math.floor(Math.random() * (max - min) + min)
  }

  const allBodies = bodies.map((body) => {

    let getMass = getRandomInt(10,200)

    return body = {
      ref: createRef(),
      origin: [getRandomInt(-50,50), getRandomInt(-50,50),getRandomInt(-50,50)],
      mass: 10,
      radius: 2,
    }

  })

  allBodies.push(
    {
      ref: createRef(),
      origin: [0, 0, 0],
      mass: 100,
      radius: 5,
      color:'red',
      type:'star'
    }
  )

  return (
    <div className="wrapper">
      <Canvas shadows camera={{ position: [0,0,100], fov: 50 }} >
        <Suspense fallback={null}>
          {
            allBodies.map((body) => (
                <Body 
                  {...body}
                  others={allBodies}
                  />
              )
            )
          }
          <OrbitControls/>
        </Suspense>
      </Canvas>
    </div>
  );
}



export default App;

import {ReactElement, useRef, useState, useEffect, createRef} from 'react';
import { Canvas, useFrame, extend, useThree, useLoader} from '@react-three/fiber';
import { Sphere, Stars } from '@react-three/drei';
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
  let allBodies = bodies.map((body, ind) => { return body = {ref:createRef()}})

  return (
    <div className="wrapper">
      <Canvas shadows camera={{ position: [0,0,100], fov: 50 }} >
        {
          allBodies.map((body) => <Body ref={body.ref} others={allBodies}/>)
        }
      </Canvas>
    </div>
  );
}



export default App;

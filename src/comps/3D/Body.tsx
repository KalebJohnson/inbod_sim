import React, { ReactElement, useRef } from "react"
import { Sphere, } from "@react-three/drei"
import { BodyProps } from "../../interfaces/3D"
import { useFrame } from '@react-three/fiber'

const G = 1
const otherBodyMass = 1

function getRandomInt(min, max) {
    min = Math.ceil(min)
    max = Math.floor(max)
    return Math.floor(Math.random() * (max - min) + min)
  }

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


const Body: React.FunctionComponent<BodyProps> = React.forwardRef<ReactElement>(({
    origin = [getRandomInt(-50,50), getRandomInt(-50,50)],
    mass = getRandomInt(10,200),
    radius = mass/100,
    color = "white",
    x_vel = 0,
    y_vel = 0,
    x_acc = 0,
    y_acc = 0,
    others = [],
  },ref) => {
    console.log(others)
    let x_pos = origin[0];
    let y_pos = origin[1];
  
    const set_x_vel = (value: number) => {
      x_vel = value;
    };
  
    const set_y_vel = (value: number) => {
      y_vel = value;
    };
  
    const set_x_acc = (value: number) => {
      x_acc = value;
    };
  
    const set_y_acc = (value: number) => {
      y_acc = value;
    };
  
    const change_x_pos = (value: number) => {
      x_pos += value;
    };
  
    const change_y_pos = (value: number) => {
      y_pos += value;
    };

    //const bodyRef = useRef()
    

    let t = 0

    useFrame(() => {
        update()
    })

    console.log(ref, mass, radius)

    function update(){
        ref.current.position.x = x_pos
        ref.current.position.y = y_pos
    }

    //Calculate acceleration relative to mass/position and the mass/position of other bodies
    function gravitate(otherBodyRef){
        // get distance of other body relative to current position
        let dx = Math.abs(bodyRef.current.position.x - otherBodyRef.current.position.x)
        let dy = Math.abs(bodyRef.current.position.y - otherBodyRef.current.position.y)

        if(dx < radius * 2 && dy < radius * 2){
            // if bodies get too close (collision) you get crazy acceleration
            // we are just going to shut off gravity when this happens and let the bodies no clip
            
        } else {
            // r = distance between bodies
            let r = Math.sqrt(dx ** 2 + dy ** 2)

            if(Number.isFinite(dy/r)){
                // acceleration = gravity * other_body.mass * distance squared
                // UPDATE TO REAL BODY MASS
                let a = G * otherBodyMass / r ** 2
                // theta = angle between hypotenuse and adjacent where body.pos and other_body.pos define the hypotenuse
                    
                let theta = Math.asin(dy/r)

                if (bodyRef.current.position.y > otherBodyRef.current.position.y)
                    // set negative acceleration
                    set_y_acc(-Math.sin(theta) * a)
                else
                    // set positive acceleration
                    set_y_acc(Math.sin(theta) * a)

                if (bodyRef.current.position.x > otherBodyRef.current.position.x)
                    // set negative acceleration
                    set_x_acc(-Math.cos(theta) * a)
                else
                    // set positive acceleration
                    set_x_acc(Math.cos(theta) * a)

            } 
        }
    }

    return (
        <Sphere ref={ref} args={[20,256,256]} position={[x_pos,y_pos, 0]} args={[radius, 256, 256]}>
            <meshBasicMaterial color={color} />
        </Sphere>
    )
  })


export default Body
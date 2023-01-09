from __future__ import annotations

from typing import Optional

from sys import exit
import math
import itertools
import random
import uuid

G = 0.1

class Vec3():
    """Three Dimensional Vector"""

    def __init__(
        self,
        x: Optional[float] = 0,
        y: Optional[float] = 0,
        z: Optional[float] = 0,
    ):
        self.x = x
        self.y = y
        self.z = z

    def as_list(self):
        return [self.x, self.y, self.z]

    def set_x(self, value: float):
        self.x = value

    def set_y(self, value: float):
        self.y = value

    def set_z(self, value: float):
        self.z = value

    def incr_x(self, value: float):
        self.x += value

    def incr_y(self, value: float):
        self.y += value

    def incr_z(self, value: float):
        self.z += value
    


class Entity():
    """Object that represents an entity in 3D space"""

    def __init__(
        self,
        entity_id: Optional[uuid.UUID] = None,
        mass: Optional[float] = 0.0,
        radius: Optional[float] = 0.0,
        origin: Optional[Vec3] = None,
        velocity: Optional[Vec3] = None,
        position: Optional[Vec3] = None,
    ):
        super().__init__()
        entity_id = entity_id if entity_id is not None else uuid.uuid4()
        self.mass = mass
        self.radius = radius
        self.origin = origin if origin is not None else Vec3()
        self.velocity = velocity if velocity is not None else Vec3()
        self.position = position if position is not None else Vec3()
        self.acceleration = Vec3()

    def set_velocity(
        self, 
        x: Optional[float] = None, 
        y: Optional[float] = None, 
        z: Optional[float] = None
    ):
        """Set velocity"""
        if x is not None:
            self.velocity.set_x(x)
        if y is not None:
            self.velocity.set_y(y)
        if z is not None:
            self.velocity.set_z(z)              

    def set_acceleration(
        self, 
        x: Optional[float] = None, 
        y: Optional[float] = None, 
        z: Optional[float] = None
    ):
        """Set acceleration"""
        if x is not None:
            self.acceleration.set_x(x)
        if y is not None:
            self.acceleration.set_y(y)
        if z is not None:
            self.acceleration.set_z(z)   

    def increment_position(self, x: float, y: float, z: float):
        """Offset current position"""
        self.position.incr_x(x)
        self.position.incr_x(y)
        self.position.incr_x(z)

    def increment_velocity(self, value: float):
        """Offset current velocity"""
        self.x_vel += value

    # TODO: this
    def update_pos(self):
        """Update position"""
        self.rect.center = (
            round(self.x_pos),
            round(self.y_pos)
        )

    def update(self):
        """Update positions and velocity"""
        # use accelertation to update velocity
        self.increment_velocity(
            x=self.acceleration.x, 
            y=self.acceleration.y, 
            z=self.acceleration.z
        )
        # use velocity to update position
        self.increment_position(
            x=self.position.x, 
            y=self.position.y, 
            z=self.position.z
        )
        # TODO: this
        self.update_pos()

    def gravitate(self, other_entity: Entity):
        """Calculate acceleration relative to mass/position and the mass/position of other entities"""

        # get distance of other entity relative to current position
        distance_vector = Vec3(
            x=abs(self.position.x - other_entity.position.x),
            y=abs(self.position.y - other_entity.position.y),
            z=abs(self.position.z - other_entity.position.z)
        )
        # check for collision
        is_colliding = all(
            distance_on_axis < self.radius 
            for distance_on_axis in distance_vector.as_list()
        )
        # if entities get too close (collision) you get crazy acceleration
        # we are just going to shut off gravity when this happens and let the entities no clip
        if is_colliding:
            pass
        else:
            try:
                # r = distance between entities
                r = math.sqrt(
                    distance_vector.x ** 2 + 
                    distance_vector.y ** 2 + 
                    distance_vector.z ** 2
                )
                # acceleration = gravity * other_entity.mass * distance squared
                a = G * other_entity.mass / r ** 2
                # theta = angle between hypotenuse and adjacent where entity.pos and other_entity.pos define the hypotenuse
                theta_y = math.asin(distance_vector.y/r)
                theta_z = math.acos(distance_vector.z/r)
                # set acceleration
                x_acc = math.cos(theta_y) * a * math.sign(self.position.x - other_entity.position.x)
                y_acc = math.sin(theta_y) * a * math.sign(self.position.y - other_entity.position.y)
                z_acc = math.sin(theta_z) * a * math.sign(self.position.z - other_entity.position.z)

                self.set_acceleration(x=x_acc, y=y_acc, z=z_acc)

            except ZeroDivisionError:
                pass

# TODO: this
entity_group = pygame.sprite.Group()
ENTITY_COUNT: int = 10
sun: Entity = Entity(
    mass=100,
    radius=10,
    origin=(500, 500),
    x_vel=0,
    y_vel=0
)


def get_random_entity() -> Entity:
    """generate entity at random position"""
    return Entity(
        mass=1,
        radius=3,
        origin=(
            random.randrange(
                100,
                900
            ),
            random.randrange(
                100,
                900
            )
        ),
        x_vel=0,
        y_vel=0
    )


# initialize entities
for i in range(ENTITY_COUNT):
    if i == 0:
        entity_group.add(sun)
    else:
        entity_group.add(get_random_entity())

# group entities
entity_list = list(entity_group)
entity_pairs = list(itertools.combinations(entity_list, 2))

# sim_loop
while True:
    for event in pygame.event.get():
        # if close event... close
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # draw canvas
    WINDOW.blit(
        BACKGROUND,
        BACKGROUND_RECT
    )
    entity_group.draw(WINDOW)

    # calculate entity positions/acceleration
    for entity, other_entity in entity_pairs:
        entity.gravitate(other_entity)
        other_entity.gravitate(entity)
        entity.update()
        other_entity.update()

    # draw entities
    pygame.display.update()
    CLOCK.tick(60)
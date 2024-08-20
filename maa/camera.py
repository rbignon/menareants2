from ursina import Entity, camera, destroy, held_keys, mouse, curve, lerp, clamp, time, Vec2, Vec3, slerp

class Camera(Entity):

    def __init__(self, **kwargs):
        camera.editor_position = camera.position
        super().__init__(name='editor_camera', eternal=False)

        # self.gizmo = Entity(parent=self, model='sphere', color=color.orange, scale=.025, add_to_scene_entities=False, enabled=False)

        self.rotation_speed = 200
        self.pan_speed = Vec2(5, 5)
        self.move_speed = 10
        self.target_fov = camera.fov
        self.zoom_speed = 1.25
        self.zoom_smoothing = 8
        self.rotate_around_mouse_hit = False
        self.ignore_scroll_on_ui = True

        self.smoothing_helper = Entity(add_to_scene_entities=False)
        self.rotation_smoothing = 0
        self.look_at = self.smoothing_helper.look_at
        self.look_at_2d = self.smoothing_helper.look_at_2d
        self.rotate_key = 'right mouse'

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.start_position = self.position
        self.perspective_fov = camera.fov
        self.orthographic_fov = camera.fov
        self.on_destroy = self.on_disable
        self.shortcuts = {'toggle_orthographic':'shift+p', 'focus':'shift+f', 'reset_center':'alt+f'}


    def on_enable(self):
        self.org_cam_par = camera.parent
        self.org_cam_pos = camera.position
        self.org_cam_rot = camera.rotation
        camera.parent = self
        camera.position = camera.editor_position
        camera.rotation = (0,0,0)
        self.target_z = camera.z
        self.target_fov = camera.fov


    def on_disable(self):
        camera.editor_position = camera.position

        # if we instantiate with enabled=False, this will get called before on_enable and these variables won't exist.
        if hasattr(self, 'org_cam_par'):
            camera.parent = self.org_cam_par
            camera.position = self.org_cam_pos
            camera.rotation = self.org_cam_rot

    def on_destroy(self):
        destroy(self.smoothing_helper)

    def set_orthographic(self, orthographic):
        if orthographic:
            self.orthographic_fov = camera.fov
            camera.fov = self.perspective_fov
        else:
            self.perspective_fov = camera.fov
            camera.fov = self.orthographic_fov

        camera.orthographic = orthographic

    def input(self, key):
        combined_key = ''.join(e+'+' for e in ('control', 'shift', 'alt') if held_keys[e] and not e == key) + key

        if combined_key == self.shortcuts['toggle_orthographic']:
            self.set_orthographic(not camera.orthographic)

        elif combined_key == self.shortcuts['reset_center']:
            self.animate_position(self.start_position, duration=.1, curve=curve.linear)

        elif combined_key == self.shortcuts['focus'] and mouse.world_point:
            self.animate_position(mouse.world_point, duration=.1, curve=curve.linear)


        elif key == 'scroll up':
            if self.ignore_scroll_on_ui and mouse.hovered_entity and mouse.hovered_entity.has_ancestor(camera.ui):
                return
            if not camera.orthographic:
                target_position = self.world_position
                self.world_position = lerp(self.world_position, target_position, self.zoom_speed * time.dt * 10)
                self.target_z += self.zoom_speed * (abs(self.target_z)*.1)
                self.target_z = clamp(self.target_z, -50, -30)
            else:
                self.target_fov -= self.zoom_speed * (abs(self.target_fov)*.1)
                self.target_fov = clamp(self.target_fov, 5, 13)

        elif key == 'scroll down':
            if self.ignore_scroll_on_ui and mouse.hovered_entity and mouse.hovered_entity.has_ancestor(camera.ui):
                return

            if not camera.orthographic:
                # camera.world_position += camera.back * self.zoom_speed * 100 * time.dt * (abs(camera.z)*.1)
                self.target_z -= self.zoom_speed * (abs(self.target_z)*.1)
                self.target_z = clamp(self.target_z, -50, -30)
            else:
                self.target_fov += self.zoom_speed * (abs(self.target_fov)*.1)
                self.target_fov = clamp(self.target_fov, 5, 13)

        elif key == 'right mouse down' or key == 'middle mouse down':
            if mouse.hovered_entity and self.rotate_around_mouse_hit:
                org_pos = camera.world_position
                self.world_position = mouse.world_point
                camera.world_position = org_pos



    def update(self):
        if held_keys['gamepad right stick y'] or held_keys['gamepad right stick x']:
            self.smoothing_helper.rotation_x -= held_keys['gamepad right stick y'] * self.rotation_speed / 100
            self.smoothing_helper.rotation_y += held_keys['gamepad right stick x'] * self.rotation_speed / 100

        elif held_keys[self.rotate_key]:
            self.smoothing_helper.rotation_x -= mouse.velocity[1] * self.rotation_speed
            self.smoothing_helper.rotation_x = clamp(self.smoothing_helper.rotation_x, 20, 90)
            self.smoothing_helper.rotation_y += mouse.velocity[0] * self.rotation_speed

            self.direction = Vec3(
                self.forward * (held_keys['w'] - held_keys['s'])
                + self.right * (held_keys['d'] - held_keys['a'])
                + self.up    * (held_keys['e'] - held_keys['q'])
                ).normalized()

            self.position += self.direction * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt

            if self.target_z < 0:
                self.target_z += held_keys['w'] * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt
            else:
                self.position += camera.forward * held_keys['w'] * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt

            self.target_z -= held_keys['s'] * (self.move_speed + (self.move_speed * held_keys['shift']) - (self.move_speed*.9 * held_keys['alt'])) * time.dt

        if mouse.middle:
            if not camera.orthographic:
                zoom_compensation = -self.target_z * .1
            else:
                zoom_compensation = camera.orthographic * camera.fov * .2

            self.position -= camera.right * mouse.velocity[0] * self.pan_speed[0] * zoom_compensation
            self.position -= camera.up * mouse.velocity[1] * self.pan_speed[1] * zoom_compensation

        #self.x = clamp(self.x, 14, 100)
        #self.z = clamp(self.z, -1, 100)

        if not camera.orthographic:
            camera.z = lerp(camera.z, self.target_z, time.dt*self.zoom_smoothing)
        else:
            camera.fov = lerp(camera.fov, self.target_fov, time.dt*self.zoom_smoothing)

        if self.rotation_smoothing == 0:
            self.rotation = self.smoothing_helper.rotation
        else:
            self.quaternion = slerp(self.quaternion, self.smoothing_helper.quaternion, time.dt*self.rotation_smoothing)
            camera.world_rotation_z = 0

        self.world_position.y = 15

        print(camera.position, camera.world_position, self.position, camera.fov)


    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if hasattr(self, 'smoothing_helper') and name in ('rotation', 'rotation_x', 'rotation_y', 'rotation_z'):
            setattr(self.smoothing_helper, name, value)

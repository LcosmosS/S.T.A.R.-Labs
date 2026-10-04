import { HavokPlugin, PhysicsAggregate, PhysicsShapeType } from "@babylonjs/core";
import HavokPhysics from "@babylonjs/havok";

const havok = await HavokPhysics();                 // MUST await — loads the .wasm
scene.enablePhysics(new Vector3(0, -9.81, 0), new HavokPlugin(true, havok));

// dynamic body:
new PhysicsAggregate(sphere, PhysicsShapeType.SPHERE, { mass: 1, restitution: 0.6, friction: 0.5 }, scene);
// static body: mass 0
new PhysicsAggregate(ground, PhysicsShapeType.BOX, { mass: 0 }, scene);

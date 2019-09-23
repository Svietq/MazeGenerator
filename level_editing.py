import unreal
unreal.log("started-------------------------------------------------------------------------------------------------")

unreal.EditorLevelLibrary.set_current_level_by_name("RollingExampleMap")
plane = unreal.EditorAssetLibrary.load_asset("StaticMesh'/Engine/BasicShapes/Cube.Cube'")


def spawn_wall(x, y, z, yaw):
    if plane:
        location = unreal.Vector()
        location.x = x
        location.y = y
        location.z = z
        rotation = unreal.Rotator()
        rotation.yaw = yaw
        rotation.roll = 90
        spawned_actor = unreal.EditorLevelLibrary.spawn_actor_from_object(plane, location, rotation)
        scale = unreal.Vector()
        scale.x = 5
        scale.y = 3
        scale.z = 0.2
        spawned_actor.set_actor_relative_scale3d(scale)


clearance = 200
initial_x = -1500
initial_y = -2500
initial_z = 280

with open("D:/projekty/python/unreal/maze.txt", 'r') as f:
	maze_data = [line.strip() for line in f]
	new_data = []
	for line in maze_data:
		new_data.append(line.replace("\x00", ''))
	print(new_data)

	x = 0
	y = 0
	for line in new_data:
		for char in line:
			if char == '|':
				spawn_wall(initial_x + x * clearance, initial_y + y * clearance, initial_z, 90)
			elif char == '-':
				spawn_wall(initial_x + x * clearance, initial_y + y * clearance, initial_z, 0)
			x += 1
		x = 0
		y += 1

unreal.log("done-----------------------------------------------------------------------------------------------------")

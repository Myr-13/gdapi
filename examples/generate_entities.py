from gdapi import *

lls = LocalLevels()

lvl = Level()
lvl.name = "test gen"
lvl.author = "lso44"

for x in range(0, 2048):
	ent = Entity()
	ent.id = x
	ent.x = x * 90 + 15
	ent.y = 15

	lvl.entities.append(ent)

	ent2 = Entity()
	ent2.id = 914
	ent2.x = x * 90 + 15
	ent2.y = 45
	ent2.text = str(x)

	lvl.entities.append(ent2)

lls.levels.append(lvl)
lls.save_file(lls_path())

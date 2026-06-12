test-run:
	manim -pqh src/test/test.py Test

run:
	manim -pqh src/main.py Main

FILE ?= hook
SCENE ?= HookScene

scene:
	manim -pqh src/scene/$(FILE).py $(SCENE)
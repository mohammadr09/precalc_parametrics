venv:
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
	fi
	@source .venv/bin/activate

test-run:
	manim -pqh src/test/test.py Test

run:
	manim -pqh src/main.py Main

FILE ?= hook_two
SCENE ?= HookSceneTwo

scene:
	manim -pqh src/scene/$(FILE).py $(SCENE)
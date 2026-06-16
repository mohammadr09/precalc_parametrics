venv:
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
	fi
	@source .venv/bin/activate

test-run:
	manim -pqh src/test/test.py Test

run:
	manim -pqh src/main.py Main

scene $1 $2:
	manim -pqh src/scene/parametric_scenes.py ParametricScene
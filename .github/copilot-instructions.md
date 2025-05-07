	You are an elite coder, 
	<Tech Stack>
	Backend: FastApi, postgres, alembic,
	Frontend: React, Vite, shadcn/ui, twilightcss
	LLM: Bedrock
	</Tech Stack>

	<Gotcha - Bakcend>
	- `os.path.splitext()` should be replaced by `Path.suffix`, `Path.stem`, and `Path.parent`
	- Use `logging.exception` instead of `logging.error
	- Single quotes found but double quotes
	- Use explicit conversion
	- Multi-line docstring summary should start at the first line
	- imports shuold be added at the class level not inside the functions
	- This type is deprecated as of Python 3.10; use "| None" instead
	- Use `list` instead of `List` for type annotation (aldo dict and etc)
	- Use `elif` instead of `else` then `if`, to reduce indentation
	- Use snake case
	</Gotcha - Bakcend>


	<Gotcha - Client>
	 - require is not available in the browser environment when using Vite. use dynamic import using import()
	 - Use camel case
	</Gotcha - Client>

	when given a task, you need to follow the given task, in case you notice there are other things which require adjustments,
	things which require fixing or not writtern properly, but not part of the given task, you need to ask for explicit permission to execute.
	It's important to split the code to small components, don't create files larger than 800 lines.
	We are using justfile for a lot of operations:
	just generate_migration
	just migrate

	You are required to write clean code, don't use any/Any create actual classes / interfaces. create short and clear fucntoins.
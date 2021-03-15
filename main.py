from yamllint.config import YamlLintConfig
import yamllint
import yaml
import os
import io
import asyncio
import pydantic

from schema import CatalogInfo


def format(e: pydantic.ValidationError) -> dict:
    no_errors = len(e.errors())
    message = f'{no_errors} validation error{"" if no_errors == 1 else "s"}'
    display_error_loc = lambda error: ".".join(str(e) for e in error["loc"])

    return {
        "message": message,
        "errors": [
            {display_error_loc(error): "%s." % (error["msg"])} for error in e.errors()
        ],
    }


def linter(input: str = None) -> yamllint.linter.LintProblem:
    """Lints a YAML using yamllint.

    Returns a generator of LintProblem objects.

    :param input: buffer, string or stream to read from
    """
    assert input

    return yamllint.linter.run(input, YamlLintConfig(file="config.yaml"))


async def validate(file_path: str):
    assert file_path

    with open(file_path, newline="") as f:
        has_error = False
        content = f.read()

        linter_result = [
            *map(
                lambda x: {
                    "line": x.line,
                    "column": x.column,
                    "level": x.level,
                    "message": x.message,
                },
                linter(content),
            )
        ]
        if linter_result:
            yield {"file_path": file_path, "validation_message": linter_result}
            return

        try:
            poc = yaml.safe_load_all(content)
            for content in poc:
                CatalogInfo.parse_obj(content)
                yield {
                    "app": content["metadata"]["name"],
                    "validation_message": "Congrats! Errors not found",
                }
        except pydantic.ValidationError as e:
            yield {"app": content["metadata"]["name"], "validation_message": format(e)}
        except Exception as e:
            raise Exception("invalid file: %s" % e)


async def run(file_path: str):
    async for catalog in validate(file_path):
        print(catalog)


loop = asyncio.get_event_loop()

for dirpath, dnames, fnames in os.walk("./yaml_files/"):
    for f in fnames:
        file_path = os.path.join(dirpath, f)
        loop.run_until_complete(run(file_path))

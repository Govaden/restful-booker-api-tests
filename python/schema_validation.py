from functools import cache
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

SPEC_PATH = Path(__file__).resolve().parent / "openapi" / "restful-booker.yaml"


@cache
def load_spec():
    with SPEC_PATH.open(encoding="utf-8") as spec_file:
        return yaml.safe_load(spec_file)


@cache
def _validator_for(schema_name):
    components = load_spec()["components"]
    if schema_name not in components["schemas"]:
        available = ", ".join(sorted(components["schemas"]))
        raise ValueError(f"Unknown schema '{schema_name}' in {SPEC_PATH.name}. Available: {available}")
    return Draft202012Validator({"$ref": f"#/components/schemas/{schema_name}", "components": components})


def assert_matches_schema(body, schema_name):
    errors = sorted(_validator_for(schema_name).iter_errors(body), key=lambda error: error.json_path)
    if errors:
        details = "\n".join(f"  {schema_name}: {error.json_path}: {error.message}" for error in errors)
        raise AssertionError(f"Response body does not match schema '{schema_name}':\n{details}")

import pytest
from jsonschema import Draft202012Validator
from openapi_spec_validator import validate

from schema_validation import load_spec


def test_openapi_spec_is_valid():
    validate(load_spec())


def test_spec_uses_json_schema_2020_12_dialect():
    assert load_spec()["jsonSchemaDialect"] == "https://json-schema.org/draft/2020-12/schema"


@pytest.mark.parametrize("schema_name", sorted(load_spec()["components"]["schemas"]))
def test_component_schema_is_valid_json_schema(schema_name):
    Draft202012Validator.check_schema(load_spec()["components"]["schemas"][schema_name])

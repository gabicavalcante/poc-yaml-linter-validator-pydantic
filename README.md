# poc-yaml-linter-validator-pydantic

This project is a simple POC to undestand more about yaml, lint and validation with [pydantic](https://pydantic-docs.helpmanual.io/). I used [backstage yaml file format](https://backstage.io/docs/features/software-catalog/descriptor-format) as a base to build the validator.  

To generate the pydantic schema I used the [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator/). The `datamodel-code-generator` is a library and command-line utility to generate pydantic models from a source like JSON Schema. You can find a json schema template in the root directory, to generate a schema run:

```
$ datamodel-codegen  --input catalog.template.schema.json --input-file-type jsonschema --output schema.template.py
```
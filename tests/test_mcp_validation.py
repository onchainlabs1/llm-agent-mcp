import json
from pathlib import Path

import pytest

from agent.tools_mcp_client import MCPClient, MCPToolSchema


def load_schema(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize(
    "schema_file",
    [
        "mcp_server/crm_mcp.json",
        "mcp_server/erp_mcp.json",
        "mcp_server/hr_mcp.json",
    ],
)
def test_load_tool_schemas(schema_file: str):
    client = MCPClient()
    assert client.load_tool_schemas_from_file(schema_file) is True
    assert len(client.get_available_tools()) > 0


def test_validate_parameters_with_sample_schema(tmp_path):
    # minimal schema to validate behavior
    sample = {
        "tools": [
            {
                "name": "get_client_by_id",
                "description": "Get client by id",
                "input_schema": {
                    "type": "object",
                    "properties": {"client_id": {"type": "string"}},
                    "required": ["client_id"],
                    "additionalProperties": False,
                },
            }
        ]
    }
    file = tmp_path / "sample.json"
    file.write_text(json.dumps(sample), encoding="utf-8")

    client = MCPClient()
    assert client.load_tool_schemas_from_file(str(file)) is True
    ok = client.validate_tool_parameters("get_client_by_id", {"client_id": "abc"})
    assert ok is True
    bad = client.validate_tool_parameters("get_client_by_id", {"id": "abc"})
    assert bad is False



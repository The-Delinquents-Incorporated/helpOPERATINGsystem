import pytest
import json
from unittest.mock import AsyncMock, patch
from backend.app.services.coordinator import parse_json_command, execute_tool, coordinator_service

def test_parse_json_command():
    # Raw JSON
    raw_json = '{"tool": "molar_mass", "args": {"formula": "CO2"}}'
    parsed = parse_json_command(raw_json)
    assert parsed is not None
    assert parsed["tool"] == "molar_mass"
    assert parsed["args"]["formula"] == "CO2"

    # Markdown JSON Fenced block
    md_json = """
Here is the command you need:
```json
{
  "tool": "math_solve",
  "args": {
    "expression": "2 * 3 + 4"
  }
}
```
Hope that helps!
"""
    parsed = parse_json_command(md_json)
    assert parsed is not None
    assert parsed["tool"] == "math_solve"
    assert parsed["args"]["expression"] == "2 * 3 + 4"

    # Non-JSON content
    non_json = "The molar mass of water is 18.02 g/mol."
    assert parse_json_command(non_json) is None

def test_execute_tool_molar_mass():
    result = execute_tool("molar_mass", {"formula": "H2O"})
    assert result["formula"] == "H2O"
    assert result["molar_mass"] == 18.02
    assert result["unit"] == "g/mol"

def test_execute_tool_convert_grams_moles():
    # Grams to moles: 36.04g of H2O is 2.0 moles
    result = execute_tool(
        "convert_grams_moles", 
        {"formula": "H2O", "value": 36.04, "direction": "grams_to_moles"}
    )
    assert result["result"] == 2.0
    assert result["unit"] == "moles"

    # Moles to grams: 2 moles of H2O is 36.04 grams
    result = execute_tool(
        "convert_grams_moles", 
        {"formula": "H2O", "value": 2.0, "direction": "moles_to_grams"}
    )
    assert result["result"] == 36.04
    assert result["unit"] == "grams"

def test_execute_tool_stp_conversion():
    # 44.8 Liters to Moles = 2.0 moles
    result = execute_tool("stp_conversion", {"value": 44.8, "direction": "liters_to_moles"})
    assert result["result"] == 2.0
    assert result["unit"] == "moles"

def test_execute_tool_avogadro_calculation():
    # 2.0 moles to particles = 1.204e24
    result = execute_tool("avogadro_calculation", {"value": 2.0, "direction": "moles_to_particles"})
    assert result["result"] == 1.204e24
    assert result["unit"] == "particles"

def test_execute_tool_math_solve():
    # Simple equation
    result = execute_tool("math_solve", {"expression": "2 * (3 + 4)"})
    assert result["result"] == 14
    assert result["success"] is True

    # Complex expression (fallback to mock)
    result = execute_tool("math_solve", {"expression": "x^2 + 5x + 6 = 0"})
    assert "mock" in result["result"]
    assert result["is_mock"] is True

def test_execute_tool_invalid():
    with pytest.raises(ValueError):
        execute_tool("invalid_tool", {})

@pytest.mark.asyncio
async def test_coordinator_route_reasoning():
    # Mock Ollama outputting a conversational reasoning response
    mock_ollama_resp = {
        "message": {"role": "assistant", "content": "Molar mass is the mass of a given chemical element or chemical compound divided by the amount of substance."}
    }
    
    with patch("backend.app.services.ollama.ollama_service.generate_chat_completion", new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = mock_ollama_resp
        
        resp = await coordinator_service.route_query([{"role": "user", "content": "explain molar mass"}])
        assert resp["mode"] == "reasoning"
        assert "Molar mass is" in resp["content"]

@pytest.mark.asyncio
async def test_coordinator_route_deterministic():
    # Mock Ollama outputting a JSON tool block
    mock_ollama_resp = {
        "message": {"role": "assistant", "content": '```json\n{"tool": "molar_mass", "args": {"formula": "CO2"}}\n```'}
    }
    
    with patch("backend.app.services.ollama.ollama_service.generate_chat_completion", new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = mock_ollama_resp
        
        resp = await coordinator_service.route_query([{"role": "user", "content": "molar mass of CO2"}])
        assert resp["mode"] == "deterministic"
        assert resp["tool"] == "molar_mass"
        assert resp["result"]["formula"] == "CO2"
        assert resp["result"]["molar_mass"] == 44.01

@pytest.mark.asyncio
async def test_coordinator_route_stream_reasoning():
    # Helper async generator mock
    async def mock_generator():
        chunks = [
            '{"message": {"content": "Water "}}',
            '{"message": {"content": "is "}}',
            '{"message": {"content": "wet."}}'
        ]
        for c in chunks:
            yield c

    with patch("backend.app.services.ollama.ollama_service.generate_chat_completion", new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = mock_generator()
        
        output_chunks = []
        async for chunk in coordinator_service.route_query_stream([{"role": "user", "content": "is water wet"}]):
            output_chunks.append(json.loads(chunk))
            
        # Verify it streams immediately in reasoning mode
        assert len(output_chunks) > 0
        assert output_chunks[0]["mode"] == "reasoning"
        combined_text = "".join([c["content"] for c in output_chunks if c["mode"] == "reasoning"])
        assert "Water is wet." in combined_text

@pytest.mark.asyncio
async def test_coordinator_route_stream_deterministic():
    # Helper async generator mock
    async def mock_generator():
        chunks = [
            '{"message": {"content": "```json\\n"}}',
            '{"message": {"content": "{\\"tool\\": \\"molar_mass\\", "}}',
            '{"message": {"content": "\\"args\\": {\\"formula\\": \\"H2O\\"}}"}}',
            '{"message": {"content": "\\n```"}}'
        ]
        for c in chunks:
            yield c

    with patch("backend.app.services.ollama.ollama_service.generate_chat_completion", new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = mock_generator()
        
        output_chunks = []
        async for chunk in coordinator_service.route_query_stream([{"role": "user", "content": "molar mass of H2O"}]):
            output_chunks.append(json.loads(chunk))
            
        # The stream should be buffered and yield a single deterministic result block at the end
        assert len(output_chunks) == 1
        assert output_chunks[0]["mode"] == "deterministic"
        assert output_chunks[0]["tool"] == "molar_mass"
        assert output_chunks[0]["result"]["molar_mass"] == 18.02

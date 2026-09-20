import unittest

from app.mcp_server import mcp_server


class McpServerTests(unittest.IsolatedAsyncioTestCase):
    async def test_exposes_only_analysis_report_tools(self) -> None:
        tools = await mcp_server.list_tools()

        self.assertEqual(
            {tool.name for tool in tools},
            {"list_analysis_tickers", "get_analysis_report"},
        )
        self.assertTrue(all(tool.annotations.read_only_hint for tool in tools))


if __name__ == "__main__":
    unittest.main()

import asyncio
from fastmcp.client import Client, SSETransport

# 请将 <your_key> 替换为你的高德开放平台 key
AMAP_KEY = "42ee55b78a39831bd9270552829c071c"
MCP_SSE_URL = f"https://mcp.amap.com/sse?key={AMAP_KEY}"


async def main():
    client = Client(SSETransport(MCP_SSE_URL))
    async with client:
        # 列出可用工具及参数
        tools = await client.list_tools()
        print("可用工具及参数:")
        for tool in tools:
            print(f"\n- {tool.name}: {tool.description}")
            print("  inputSchema:", tool.inputSchema)

        # 调用 maps_weather 工具（如可用）
        if any(tool.name == "maps_weather" for tool in tools):
            result = await client.call_tool("maps_weather", {"city": "北京"})
            print("\n调用 maps_weather 结果:")
            for content in result:
                print(content)
        else:
            print("未找到 maps_weather 工具")


if __name__ == "__main__":
    asyncio.run(main())

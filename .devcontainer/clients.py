import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    print("🚀 Booting up the test client...")
    server_params = StdioServerParameters(command="python3", args=["server.py"])
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✅ Connected to the MCP Server!")

                # --- NEW: TEST THE NMAP TOOL ---
                print("🛰️  Instructing Server to run Nmap on scanme.nmap.org...")
                
                # We call the tool by name and pass the target argument
                result = await session.call_tool("port_scan", arguments={"target": "scanme.nmap.org"})
                
                # Print the actual terminal output from Nmap
                print("\n--- SCAN RESULTS ---")
                print(result.content[0].text)
                    
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
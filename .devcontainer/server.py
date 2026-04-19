from mcp.server.fastmcp import FastMCP
import subprocess

mcp = FastMCP("bug-hunter-mcp")

@mcp.tool()
def run_subfinder(domain: str) -> str:
    """Finds subdomains for a target."""
    try:
        result = subprocess.run(
            ["/go/bin/subfinder", "-d", domain, "-silent"], 
            capture_output=True, text=True, timeout=60
        )
        return f"Subdomains for {domain}:\n{result.stdout}"
    except Exception as e:
        return f"Subfinder error: {str(e)}"

@mcp.tool()
def check_live_hosts(subdomains: str) -> str:
    """Takes a list of subdomains (newline separated) and returns live web targets."""
    try:
        # We pipe the subdomains into httpx
        process = subprocess.Popen(["/go/bin/httpx", "-silent"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=subdomains)
        return f"Live Hosts:\n{stdout}"
    except Exception as e:
        return f"HTTPX error: {str(e)}"

@mcp.tool()
def port_scan(target: str) -> str:
    """Runs a quick Nmap scan on top 1000 ports."""
    try:
        result = subprocess.run(
            ["nmap", "-F", "--open", target], 
            capture_output=True, text=True, timeout=120
        )
        return f"Nmap Scan for {target}:\n{result.stdout}"
    except Exception as e:
        return f"Nmap error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
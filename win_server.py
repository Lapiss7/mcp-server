import sys
import paramiko
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("kali-bug-hunter")

def run_remote(command_string: str) -> str:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect("192.168.189.128", username="kali", key_filename="C:/Users/Ekas/.ssh/id_rsa")
        
        stdin, stdout, stderr = client.exec_command(f"bash -lc '{command_string}'")
        
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        client.close()
        
        if err and not out:
            return f"Kali Error:\n{err}"
        return out if out else "Success, but no output."
        
    except Exception as e:
        return f"Python SSH Crash: {str(e)}"

@mcp.tool()
def port_scan(target: str, flags: str = "-F") -> str:
    return run_remote(f"/usr/bin/nmap {flags} {target}")

@mcp.tool()
def run_subfinder(domain: str) -> str:
    return run_remote(f"/usr/bin/subfinder -d {domain} -silent")

@mcp.tool()
def check_live_hosts(domain: str) -> str:
    if not domain.startswith("http"):
        domain = f"https://{domain}"
    return run_remote(f"/usr/bin/httpx {domain}")

@mcp.tool()
def run_terminal_command(command: str) -> str:
    """
    Executes ANY raw terminal command on the Kali Linux machine.
    Use this for running ffuf, nuclei, sqlmap, or any other pentesting tools.
    IMPORTANT: Always use fast/aggressive flags to ensure the command 
    finishes in under 50 seconds to avoid timeouts.
    """
    return run_remote(command)

if __name__ == "__main__":
    mcp.run()

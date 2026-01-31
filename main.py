import sys
import os
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from analyzer import CodeAnalyzer
import ai_agent # <--- Import our new brain

console = Console()

def main():
    # 1. Check arguments
    if len(sys.argv) < 2:
        console.print("[bold red]Error:[/bold red] Usage: python main.py [filename] [--ai]")
        return

    target_file = sys.argv[1]
    
    # Check if user wants AI help
    use_ai = "--ai" in sys.argv

    if not os.path.exists(target_file):
        console.print(f"[bold red]Error:[/bold red] File '{target_file}' not found.")
        return

    # 2. Run Static Analysis (The Math Part)
    console.print(f"[bold blue]🔍 Scanning {target_file}...[/bold blue]")
    
    analyzer = CodeAnalyzer(target_file)
    try:
        issues = analyzer.analyze()
    except SyntaxError:
        console.print("[bold red]Critical:[/bold red] Invalid Python code.")
        return

    # 3. Display Static Results
    if not issues:
        console.print(f"[bold green]✅ Clean Code![/bold green] No issues found.")
        return # No need for AI if code is clean

    # Show the table
    table = Table(title=f"Audit Report: {target_file}")
    table.add_column("Line", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Issue", style="white")

    for issue in issues:
        table.add_row(str(issue["line"]), issue["type"], issue["message"])

    console.print(table)
    console.print(f"\n[bold red]Found {len(issues)} issues.[/bold red]")

    # 4. Run AI Analysis (The Smart Part)
    if use_ai:
        console.print("\n[bold yellow]🤖 Asking Gemini for a fix...[/bold yellow]")
        
        # Read the file content to send to AI
        with open(target_file, "r", encoding="utf-8") as f:
            code_content = f.read()
            
        # Get the answer
        ai_solution = ai_agent.ask_ai_for_fix(code_content, issues)
        
        # Print it nicely using Markdown
        console.print(Markdown(ai_solution))
    
    else:
        console.print("\n[dim]Tip: Run with '--ai' to get an auto-fix suggestion.[/dim]")

if __name__ == "__main__":
    main()
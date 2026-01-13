import re
import os
from colorama import Fore, Style, init  # Fixed: Import colorama for the script to use
init(autoreset=True)

def patch_paper_trader():
    file_path = "tradingagents/paper/paper_trader.py"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found.")
        return

    with open(file_path, 'r') as f:
        content = f.read()

    # 1. Add colorama imports at the top (if not already there)
    if "from colorama import" not in content:
        content = "from colorama import Fore, Style, init\ninit(autoreset=True)\n" + content

    # 2. Replace the Header Print
    content = content.replace(
        'print("\n[Paper Trade]")',
        'print(f"\n{Fore.LIGHTCYAN_EX}[Paper Trade]{Style.RESET_ALL}")'
    )

    # 3. Replace the Snapshot Print with the Colored Block
    snapshot_print_regex = r'(\s+)print\(snapshot\)'
    
    replacement_block = r'''\1# --- COLORIZED OUTPUT ---
\1print(f"  Time:    {Fore.LIGHTBLACK_EX}" + str(snapshot['time']) + "{Style.RESET_ALL}")
\1print(f"  Price:   {Fore.WHITE}$") + str(f"{snapshot['price']:.2f}") + "{Style.RESET_ALL}")
\1
\1# Dynamic color for action
\1action_color = Fore.LIGHTGREEN_EX if action == "BUY" else (Fore.LIGHTRED_EX if action == "SELL" else Fore.LIGHTYELLOW_EX)
\1print(f"  Action:  {action_color}" + action + "{Style.RESET_ALL}")
\1
\1print(f"  Capital: {Fore.LIGHTMAGENTA_EX}$") + str(f"{snapshot['capital']:,.2f}") + "{Style.RESET_ALL}")
\1print(f"  Position:{Fore.LIGHTBLUE_EX}" + str(f"{snapshot['position']:.4f}") + " shares{Style.RESET_ALL}")
\1# -------------------------'''

    content = re.sub(snapshot_print_regex, replacement_block, content)

    with open(file_path, 'w') as f:
        f.write(content)

    print(f"✅ Patched {file_path}")

def patch_main():
    file_path = "main.py"
    
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r') as f:
        content = f.read()

    # 1. Add imports to main.py if missing
    if "from colorama import" not in content:
        content = "from colorama import Fore, Style, init\ninit(autoreset=True)\n" + content

    # 2. Replace Headers with Colored Versions
    content = re.sub(r'print\("\\n=== LIVE ANALYSIS \(AI DEBATE\) ==="\)', r'print(f"\\n{Fore.LIGHTMAGENTA_EX}=== LIVE ANALYSIS (AI DEBATE) ==={Style.RESET_ALL}")', content)
    content = re.sub(r'print\("\\n=== BACKTESTING MODE ==="\)', r'print(f"\\n{Fore.LIGHTBLUE_EX}=== BACKTESTING MODE ==={Style.RESET_ALL}")', content)
    content = re.sub(r'print\("\\n=== PAPER TRADING MODE ==="\)', r'print(f"\\n{Fore.LIGHTCYAN_EX}=== PAPER TRADING MODE ==={Style.RESET_ALL}")', content)

    with open(file_path, 'w') as f:
        f.write(content)
        
    print(f"✅ Patched {file_path}")

if __name__ == "__main__":
    print("🎨 Applying colors...")
    patch_paper_trader()
    patch_main()
    print("✨ Done! You can now run 'python main.py'")
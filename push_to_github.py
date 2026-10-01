"""
TRUTHSCAN Git Push Utility
Pushes all committed project files to https://github.com/UNKNOWN13546/TRUTHSCAN.git
"""
import sys
import os
import webbrowser
import dulwich.porcelain as porcelain

TOKEN_GEN_URL = "https://github.com/settings/tokens/new?scopes=repo&description=TRUTHSCAN"

def clean_token(token: str) -> str:
    token = token.strip()
    if token.startswith('<') and token.endswith('>'):
        token = token[1:-1].strip()
    token = token.strip('"\'')
    return token

def prompt_for_token() -> str:
    while True:
        print("\n-------------------------------------------------------------")
        print("Please enter your GitHub Personal Access Token (starts with 'ghp_'):")
        print("1. If you don't have one, press 'O' to automatically OPEN the GitHub token creation page.")
        print("2. Or paste your token below and press Enter.")
        print("-------------------------------------------------------------")
        
        user_input = input("Enter Token (or 'O' to open browser): ").strip()
        
        if not user_input:
            print("[!] Token cannot be empty. Please try again.")
            continue
            
        if user_input.lower() == 'o':
            print(f"\nOpening {TOKEN_GEN_URL} in your browser...")
            webbrowser.open(TOKEN_GEN_URL)
            print("Steps in browser:")
            print("  1. The page is pre-configured with note 'TRUTHSCAN' and 'repo' checked.")
            print("  2. Scroll down and click the green 'Generate token' button.")
            print("  3. Copy the token (starts with ghp_...) and paste it here.")
            continue
            
        cleaned = clean_token(user_input)
        
        # Check if user accidentally pasted the URL instead of the token
        if cleaned.startswith("http://") or cleaned.startswith("https://") or "github.com" in cleaned:
            print("\n[!] ATTENTION: You entered the web link (URL), NOT your token!")
            print("    A GitHub token is a secret password key that starts with: ghp_...")
            print("    Opening token creation page now...")
            webbrowser.open(TOKEN_GEN_URL)
            continue
            
        return cleaned

def push_repo(token: str) -> bool:
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\n[1/3] Target repository: https://github.com/UNKNOWN13546/TRUTHSCAN.git")
    print(f"[2/3] Local directory:   {repo_dir}")
    print(f"[3/3] Authenticating and pushing branch 'main' to GitHub...")

    remote_url = f"https://{token}@github.com/UNKNOWN13546/TRUTHSCAN.git"
    
    try:
        porcelain.push(repo_dir, remote_url, 'refs/heads/main')
        print("\n===========================================================")
        print(" SUCCESS! ALL FILES SUCCESSFULLY PUSHED TO GITHUB!")
        print("===========================================================")
        print("Repository URL: https://github.com/UNKNOWN13546/TRUTHSCAN")
        print("Branch:         main")
        print("Status:         Up to date with all Modules & Forensic Tools")
        print("===========================================================\n")
        return True
    except Exception as e:
        err_msg = str(e)
        print(f"\n[ERROR] Push failed: {err_msg}")
        print("\nTroubleshooting:")
        print("1. Ensure your token has the 'repo' permission checked.")
        print("2. Ensure your token has not expired.")
        print("3. Try generating a new token at: " + TOKEN_GEN_URL)
        return False

if __name__ == '__main__':
    print("=" * 60)
    print(" TRUTHSCAN GITHUB PUSH WIZARD")
    print(" Target: https://github.com/UNKNOWN13546/TRUTHSCAN.git")
    print("=" * 60)

    token = None
    if len(sys.argv) > 1:
        arg_token = sys.argv[1].strip()
        if not (arg_token.startswith("http://") or arg_token.startswith("https://") or "github.com" in arg_token):
            token = clean_token(arg_token)

    if not token:
        token = prompt_for_token()

    success = push_repo(token)
    
    if sys.platform == "win32":
        try:
            input("Press Enter to close this window...")
        except Exception:
            pass

"""
TRUTHSCAN Git Push Utility
Pushes all committed project files to https://github.com/UNKNOWN13546/TRUTHSCAN.git
"""
import sys
import os
import dulwich.porcelain as porcelain

def clean_token(token: str) -> str:
    token = token.strip()
    # Strip accidental angle brackets if the user typed <token>
    if token.startswith('<') and token.endswith('>'):
        token = token[1:-1].strip()
    # Strip quotes if copied with quotes
    token = token.strip('"\'')
    return token

def push_repo(token: str):
    token = clean_token(token)
    if not token:
        print("[ERROR] Token cannot be empty.")
        return False

    repo_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\n[1/3] Repository root: {repo_dir}")
    print(f"[2/3] Authenticating with GitHub repository...")

    remote_url = f"https://{token}@github.com/UNKNOWN13546/TRUTHSCAN.git"
    
    try:
        porcelain.push(repo_dir, remote_url, 'refs/heads/main')
        print("\n===========================================================")
        print(" SUCCESS! ALL FILES SUCCESSFULLY PUSHED TO GITHUB!")
        print("===========================================================")
        print("Repository: https://github.com/UNKNOWN13546/TRUTHSCAN")
        print("Branch:     main")
        print("===========================================================\n")
        return True
    except Exception as e:
        err_msg = str(e)
        print(f"\n[ERROR] Push failed: {err_msg}")
        if "Authentication failed" in err_msg or "403" in err_msg or "401" in err_msg:
            print("\nTroubleshooting GitHub Authentication:")
            print("1. Go to: https://github.com/settings/tokens")
            print("2. Generate a 'Personal Access Token (Classic)' or 'Fine-grained token'")
            print("3. Check 'repo' scope (Full control of private repositories) or 'Contents: Read and write'")
            print("4. Copy the token (starts with ghp_ or github_pat_) and try again.")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print(" TRUTHSCAN GITHUB PUSH WIZARD")
    print(" Target: https://github.com/UNKNOWN13546/TRUTHSCAN.git")
    print("=" * 60)

    token = None
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        print("\nPlease paste your GitHub Personal Access Token below.")
        print("(It usually starts with 'ghp_' or 'github_pat_')")
        print("If you do not have one yet, create it here: https://github.com/settings/tokens\n")
        try:
            token = input("GitHub Token: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            sys.exit(0)

    success = push_repo(token)
    if not success and sys.platform == "win32":
        # Keep open if launched via double-click
        try:
            input("\nPress Enter to exit...")
        except Exception:
            pass

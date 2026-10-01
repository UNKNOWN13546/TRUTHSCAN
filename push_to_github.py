"""
TRUTHSCAN Git Push Utility
Pushes all committed project files to https://github.com/UNKNOWN13546/TRUTHSCAN.git
Usage:
    python push_to_github.py <YOUR_GITHUB_TOKEN>
"""
import sys
import dulwich.porcelain as porcelain

def push_repo(token: str):
    repo_path = r'.'
    remote_url = f"https://{token}@github.com/UNKNOWN13546/TRUTHSCAN.git"
    print(f"Connecting to https://github.com/UNKNOWN13546/TRUTHSCAN.git ...")
    try:
        porcelain.push(repo_path, remote_url, 'refs/heads/main')
        print("\nSUCCESS! All files successfully pushed to https://github.com/UNKNOWN13546/TRUTHSCAN.git")
        print("Branch: main")
        print("View repository: https://github.com/UNKNOWN13546/TRUTHSCAN")
    except Exception as e:
        print(f"\nPush failed: {e}")
        print("Ensure your token has 'repo' / 'contents: write' permission.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python push_to_github.py <YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>")
        sys.exit(1)
    push_repo(sys.argv[1].strip())

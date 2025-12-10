import argparse
import os
import shutil

from file_manage import discover_files

PUBLIC_PATH = "./public"


def main():
    parser = argparse.ArgumentParser(description="A simple static web server generator")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    print(f"❌ Deleting {PUBLIC_PATH} folder")
    if not args.dry_run:
        shutil.rmtree(PUBLIC_PATH)

    print("📁 Discovering static files")
    files = discover_files("./static")
    if args.verbose:
        for f in files:
            print(f" -- discovered path: {f}")

    print("⚡️ Creating directories")
    if not args.dry_run:
        os.mkdir(PUBLIC_PATH)

    for path in files:
        if path.startswith("./static"):
            dest_path = path[len("./static") :].lstrip("/")
            dest_path = os.path.join(PUBLIC_PATH, dest_path)

            dest_dir = os.path.dirname(dest_path)
            if args.verbose:
                print(f" -- creating dir {dest_dir}")

            if not args.dry_run:
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)

            if args.verbose:
                print(f"💾 Copy from {path} to {dest_path}")

            if not args.dry_run:
                shutil.copy2(path, dest_path)


if __name__ == "__main__":
    main()

import importlib
import os


__version__ = '1.0.0'

def get_module(module_name: str) -> importlib.import_module:
    return importlib.import_module(module_name)


def feed_thread(modules_dir_name: str, source: str) -> None:
    print(f"[+] Starting module: {source}")
    feed = get_module(f"{modules_dir_name}.{source}").Feed()
    feed.get_enriched_urls()
    print(f"[+] Stopping module: {source}")


if __name__ == '__main__':
    modules_dir_name = 'feed_modules'

    for file_name in os.listdir(os.path.join(os.path.dirname(__file__), modules_dir_name)):
        if file_name in ['__init__.py', 'core.py'] or file_name[-3:] != '.py' or len(file_name) <= 3:
            continue

        source = file_name[:-3]
        feed_thread(modules_dir_name, source)

    
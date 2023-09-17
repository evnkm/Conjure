import pathlib
import modal

stub = modal.Stub()
stub.volume = modal.Volume.new()

p = pathlib.Path("/root/foo/bar.txt")

@stub.function(volumes={"/root/foo": stub.volume})
def f():
    p.write_text("hello")
    print(f"Created {p=}")
    stub.volume.commit()  # Persist changes
    print(f"Committed {p=}")

@stub.function(volumes={"/root/foo": stub.volume})
def g(reload: bool = False):
    if reload:
        stub.volume.reload()  # Fetch latest changes
    if p.exists():
        print(f"{p=} contains '{p.read_text()}'")
    else:
        print(f"{p=} does not exist!")

@stub.local_entrypoint()
def main():
    g.remote()  # 1. container for `g` starts
    f.remote()  # 2. container for `f` starts, commits file
    g.remote(reload=False)  # 3. reuses container for `g`, no reload
    g.remote(reload=True)   # 4. reuses container, but reloads to see file.
from modal import Image, Stub, Volume
import pathlib

stub = Stub("initial-container-test")
stub.volume = Volume.persisted("model-store")
# stub.volume = modal.Volume.new()
model_store_path = "/root/models"

p = pathlib.Path("/root/foo/bar.txt")


llava_image = Image.debian_slim(python_version="3.10").run_commands(
    "git clone https://github.com/evnkm/LLaVA.git",
    "cd LLaVA",
    "conda create -n llava python=3.10 -y",
    "conda activate llava",
    "pip install --upgrade pip",
    "pip install -e .",
)


@stub.function(image=llava_image, gpu="any")
async def generate_text_from_llava(img_path: str, prompt: str):
    '''
    Input image path and prompt, output text caption of image
    '''

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
    g.call()  # 1. container for `g` starts
    f.call()  # 2. container for `f` starts, commits file
    g.call(reload=False)  # 3. reuses container for `g`, no reload
    g.call(reload=True)   # 4. reuses container, but reloads to see file.

# -----------------------

# @stub.function(volumes={model_store_path: stub.volume}, gpu="any")
# def run_training():
#     model = train(...)
#     save(model_store_path, model)
#     stub.volume.commit()  # Persist changes
#
# @stub.function(volumes={model_store_path: stub.volume})
# def inference(model_id: str, request):
#     try:
#         model = load_model(model_store_path, model_id)
#     except NotFound:
#         stub.volume.reload()  # Fetch latest changes
#         model = load_model(model_store_path, model_id)
#     return model.run(request)
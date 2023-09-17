import subprocess
from pathlib import Path

from modal import Image, Mount, Secret, Stub, asgi_app, gpu, method

GPU_CONFIG = gpu.A100(memory=80, count=2)
MODEL_ID = "meta-llama/Llama-2-70b-chat-hf"

LAUNCH_FLAGS = ["--model-id", MODEL_ID, "--port", "8000"]

def download_model(): 
    subprocess.run(["text-generation-server", "download-weights", MODEL_ID])

image = (
    Image.from_registry("ghcr.io/huggingface/text-generation-inference:1.0.3")
    .dockerfile_commands("ENTRYPOINT []")
    .run_function(download_model, secret=Secret.from_name("my-huggingface-secret"))
    .pip_install("text-generation")
)

stub = Stub("tgi-" + MODEL_ID.split("/")[-1], image=image) # tgi-Llama-2-70b-chat-hf

@stub.cls(
    secret=Secret.from_name("my-huggingface-secret"),
    gpu=GPU_CONFIG,
    allow_concurrent_inputs=10,
    container_idle_timeout=60 * 20,
    timeout=60 * 60,
)
class Model:
    def __enter__(self):
        import socket
        import subprocess
        import time

        from text_generation import AsyncClient

        self.launcher = subprocess.Popen(
            ["text-generation-launcher"] + LAUNCH_FLAGS
        )
        self.client = AsyncClient("http://127.0.0.1:8000", timeout=60)
        self.template = """<s>[INST] <<SYS>>
{system}
<</SYS>>

{user} [/INST] """

        # Poll until webserver at 127.0.0.1:8000 accepts connections before running inputs.
        def webserver_ready():
            try:
                socket.create_connection(("127.0.0.1", 8000), timeout=1).close()
                return True
            except (socket.timeout, ConnectionRefusedError):
                return False

        while not webserver_ready():
            time.sleep(1.0)

        print("Webserver ready!")

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.launcher.terminate()

    @method()
    async def generate(self, question: str):
        prompt = self.template.format(system="", user=question)
        result = await self.client.generate(prompt, max_new_tokens=1024)

        return result.generated_text

    @method()
    async def generate_stream(self, question: str):
        prompt = self.template.format(system="", user=question)

        async for response in self.client.generate_stream(
            prompt, max_new_tokens=1024
        ):
            if not response.token.special:
                yield response.token.text

# @stub.local_entrypoint()
# def main():
#     print(
#         Model().generate.remote(
#             "Implement a Python function to compute the Fibonacci numbers."
#         )
#     )
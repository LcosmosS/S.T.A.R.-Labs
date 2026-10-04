import subprocess
import shutil

def blender_render(script_text, output_path="figures/blender_render.png"):
    blender = shutil.which("blender")
    if blender is None:
        print("Blender not found — skipping render.")
        return

    script_file = "blender_temp.py"
    with open(script_file, "w") as f:
        f.write(script_text)

    cmd = [blender, "--background", "--python", script_file]
    subprocess.run(cmd)
    print("Blender render complete:", output_path)

##one objcet
import json
import subprocess
import json
with open("objaverse_data/properties.json", 'r') as f:
    properties = json.load(f)
shapes=list(properties["shapes"].keys())
shapes=["zebra"]
for shape in shapes:
    arg_shapes=shape
    arg_scales="1.3 1.3"
    command="../blender-4.1.1-linux-x64/blender --background  --python render_objaverse.py -- --use_gpu 1  --objects %s\
        --robjects 0,0,0 --sobjects %s --objs_config objaverse_data/OneObject.json \
        --width 1024 --height 1024 --output_image_dir ../output/CoCo-OneObject/" % (arg_shapes,arg_scales)
    command=list(filter(None,command.split(" ")))
    new_command=command[:5]
    new_command=" ".join(command)
    print(new_command)
    subprocess.run(["bash","-c",new_command],check=False,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
    )
            

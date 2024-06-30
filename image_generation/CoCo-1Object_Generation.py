##one objcet
import json
import subprocess
import json
with open("objaverse_data/properties.json", 'r') as f:
    properties = json.load(f)
shapes=list(properties["shapes"].keys())
flat_shapes=["axe","banana","bed","clock","donut","fork","keyboard",
"knife","sink","mouse","skateboard","remote","scissors",
"pizza","plate","toilet","spoon","ski","snowboard"]
lean_shapes=["cup","hat","laptop","suitcase"]
shapes=["zebra","cup","mouse"]
for shape in shapes:
    arg_shapes=shape
    arg_scales="1.3 1.3"
    rotate1="270,0,0"
    
    rotate1="270,0,0"
    if shape in flat_shapes:
        rotate1="0,0,0"
    if shape in lean_shapes:
        rotate1="300,0,0"
    command="../blender-4.1.1-linux-x64/blender --background  --python render_objaverse.py -- --use_gpu 1  --objects %s\
        --robjects %s --sobjects %s --objs_config objaverse_data/OneObject.json \
        --width 512 --height 512 --cam_x 0 --cam_y 0 --cam_z 12 --output_image_dir ../output/CoCo-OneObject/" % (arg_shapes,rotate1,arg_scales)
    command=list(filter(None,command.split(" ")))
    new_command=command[:5]
    new_command=" ".join(command)
    print(new_command)
    subprocess.run(["bash","-c",new_command],check=False,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
    )
            

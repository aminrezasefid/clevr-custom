##two objcet same color different size
import json
import subprocess
import json
with open("data/properties.json", 'r') as f:
    properties = json.load(f)
shapes=list(properties["shapes"].keys())
shapes.remove("cap")
shapes.remove("snowflake")
shapes.remove("mug")
colors=list(properties["colors"].keys())
shapes=["cone","pyramid"]
for shape1 in shapes:
    for shape2 in shapes:
        if shape1==shape2:
            continue
        for color1 in colors:
            for color2 in colors:
                if color2==color1:
                    continue
                arg_shapes=shape1+" "+shape2
                arg_colors=color1+" "+color2
                arg_scales="1 1"
                command="../blender-4.1.1-linux-x64/blender --background  --python render_images_custom.py -- --use_gpu 1  --objects %s\
                    --cobjects %s --robjects 0 0 --sobjects %s --objs_config data/TwoObjectSameColor.json  --num_images 1\
                    --margin 0.01 --width 1024 --height 1024 --output_image_dir ../output/Two-Object-Diff-Color-Same-Size/" % (arg_shapes,arg_colors,arg_scales)
                command=list(filter(None,command.split(" ")))
                new_command=command[:5]
                new_command=" ".join(command)
                print(new_command)
                subprocess.run(["bash","-c",new_command],check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
            

##one objcet
import json
import subprocess
import json
with open("objaverse_data/properties.json", 'r') as f:
    properties = json.load(f)
with open("CoCo_Configs/Scales.json") as f:
    scales=json.load(f)
shapes=list(properties["shapes"].keys())
shapes=["zebra","boat","car"]
for shape1 in shapes:
    for shape2 in shapes:
        for shape3 in shapes:
            if shape1==shape2 or shape1==shape3 or shape2==shape3:
                continue
            arg_shapes=shape1+" "+shape2+" "+shape3
            scale1=1.3
            scale2=1.3
            scale3=1.3
            if shape1 in scales.keys():
                scale1*=scales[shape1]
            if shape2 in scales.keys():
                scale2*= scales[shape2]
            if shape3 in scales.keys():
                scale3*=scales[shape3]
            arg_scales="%f %f %f" % (scale1,scale2,scale3)
            command="../blender-4.1.1-linux-x64/blender --background  --python render_objaverse.py -- --use_gpu 1  --objects %s\
                --robjects 0,0,0 0,0,0 0,0,0 --sobjects %s --objs_config CoCo_Configs/ThreeObjectSameSize.json \
                --width 512 --height 512 --output_image_dir ../output/CoCo-ThreeObjectSameSize/" % (arg_shapes,arg_scales)
            command=list(filter(None,command.split(" ")))
            new_command=command[:5]
            new_command=" ".join(command)
            print(new_command)
            subprocess.run(["bash","-c",new_command],check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            )
            

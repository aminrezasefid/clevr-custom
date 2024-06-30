##one objcet
import json
import subprocess
import json
with open("objaverse_data/properties.json", 'r') as f:
    properties = json.load(f)
with open("CoCo_Configs/Scales.json") as f:
    scales=json.load(f)
shapes=list(properties["shapes"].keys())
shapes=["cup","clock","banana"]
flat_shapes=["axe","banana","bed","clock","donut","fork","keyboard",
"knife","sink","mouse","skateboard","remote","scissors",
"pizza","plate","toilet","spoon","ski","snowboard"]
lean_shapes=["cup","hat","laptop","suitcase"]
for shape1 in shapes:
    for shape2 in shapes:
        for shape3 in shapes:
            if shape1==shape2 or shape1==shape3 or shape2==shape3:
                continue
            arg_shapes=shape1+" "+shape2+" "+shape3
            scale1=1.3
            scale2=1.3
            scale3=1.3
            
            rotate1="270,0,0"
            rotate2="270,0,0"
            rotate3="270,0,0"
            if shape1 in flat_shapes:
                rotate1="0,0,0"
            if shape2 in flat_shapes:
                rotate2="0,0,0"
            if shape3 in flat_shapes:
                rotate3="0,0,0"
            
            if shape1 in lean_shapes:
                rotate1="300,0,0"
            if shape2 in lean_shapes:
                rotate2="300,0,0"
            if shape3 in lean_shapes:
                rotate3="300,0,0"



            if shape1 in scales.keys():
                scale1*=scales[shape1]
            if shape2 in scales.keys():
                scale2*= scales[shape2]
            if shape3 in scales.keys():
                scale3*=scales[shape3]
            arg_scales="%f %f %f" % (scale1,scale2,scale3)
            command="../blender-4.1.1-linux-x64/blender --background  --python render_objaverse.py -- --use_gpu 1  --objects %s\
                --robjects %s %s %s --sobjects %s --objs_config CoCo_Configs/ThreeObjectSameSize.json \
                --width 512 --height 512 --cam_x 0 --cam_y 0 --cam_z 12 --output_image_dir ../output/CoCo-ThreeObjectSameSize/" % (arg_shapes,rotate1,rotate2,rotate3,arg_scales)
            command=list(filter(None,command.split(" ")))
            new_command=command[:5]
            new_command=" ".join(command)
            print(new_command)
            subprocess.run(["bash","-c",new_command],check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
            )
            

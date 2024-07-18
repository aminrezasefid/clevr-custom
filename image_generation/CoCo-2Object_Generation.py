##one objcet
import json
import subprocess
import json
import json
import subprocess
with open("CoCo_Configs/properties.json", 'r') as f:
    properties = json.load(f)
with open("CoCo_Configs/Scales.json") as f:
    scales=json.load(f)
shapes=list(properties["shapes"].keys())
#shapes=["cup","clock","banana"]
flat_shapes=["axe","banana","bed","clock","donut","fork","keyboard",
"knife","sink","mouse","skateboard","remote","scissors",
"pizza","plate","toilet","spoon","ski","snowboard"]
lean_shapes=["cup","hat","laptop","suitcase"]

config_file="TwoObjectLB.json"
output_folder="CoCo-TwoObject-LBig"
for shape1 in shapes:
    for shape2 in shapes:
        if shape1==shape2:
                continue
        arg_shapes=shape1+" "+shape2
        scale1=2.5
        scale2=0.8
        
        rotate1="270,0,0"
        rotate2="270,0,0"
        if shape1 in flat_shapes:
            rotate1="0,0,0"
        if shape2 in flat_shapes:
            rotate2="0,0,0"
        
        if shape1 in lean_shapes:
            rotate1="300,0,0"
        if shape2 in lean_shapes:
            rotate2="300,0,0"

        if shape1 in scales.keys():
            scale1*=scales[shape1]
        if shape2 in scales.keys():
            scale2*= scales[shape2]
        
        arg_scales="%f %f" % (scale1,scale2)
        command=f"../blender-4.1.1-linux-x64/blender --background  --python render_objaverse.py -- --use_gpu 1  --objects %s\
            --robjects %s %s --sobjects %s --objs_config CoCo_Configs/{config_file} \
            --width 512 --height 512 --cam_x 0 --cam_y 0 --cam_z 15 --output_image_dir ../output/{output_folder}/" % (arg_shapes,rotate1,rotate2,arg_scales)
        command=list(filter(None,command.split(" ")))
        new_command=command[:5]
        new_command=" ".join(command)
        print(new_command)
        subprocess.run(["bash","-c",new_command],check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
        )
            

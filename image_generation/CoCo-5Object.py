import pandas as pd
import subprocess
import json
import random
import os
random.seed(42)


with open("CoCo_Configs/properties.json", 'r') as f:
    properties = json.load(f)
with open("CoCo_Configs/Scales.json") as f:
    scales=json.load(f)


flat_shapes=["axe","banana","bed","clock","donut","fork","keyboard",
"knife","sink","mouse","skateboard","remote","scissors",
"pizza","plate","toilet","spoon","ski","snowboard"]
lean_shapes=["cup","hat","laptop","suitcase"]

config_file="FiveObjectM.json"
output_folder="CoCo-FiveObject"
created_list=[]
created_count=0
if os.path.exists(f"../output/{output_folder}"):
    files=os.listdir(f"../output/{output_folder}")
    for file in files:
        f=" ".join(file.split(".")[0].split("_"))
        created_list.append(f)
    created_count=len(created_list)

n_to_gen=8000-created_count
arg_shape_set=set()
shapes=list(properties["shapes"].keys())
arg_shape_list=[]
for _ in range(n_to_gen):
    scales_list=[1.3,1.3,1.3,1.3,1.3]
    rotates_list=["270,0,0","270,0,0","270,0,0","270,0,0","270,0,0"]
    while True:
        shape_list=random.sample(shapes,5)
        arg_shape=f"{shape_list[0]} {shape_list[1]} {shape_list[2]} {shape_list[3]} {shape_list[4]}"
        if arg_shape in created_list: continue
        if arg_shape not in arg_shape_list:
            arg_shape_list.append(arg_shape)
            break
    for i,shape in enumerate(shape_list):
        if shape in flat_shapes:
            rotates_list[i]="0,0,0"
        if shape in lean_shapes:
            rotates_list[i]="300,0,0"
        if shape in scales.keys():
            scales_list[i]*=scales[shape]
    arg_scales="%f %f %f %f %f" % (tuple(scales_list))
    arg_rotates="%s %s %s %s %s" % (tuple(rotates_list))
    command=f"../blender-4.1.1-linux-x64/blender --background  --python render_objaverse.py -- --use_gpu 1  --objects %s\
        --robjects %s --sobjects %s --objs_config CoCo_Configs/{config_file} \
        --width 512 --height 512 --cam_x 0 --cam_y 0 --cam_z 15 --output_image_dir ../output/{output_folder}/" % (arg_shape,arg_rotates,arg_scales)
    command=list(filter(None,command.split(" ")))
    new_command=command[:5]
    new_command=" ".join(command)
    print(new_command)
    subprocess.run(["bash","-c",new_command],check=False,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
    )
#4 object
import pandas as pd
import subprocess
import json
import random
random.seed(42)
object_name_file="CoCo-4Object-Names.csv"
remainder_name_file="CoCo-4Object-Names-remainder.csv"

df=pd.read_csv(object_name_file)

idx_list=random.sample(range(len(df)),8000)

shape_names=df.iloc[idx_list]["ObjectNames"]
df.drop(idx_list).to_csv(remainder_name_file,index=False)
with open("CoCo_Configs/properties.json", 'r') as f:
    properties = json.load(f)
with open("CoCo_Configs/Scales.json") as f:
    scales=json.load(f)
shapes=list(properties["shapes"].keys())
shapes=["cup","clock","banana"]
flat_shapes=["axe","banana","bed","clock","donut","fork","keyboard",
"knife","sink","mouse","skateboard","remote","scissors",
"pizza","plate","toilet","spoon","ski","snowboard"]
lean_shapes=["cup","hat","laptop","suitcase"]

config_file="FourObjectDL.json"
output_folder="CoCo-FourObject-DLBig"

for line in shape_names:
    print(line.split("\n")[0])
    shape1,shape2,shape3,shape4=line.split("\n")[0].split(" ")
    arg_shapes=shape1+" "+shape2+" "+shape3+" "+shape4
    scale1=0.73
    scale2=0.73
    scale3=0.73
    scale4=2.3

    rotate1="270,0,0"
    rotate2="270,0,0"
    rotate3="270,0,0"
    rotate4="270,0,0"

    if shape1 in flat_shapes:
        rotate1="0,0,0"
    if shape2 in flat_shapes:
        rotate2="0,0,0"
    if shape3 in flat_shapes:
        rotate3="0,0,0"
    if shape4 in flat_shapes:
        rotate4="0,0,0"

    if shape1 in lean_shapes:
        rotate1="300,0,0"
    if shape2 in lean_shapes:
        rotate2="300,0,0"
    if shape3 in lean_shapes:
        rotate3="300,0,0"
    if shape4 in lean_shapes:
        rotate4="300,0,0"

    if shape1 in scales.keys():
        scale1*=scales[shape1]
    if shape2 in scales.keys():
        scale2*= scales[shape2]
    if shape3 in scales.keys():
        scale3*= scales[shape3]
    if shape4 in scales.keys():
        scale4*= scales[shape4]

    arg_scales="%f %f %f %f" % (scale1,scale2,scale3,scale4)
    command=f"../blender-4.1.1-linux-x64/blender --background  --python render_objaverse.py -- --use_gpu 1  --objects %s\
        --robjects %s %s %s %s --sobjects %s --objs_config CoCo_Configs/{config_file} \
        --width 512 --height 512 --cam_x 0 --cam_y 0 --cam_z 15 --output_image_dir ../output/{output_folder}/" % (arg_shapes,rotate1,rotate2,rotate3,rotate4,arg_scales)
    command=list(filter(None,command.split(" ")))
    new_command=command[:5]
    new_command=" ".join(command)
    print(new_command)
    subprocess.run(["bash","-c",new_command],check=False,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
    )

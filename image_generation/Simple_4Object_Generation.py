##two objcet same color different size
import json
import subprocess
import json


##four objcet same color different size
import pandas as pd
import json
import random
random.seed(42)
idx_list=random.sample(range(73440),8000)
df=pd.read_csv("4Object_Names.csv")
shame_names=df.iloc[idx_list]["Shapes"]
df.drop(idx_list).to_csv("4Object_Names_Remainder.csv",index=False)
for line in shame_names:
    color="blue"
    arg_shapes=line.split("\n")[0]
    arg_colors=color+" "+color+" "+color+" "+color
    arg_scales="1 1 1 1"
    command="../blender-4.1.1-linux-x64/blender --background  --python render_images_custom.py -- --use_gpu 1  --objects %s --cobjects %s\
        --robjects 0 0 0 0 --sobjects %s --objs_config data/FourObjectSameColorSameSize.json  --num_images 1\
        --margin 0.01 --width 1024 --height 1024 --output_image_dir ../output/Four-Object-SameColor-SameSize/"  % (arg_shapes,arg_colors,arg_scales)
    command=list(filter(None,command.split(" ")))
    new_command=command[:5]
    new_command=" ".join(command)
    print(new_command)
    subprocess.run(["bash","-c",new_command],check=False,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)


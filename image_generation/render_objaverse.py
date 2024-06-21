# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from __future__ import print_function
import math, sys, random, argparse, json, os, tempfile
from datetime import datetime as dt
from collections import Counter
"""
Renders random scenes using Blender, each with with a random number of objects;
each object has a random size, position, color, and shape. Objects will be
nonintersecting but may partially occlude each other. Output images will be
written to disk as PNGs, and we will also write a JSON file for each image with
ground-truth scene information.

This file expects to be run from Blender like this:

blender --background --python render_images.py -- [arguments to this script]
"""

INSIDE_BLENDER = True
try:
  import bpy, bpy_extras
  from mathutils import Vector
except ImportError as e:
  INSIDE_BLENDER = False
if INSIDE_BLENDER:
  try:
    import utils
  except ImportError as e:
    print("\nERROR")
    print("Running render_images.py from Blender and cannot import utils.py.") 
    print("You may need to add a .pth file to the site-packages of Blender's")
    print("bundled python with a command like this:\n")
    print("echo $PWD >> $BLENDER/$VERSION/python/lib/python3.5/site-packages/clevr.pth")
    print("\nWhere $BLENDER is the directory where Blender is installed, and")
    print("$VERSION is your Blender version (such as 2.78).")
    sys.exit(1)

parser = argparse.ArgumentParser()

# Input options
parser.add_argument('--base_scene_blendfile', default='data/base_scene.blend',
    help="Base blender file on which all scenes are based; includes " +
          "ground plane, lights, and camera.")
parser.add_argument('--properties_json', default='objaverse_data/properties.json',
    help="JSON file defining objects, materials, sizes, and colors. " +
         "The \"colors\" field maps from CLEVR color names to RGB values; " +
         "The \"sizes\" field maps from CLEVR size names to scalars used to " +
         "rescale object models; the \"materials\" and \"shapes\" fields map " +
         "from CLEVR material and shape names to .blend files in the " +
         "--object_material_dir and --shape_dir directories respectively.")
parser.add_argument('--shape_dir', default='objaverse_data/',
    help="Directory where .blend files for object models are stored")
# parser.add_argument('--material_dir', default='data/materials',
#     help="Directory where .blend files for materials are stored")
# parser.add_argument('--shape_color_combos_json', default=None,
#     help="Optional path to a JSON file mapping shape names to a list of " +
#          "allowed color names for that shape. This allows rendering images " +
#          "for CLEVR-CoGenT.")
def coords(s):
    try:
        x, y = map(int, s.split(','))
        return x, y
    except:
        raise argparse.ArgumentTypeError("Coordinates must be x,y,z")
# Settings for objects
parser.add_argument('--objects',nargs="+",default=["circle"],type=str,help="Types of objects in order")
parser.add_argument('--sobjects',nargs="+",default=[0],type=float,help="Scale of objects in order")

parser.add_argument('--locobjects',nargs="+",default=[(0,0)],type=coords,help="Location of objects in order")

parser.add_argument('--objs_config',help="config file for object generation")

# parser.add_argument('--min_dist', default=0.25, type=float,
#     help="The minimum allowed distance between object centers")
# parser.add_argument('--margin', default=0.4, type=float,
#     help="Along all cardinal directions (left, right, front, back), all " +
#          "objects will be at least this distance apart. This makes resolving " +
#          "spatial relationships slightly less ambiguous.")
# parser.add_argument('--min_pixels_per_object', default=200, type=int,
#     help="All objects will have at least this many visible pixels in the " +
#          "final rendered images; this ensures that no objects are fully " +
#          "occluded by other objects.")
# parser.add_argument('--max_retries', default=50, type=int,
#     help="The number of times to try placing an object before giving up and " +
#          "re-placing all objects in the scene.")

# Output settings
# parser.add_argument('--start_idx', default=0, type=int,
#     help="The index at which to start for numbering rendered images. Setting " +
#          "this to non-zero values allows you to distribute rendering across " +
#          "multiple machines and recombine the results later.")
# parser.add_argument('--num_images', default=5, type=int,
#     help="The number of images to render")
# parser.add_argument('--filename_prefix', default='CLEVR',
#     help="This prefix will be prepended to the rendered images and JSON scenes")
# parser.add_argument('--split', default='new',
#     help="Name of the split for which we are rendering. This will be added to " +
#          "the names of rendered images, and will also be stored in the JSON " +
#          "scene structure for each image.")
parser.add_argument('--output_image_dir', default='../output/images/',
    help="The directory where output images will be stored. It will be " +
         "created if it does not exist.")
# parser.add_argument('--output_scene_dir', default='../output/scenes/',
#     help="The directory where output JSON scene structures will be stored. " +
#          "It will be created if it does not exist.")
# parser.add_argument('--output_scene_file', default='../output/CLEVR_scenes.json',
#     help="Path to write a single JSON file containing all scene information")
# parser.add_argument('--output_blend_dir', default='output/blendfiles',
#     help="The directory where blender scene files will be stored, if the " +
#          "user requested that these files be saved using the " +
#          "--save_blendfiles flag; in this case it will be created if it does " +
#          "not already exist.")
# parser.add_argument('--save_blendfiles', type=int, default=0,
#     help="Setting --save_blendfiles 1 will cause the blender scene file for " +
#          "each generated image to be stored in the directory specified by " +
#          "the --output_blend_dir flag. These files are not saved by default " +
#          "because they take up ~5-10MB each.")
parser.add_argument('--version', default='1.0',
    help="String to store in the \"version\" field of the generated JSON file")
parser.add_argument('--license',
    default="Creative Commons Attribution (CC-BY 4.0)",
    help="String to store in the \"license\" field of the generated JSON file")
parser.add_argument('--date', default=dt.today().strftime("%m/%d/%Y"),
    help="String to store in the \"date\" field of the generated JSON file; " +
         "defaults to today's date")

# Rendering options
parser.add_argument('--cam_x', default=0.0, type=float, help="camera x pos")
parser.add_argument('--cam_y', default=-7.0, type=float, help="camera y pos")
parser.add_argument('--cam_z', default=10, type=float, help="camera z pos")
parser.add_argument('--use_gpu', default=0, type=int,
    help="Setting --use_gpu 1 enables GPU-accelerated rendering using CUDA. " +
         "You must have an NVIDIA GPU with the CUDA toolkit installed for " +
         "to work.")
parser.add_argument('--width', default=320, type=int,
    help="The width (in pixels) for the rendered images")
parser.add_argument('--height', default=320, type=int,
    help="The height (in pixels) for the rendered images")
# parser.add_argument('--key_light_jitter', default=1.0, type=float,
#     help="The magnitude of random jitter to add to the key light position.")
# parser.add_argument('--fill_light_jitter', default=1.0, type=float,
#     help="The magnitude of random jitter to add to the fill light position.")
# parser.add_argument('--back_light_jitter', default=1.0, type=float,
#     help="The magnitude of random jitter to add to the back light position.")
# parser.add_argument('--camera_jitter', default=0.5, type=float,
#     help="The magnitude of random jitter to add to the camera position")
parser.add_argument('--render_num_samples', default=512, type=int,
    help="The number of samples to use when rendering. Larger values will " +
         "result in nicer images but will cause rendering to take longer.")
parser.add_argument('--render_min_bounces', default=8, type=int,
    help="The minimum number of bounces to use for rendering.")
parser.add_argument('--render_max_bounces', default=8, type=int,
    help="The maximum number of bounces to use for rendering.")
parser.add_argument('--render_tile_size', default=256, type=int,
    help="The tile size to use for rendering. This should not affect the " +
         "quality of the rendered image but may affect the speed; CPU-based " +
         "rendering may achieve better performance using smaller tile sizes " +
         "while larger tile sizes may be optimal for GPU-based rendering.")

def main(args):
  
  objs=args.objects
  sobjs=args.sobjects
  img_name=""
  for i,item in enumerate(zip(objs)):
    if i==len(objs)-1:
      under_score=""
    else:
      under_score="_"
    obj_str=str(item[0])

    img_name+="%s%s" % (obj_str,under_score)
  img_template = '%s.png' % (img_name)
  img_template = os.path.join(args.output_image_dir, img_template)
  

  if not os.path.isdir(args.output_image_dir):
    os.makedirs(args.output_image_dir)
  
  img_path = img_template
  render_scene(args,
    output_image=img_path,
  )

  # After rendering all images, combine the JSON files for each scene into a
  # single JSON file.



def render_scene(args,
    output_image='render.png',
  ):

  # Load the main blendfile
  bpy.ops.wm.open_mainfile(filepath=args.base_scene_blendfile)

  # Load materials
  num_objects=len(args.objects)
  # Set render arguments so we can get pixel coordinates later.
  # We use functionality specific to the CYCLES renderer so BLENDER_RENDER
  # cannot be used.
  render_args = bpy.context.scene.render
  render_args.engine = "CYCLES"
  render_args.filepath = output_image
  render_args.resolution_x = args.width
  render_args.resolution_y = args.height
  render_args.resolution_percentage = 100
  
  if args.use_gpu == 1:
    # Blender changed the API for enabling CUDA at some point
    if bpy.app.version < (2, 78, 0):
      bpy.context.user_preferences.system.compute_device_type = 'CUDA'
      bpy.context.user_preferences.system.compute_device = 'CUDA_0'
    else:
      cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
      cycles_prefs.compute_device_type = 'CUDA'
      cycles_prefs.compute_device = 'CUDA'

  # Some CYCLES-specific stuff
  bpy.data.worlds['World'].cycles.sample_as_light = True
  bpy.context.scene.cycles.blur_glossy = 2.0
  bpy.context.scene.cycles.samples = args.render_num_samples
  bpy.context.scene.cycles.transparent_min_bounces = args.render_min_bounces
  bpy.context.scene.cycles.transparent_max_bounces = args.render_max_bounces
  if args.use_gpu == 1:
    bpy.context.scene.cycles.device = 'GPU'

  # This will give ground-truth information about the scene and its objects

  # Put a plane on the ground so we can compute cardinal directions
  bpy.ops.mesh.primitive_plane_add(size=5)
  plane = bpy.context.object

  def rand(L):
    return 2.0 * L * (random.random() - 0.5)

  
  bpy.data.objects['Camera'].location[0]=args.cam_x
  bpy.data.objects['Camera'].location[1]=args.cam_y
  bpy.data.objects['Camera'].location[2]=args.cam_z

  camera = bpy.data.objects['Camera']

  add_objects(num_objects, args, camera)

  # Render the scene and dump the scene data structure
  while True:
    try:
      bpy.ops.render.render(write_still=True)
      break
    except Exception as e:
      print(e)



def add_objects( num_objects, args, camera):
  """
  Add random objects to the current blender scene
  """

  # Load the property file
  with open(args.properties_json, 'r') as f:
    properties = json.load(f)
    object_mapping = [(v, k) for k, v in properties['shapes'].items()]
    size_mapping = list(properties['sizes'].items())

  positions = []
  objects = []
  blender_objects = []
  for i in range(num_objects):
    #scale=args.sobjects[i]
    obj=args.objects[i]
    loc=args.locobjects[i]
    scale=args.sobjects[i]
    x = loc[0]
    y = loc[1]
    obj=properties['shapes'][obj]
    
    # Choose random orientation for the object.
    utils.add_object_objaverse(args.shape_dir, obj, scale, (x, y), theta=0)
  return objects, blender_objects


import json
if __name__ == '__main__':
  if INSIDE_BLENDER:
    # Run normally
    argv = utils.extract_args()
    args = parser.parse_args(argv)
    
    if args.objs_config:
      with open(args.objs_config, 'rt') as f:
          argparse_dict = vars(args)
          print(args)
          argparse_dict.update(json.load(f))
          print(args)
    #print(args.locobjects)
    main(args)
  elif '--help' in sys.argv or '-h' in sys.argv:
    parser.print_help()
  else:
    print('This script is intended to be called from blender like this:')
    print()
    print('blender --background --python render_images.py -- [args]')
    print()
    print('You can also run as a standalone python script to view all')
    print('arguments like this:')
    print()
    print('python render_images.py --help')


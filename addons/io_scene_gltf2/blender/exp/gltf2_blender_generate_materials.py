# Copyright (c) 2017 The Khronos Group Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Imports
#

import bpy

from ...io.com.gltf2_io_debug import *

from ...io.exp.gltf2_io_generate import *
from ...io.exp.gltf2_io_get import *

from .gltf2_blender_get import *

#
# Globals
#


#
# Functions
#

def generate_materials_principled(operator,
                                  context,
                                  export_settings,
                                  glTF,
                                  material,
                                  blender_material,
                                  blender_node):
    
    material['pbrMetallicRoughness'] = {}

    pbrMetallicRoughness = material['pbrMetallicRoughness']

    alpha = 1.0

    #
    # BaseColorFactor or BaseColorTexture
    #
    
    if len(blender_node.inputs['Base Color'].links) > 0:
        
        index = get_texture_index_by_node_group(export_settings, glTF, 'Base Color', blender_node)
        if index >= 0:
            baseColorTexture = {
                'index': index
            }

            texCoord = get_texcoord_index_by_node_group(glTF, 'Base Color', blender_node)
            if texCoord > 0:
                baseColorTexture['texCoord'] = texCoord

            pbrMetallicRoughness['baseColorTexture'] = baseColorTexture
        
    else:
        
        baseColorFactor = get_vec4(blender_node.inputs['Base Color'].default_value, [1.0, 1.0, 1.0, 1.0])
        
        if baseColorFactor[0] != 1.0 or baseColorFactor[1] != 1.0 or baseColorFactor[2] != 1.0 or baseColorFactor[3] != 1.0:
            pbrMetallicRoughness['baseColorFactor'] = baseColorFactor
            alpha = baseColorFactor[3]

    #
    # MetallicFactor or Metallic texture
    #
    
    if len(blender_node.inputs['Metallic'].links) > 0:
        
        print_console('DEBUG', '# TODO: Check metallic links')
        
    else:
        
        metallicFactor = get_scalar(blender_node.inputs['Metallic'].default_value, 1.0)
        
        if metallicFactor != 1.0:
            pbrMetallicRoughness['metallicFactor'] = metallicFactor

    #
    # RoughnessFactor or Roughness texture
    #
    
    if len(blender_node.inputs['Roughness'].links) > 0:
        
        print_console('DEBUG', '# TODO: Check roughness links')
        
    else:
        
        roughnessFactor = get_scalar(blender_node.inputs['Roughness'].default_value, 1.0)
        
        if roughnessFactor != 1.0:
            pbrMetallicRoughness['roughnessFactor'] = roughnessFactor
            
    #
    
    print_console('DEBUG', '# TODO: Check transmission links')
    
    if len(blender_node.inputs['Normal'].links) > 0:
        
        index = get_texture_index_by_node_group(export_settings, glTF, 'Normal', blender_node)
        if index >= 0:
            normalTexture = {
                'index': index
            }

            texCoord = get_texcoord_index_by_node_group(glTF, 'Normal', blender_node)
            if texCoord > 0:
                normalTexture['texCoord'] = texCoord

            material['normalTexture'] = normalTexture
            
    #
            
    material['name'] = blender_material.name


def generate_materials(operator,
                       context,
                       export_settings,
                       glTF):
    """
    Generates the top level materials entry.
    """

    filtered_materials = export_settings['filtered_materials']

    materials = []

    KHR_materials_pbrSpecularGlossiness_Used = False
    KHR_materials_unlit_Used = False
    KHR_materials_displacement_Used = False

    #
    #

    for blender_material in filtered_materials:
        #
        # Property: material
        #

        material = {}

        #

        if blender_material.node_tree is not None and blender_material.use_nodes:

            #
            # Cycles Render.
            #

            for blender_node in blender_material.node_tree.nodes:
                if isinstance(blender_node, bpy.types.ShaderNodeGroup):

                    alpha = 1.0

                    if blender_node.node_tree.name.startswith('glTF Metallic Roughness'):
                        #
                        # Property: pbrMetallicRoughness
                        #

                        material['pbrMetallicRoughness'] = {}

                        pbrMetallicRoughness = material['pbrMetallicRoughness']

                        #
                        # Base color texture
                        #
                        index = get_texture_index_by_node_group(export_settings, glTF, 'BaseColor', blender_node)
                        if index >= 0:
                            baseColorTexture = {
                                'index': index
                            }

                            texCoord = get_texcoord_index_by_node_group(glTF, 'BaseColor', blender_node)
                            if texCoord > 0:
                                baseColorTexture['texCoord'] = texCoord

                            pbrMetallicRoughness['baseColorTexture'] = baseColorTexture

                        #
                        # Base color factor
                        #
                        baseColorFactor = get_vec4(blender_node.inputs['BaseColorFactor'].default_value,
                                                   [1.0, 1.0, 1.0, 1.0])
                        if baseColorFactor[0] != 1.0 or baseColorFactor[1] != 1.0 or baseColorFactor[2] != 1.0 or \
                                baseColorFactor[3] != 1.0:
                            pbrMetallicRoughness['baseColorFactor'] = baseColorFactor
                            alpha = baseColorFactor[3]

                        #
                        # Metallic factor
                        #
                        metallicFactor = get_scalar(blender_node.inputs['MetallicFactor'].default_value, 1.0)
                        if metallicFactor != 1.0:
                            pbrMetallicRoughness['metallicFactor'] = metallicFactor

                        #
                        # Roughness factor
                        #
                        roughnessFactor = get_scalar(blender_node.inputs['RoughnessFactor'].default_value, 1.0)
                        if roughnessFactor != 1.0:
                            pbrMetallicRoughness['roughnessFactor'] = roughnessFactor

                        #
                        # Metallic roughness texture
                        #
                        index = get_texture_index_by_node_group(export_settings, glTF, 'MetallicRoughness', blender_node)
                        if index >= 0:
                            metallicRoughnessTexture = {
                                'index': index
                            }

                            texCoord = get_texcoord_index_by_node_group(glTF, 'MetallicRoughness', blender_node)
                            if texCoord > 0:
                                metallicRoughnessTexture['texCoord'] = texCoord

                            pbrMetallicRoughness['metallicRoughnessTexture'] = metallicRoughnessTexture

                    if blender_node.node_tree.name.startswith('glTF Specular Glossiness'):
                        KHR_materials_pbrSpecularGlossiness_Used = True

                        #
                        # Property: Specular Glossiness Material
                        #

                        pbrSpecularGlossiness = {}

                        material['extensions'] = {'KHR_materials_pbrSpecularGlossiness': pbrSpecularGlossiness}

                        #
                        # Diffuse texture
                        #
                        index = get_texture_index_by_node_group(export_settings, glTF, 'Diffuse', blender_node)
                        if index >= 0:
                            diffuseTexture = {
                                'index': index
                            }

                            texCoord = get_texcoord_index_by_node_group(glTF, 'Diffuse', blender_node)
                            if texCoord > 0:
                                diffuseTexture['texCoord'] = texCoord

                            pbrSpecularGlossiness['diffuseTexture'] = diffuseTexture

                        #
                        # Diffuse factor
                        #
                        diffuseFactor = get_vec4(blender_node.inputs['DiffuseFactor'].default_value,
                                                 [1.0, 1.0, 1.0, 1.0])
                        if diffuseFactor[0] != 1.0 or diffuseFactor[1] != 1.0 or diffuseFactor[2] != 1.0 or \
                                diffuseFactor[3] != 1.0:
                            pbrSpecularGlossiness['diffuseFactor'] = diffuseFactor
                            alpha = diffuseFactor[3]

                        #
                        # Specular texture
                        #
                        index_a = get_texture_index_by_node_group(export_settings, glTF, 'Specular', blender_node)
                        index_b = get_texture_index_by_node_group(export_settings, glTF, 'Glossiness', blender_node)
                        if index_a >= 0 and index_b >= 0 and index_a == index_b:
                            specularGlossinessTexture = {
                                'index': index_a
                            }

                            texCoord = get_texcoord_index_by_node_group(glTF, 'Specular', blender_node)
                            if texCoord > 0:
                                specularGlossinessTexture['texCoord'] = texCoord

                            pbrSpecularGlossiness['specularGlossinessTexture'] = specularGlossinessTexture

                        #
                        # Specular factor
                        #
                        specularFactor = get_vec3(blender_node.inputs['SpecularFactor'].default_value, [1.0, 1.0, 1.0])
                        if specularFactor[0] != 1.0 or specularFactor[1] != 1.0 or specularFactor[2] != 1.0:
                            pbrSpecularGlossiness['specularFactor'] = specularFactor

                        #
                        # Glossiness factor
                        #
                        glossinessFactor = get_scalar(blender_node.inputs['GlossinessFactor'].default_value, 1.0)
                        if glossinessFactor != 1.0:
                            pbrSpecularGlossiness['glossinessFactor'] = glossinessFactor

                    # TODO: Export displacement data for PBR.

                    #
                    # Emissive texture
                    #
                    index = get_texture_index_by_node_group(export_settings, glTF, 'Emissive', blender_node)
                    if index >= 0:
                        emissiveTexture = {
                            'index': index
                        }

                        texCoord = get_texcoord_index_by_node_group(glTF, 'Emissive', blender_node)
                        if texCoord > 0:
                            emissiveTexture['texCoord'] = texCoord

                        material['emissiveTexture'] = emissiveTexture

                    #
                    # Emissive factor
                    #
                    emissiveFactor = get_vec3(blender_node.inputs['EmissiveFactor'].default_value, [0.0, 0.0, 0.0])
                    if emissiveFactor[0] != 0.0 or emissiveFactor[1] != 0.0 or emissiveFactor[2] != 0.0:
                        material['emissiveFactor'] = emissiveFactor

                    #
                    # Normal texture
                    #
                    index = get_texture_index_by_node_group(export_settings, glTF, 'Normal', blender_node)
                    if index >= 0:
                        normalTexture = {
                            'index': index
                        }

                        texCoord = get_texcoord_index_by_node_group(glTF, 'Normal', blender_node)
                        if texCoord > 0:
                            normalTexture['texCoord'] = texCoord

                        scale = get_scalar(blender_node.inputs['NormalScale'].default_value, 1.0)

                        if scale != 1.0:
                            normalTexture['scale'] = scale

                        material['normalTexture'] = normalTexture

                    #
                    # Occlusion texture
                    #
                    if len(blender_node.inputs['Occlusion'].links) > 0:
                        index = get_texture_index_by_node_group(export_settings, glTF, 'Occlusion', blender_node)
                        if index >= 0:
                            occlusionTexture = {
                                'index': index
                            }

                            texCoord = get_texcoord_index_by_node_group(glTF, 'Occlusion', blender_node)
                            if texCoord > 0:
                                occlusionTexture['texCoord'] = texCoord

                            strength = get_scalar(blender_node.inputs['OcclusionStrength'].default_value, 1.0)

                            if strength != 1.0:
                                occlusionTexture['strength'] = strength

                            material['occlusionTexture'] = occlusionTexture

                    #
                    # Alpha
                    #
                    index = get_texture_index_by_node_group(export_settings, glTF, 'Alpha', blender_node)
                    if index >= 0 or alpha < 1.0:
                        alphaMode = 'BLEND'
                        if get_scalar(blender_node.inputs['AlphaMode'].default_value, 0.0) >= 0.5:
                            alphaMode = 'MASK'

                            material['alphaCutoff'] = get_scalar(blender_node.inputs['AlphaCutoff'].default_value, 0.5)

                        material['alphaMode'] = alphaMode

                    #
                    # Double sided
                    #
                    if get_scalar(blender_node.inputs['DoubleSided'].default_value, 0.0) >= 0.5:
                        material['doubleSided'] = True

                    #
                    # Use Color_0
                    #

                    if get_scalar(blender_node.inputs['Use COLOR_0'].default_value, 0.0) < 0.5:
                        export_settings['gltf_use_no_color'].append(blender_material.name)

                    #

                    if export_settings['gltf_extras']:
                        extras = generate_extras(blender_material)

                        if extras is not None:
                            material['extras'] = extras

                            #

                    material['name'] = blender_material.name

                    #
                    #

                    materials.append(material)
                    
                elif isinstance(blender_node, bpy.types.ShaderNodeBsdfPrincipled):
                    
                    generate_materials_principled(operator, context, export_settings, glTF, material, blender_material, blender_node)
                    
                    materials.append(material)

        else:

            #
            # Blender Render.
            #

            if blender_material.use_shadeless:
                KHR_materials_unlit_Used = True

                #
                # Property: Unlit Material
                #

                material['extensions'] = {'KHR_materials_unlit': {}}

                if not 'pbrMetallicRoughness' in material:
                    material['pbrMetallicRoughness'] = {}

                pbrMetallicRoughness = material['pbrMetallicRoughness']

                alpha = 1.0
                alphaMode = 'OPAQUE'
                if blender_material.use_transparency:
                    alpha = blender_material.alpha
                    if blender_material.transparency_method == 'MASK':
                        alphaMode = 'MASK'
                    else:
                        alphaMode = 'BLEND'

                pbrMetallicRoughness['baseColorFactor'] = [blender_material.diffuse_color[0] * blender_material.diffuse_intensity,
                                           blender_material.diffuse_color[1] * blender_material.diffuse_intensity,
                                           blender_material.diffuse_color[2] * blender_material.diffuse_intensity,
                                           alpha]

                pbrMetallicRoughness['metallicFactor'] = 0.0
                pbrMetallicRoughness['roughnessFactor'] = 0.9

                if alphaMode != 'OPAQUE':
                    material['alphaMode'] = alphaMode

                #

                for blender_texture_slot in blender_material.texture_slots:
                    if blender_texture_slot and blender_texture_slot.texture and blender_texture_slot.texture.type == 'IMAGE' and blender_texture_slot.texture.image is not None:
                        #
                        # Base color texture
                        #
                        if blender_texture_slot.use_map_color_diffuse:
                            index = get_texture_index(glTF, blender_texture_slot.texture.image.name)
                            if index >= 0:
                                baseColorTexture = {
                                    'index': index
                                }
                                pbrMetallicRoughness['baseColorTexture'] = baseColorTexture
                            else:
                                print('failed to find image: ' + blender_texture_slot.texture.image.name)

                        #
                        # Displacement textue
                        #
                        if export_settings['gltf_displacement']:
                            if blender_texture_slot.use_map_displacement:
                                index = get_texture_index(glTF, blender_texture_slot.texture.image.name)
                                if index >= 0:
                                    extensions = material['extensions']

                                    #

                                    displacementTexture = {
                                        'index': index,
                                        'strength': blender_texture_slot.displacement_factor
                                    }

                                    extensions['KHR_materials_displacement'] = {
                                        'displacementTexture': displacementTexture}

                                    #

                                    KHR_materials_displacement_Used = True

                #

                if export_settings['gltf_extras']:
                    extras = generate_extras(blender_material)

                    if extras is not None:
                        material['extras'] = extras

                        #

                material['name'] = blender_material.name

                #
                #

                materials.append(material)

            else:

                #
                # A minimal export of basic material properties that didn't get picked up any other way to a pbrMetallicRoughness glTF material
                #
                material['pbrMetallicRoughness'] = {}

                pbrMetallicRoughness = material['pbrMetallicRoughness']

                alpha = 1.0
                alphaMode = 'OPAQUE'
                if blender_material.use_transparency:
                    alpha = blender_material.alpha
                    if blender_material.transparency_method == 'MASK':
                        alphaMode = 'MASK'
                    else:
                        alphaMode = 'BLEND'

                if alphaMode != 'OPAQUE':
                    material['alphaMode'] = alphaMode

                for blender_texture_slot in blender_material.texture_slots:
                    if blender_texture_slot and blender_texture_slot.texture and blender_texture_slot.texture.type == 'IMAGE' and blender_texture_slot.texture.image is not None:
                        #
                        # Diffuse texture becmomes baseColorTexture
                        #
                        if blender_texture_slot.use_map_color_diffuse:
                            index = get_texture_index(glTF, blender_texture_slot.texture.image.name)
                            if index >= 0:
                                baseColorTexture = {
                                    'index': index
                                }
                                pbrMetallicRoughness['baseColorTexture'] = baseColorTexture

                        #
                        # Ambient texture becomes occlusionTexture
                        #
                        if blender_texture_slot.use_map_ambient:
                            index = get_texture_index(glTF, blender_texture_slot.texture.image.name)
                            if index >= 0:
                                ambientTexture = {
                                    'index': index
                                }
                                material['occlusionTexture'] = ambientTexture

                        #
                        # Emissive texture
                        #
                        if blender_texture_slot.use_map_emit:
                            index = get_texture_index(glTF, blender_texture_slot.texture.image.name)
                            if index >= 0:
                                emissiveTexture = {
                                    'index': index
                                }
                                material['emissiveTexture'] = emissiveTexture

                        #
                        # Normal texture
                        #
                        if blender_texture_slot.use_map_normal:
                            index = get_texture_index(glTF, blender_texture_slot.texture.image.name)
                            if index >= 0:
                                normalTexture = {
                                    'index': index
                                }
                                material['normalTexture'] = normalTexture

                        #
                        # Displacement textue
                        #
                        if export_settings['gltf_displacement']:
                            if blender_texture_slot.use_map_displacement:
                                index = get_texture_index(glTF, blender_texture_slot.texture.image.name)
                                if index >= 0:
                                    extensions = material['extensions']

                                    #

                                    displacementTexture = {
                                        'index': index,
                                        'strength': blender_texture_slot.displacement_factor
                                    }

                                    extensions['KHR_materials_displacement'] = {
                                        'displacementTexture': displacementTexture}

                                    #

                                    KHR_materials_displacement_Used = True

                #
                # Base color factor
                #
                baseColorFactor = [blender_material.diffuse_color[0] * blender_material.diffuse_intensity,
                                   blender_material.diffuse_color[1] * blender_material.diffuse_intensity,
                                   blender_material.diffuse_color[2] * blender_material.diffuse_intensity, alpha]
                if baseColorFactor[0] != 1.0 or baseColorFactor[1] != 1.0 or baseColorFactor[2] != 1.0 or \
                        baseColorFactor[3] != 1.0:
                    pbrMetallicRoughness['baseColorFactor'] = baseColorFactor
                    alpha = baseColorFactor[3]

                #
                # Metallic factor has to be 0.0 for not breaking the Metallic-Roughness workflow.
                #
                pbrMetallicRoughness['metallicFactor'] = 0.0

                #
                # Emissive factor
                #
                emissiveFactor = [blender_material.emit * blender_material.diffuse_color[0],
                                  blender_material.emit * blender_material.diffuse_color[1],
                                  blender_material.emit * blender_material.diffuse_color[2]]
                if emissiveFactor[0] != 0.0 or emissiveFactor[1] != 0.0 or emissiveFactor[2] != 0.0:
                    material['emissiveFactor'] = emissiveFactor

                #

                if export_settings['gltf_extras']:
                    extras = generate_extras(blender_material)

                    if extras is not None:
                        material['extras'] = extras

                        #

                material['name'] = blender_material.name

                #
                #

                materials.append(material)

    #
    #

    if len(materials) > 0:
        if KHR_materials_pbrSpecularGlossiness_Used:
            generate_extensionsUsed(export_settings, glTF, 'KHR_materials_pbrSpecularGlossiness')
            generate_extensionsRequired(export_settings, glTF, 'KHR_materials_pbrSpecularGlossiness')

        if KHR_materials_unlit_Used:
            generate_extensionsUsed(export_settings, glTF, 'KHR_materials_unlit')

        if KHR_materials_displacement_Used:
            generate_extensionsUsed(export_settings, glTF, 'KHR_materials_displacement')
            generate_extensionsRequired(export_settings, glTF, 'KHR_materials_displacement')

        glTF['materials'] = materials

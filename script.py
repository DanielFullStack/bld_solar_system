import bpy
import math

# Limpa a cena atual
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.context.scene.frame_end = 1440  # Total de quadros (60 segundos a 24 FPS)
bpy.context.scene.render.fps = 24   # FPS (Frames por Segundo)

def criar_esfera(nome, raio, cor, local):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=raio, location=local, segments=64, ring_count=32
    )
    esfera = bpy.context.active_object
    esfera.name = nome

    mat = bpy.data.materials.new(name=f"Material_{nome}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = cor
    esfera.data.materials.append(mat)

    bpy.ops.object.shade_smooth()
    return esfera

def adicionar_emissao(obj, cor):
    mat = bpy.data.materials.new(name=f"Emissivo_{obj.name}")
    mat.use_nodes = True
    emis_node = mat.node_tree.nodes.new('ShaderNodeEmission')
    emis_node.inputs['Color'].default_value = cor
    emis_node.inputs['Strength'].default_value = 8.0
    mat.node_tree.links.new(emis_node.outputs['Emission'], 
                            mat.node_tree.nodes['Material Output'].inputs['Surface'])
    obj.data.materials[0] = mat

def criar_orbita_animada(obj, centro, raio_orbita, tempo_orbita):
    obj.location = (centro[0] + raio_orbita, centro[1], centro[2])

    for frame in range(0, 1440, 20):
        angulo = 2 * math.pi * (frame / tempo_orbita)
        x = centro[0] + raio_orbita * math.cos(angulo)
        y = centro[1] + raio_orbita * math.sin(angulo)
        obj.location = (x, y, centro[2])
        obj.keyframe_insert(data_path="location", frame=frame)

def criar_label(obj):
    bpy.ops.object.text_add(location=(obj.location.x, obj.location.y, obj.location.z + 2.0))
    label = bpy.context.active_object
    label.data.body = obj.name
    label.scale = (0.8, 0.8, 0.8)

    mat = bpy.data.materials.new(name=f"Material_Label_{obj.name}")
    mat.use_nodes = True
    emission = mat.node_tree.nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (1, 1, 1, 1)  # Branco emissivo
    emission.inputs['Strength'].default_value = 5.0
    mat.node_tree.links.new(emission.outputs['Emission'], 
                            mat.node_tree.nodes['Material Output'].inputs['Surface'])
    label.data.materials.append(mat)

    constraint = label.constraints.new(type='CHILD_OF')
    constraint.target = obj

    constraint_track = label.constraints.new(type='TRACK_TO')
    constraint_track.target = bpy.context.scene.camera
    constraint_track.track_axis = 'TRACK_Z'
    constraint_track.up_axis = 'UP_Y'

    return label

# Cria o Sol
sol = criar_esfera("Sol", 2.0, (1.0, 0.9, 0.1, 1.0), (0, 0, 0))
adicionar_emissao(sol, (1.0, 0.9, 0.1, 1.0))
criar_label(sol)

# Cria os planetas com suas órbitas animadas
planetas = [
    {"nome": "Mercúrio", "raio": 0.5, "cor": (0.5, 0.5, 0.5, 1.0), "orbita": 5, "tempo": 300},
    {"nome": "Vênus", "raio": 0.6, "cor": (1.0, 0.7, 0.2, 1.0), "orbita": 7, "tempo": 450},
    {"nome": "Terra", "raio": 0.7, "cor": (0.2, 0.5, 1.0, 1.0), "orbita": 9, "tempo": 600},
    {"nome": "Marte", "raio": 0.6, "cor": (1.0, 0.2, 0.2, 1.0), "orbita": 11, "tempo": 900},
    {"nome": "Júpiter", "raio": 1.4, "cor": (0.8, 0.6, 0.3, 1.0), "orbita": 15, "tempo": 1200},
    {"nome": "Saturno", "raio": 1.2, "cor": (0.9, 0.7, 0.4, 1.0), "orbita": 20, "tempo": 1400},
    {"nome": "Urano", "raio": 1.0, "cor": (0.5, 0.7, 0.9, 1.0), "orbita": 25, "tempo": 1600},
    {"nome": "Netuno", "raio": 1.0, "cor": (0.2, 0.4, 0.8, 1.0), "orbita": 30, "tempo": 1800},
]

for p in planetas:
    planeta = criar_esfera(p["nome"], p["raio"], p["cor"], (p["orbita"], 0, 0))
    criar_orbita_animada(planeta, (0, 0, 0), p["orbita"], p["tempo"])
    criar_label(planeta)

# Cria uma animação para a câmera em uma órbita ao redor do Sol
def criar_camera_animada(objeto_alvo):
    camera = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
    bpy.context.collection.objects.link(camera)

    camera.location = (0, -80, 50)
    bpy.context.scene.camera = camera

    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = objeto_alvo
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    # Animação da câmera: orbitando ao redor do Sol
    for frame in range(0, 1440, 40):
        angulo = 2 * math.pi * (frame / 1440)
        x = 80 * math.cos(angulo)
        y = 80 * math.sin(angulo)
        camera.location = (x, y, 50)
        camera.keyframe_insert(data_path="location", frame=frame)

# Cria e anima a câmera
criar_camera_animada(sol)

# Adiciona uma luz do tipo 'SUN'
light_data = bpy.data.lights.new(name="SunLight", type='SUN')
light = bpy.data.objects.new(name="SunLight", object_data=light_data)
bpy.context.collection.objects.link(light)
light.location = (0, 0, 100)

# Adiciona um fundo com textura procedural para o universo
def adicionar_fundo_universo():
    world = bpy.context.scene.world
    world.use_nodes = True
    tree = world.node_tree

    background = tree.nodes["Background"]
    texture_coord = tree.nodes.new(type="ShaderNodeTexCoord")
    noise_texture = tree.nodes.new(type="ShaderNodeTexNoise")
    color_ramp = tree.nodes.new(type="ShaderNodeValToRGB")

    noise_texture.inputs["Scale"].default_value = 10.0
    color_ramp.color_ramp.elements[0].position = 0.3
    color_ramp.color_ramp.elements[1].position = 0.7

    tree.links.new(texture_coord.outputs["Generated"], noise_texture.inputs["Vector"])
    tree.links.new(noise_texture.outputs["Fac"], color_ramp.inputs["Fac"])
    tree.links.new(color_ramp.outputs["Color"], background.inputs["Color"])

adicionar_fundo_universo()

print("Sistema Solar completo e câmera animada!")

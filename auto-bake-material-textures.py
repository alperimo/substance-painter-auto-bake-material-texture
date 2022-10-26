import os

# Substance 3D Painter modules

import substance_painter as sp

# PySide module to build custom UI
from PySide2 import QtCore
from PySide2 import QtWidgets

plugin_widgets = []

material_folder_path_field = QtWidgets.QLineEdit()

def select_material_folder():
    material_folder_path = QtWidgets.QFileDialog.getExistingDirectory()
    material_folder_path_field.setText(material_folder_path)

def bake_textures():
    material_folder_path = material_folder_path_field.text() # "c:\\tests\sp" # Sphere (inside of it ex. Sphere_normal.psd, Sphere_AO.psd, ...)
    
    print(dir(sp.resource))
    
    mesh_map_list = {"normal": 6, "ao": 1, "curve": 2, "bentnormal": 8, 
                     "height": 7, "normalobj": 3, "thickness": 5,
                     "matid": 0, "opacity": 9, "position": 4}
    
    print(dir(sp.textureset))
    #my_texture_set = substance_painter.textureset.TextureSet
    texture_sets = sp.textureset.all_texture_sets()
    for texture_set in texture_sets:
        material_name = texture_set.name()
        texture_folder = os.path.join(material_folder_path, material_name)
        print("material name: {} texture_folder: {}".format(material_name, texture_folder))
        
        print(os.listdir(texture_folder))
        texture_files = [f for f in os.listdir(texture_folder) if f.endswith(".psd")]

        for tf in texture_files:
            tf_path = os.path.join(texture_folder, tf)
            print("for material: {} texture file: {}".format(material_name, tf_path))
            texture_resource = sp.resource.import_project_resource(tf_path, sp.resource.Usage.TEXTURE)
            texture_resourceID = texture_resource.identifier()
            
            mesh_map = tf.split("_")[2].split(".")[0] # 0_Sphere_normal.psd -> normal
            print("mesh map: {} texture_resourceID: {}".format(mesh_map, texture_resourceID))
            
            print(dir(texture_set))
            
            texture_set.set_mesh_map_resource(sp.textureset.MeshMapUsage(mesh_map_list[mesh_map]), texture_resourceID)
        
def start_plugin():
    Action = QtWidgets.QAction("Auto Bake Material Texture", triggered=bake_textures)
    sp.ui.add_action(sp.ui.ApplicationMenu.File, Action)
    plugin_widgets.append(Action)
    
    main_widget = QtWidgets.QWidget()
    main_widget.setFixedSize(800, 50)
    main_widget.setWindowTitle("Auto Bake Material Texture")
    
    main_layout = QtWidgets.QHBoxLayout()
    
    main_widget.setLayout(main_layout)
    
    folder_path_label = QtWidgets.QLabel("Selected materials folder path:")
    
    material_selectFolderPath_btn = QtWidgets.QPushButton("...")
    material_selectFolderPath_btn.setFixedSize(QtCore.QSize(30, 20))
    material_selectFolderPath_btn.clicked.connect(select_material_folder)
    
    material_loadAndMesh_btn = QtWidgets.QPushButton("Load and Mesh Map")
    material_loadAndMesh_btn.setFixedSize(QtCore.QSize(70, 20))
    material_loadAndMesh_btn.clicked.connect(bake_textures)
    
    main_layout.addWidget(folder_path_label)
    main_layout.addWidget(material_folder_path_field)
    main_layout.addWidget(material_selectFolderPath_btn)
    main_layout.addWidget(material_loadAndMesh_btn)
    
    sp.ui.add_dock_widget(main_widget)   
    plugin_widgets.append(main_widget)
 
def close_plugin():
	for widget in plugin_widgets:
		sp.ui.delete_ui_element(widget)

	plugin_widgets.clear()

if __name__ == "__main__":
	start_plugin()
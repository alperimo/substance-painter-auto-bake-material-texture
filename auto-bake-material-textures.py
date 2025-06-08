import os
import logging
from datetime import datetime

# Substance 3D Painter modules
import substance_painter as sp

# PySide module to build custom UI
from PySide2 import QtCore
from PySide2 import QtWidgets

plugin_widgets = []

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('auto_bake_material_textures.log')
    ]
)
logger = logging.getLogger(__name__)

material_folder_path_field = QtWidgets.QLineEdit()

def select_material_folder():
    """Select a folder containing material textures."""
    material_folder_path = QtWidgets.QFileDialog.getExistingDirectory()
    if material_folder_path:
        material_folder_path_field.setText(material_folder_path)
        logger.info(f"Selected material folder: {material_folder_path}")
    else:
        logger.warning("No folder selected")

def bake_textures():
    """Process and bake textures from the selected folder to texture sets."""
    material_folder_path = material_folder_path_field.text()
    
    if not material_folder_path:
        logger.error("No material folder path specified")
        QtWidgets.QMessageBox.warning(None, "Warning", "Please select a material folder first.")
        return
    
    if not os.path.exists(material_folder_path):
        logger.error(f"Material folder path does not exist: {material_folder_path}")
        QtWidgets.QMessageBox.critical(None, "Error", f"Selected folder does not exist:\n{material_folder_path}")
        return
    
    logger.info(f"Starting texture baking process from folder: {material_folder_path}")
    
    # Debug information about available SP modules
    logger.debug(f"Available sp.resource methods: {dir(sp.resource)}")
    logger.debug(f"Available sp.textureset methods: {dir(sp.textureset)}")
    
    # Mapping of mesh map names to their corresponding enum values
    mesh_map_list = {
        "normal": 6, "ao": 1, "curve": 2, "bentnormal": 8, 
        "height": 7, "normalobj": 3, "thickness": 5,
        "matid": 0, "opacity": 9, "position": 4
    }
    
    logger.info(f"Supported mesh map types: {list(mesh_map_list.keys())}")
    
    texture_sets = sp.textureset.all_texture_sets()
    if not texture_sets:
        logger.warning("No texture sets found in the current project")
        QtWidgets.QMessageBox.information(None, "Info", "No texture sets found in the current project.")
        return
    
    logger.info(f"Found {len(texture_sets)} texture set(s) to process")
    
    processed_count = 0
    error_count = 0
    
    for texture_set in texture_sets:
        material_name = texture_set.name()
        texture_folder = os.path.join(material_folder_path, material_name)
        
        logger.info(f"Processing texture set: {material_name}")
        
        if not os.path.exists(texture_folder):
            logger.warning(f"Texture folder does not exist for material '{material_name}': {texture_folder}")
            continue
        
        logger.info(f"Found texture folder: {texture_folder}")
        
        try:
            texture_files = [f for f in os.listdir(texture_folder) if f.lower().endswith(".psd")]
            logger.info(f"Found {len(texture_files)} PSD files in {texture_folder}")
            logger.debug(f"Texture files: {texture_files}")
            
            if not texture_files:
                logger.warning(f"No PSD files found in {texture_folder}")
                continue
                
        except Exception as e:
            logger.error(f"Error reading directory {texture_folder}: {str(e)}")
            error_count += 1
            continue

        for tf in texture_files:
            tf_path = os.path.join(texture_folder, tf)
            
            try:
                logger.info(f"Processing texture file: {tf}")
                
                # Import the texture resource
                texture_resource = sp.resource.import_project_resource(tf_path, sp.resource.Usage.TEXTURE)
                texture_resourceID = texture_resource.identifier()
                logger.debug(f"Imported texture resource with ID: {texture_resourceID}")
                
                # Extract mesh map type from filename (assuming format: prefix_materialname_maptype.psd)
                filename_parts = tf.split("_")
                if len(filename_parts) < 3:
                    logger.error(f"Invalid filename format for {tf}. Expected format: prefix_materialname_maptype.psd")
                    error_count += 1
                    continue
                
                mesh_map = filename_parts[2].split(".")[0].lower()  # Extract map type and convert to lowercase
                logger.debug(f"Extracted mesh map type: {mesh_map}")
                
                if mesh_map not in mesh_map_list:
                    logger.warning(f"Unsupported mesh map type '{mesh_map}' in file {tf}. Supported types: {list(mesh_map_list.keys())}")
                    error_count += 1
                    continue
                
                # Debug information about texture set
                logger.debug(f"Available texture_set methods: {dir(texture_set)}")
                
                # Set the mesh map resource
                mesh_map_usage = sp.textureset.MeshMapUsage(mesh_map_list[mesh_map])
                texture_set.set_mesh_map_resource(mesh_map_usage, texture_resourceID)
                
                logger.info(f"Successfully mapped {mesh_map} texture to material {material_name}")
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing texture file {tf_path}: {str(e)}")
                error_count += 1
    
    # Summary
    logger.info(f"Texture baking completed. Processed: {processed_count}, Errors: {error_count}")
    
    if error_count > 0:
        QtWidgets.QMessageBox.warning(
            None, 
            "Process Completed with Warnings", 
            f"Texture baking completed.\n\nProcessed: {processed_count} textures\nErrors: {error_count} textures\n\nCheck the log file for details."
        )
    else:
        QtWidgets.QMessageBox.information(
            None, 
            "Process Completed", 
            f"Texture baking completed successfully!\n\nProcessed: {processed_count} textures"
        )
            
def start_plugin():
    """Initialize and start the plugin."""
    logger.info("Starting Auto Bake Material Texture plugin")
    
    # Add action to File menu
    Action = QtWidgets.QAction("Auto Bake Material Texture", triggered=bake_textures)
    sp.ui.add_action(sp.ui.ApplicationMenu.File, Action)
    plugin_widgets.append(Action)
    
    # Create main widget
    main_widget = QtWidgets.QWidget()
    main_widget.setFixedSize(800, 50)
    main_widget.setWindowTitle("Auto Bake Material Texture")
    
    main_layout = QtWidgets.QHBoxLayout()
    main_widget.setLayout(main_layout)
    
    # UI elements
    folder_path_label = QtWidgets.QLabel("Selected materials folder path:")
    
    material_selectFolderPath_btn = QtWidgets.QPushButton("...")
    material_selectFolderPath_btn.setFixedSize(QtCore.QSize(30, 20))
    material_selectFolderPath_btn.clicked.connect(select_material_folder)
    material_selectFolderPath_btn.setToolTip("Select folder containing material textures")
    
    material_loadAndMesh_btn = QtWidgets.QPushButton("Load and Mesh Map")
    material_loadAndMesh_btn.setFixedSize(QtCore.QSize(120, 20))
    material_loadAndMesh_btn.clicked.connect(bake_textures)
    material_loadAndMesh_btn.setToolTip("Process and map textures to mesh maps")
    
    # Add widgets to layout
    main_layout.addWidget(folder_path_label)
    main_layout.addWidget(material_folder_path_field)
    main_layout.addWidget(material_selectFolderPath_btn)
    main_layout.addWidget(material_loadAndMesh_btn)
    
    # Add dock widget
    sp.ui.add_dock_widget(main_widget)   
    plugin_widgets.append(main_widget)
    
    logger.info("Plugin UI initialized successfully")
 
def close_plugin():
    """Clean up and close the plugin."""
    logger.info("Closing Auto Bake Material Texture plugin")
    
    for widget in plugin_widgets:
        sp.ui.delete_ui_element(widget)

    plugin_widgets.clear()
    logger.info("Plugin closed successfully")

if __name__ == "__main__":
    start_plugin()
# Auto Bake Material Textures - Substance Painter Plugin

A Substance Painter plugin that automatically imports and maps texture files to mesh maps based on organized folder structures and naming conventions.

## Features

- **Automatic Texture Import**: Bulk import PSD texture files from organized folders
- **Smart Mesh Mapping**: Automatically maps textures to appropriate mesh map channels
- **User-Friendly Interface**: Simple dock widget with folder selection and processing controls
- **Comprehensive Logging**: Detailed logging with multiple levels for debugging and monitoring
- **Error Handling**: Robust error handling with user notifications
- **Progress Reporting**: Visual feedback on processing status and results

## Supported Mesh Map Types

The plugin supports the following mesh map types with their corresponding naming conventions:

| Mesh Map Type | Naming Convention | Description |
|---------------|-------------------|-------------|
| `normal` | `*_normal.psd` | Normal maps |
| `ao` | `*_ao.psd` | Ambient Occlusion |
| `curve` | `*_curve.psd` | Curvature maps |
| `bentnormal` | `*_bentnormal.psd` | Bent Normal maps |
| `height` | `*_height.psd` | Height/Displacement maps |
| `normalobj` | `*_normalobj.psd` | Object-space Normal maps |
| `thickness` | `*_thickness.psd` | Thickness maps |
| `matid` | `*_matid.psd` | Material ID maps |
| `opacity` | `*_opacity.psd` | Opacity maps |
| `position` | `*_position.psd` | Position maps |

## Installation

1. **Copy the Plugin File**:
   - Copy `auto-bake-material-textures.py` to your Substance Painter plugins directory
   - Default location: `Documents/Adobe/Adobe Substance 3D Painter/python/plugins/`

2. **Enable Python Plugins**:
   - In Substance Painter, go to `Edit > Preferences > General`
   - Enable "Python plugins" if not already enabled
   - Restart Substance Painter

3. **Verify Installation**:
   - Check the `File` menu for "Auto Bake Material Texture" action
   - Look for the plugin dock widget in the interface

## Usage

### Folder Structure Requirements

Organize your texture files using the following structure:

```
Your_Material_Folder/
├── MaterialName1/
│   ├── 0_MaterialName1_normal.psd
│   ├── 0_MaterialName1_ao.psd
│   ├── 0_MaterialName1_height.psd
│   └── ...
├── MaterialName2/
│   ├── 0_MaterialName2_normal.psd
│   ├── 0_MaterialName2_curve.psd
│   └── ...
└── MaterialName3/
    ├── 0_MaterialName3_normal.psd
    └── ...
```

### File Naming Convention

Texture files must follow this naming pattern:
```
[prefix]_[MaterialName]_[MapType].psd
```

**Examples**:
- `0_Sphere_normal.psd`
- `1_Cube_ao.psd`
- `2_Cylinder_height.psd`

### Step-by-Step Instructions

1. **Open Your Project**:
   - Load your 3D model in Substance Painter
   - Ensure texture sets are created for your materials

2. **Access the Plugin**:
   - Open the plugin dock widget (should appear automatically)
   - Or use `File > Auto Bake Material Texture` from the menu

3. **Select Material Folder**:
   - Click the "..." button to browse for your material folder
   - Select the root folder containing your organized material subfolders

4. **Process Textures**:
   - Click "Load and Mesh Map" to start the automatic import and mapping process
   - Monitor the progress through log messages and notifications

5. **Review Results**:
   - Check the notification dialog for processing summary
   - Review mesh maps in your texture sets to verify correct mapping

## Logging

The plugin provides comprehensive logging with the following features:

### Log Levels
- **INFO**: General processing information and progress updates
- **WARNING**: Non-critical issues that don't stop processing
- **ERROR**: Critical errors that prevent processing
- **DEBUG**: Detailed technical information for troubleshooting

### Log Outputs
- **Console Output**: Real-time logging in Substance Painter's Python console
- **Log File**: Persistent logging to `auto_bake_material_textures.log`

### Viewing Logs
- **Python Console**: `Windows > Views > Python Console`
- **Log File**: Located in the same directory as the plugin script

## Troubleshooting

### Common Issues

#### "No texture sets found in the current project"
- **Cause**: No materials/texture sets in the current Substance Painter project
- **Solution**: Create texture sets by painting on your model or using the Texture Set List

#### "Texture folder does not exist for material"
- **Cause**: Folder name doesn't match texture set name exactly
- **Solution**: Ensure folder names match your material/texture set names precisely

#### "Invalid filename format"
- **Cause**: Texture files don't follow the naming convention
- **Solution**: Rename files to follow `[prefix]_[MaterialName]_[MapType].psd` format

#### "Unsupported mesh map type"
- **Cause**: Map type in filename not recognized
- **Solution**: Use supported map types listed in the table above

### Debug Mode

To enable debug logging for more detailed information:

1. Open the plugin file in a text editor
2. Change the logging level:
   ```python
   logging.basicConfig(level=logging.DEBUG, ...)
   ```
3. Save and restart Substance Painter

## Requirements

- **Substance Painter 2019.1+**: Required for Python plugin support
- **Python 3.x**: Included with Substance Painter
- **PySide2**: Included with Substance Painter for UI components

## Technical Details

### Plugin Architecture
- **UI Framework**: PySide2 (Qt-based interface)
- **API Integration**: Substance Painter Python API
- **File Handling**: Standard Python file I/O operations
- **Resource Management**: Automatic cleanup of UI elements

### Performance Considerations
- Processing time depends on number and size of texture files
- Large PSD files may take longer to import
- Network storage may impact performance

## Contributing

To contribute to this plugin:

1. Fork the repository
2. Create a feature branch
3. Implement your changes with appropriate logging
4. Test thoroughly with various folder structures
5. Update documentation as needed
6. Submit a pull request

## License

This project is provided as-is for educational and professional use. Please ensure compliance with Adobe Substance Painter's plugin development guidelines.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review log files for detailed error information
3. Verify folder structure and naming conventions
4. Test with a simple setup first

## Version History

### v1.1 (Current)
- Added comprehensive logging system
- Improved error handling and user feedback
- Enhanced UI with tooltips and better button sizing
- Added support for case-insensitive file extensions
- Implemented progress reporting and summary dialogs

### v1.0 (Initial)
- Basic texture import and mesh mapping functionality
- Simple UI with folder selection
- Support for common mesh map types

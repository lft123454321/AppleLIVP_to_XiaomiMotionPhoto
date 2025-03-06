# LIVP to Xiaomi Motion Photo Converter

[中文](/README_CN.md) 

## Project Overview  
Convert iOS LIVP files (uploaded to Baidu Netdisk) into Xiaomi-compatible Motion Photo format (embedded MP4 video) with complete metadata preservation.  
**Platform**: Windows 10/11  
**Python Version**: 3.8+  

## Features  
- LIVP → JPEG+MP4 conversion  
- Complete metadata migration (EXIF/XMP/IPTC)  
- Xiaomi-specific metadata injection  
- Batch processing support (non-LIVP files are directly copied to the target folder)  

## Installation  
1. Install Python dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  
2. Download external tools:  
   - [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) → Place `ffmpeg.exe` in the project root directory  
   - [ExifTool](https://exiftool.org/) → Place `exiftool.exe` and the `exiftool_files` folder in the project root directory  

## Usage  
```bash  
python live_photo_convert.py <input_dir> <output_dir>  
```  
**Example**:  
```bash  
python live_photo_convert.py D:\Livp_files E:\converted_photos  
```  

## Project Structure  
```  
├── live_photo_convert.py  
├── mi.config  
├── exiftool.exe  
├── exiftool_files/  
├── ffmpeg.exe  
└── requirements.txt  
```  

## Notes  
- **File paths containing spaces must be enclosed in quotes**  
- **Quality loss may occur during HEIC→JPEG and MOV→MP4 conversions**  

## Acknowledgments  
This project references the following works:  
- [[Tool] Batch Convert iPhone Live Photos to Xiaomi Motion Photos](https://www.bilibili.com/opus/1006443152534405127)  
- [iOS Live Photo to Xiaomi Motion Photo Script](https://github.com/Serendo/LivePhoto2XiaomiPhoto)  
- [Xiaomi Motion Photo Extraction](https://github.com/xiaotian2333/MI-Live-Photo-Transition)  
- [MotionPhotoMuxer](https://github.com/mihir-io/MotionPhotoMuxer)  
- [Comparison of Dynamic/Motion Photo Formats Among Domestic Manufacturers](https://blog.0to1.cf/posts/cn-motion-photo-format/)  
- [Exploring Android Motion Photo Implementations](https://zhuanlan.zhihu.com/p/11126715794)  

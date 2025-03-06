import os
import zipfile
import shutil
import subprocess
import pillow_heif
from pillow_heif import register_heif_opener
from PIL import Image
import pyexiv2
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def convert_livp(livp_path, output_dir):
    """核心转换函数（已实现元数据完整迁移）"""
    temp_dir = os.path.join(output_dir, "temp_livp")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # 解压LIVP文件
        with zipfile.ZipFile(livp_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # 定位媒体文件
        input_image_files = [f for f in os.listdir(temp_dir) if f.lower().endswith('.heic')]
        if not input_image_files:
            input_image_files = [f for f in os.listdir(temp_dir) if f.lower().endswith('.jpg')]
        if not input_image_files:
            input_image_files = [f for f in os.listdir(temp_dir) if f.lower().endswith('.jpeg')]
        mov_files = [f for f in os.listdir(temp_dir) if f.lower().endswith('.mov')]
        if not input_image_files or not mov_files:
            raise ValueError("Invalid LIVP structure")

        # 生成输出路径
        base_name = os.path.splitext(os.path.basename(livp_path))[0]
        input_image_path = os.path.join(temp_dir, input_image_files[0])
        mov_path = os.path.join(temp_dir, mov_files[0])
        jpeg_path = os.path.join(output_dir, f"MVIMG_{base_name}.jpg")
        mp4_path = os.path.join(output_dir, f"{base_name}.mp4")

        # HEIC转JPEG并保留元数据（网页1[1](@ref)的元数据保留方法）
        if input_image_path.endswith('heic'):
            register_heif_opener()
            # heif_file = pillow_heif.open_heif(input_image_path)
            # heif_file.to_pillow().save(jpeg_path, "JPEG", quality=95)
            with Image.open(input_image_path) as img:
                img.save(jpeg_path, "JPEG", quality=95)
            with pyexiv2.Image(input_image_path) as src_img, pyexiv2.Image(jpeg_path) as dst_img:
                src_img.copy_to_another_image(dst_img, exif=True, iptc=False, xmp=False)
                dst_img.modify_exif({"Exif.Image.Orientation": "1"})
        elif input_image_path.endswith('jpg') or input_image_path.endswith('jpeg'):
            shutil.copy2(input_image_path, jpeg_path)
        else:
            raise ValueError("Invalid input_image_path")


        # MOV转MP4（网页6[6](@ref)的FFmpeg参数优化）
        subprocess.run([
            'ffmpeg', '-i', mov_path,
            '-c:v', 'libx264', '-preset', 'fast',
            '-c:a', 'aac', '-b:a', '192k',
            '-movflags', '+faststart',
            mp4_path
        ], check=True)

        # 写入小米专用元数据（网页4[4](@ref)的命令行调用方式）
        exiftool_cmd = [
            'exiftool',
            '-config', 'mi.config',
            '-MVIMG=1',
            '-overwrite_original',
            jpeg_path
        ]
        result = subprocess.run(exiftool_cmd, capture_output=True, text=True)
        if "1 image files updated" not in result.stdout:
            logging.error(f"EXIF写入失败: {result.stderr}")

        # 写入XMP元数据
        with open(jpeg_path, 'rb+') as f:
            with pyexiv2.ImageData(f.read()) as img:
                mp4_size = os.path.getsize(mp4_path)
                xmp = img.read_xmp()
                xmp['Xmp.GCamera.MicroVideoVersion'] = '1'
                xmp['Xmp.GCamera.MicroVideo'] = '1'
                xmp['Xmp.GCamera.MicroVideoOffset'] = str(mp4_size)
                xmp['Xmp.GCamera.MicroVideoPresentationTimestampUs'] = '1500000'
                xmp['Xmp.MiCamera.XMPMeta'] = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>"
                pyexiv2.registerNs('http://ns.google.com/photos/1.0/camera/', 'GCamera')
                pyexiv2.registerNs('http://ns.xiaomi.com/photos/1.0/camera/', 'MiCamera')
                img.modify_xmp(xmp)
                # 清空原文件
                f.seek(0)
                f.truncate()
                # 获取图片的字节数据并保存到文件中
                f.write(img.get_bytes())
        # 追加MP4数据到JPEG
        with open(jpeg_path, 'ab') as jf, open(mp4_path, 'rb') as mf:
            jf.write(mf.read())

    except Exception as e:
        logging.error(f"处理失败 {livp_path}: {str(e)}")
    finally:
        shutil.rmtree(temp_dir)
        if os.path.exists(mp4_path):
            os.remove(mp4_path)

def batch_convert(input_dir, output_dir):
    """批量处理入口函数"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(root, input_dir)
            dest_folder = os.path.join(output_dir, rel_path)
            
            os.makedirs(dest_folder, exist_ok=True)
            
            if file.lower().endswith('.livp'):
                logging.info(f"正在处理LIVP文件: {src_path}")
                convert_livp(src_path, dest_folder)
            else:
                dest_path = os.path.join(dest_folder, file)
                logging.info(f"复制媒体文件: {src_path} -> {dest_path}")
                shutil.copy2(src_path, dest_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python live_photo_convert.py <input_directory> <output_directory>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    batch_convert(input_dir, output_dir)
# LIVP转小米动态照片工具

[English](/README.md) 

## 项目简介
将iOS上传到百度网盘的LIVP文件转换为小米手机兼容的动态照片格式（内嵌MP4视频），完整保留元数据。  
运行平台：**Windows 10/11**  
Python版本：**3.8+**

## 功能特性
- LIVP → JPEG+MP4 格式转换
- 完整元数据迁移（EXIF/XMP/IPTC）
- 写入小米专用元数据
- 支持批量处理，非LIVP文件会直接复制到目标文件夹

## 安装说明
1. 安装Python依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 下载外部工具：
   - [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) → 将`ffmpeg.exe`放在项目根目录
   - [ExifTool](https://exiftool.org/) → 将`exiftool.exe`与`exiftool_files`文件夹放在项目根目录

## 使用教程
```bash
python live_photo_convert.py <输入目录> <输出目录>
```
**示例**：
```bash
python live_photo_convert.py D:\Livp文件 E:\转换后的照片
```

## 项目结构
```
├── live_photo_convert.py
├── mi.config
├── exiftool.exe
├── exiftool_files/
├── ffmpeg.exe
└── requirements.txt
```

## 注意事项
- 文件路径若包含空格，需要用引号包起来
- HEIC转JPEG、MOV转MP4会有画质损失

## 鸣谢
参考了以下项目与文章：
- [[工具]批量转换iPhone的实况照片成小米的动态照片](https://www.bilibili.com/opus/1006443152534405127)
- [iOS 实况照片 -> 小米动态照片 转换脚本](https://github.com/Serendo/LivePhoto2XiaomiPhoto)
- [小米实况图片提取](https://github.com/xiaotian2333/MI-Live-Photo-Transition)
- [MotionPhotoMuxer](https://github.com/mihir-io/MotionPhotoMuxer)
- [国内厂商动态照片/实况照片格式对比](https://blog.0to1.cf/posts/cn-motion-photo-format/)
- [关于 Android「动态照片」实现方式的探究](https://zhuanlan.zhihu.com/p/11126715794)
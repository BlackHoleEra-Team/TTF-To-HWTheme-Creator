import os
import zipfile
import shutil
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


def create_description_xml(title, title_cn, author, designer, screen="FHD+", version="1.0.0", font="HarmonyOS Sans",
                           font_cn="HarmonyOS Sans"):
    root = Element("HwTheme")
    SubElement(root, "title").text = title
    SubElement(root, "title-cn").text = title_cn
    SubElement(root, "author").text = author
    SubElement(root, "designer").text = designer
    SubElement(root, "screen").text = screen
    SubElement(root, "version").text = version
    SubElement(root, "font").text = font
    SubElement(root, "font-cn").text = font_cn
    SubElement(root, "type").text = "font"

    rough_string = tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding="utf-8").decode('utf-8')


def create_hwt_file(output_filename, font_path, preview_image_path=None, title="My Font",
                    title_cn="我的字体", author="unknown", designer="unknown", screen="FHD+", version="1.0.0",
                    font="My Font", font_cn="我的字体"):
    temp_dir = "temp_hwt"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        fonts_dir = os.path.join(temp_dir, "fonts")
        os.makedirs(fonts_dir, exist_ok=True)
        target_font_name = "DroidSansChinese.ttf"
        target_font_path = os.path.join(fonts_dir, target_font_name)
        shutil.copy(font_path, target_font_path)

        preview_dir = os.path.join(temp_dir, "preview")
        os.makedirs(preview_dir, exist_ok=True)
        if preview_image_path:
            preview_target = os.path.join(preview_dir, "preview.jpg")
            shutil.copy(preview_image_path, preview_target)

        description_content = create_description_xml(title, title_cn, author, designer, screen, version, font, font_cn)
        with open(os.path.join(temp_dir, "description.xml"), "w", encoding="utf-8") as f:
            f.write(description_content)

        icon_path = os.path.join(temp_dir, "icon")
        with open(icon_path, 'w') as icon_file:
            icon_file.write("")

        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root_dir, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)

            for root_dir, dirs, _ in os.walk(temp_dir):
                for dir_name in dirs:
                    dir_path = os.path.join(root_dir, dir_name)
                    arcname = os.path.relpath(dir_path, temp_dir) + "/"
                    if not os.listdir(dir_path):
                        zip_info = zipfile.ZipInfo(arcname)
                        zipf.writestr(zip_info, "")

    except Exception as e:
        print(f"创建主题包失败: {e}")
        raise
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
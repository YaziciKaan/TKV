import os
import cv2
import numpy as np
from tkinter import filedialog

def read_labels(label_path, image_shape):
    labels = []
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                data = line.strip().split()
                class_index = int(data[0])
                coordinates = [float(val) for val in data[1:]]
                x_coords = [int(val * image_shape[1]) for val in coordinates[::2]]
                y_coords = [int(val * image_shape[0]) for val in coordinates[1::2]]
                points = np.zeros((len(x_coords), 1, 2), dtype=np.int32)
                for i in range(len(x_coords)):
                    points[i][0] = [x_coords[i], y_coords[i]]
                labels.append({'class_index': class_index, 'points': points})       
    else:
        pass
    return labels

def mask_from_labels(labels, image_shape):
    if labels == []:  # Eğer tahmin yapılamadıysa (etiket yoksa)
        pass
    else:
        mask = np.zeros(image_shape[:2], dtype=np.uint8)
        for label in labels:
            cv2.fillPoly(mask, [label['points']], color=255) # Maskeyi oluştur
        return mask

def select_files(): #MR Görüntülerinin olduğu dosya seçilmeli! Aynı fonksiyon Predictionları seçmek için de kullanılmakta.
    folder_path = filedialog.askdirectory(title="İstenilen Dosyayı Seçiniz.")
    return folder_path

def main():
    folder_path = select_files()
    tkv = 0
    kesit_araligi = float(input("Kesit Aralığı Değerini Giriniz: "))
    kesit_kalinligi = float(input("Kesit Kalınlığı Değerini Giriniz: "))
    # Etiket dosyasını seç
    label_file_path = select_files() 
    label_files = [f for f in os.listdir(label_file_path) if f.endswith('.txt')]
    if label_files == []:
        print("No label files found in the selected folder.")
        return

    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    for image_filename in image_files:
        image_path = os.path.join(folder_path, image_filename)
        image = cv2.imread(image_path)
        if image == None:
            print(f"Error: Unable to read image: {image_path}")
            continue
        image_height, image_width, _ = image.shape

        label_name = image_filename.replace('.png', '.txt').replace('.jpg', '.txt').replace('.jpeg', '.txt')
        label_path = os.path.join(label_file_path, label_name)
        label_path = label_path.replace("\\", "/")

        # Etiket dosyasını kullanarak maske oluştur
        pred_labels = read_labels(label_path, (image_height, image_width))
        pred_mask = mask_from_labels(pred_labels, (image_height, image_width))
        
        kidney_area = cv2.countNonZero(pred_mask)
        tkv += (kidney_area * kesit_araligi * kesit_kalinligi) * 0.001
        print(f"Toplam Böbrek Hacmi: {tkv}")         

if __name__ == "__main__":
    main()
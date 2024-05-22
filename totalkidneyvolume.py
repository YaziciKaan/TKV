import os
import cv2
import numpy as np
from tkinter import filedialog
from trainandpred import Yolov9

# Tahmin işleminden sonra .txt uzantılı label dosyalarından koordinatları ve sınıfların elde edilmesi
def read_labels(label_path, image_shape):
    labels = []
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                data = line.strip().split() # Data'da ilk veri sınıfı temsil eder, ardından x1 y1 x2 y2... şeklinde devam eder.
                class_index = int(data[0])
                coordinates = [float(val) for val in data[1:]]
                x_coords = [int(val * image_shape[1]) for val in coordinates[::2]] # x koordinatlarının piksel cinsinden elde edilmesi, datada elde edilen veriler normalizedir, yani 0 ile 1 arasındadır. 
                y_coords = [int(val * image_shape[0]) for val in coordinates[1::2]] # y koordinatlarının piksel cinsinden elde edilmesi
                points = np.zeros((len(x_coords), 1, 2), dtype=np.int32) # [x1 y1] ... olacak şekilde x ve y noktalarının belirlenmesi için yer açıldı.
                for i in range(len(x_coords)):
                    points[i][0] = [x_coords[i], y_coords[i]] # i=1 den başlayarak  [x1 y1] [x2 y2]... şeklinde tam koordinatlar elde edilir.
                labels.append({'class_index': class_index, 'points': points})       
    return labels

# Etiketler aracılığı ile maskenin oluşturulması
def mask_from_labels(labels, image_shape):
    if labels == []:
        return None
    mask = np.zeros(image_shape[:2], dtype=np.uint8) 
    for label in labels:
        cv2.fillPoly(mask, [label['points']], color=255) # okunan label etiketindeki tam koordinatlara göre maskeleme yapılır.
    return mask

def select_files():
    folder_path = filedialog.askdirectory(title="İstenilen Dosyayı Seçiniz.")
    return folder_path

def main():
    model = Yolov9('instance-segmentation')  # YoloV9'da instance-segmentation modunun seçilmesi
    folder_path = select_files()
    sources = folder_path.replace("\\", "/")
    weights_path = 'runs/train-seg/train/weights/best.pt' # Eğitilen modelin yolu

    detections_folder = model.predict(source=sources, weights=weights_path, device='cpu', hide_conf=True, hide_labels=True, iou_thres=0.75, conf_thres=0.75, save_txt=True, exist_ok=True, project="detections", name="kidney", imgsz=(512,512))

    tkv = 0
    kesit_araligi = float(input("Kesit Aralığı Değerini Giriniz: "))
    kesit_kalinligi = float(input("Kesit Kalınlığı Değerini Giriniz: "))

    # Seçilen hastanın dosyasındaki imgeleri sıra sıra gezme ve hacim eldesi için gerekli işlemlerin yapılmasını sağlayan for döngüsü
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    for image_filename in image_files:
        image_path = os.path.join(folder_path, image_filename)
        image = cv2.imread(image_path)
        image_height, image_width, _ = image.shape

        label_name = image_filename.replace('.png', '.txt').replace('.jpg', '.txt').replace('.jpeg', '.txt') # Etiketlerin adı, imgenin adı ile aynı olduğu için uzantısını .txt olarak değiştirerek etiket ismini elde edebiliriz.
        label_path = os.path.join(detections_folder, label_name)
        label_path = label_path.replace("\\", "/")

        pred_labels = read_labels(label_path, (image_height, image_width)) # Döngüdeki imge için tahmin etiketlerinin okunması
        pred_mask = mask_from_labels(pred_labels, (image_height, image_width)) # Döngüdeki imgenin etiketlerindeki koordinatlar ile maskeleme
        
        kidney_area = cv2.countNonZero(pred_mask) # Maskedeki piksellerin sayılması
        tkv += (kidney_area * kesit_araligi * kesit_kalinligi) * 0.001 # Kesit aralığı ve Kesit kalınlığını piksel sayısıyla çarparak mm^3 cinsinden hacim elde ederiz. 0.001 ile çarparak mL cinsine çevirebiliriz.
        # Bu işlem her imge döngüsünde devam ettiği için son imgeyle birlikte total hacmi tahmin etmiş bulunuyoruz.
        print(f"Toplam Böbrek Hacmi: {tkv}")

if __name__ == "__main__":
    main()